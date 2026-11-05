# Guia da equipe — eventos de máquinas

## Separação de responsabilidades

O contrato entre produtores e aplicação é um evento JSON com `machine_id` e `states`. A API e a dashboard não exigem Opta, IHM, CLP, MAC, firmware ou pinos. Essas integrações são adaptadores opcionais.

```text
Produtor → evento JSON → API → MySQL → Dashboard
```

- O produtor observa ou simula estados.
- O adaptador traduz um protocolo, quando necessário.
- A API valida, persiste e oferece consultas.
- A dashboard acompanha máquinas e observações recebidas.

A coleta física para CNC Mitsubishi M60, M70 e M80 continua possível por IHM/CLP → Opta → serial → ponte. Esse é um produtor, sem alterar o contrato da aplicação.

## Contrato

```json
{"machine_id":"CNC-001","states":{"ativo":true,"inativo":false,"emergencia":false,"motor_ligado":true,"alarme":false,"porta_aberta":false}}
```

`machine_id` aceita UUID ou código da máquina cadastrada em `/api/cncs`. Cada evento é um snapshot completo: não há merge com estados anteriores. Ausente significa não informado. O perfil principal tem `ativo`, `inativo`, `emergencia`, `motor_ligado`, `alarme` e `porta_aberta`; nomes adicionais e os sinais legados continuam preservados e exibidos.

`ativo` e `inativo` são entradas independentes, sem deduzir uma pelo complemento da outra. Emergência e alarme têm prioridade; inativo impede classificar como operando. A consulta de status retorna `diagnostics`: porta aberta com emergência resulta em **Operação falha**; ativo e inativo simultâneos resultam em **Sinais de atividade conflitantes**. Os diagnósticos são derivados da mesma observação, não alteram os sinais nem exigem migração do banco. A dashboard notifica uma nova combinação mesmo que o status resumido não mude e identifica como antigos os diagnósticos sem comunicação atual.

As consultas de estado e de histórico também expõem `signal_outputs`: uma lista de interpretações com `code`, `level` (`info`, `attention` ou `critical`), `title`, `message` e `signals`. A fonte única é `backend/services/signalOutputs.py`. O painel **Interações entre sinais** da dashboard filtra por máquina e nível, pagina seis máquinas e oferece acesso a todas as interpretações nos detalhes. Condições sem falha, leitura parcial e corrente simulada também geram saídas. Os outputs não mudam o estado nem acionam relés; sem comunicação atual, ficam identificados como antigos. Interpretações informativas não geram toasts repetidos.

O firmware USB/HTTP 2.1.1 usa o perfil `six_signals_current_reserved_v3`. O mapa da IHM informado para a instalação determina a ligação sequencial esperada abaixo; a conexão elétrica e a polaridade devem ser conferidas na bancada.

| Saída IHM/CLP esperada | Indicação na IHM | Entrada Opta | Chave em `states` |
|---|---|---|---|
| Q0.0 | Em execução | I1/A0 | `ativo` |
| Q0.1 | Parada | I2/A1 | `inativo` |
| Q0.2 | Emergência | I3/A2 | `emergencia` |
| Q0.3 | Motor ligado | I4/A3 | `motor_ligado` |
| Q0.4 | Porta aberta | I5/A4 | `porta_aberta` |
| Q0.5 | Alerta erro | I6/A5 | `alarme` |

I7/A6 fica livre e I8/A7 é reservada para corrente, sem leitura física. O `Main.pdf` ainda representa o mapeamento anterior e não confirma o vínculo atual. A troca da posição física dos dois últimos sinais não muda as chaves JSON nem suas regras na aplicação. O simulador emite os seis sinais e aceita `--also emergencia`, por exemplo, junto de `--state porta_aberta`.

`analog_signals` e `extra_signals` são campos opcionais do evento. `analog_signals.current` é uma corrente finita e não negativa em A; números como strings, booleanos e null são rejeitados. Sem leitura, omitir a chave, sem representar ausência como zero. `--current 12.5` no simulador envia corrente marcada por `extra_signals.current_input.source="simulated"`. Firmware, ponte, API, histórico e dashboard preservam o valor e sua origem. I8 não é consultada digitalmente nem por ADC enquanto a medição física estiver desativada.

`event_id` e `timestamp` são opcionais. Repetir a chave do evento com o mesmo conteúdo não duplica a leitura nem renova sua presença; mudar o conteúdo retorna 409. A idempotência do contrato genérico é por máquina. Leituras antigas entram no histórico sem reverter o estado atual. Booleanos como strings ou números retornam 422.

A ausência de eventos é identificada pelo timeout de recepção, sem consultar o coletor. `online` representa chegada recente de eventos. `DADOS_DESATUALIZADOS` distingue uma recepção recente de uma observação antiga.

## Fontes ativos

| Caminho | Responsabilidade |
|---|---|
| `backend/schemas/event.py` | Contrato público mínimo |
| `backend/services/events.py` | Ingestão por máquina e idempotência |
| `backend/services/machineState.py` | Interpretação dos estados |
| `backend/services/eventRepository.py` | Consultas e compatibilidade do histórico anterior |
| `backend/services/telemetry.py` | Adaptador de produtores que usam cadastro de dispositivo |
| `tools/simuladorCnc.py` | Produz JSON Lines em stdout, sem rede |
| `tools/publicarEventos.py` | Lê stdin e publica os eventos |
| `tools/ponteUsb.py` | Traduz serial para eventos; pode emitir stdout sem rede |
| `frontend/src/services/machineData.js` | Consulta somente máquinas, estado, histórico e utilização |
| `frontend/src/components/cncSignals/cncSignals.jsx` | Exibe estados recebidos, sem pinos ou hardware |

## Rotas

| Método | Rota | Uso |
|---|---|---|
| POST | `/api/events` | Receber evento de qualquer produtor |
| POST / GET | `/api/cncs` | Cadastrar / listar máquinas |
| GET / PUT / DELETE | `/api/cncs/{uuid}` | Consultar / editar / excluir máquina |
| GET | `/api/cncs/{uuid}/status` | Estados e última observação |
| GET | `/api/cncs/{uuid}/history` | Histórico paginado |
| GET | `/api/cncs/{uuid}/utilization` | Utilização observada |

`INGEST_API_KEY` habilita autenticação pelo cabeçalho `X-API-Key`. Os nomes antigos da chave e do cabeçalho continuam aceitos para adaptadores existentes. A página de coletores opcionais consulta `/api/devices` por conta própria; a dashboard não precisa dessa consulta.

## Persistência e compatibilidade

Eventos novos ficam em `machine_events`, com vínculo direto à máquina. Sua sequência ordena eventos no mesmo segundo. A tabela é criada na inicialização sem alterar colunas antigas. Leituras existentes em `telemetry` continuam consultáveis.

Remover ou realocar um coletor não remove nem transfere o histórico da máquina. Para coletores antigos, leituras ainda dependentes do vínculo são preservadas no armazenamento por máquina antes da alteração. Excluir a máquina continua removendo seu histórico.

MySQL é o banco da instalação. SQLite pode ser escolhido para teste isolado. A configuração e os comandos completos estão no [README](../../README.md), e o exemplo mínimo em [machine-event.json](../../examples/machine-event.json).
