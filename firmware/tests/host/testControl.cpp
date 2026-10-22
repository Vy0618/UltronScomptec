#include <cassert>
#include <cstdio>
#include <cstring>
#include <initializer_list>
#include "Arduino.h"
#include "../../optaMesaMonitor/telemetry.h"
uint32_t hostMillis = 0;
int hostPins[32] = {};
HostSerial Serial;
MesaSnapshot observed;
void telemetryBegin() {}
void telemetryPublish(const MesaSnapshot& snapshot) { observed = snapshot; }

// Execute the actual controller, replacing only GPIO/time/transport boundaries.
#include "../../optaMesaMonitor/mesaControl.cpp"

void advance(uint32_t ms) { for (uint32_t i = 0; i < ms; ++i) { ++hostMillis; mesaLoop(); } }
void resetController() {
  hostMillis = 0; memset(hostPins, 0, sizeof(hostPins));
  hostPins[A1] = hostPins[A2] = hostPins[A3] = HIGH;
  estado = Estado::AGUARDANDO_PECA; limparClassificacao();
  contadorTotal = contadorReto = contadorQueda1 = contadorQueda2 = contadorFalhas = 0;
  i6AtivoDesde = i7AtivoDesde = 0; rampa1Cheia = rampa2Cheia = false;
  saidasComandadas = 0; mesaSetup(); mesaLoop();
  assert(hostPins[D0] == HIGH && hostPins[D1] == LOW && hostPins[D2] == LOW);
}
void enterPiece(uint8_t heightPin, bool metal) {
  hostPins[heightPin] = LOW; hostPins[A4] = metal ? HIGH : LOW;
  advance(21); assert(contadorTotal == 1 && estado == Estado::COLETANDO_ALTURA);
  hostPins[heightPin] = HIGH;
  advance(41); assert(estado == Estado::AGUARDANDO_METAL);
  advance(1);
}
int main() {
  resetController(); enterPiece(A2, true);
  assert(estado == Estado::ACIONANDO_QUEDA1 && hostPins[D1] == HIGH && observed.cycleActive);
  assert(observed.commandedOutputs == 3 && observed.metal);
  advance(2999); assert(hostPins[D1] == HIGH && contadorQueda1 == 0);
  advance(1); assert(hostPins[D1] == LOW && contadorQueda1 == 1 && estado == Estado::AGUARDANDO_PECA);
  puts("PASS control: small metal / exact 3000 ms actuator / snapshot");

  for (uint8_t height : {uint8_t(A1), uint8_t(A3)}) {
    resetController(); enterPiece(height, true);
    assert(estado == Estado::ACIONANDO_QUEDA2 && hostPins[D2] == HIGH);
    advance(3499); assert(contadorQueda2 == 0);
    advance(1); assert(contadorQueda2 == 1 && hostPins[D2] == LOW);
  }
  puts("PASS control: medium and large metal / 3500 ms actuator");

  resetController(); enterPiece(A2, false);
  assert(estado == Estado::AGUARDANDO_METAL);
  advance(499); assert(estado == Estado::AGUARDANDO_RETO && hostPins[D1] == LOW && hostPins[D2] == LOW);
  advance(2499); assert(contadorReto == 0);
  advance(1); assert(contadorReto == 1);
  puts("PASS control: non-metal / 500 ms metal window / straight timer");

  resetController(); hostPins[A2] = LOW; advance(21); advance(4000);
  assert(estado == Estado::FALHA && contadorFalhas == 1 && observed.fault && !observed.cycleActive);
  advance(1000); assert(estado == Estado::AGUARDANDO_PECA && hostPins[D0] == HIGH);
  puts("PASS control: blocked height timeout / recovery / conveyor preserved");

  resetController(); hostPins[A5] = HIGH; hostPins[A6] = HIGH;
  advance(1700); assert(!rampa1Cheia && !rampa2Cheia);
  advance(1); assert(rampa1Cheia && rampa2Cheia && observed.ramp1Full);
  hostPins[A5] = hostPins[A6] = LOW; advance(1); assert(!rampa1Cheia && !rampa2Cheia);
  puts("PASS control: 1700 ms occupancy / clear ramp");

  resetController(); enterPiece(A2, true);
  hostPins[A2] = LOW; advance(100); hostPins[A2] = HIGH; advance(100);
  assert(contadorTotal == 1 && estado == Estado::ACIONANDO_QUEDA1);
  puts("PASS control: documented one-piece-at-a-time rule");
}
