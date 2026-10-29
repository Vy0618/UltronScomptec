# Integração CNC — IHM/CLP, Arduino Opta e servidor

Este é um adaptador opcional. A dashboard e a API funcionam sem ele, recebendo apenas ID da máquina e estados.

O projeto monitora máquinas das famílias Mitsubishi M60, M70 e M80 por sinais booleanos disponibilizados pela IHM/CLP. O objetivo é uma coleta pouco invasiva, sem alteração do programa da CNC ou comandos para seus atuadores. A conexão elétrica deve corresponder às interfaces autorizadas da instalação.

```text
Computador / Máquina
  → situação simulada na IHM / CLP
  → oito sinais digitais
  → Arduino Opta
  → serial USB
  → ponte Python no servidor
  → API FastAPI → MySQL → Dashboard
```

## Coleta

| Entrada | Pino | Sinal |
|---|---|---|
| I1 | A0 | `em_execucao` |
| I2 | A1 | `pausa` |
| I3 | A2 | `parada` |
| I4 | A3 | `emergencia` |
| I5 | A4 | `motor_ligado` |
| I6 | A5 | `automatico` |
| I7 | A6 | `manual` |
| I8 | A7 | `alarme` |

O firmware em [optaCncMonitor](../../firmware/optaCncMonitor) apenas lê entradas. Não configura nem escreve saídas de relé. O padrão é nível alto ativo, com inversão por máscara e filtro individual em `config.h`. Os sinais são independentes e preservados inclusive em combinações contraditórias.

## Serial e persistência

USB é o transporte padrão, a 115200. Cada linha começa com `CNC_JSON:` e contém protocolo 1, sequência, uptime, versão do firmware e `payload`. A aquisição publica a amostra inicial, mudanças nos sinais e heartbeat de 1 s. A comunicação roda separada da aquisição.

A ponte [ponteUsb.py](../../tools/ponteUsb.py) lê a porta e, com `--machine-id`, traduz os estados para `/api/events`, sem cadastrar dispositivo. `--stdout` emite JSON Lines sem acessar a rede. MAC e UUID de dispositivo são opções de compatibilidade para instalações antigas. O horário UTC da ponte representa a recepção USB. Reenvios à API preservam o identificador e o conteúdo da leitura para evitar duplicação. As filas são limitadas e não persistentes; uma interrupção pode perder transições.

O backend relaciona cada leitura ao dispositivo e à CNC, armazenando os dados no MySQL. O dashboard consulta apenas os eventos da máquina e exibe os estados, o histórico e a atualidade das observações, sem pinos ou metadados do coletor. O estado resumido atual reconhece execução, emergência e alarme; pausa é preservada como sinal e não tem estado próprio no resumo.

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
