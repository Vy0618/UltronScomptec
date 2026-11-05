# Integração CNC — IHM/CLP, Arduino Opta e servidor

Este é um adaptador opcional. A dashboard e a API funcionam sem ele, recebendo apenas ID da máquina e estados.

O projeto monitora máquinas das famílias Mitsubishi M60, M70 e M80 por sinais booleanos disponibilizados pela IHM/CLP. O objetivo é uma coleta pouco invasiva, sem alteração do programa da CNC ou comandos para seus atuadores. A conexão elétrica deve corresponder às interfaces autorizadas da instalação.

```text
Computador / Máquina
  → situação simulada na IHM / CLP
  → seis sinais digitais
  → Arduino Opta
  → serial USB
  → ponte Python no servidor
  → API FastAPI → MySQL → Dashboard
```

## Coleta

A ligação sequencial esperada segue o mapa da IHM informado para esta instalação:

| Saída IHM/CLP esperada | Indicação na IHM | Entrada Opta | Pino | Chave em `states` / finalidade |
|---|---|---|---|---|
| Q0.0 | Em execução | I1 | A0 | `ativo` |
| Q0.1 | Parada | I2 | A1 | `inativo` |
| Q0.2 | Emergência | I3 | A2 | `emergencia` |
| Q0.3 | Motor ligado | I4 | A3 | `motor_ligado` |
| Q0.4 | Porta aberta | I5 | A4 | `porta_aberta` |
| Q0.5 | Alerta erro | I6 | A5 | `alarme` |
| — | — | I7 | A6 | Reserva livre |
| — | — | I8 | A7 | Corrente em A; medição física desativada |

O firmware em [optaCncMonitor](../../firmware/optaCncMonitor) apenas lê entradas. Não configura nem escreve saídas de relé. O padrão é nível alto ativo, com inversão por máscara e filtro individual em `config.h`. Os sinais são independentes e preservados inclusive em combinações contraditórias.

O perfil é `six_signals_current_reserved_v3`, definido em `signalProfile.h`, com firmware USB/HTTP 2.1.1. I7 e I8 ficam configuradas como entrada, sem leitura digital; não há leitura ADC ou corrente fabricada. A tabela é o vínculo esperado, sem validação física já realizada: confira ligação elétrica e polaridade antes do ensaio na bancada. O `Main.pdf` usa o mapeamento anterior de oito sinais, sem porta aberta, e não confirma o vínculo atual.

Corrente pode ser enviada por `POST /api/events` em `analog_signals.current`, em A, com a origem em `extra_signals.current_input`. O comando `tools/simuladorCnc.py --machine-id CNC-001 --state ativo --current 12.5` produz um evento simulado para publicar com `tools/publicarEventos.py`. Sem corrente, a chave é omitida e a interface mantém o valor como não informado; zero continua sendo uma leitura válida.

## Serial e persistência

USB é o transporte padrão, a 115200. Cada linha começa com `CNC_JSON:` e contém protocolo 1, sequência, uptime, versão do firmware e `payload`. A aquisição publica a amostra inicial, mudanças nos sinais e heartbeat de 1 s. A comunicação roda separada da aquisição.

A ponte [ponteUsb.py](../../tools/ponteUsb.py) lê a porta e, com `--machine-id`, traduz os estados para `/api/events`, sem cadastrar dispositivo. `--stdout` emite JSON Lines sem acessar a rede. MAC e UUID de dispositivo são opções de compatibilidade para instalações antigas. O horário UTC da ponte representa a recepção USB. Reenvios à API preservam o identificador e o conteúdo da leitura para evitar duplicação. As filas são limitadas e não persistentes; uma interrupção pode perder transições.

O backend relaciona as leituras à CNC e, quando informado pelo adaptador, ao dispositivo. O dashboard consulta os eventos da máquina e exibe os sinais e sua atualidade. Emergência e alarme têm prioridade sobre atividade; inativo leva a parada. Porta aberta com emergência gera o diagnóstico **Operação falha**. Ativo e inativo simultâneos geram **Sinais de atividade conflitantes**, preservando ambos os sinais observados.

HTTP/Wi-Fi continua disponível como transporte alternativo selecionado na compilação. Ele não é necessário para a coleta por USB.

## Executar

Os comandos de instalação, compilação, gravação e ponte estão no [README da raiz](../../README.md). O payload compartilhado está em [monitorSample.json](../../firmware/optaCncMonitor/monitorSample.json).

```bash
python3 tools/configurarTransmissao.py --transporte usb --somente-compilar
# Para gravar, substitua a porta pela identificada na sua instalação:
python3 tools/configurarTransmissao.py --transporte usb --porta /dev/ttyACM0
.venv/bin/python tools/ponteUsb.py --porta /dev/ttyACM0 --machine-id CNC-001
```

A instalação usa MySQL. O teste de software pode usar SQLite isolado e enviar os mesmos booleanos por `curl`, dispensando hardware. Esse teste não valida a IHM/CLP, polaridade, captura elétrica, driver USB ou acesso remoto de uma instalação real. O perfil não lê códigos proprietários de falha Mitsubishi e não substitui o circuito de emergência.
