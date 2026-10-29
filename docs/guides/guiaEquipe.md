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
{"machine_id":"CNC-001","states":{"em_execucao":true,"alarme":false}}
```

`machine_id` aceita UUID ou código da máquina cadastrada em `/api/cncs`. Cada evento é um snapshot completo: não há merge com estados anteriores. Ausente significa não informado. Os estados conhecidos são execução, pausa, parada, emergência, motor ligado, automático, manual e alarme; nomes adicionais são preservados e exibidos.

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
