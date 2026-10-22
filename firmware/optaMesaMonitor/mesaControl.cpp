#include <Arduino.h>
#include "mesaControl.h"
#include "telemetry.h"
#include "config.h"

// USB frames have a single writer. Disable textual controller diagnostics in
// this mode so they cannot interleave with JSON or block the control loop.
#if ULTRON_TELEMETRY_USB
namespace {
struct SilentControlLog {
  template<class T> void print(const T&) {}
  template<class T> void println(const T&) {}
  void println() {}
} controlLog;
}
#else
static auto& controlLog = Serial;
#endif

/*
 * MESA SELETORA DE PECAS - OPTA V2
 * Placa: Arduino Opta Pro/Advanced Finder
 *
 * Mapeamento confirmado:
 *   I1 = A0 - sensor de entrada (somente diagnostico nesta versao)
 *   I2 = A1 - altura media   (feixe bloqueado = LOW)
 *   I3 = A2 - altura pequena (feixe bloqueado = LOW)
 *   I4 = A3 - altura grande  (feixe bloqueado = LOW)
 *   I5 = A4 - indutivo       (metal detectado = HIGH)
 *   I6 = A5 - queda 1        (ocupacao, nao encerra o ciclo)
 *   I7 = A6 - queda 2        (ocupacao, nao encerra o ciclo)
 *
 *   O1 = D0 - esteira
 *   O2 = D1 - atuador da queda 1
 *   O3 = D2 - atuador da queda 2
 *
 * Regras:
 *   nao metalica              -> reto
 *   metalica pequena          -> queda 1 / O2
 *   metalica media ou grande  -> queda 2 / O3
 *
 * A altura e o metal sao memorizados em instantes independentes.
 * O atuador selecionado permanece ligado por 3 segundos.
 * Base original preservada. Monitoramento Wi-Fi copia estados apos o controle.
 */

// -----------------------------------------------------------------------------
// Entradas
// -----------------------------------------------------------------------------
constexpr uint8_t I1_ENTRADA = A0;
constexpr uint8_t I2_MEDIA   = A1;
constexpr uint8_t I3_PEQUENA = A2;
constexpr uint8_t I4_GRANDE  = A3;
constexpr uint8_t I5_METAL   = A4;
constexpr uint8_t I6_QUEDA1  = A5;
constexpr uint8_t I7_QUEDA2  = A6;

// -----------------------------------------------------------------------------
// Saidas confirmadas no teste fisico
// -----------------------------------------------------------------------------
constexpr uint8_t O1_ESTEIRA = D0;
constexpr uint8_t O2_QUEDA1  = D1;
constexpr uint8_t O3_QUEDA2  = D2;

// -----------------------------------------------------------------------------
// Tempos de calibracao
// -----------------------------------------------------------------------------
constexpr unsigned long DEBOUNCE_ALTURA_MS = 20;
constexpr unsigned long ALTURA_LIVRE_ESTAVEL_MS = 40;

// AJUSTE PRINCIPAL: depois que a peca sai do modulo de altura, este e o prazo
// maximo para I5 detectar metal. Se I5 nao detectar, a peca e nao metalica.
constexpr unsigned long JANELA_I5_MS = 500;

// Mantem o desviador avancado tempo suficiente para a peca ser derrubada.
constexpr unsigned long TEMPO_ATUADOR_QUEDA1_MS = 3000;
constexpr unsigned long TEMPO_ATUADOR_QUEDA2_MS = 3500;

// TIMER DA PECA QUE SEGUE RETO.
// Substituir futuramente pelo fim de curso ligado em I8.
constexpr unsigned long TEMPO_RETO_SEM_I8_MS = 2500;

// Evita que uma peca presa mantenha o sistema eternamente em classificacao.
constexpr unsigned long TIMEOUT_MODULO_ALTURA_MS = 4000;

// I6/I7 continuamente detectando por este tempo indicam 3 ou mais pecas.
constexpr unsigned long TEMPO_RAMPA_CHEIA_MS = 1700;

enum class Estado : uint8_t {
  AGUARDANDO_PECA,
  COLETANDO_ALTURA,
  AGUARDANDO_METAL,
  ACIONANDO_QUEDA1,
  ACIONANDO_QUEDA2,
  AGUARDANDO_RETO,
  FALHA
};

enum class Altura : uint8_t {
  INVALIDA,
  PEQUENA,
  MEDIA,
  GRANDE
};

Estado estado = Estado::AGUARDANDO_PECA;
Altura alturaAtual = Altura::INVALIDA;

bool viuPequena = false;
bool viuMedia = false;
bool viuGrande = false;
bool metalDetectado = false;

unsigned long estadoIniciadoEm = 0;
unsigned long alturaBloqueadaDesde = 0;
unsigned long alturaLivreDesde = 0;
unsigned long i6AtivoDesde = 0;
unsigned long i7AtivoDesde = 0;

bool rampa1Cheia = false;
bool rampa2Cheia = false;
bool moduloAlturaArmado = false;

uint32_t contadorTotal = 0;
uint32_t contadorReto = 0;
uint32_t contadorQueda1 = 0;
uint32_t contadorQueda2 = 0;
uint32_t contadorFalhas = 0;

// Estados anteriores apenas para diagnostico serial.
bool entradasAnteriores[7] = {false, false, false, false, false, false, false};

// Sensores de altura sao barreiras: LOW significa que a peca bloqueou o feixe.
bool i2Bloqueado() { return digitalRead(I2_MEDIA) == LOW; }
bool i3Bloqueado() { return digitalRead(I3_PEQUENA) == LOW; }
bool i4Bloqueado() { return digitalRead(I4_GRANDE) == LOW; }

bool algumSensorAlturaBloqueado() {
  return i2Bloqueado() || i3Bloqueado() || i4Bloqueado();
}

// Os demais sensores seguem a polaridade validada pelo teste anterior.
bool i5DetectouMetal() { return digitalRead(I5_METAL) == HIGH; }
bool i6DetectouPeca()  { return digitalRead(I6_QUEDA1) == HIGH; }
bool i7DetectouPeca()  { return digitalRead(I7_QUEDA2) == HIGH; }

const char* nomeAltura(Altura altura) {
  switch (altura) {
    case Altura::PEQUENA: return "pequena";
    case Altura::MEDIA:   return "media";
    case Altura::GRANDE:  return "grande";
    default:              return "invalida";
  }
}

const char* nomeEstado(Estado valor) {
  switch (valor) {
    case Estado::AGUARDANDO_PECA:   return "aguardando_peca";
    case Estado::COLETANDO_ALTURA:  return "coletando_altura";
    case Estado::AGUARDANDO_METAL:  return "aguardando_metal";
    case Estado::ACIONANDO_QUEDA1:  return "acionando_queda1";
    case Estado::ACIONANDO_QUEDA2:  return "acionando_queda2";
    case Estado::AGUARDANDO_RETO:   return "aguardando_reto";
    case Estado::FALHA:             return "falha";
  }
  return "desconhecido";
}

void mudarEstado(Estado novoEstado) {
  estado = novoEstado;
  estadoIniciadoEm = millis();
  controlLog.print("ESTADO -> ");
  controlLog.println(nomeEstado(estado));
}

uint8_t saidasComandadas = 0;

void escreverSaida(uint8_t saida, uint8_t led, bool ligada) {
  const uint8_t bit = saida == O1_ESTEIRA ? 1 : saida == O2_QUEDA1 ? 2 : 4;
  if (ligada) saidasComandadas |= bit;
  else saidasComandadas &= ~bit;
  digitalWrite(saida, ligada ? HIGH : LOW);
  digitalWrite(led, ligada ? HIGH : LOW);
}

void desligarAtuadores() {
  escreverSaida(O2_QUEDA1, LED_D1, false);
  escreverSaida(O3_QUEDA2, LED_D2, false);
}

void limparClassificacao() {
  alturaAtual = Altura::INVALIDA;
  viuPequena = false;
  viuMedia = false;
  viuGrande = false;
  metalDetectado = false;
  alturaBloqueadaDesde = 0;
  alturaLivreDesde = 0;
}

void iniciarNovaPeca() {
  limparClassificacao();
  contadorTotal++;
  moduloAlturaArmado = false;
  mudarEstado(Estado::COLETANDO_ALTURA);
  controlLog.print("NOVA PECA #");
  controlLog.println(contadorTotal);
}

void memorizarSensores() {
  if (i3Bloqueado()) viuPequena = true;
  if (i2Bloqueado()) viuMedia = true;
  if (i4Bloqueado()) viuGrande = true;
  if (i5DetectouMetal()) metalDetectado = true;
}

void consolidarAltura() {
  // Prioridade para a maior altura bloqueada pela mesma peca.
  if (viuGrande)      alturaAtual = Altura::GRANDE;
  else if (viuMedia)  alturaAtual = Altura::MEDIA;
  else if (viuPequena) alturaAtual = Altura::PEQUENA;
  else                alturaAtual = Altura::INVALIDA;
}

void decidirDestino() {
  consolidarAltura();

  controlLog.print("CLASSIFICACAO: altura=");
  controlLog.print(nomeAltura(alturaAtual));
  controlLog.print(" material=");
  controlLog.println(metalDetectado ? "metalico" : "nao_metalico");

  if (alturaAtual == Altura::INVALIDA) {
    contadorFalhas++;
    controlLog.println("FALHA: nenhuma altura valida foi memorizada");
    mudarEstado(Estado::FALHA);
    return;
  }

  if (!metalDetectado) {
    controlLog.println("DESTINO: RETO");
    mudarEstado(Estado::AGUARDANDO_RETO);
    return;
  }

  if (alturaAtual == Altura::PEQUENA) {
    controlLog.println("DESTINO: QUEDA 1 - O2 LIGADO");
    escreverSaida(O2_QUEDA1, LED_D1, true);
    mudarEstado(Estado::ACIONANDO_QUEDA1);
    return;
  }

  controlLog.println("DESTINO: QUEDA 2 - O3 LIGADO");
  escreverSaida(O3_QUEDA2, LED_D2, true);
  mudarEstado(Estado::ACIONANDO_QUEDA2);
}

void atualizarRampa(
  bool sensorAtivo,
  unsigned long &ativoDesde,
  bool &rampaCheia,
  const char* nome
) {
  const unsigned long agora = millis();

  if (sensorAtivo) {
    if (ativoDesde == 0) ativoDesde = agora;

    if (!rampaCheia && agora - ativoDesde >= TEMPO_RAMPA_CHEIA_MS) {
      rampaCheia = true;
      controlLog.print("ALERTA: ");
      controlLog.print(nome);
      controlLog.println(" com 3 ou mais pecas");
    }
  } else {
    ativoDesde = 0;
    rampaCheia = false;
  }
}

void atualizarRampas() {
  atualizarRampa(i6DetectouPeca(), i6AtivoDesde, rampa1Cheia, "queda 1");
  atualizarRampa(i7DetectouPeca(), i7AtivoDesde, rampa2Cheia, "queda 2");
}

void atualizarDiagnosticoEntradas() {
  const uint8_t pinos[7] = {
    I1_ENTRADA, I2_MEDIA, I3_PEQUENA, I4_GRANDE,
    I5_METAL, I6_QUEDA1, I7_QUEDA2
  };

  for (uint8_t i = 0; i < 7; i++) {
    const bool leitura = digitalRead(pinos[i]);
    if (leitura != entradasAnteriores[i]) {
      entradasAnteriores[i] = leitura;
      controlLog.print("I");
      controlLog.print(i + 1);
      controlLog.print(" -> ");
      controlLog.println(leitura ? "HIGH" : "LOW");
    }
  }
}

void atualizarControle() {
  const unsigned long agora = millis();
  const unsigned long decorrido = agora - estadoIniciadoEm;
  const bool alturaBloqueada = algumSensorAlturaBloqueado();

  switch (estado) {
    case Estado::AGUARDANDO_PECA:
      // Rearma somente depois de observar o modulo completamente livre.
      if (!alturaBloqueada) moduloAlturaArmado = true;

      if (moduloAlturaArmado && alturaBloqueada) {
        if (alturaBloqueadaDesde == 0) alturaBloqueadaDesde = agora;

        if (agora - alturaBloqueadaDesde >= DEBOUNCE_ALTURA_MS) {
          iniciarNovaPeca();
          memorizarSensores();
        }
      } else {
        alturaBloqueadaDesde = 0;
      }
      break;

    case Estado::COLETANDO_ALTURA:
      memorizarSensores();

      if (alturaBloqueada) {
        alturaLivreDesde = 0;
      } else {
        if (alturaLivreDesde == 0) alturaLivreDesde = agora;

        if (agora - alturaLivreDesde >= ALTURA_LIVRE_ESTAVEL_MS) {
          consolidarAltura();
          controlLog.print("ALTURA MEMORIZADA: ");
          controlLog.println(nomeAltura(alturaAtual));
          mudarEstado(Estado::AGUARDANDO_METAL);
        }
      }

      if (decorrido >= TIMEOUT_MODULO_ALTURA_MS) {
        contadorFalhas++;
        controlLog.println("FALHA: timeout no modulo de altura");
        mudarEstado(Estado::FALHA);
      }
      break;

    case Estado::AGUARDANDO_METAL:
      if (i5DetectouMetal()) metalDetectado = true;

      if (metalDetectado) {
        // Metal pode ter sido detectado durante ou depois da leitura da altura.
        decidirDestino();
      } else if (decorrido >= JANELA_I5_MS) {
        // Todo o prazo terminou sem I5: assume material nao metalico.
        decidirDestino();
      }
      break;

    case Estado::ACIONANDO_QUEDA1:
      if (decorrido >= TEMPO_ATUADOR_QUEDA1_MS) {
        escreverSaida(O2_QUEDA1, LED_D1, false);
        contadorQueda1++;
        controlLog.println("O2 DESLIGADO - Queda 1 concluida");
        limparClassificacao();
        mudarEstado(Estado::AGUARDANDO_PECA);
      }
      break;

    case Estado::ACIONANDO_QUEDA2:
      if (decorrido >= TEMPO_ATUADOR_QUEDA2_MS) {
        escreverSaida(O3_QUEDA2, LED_D2, false);
        contadorQueda2++;
        controlLog.println("O3 DESLIGADO - Queda 2 concluida");
        limparClassificacao();
        mudarEstado(Estado::AGUARDANDO_PECA);
      }
      break;

    case Estado::AGUARDANDO_RETO:
      if (decorrido >= TEMPO_RETO_SEM_I8_MS) {
        contadorReto++;
        controlLog.println("PECA RETA CONCLUIDA PELO TIMER SEM I8");
        limparClassificacao();
        mudarEstado(Estado::AGUARDANDO_PECA);
      }
      break;

    case Estado::FALHA:
      desligarAtuadores();
      if (decorrido >= 1000) {
        limparClassificacao();
        mudarEstado(Estado::AGUARDANDO_PECA);
      }
      break;
  }
}

void mesaSetup() {
  Serial.begin(115200);

  pinMode(I1_ENTRADA, INPUT);
  pinMode(I2_MEDIA, INPUT);
  pinMode(I3_PEQUENA, INPUT);
  pinMode(I4_GRANDE, INPUT);
  pinMode(I5_METAL, INPUT);
  pinMode(I6_QUEDA1, INPUT);
  pinMode(I7_QUEDA2, INPUT);

  pinMode(O1_ESTEIRA, OUTPUT);
  pinMode(O2_QUEDA1, OUTPUT);
  pinMode(O3_QUEDA2, OUTPUT);

  pinMode(LED_D0, OUTPUT);
  pinMode(LED_D1, OUTPUT);
  pinMode(LED_D2, OUTPUT);

  desligarAtuadores();
  escreverSaida(O1_ESTEIRA, LED_D0, true);

  for (uint8_t i = 0; i < 7; i++) entradasAnteriores[i] = false;

  estadoIniciadoEm = millis();
  moduloAlturaArmado = !algumSensorAlturaBloqueado();
  telemetryBegin();

  controlLog.println();
  controlLog.println("============================================");
  controlLog.println("MESA OPTA V2 INICIADA");
  controlLog.println("O1 esteira ligada");
  controlLog.println("Inicio da peca: bloqueio em I2, I3 ou I4");
  controlLog.println("I5 independente; janela configurada em 500 ms");
  controlLog.println("============================================");
}

// Observação somente após atualizarControle(); nenhuma regra de seleção é alterada.
void publicarSnapshotTelemetry() {
  static uint32_t previousMs = 0;
  static uint64_t uptimeMs = 0;
  const uint32_t now = millis();
  uptimeMs += uint32_t(now - previousMs);
  previousMs = now;
  MesaSnapshot sample;
  sample.capturedMs = now;
  sample.uptimeMs = uptimeMs;
  const uint8_t pins[7] = {I1_ENTRADA, I2_MEDIA, I3_PEQUENA, I4_GRANDE, I5_METAL, I6_QUEDA1, I7_QUEDA2};
  for (uint8_t i = 0; i < 7; ++i) if (digitalRead(pins[i]) == HIGH) sample.rawInputs |= 1U << i;
  sample.commandedOutputs = saidasComandadas;
  sample.state = nomeEstado(estado);
  sample.height = nomeAltura(alturaAtual);
  sample.cycleActive = estado != Estado::AGUARDANDO_PECA && estado != Estado::FALHA;
  sample.fault = estado == Estado::FALHA;
  sample.metal = metalDetectado;
  sample.ramp1Full = rampa1Cheia;
  sample.ramp2Full = rampa2Cheia;
  sample.total = contadorTotal;
  sample.straight = contadorReto;
  sample.drop1 = contadorQueda1;
  sample.drop2 = contadorQueda2;
  sample.faults = contadorFalhas;
  telemetryPublish(sample);
}

void mesaLoop() {
  atualizarDiagnosticoEntradas();
  atualizarRampas();
  atualizarControle();
  publicarSnapshotTelemetry();
}
