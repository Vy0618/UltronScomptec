# Comparação do backend — análise estática

Data: 04/11/2026. Nenhum serviço, teste, banco de dados ou firmware foi executado nesta análise. Não foram alterados arquivos de aplicação. Valores de credenciais não são reproduzidos.

## Referências

- **Atual**: `C:/Users/pedro/OneDrive/Desktop/UltronScomptec-main/backend`.
- **Aninhada**: `C:/Users/pedro/OneDrive/Desktop/UltronScomptec-main/UltronScomptec-main/backend`.
- **Ultron (1)**: `C:/Users/pedro/OneDrive/Desktop/UltronScomptec-main (1)/UltronScomptec-main/backend`.
- **HTTP**: `C:/Users/pedro/OneDrive/Desktop/SCOMPTECHTTP/SCOMPTEC- Back`.
- **V3**: `C:/Users/pedro/OneDrive/Desktop/SCOMPTECV3/SCOMPTEC- Back`.
- **TCC**: `C:/Users/pedro/OneDrive/Desktop/ps3youtube/ScompTecTCC-main/SCOMPTEC- Back`.

Os nomes indicam pastas, não uma ordem cronológica comprovada. Para equivalências lógicas foram considerados `Database` → `database`, `Schema` → `schemas`, `Services` → `services` e nomes em snake_case → camelCase quando há correspondência clara.

## Atual versus cópia aninhada: diferenças mais específicas desta versão

A aninhada é a mais próxima entre os backends inspecionados: 39 arquivos contra 42 na atual. Após alinhar caminhos, 7 arquivos existentes diferem e 3 são novos; os outros 32 arquivos são idênticos em bytes. Não há remoção de arquivo do backend nessa comparação.

| Arquivo atual | Diferença observada | Efeito |
|---|---|---|
| `schemas/event.py:12` | Acrescenta `analog_signals` e `extra_signals` no contrato de entrada e saída de `/api/events`; valida corrente negativa. | Eventos diretos passam a transportar corrente e origem. Os números de `analog_signals` precisam ser finitos e estritos; `current` e `corrente` não podem ser negativos. Ausência é diferente de zero. |
| `schemas/cnc.py:31` | Acrescenta `SignalDiagnostic`, `diagnostics` e `signal_outputs`. | Consultas de estado retornam diagnósticos combinados e interpretações estruturadas. |
| `schemas/telemetry.py:25` | Acrescenta `signal_outputs` a cada item de histórico. | A resposta histórica contém interpretação por leitura. |
| `services/events.py:81` | Normaliza atividade pela função nova e encaminha analógicos/metadados ao armazenamento. | Reconhece o perfil `ativo/inativo` e preserva corrente recebida. |
| `services/machineState.py:4` | Nova precedência de atividade; novos diagnósticos. | `inativo=true` impede estado de operação; `ativo=false` explícito prevalece sobre nomes legados, sem fabricar um sinal complementar. |
| `services/cncService.py:125` | Acrescenta diagnósticos e saídas ao estado; calcula saídas em cada item histórico na linha 156. | Status individual/coletivo e histórico compartilham regras. |
| `tests/testEvents.py:164` | Novos cenários para atividade, combinações, corrente e saídas históricas. | Amplia especificações verificáveis de contrato e persistência; testes não executados nesta análise. |
| `schemas/signalOutput.py:1` (novo) | Schema com código, nível, título, mensagem e sinais. | Formaliza a estrutura de interpretação. |
| `services/signalOutputs.py:23` (novo) | Interpretação de combinações e leituras parciais, com ordenação critical/attention/info. | Traz mensagens para combinações reconhecidas, sinais isolados, ausência, corrente e atividade legada. |
| `tests/testSignalOutputs.py:45` (novo) | Testa combinações documentadas, as 64 combinações booleanas, corrente/origem, leitura parcial e aliases. | A cobertura expressa regras de interpretação sem modificar o estado calculado. |

Regras novas de estado e diagnóstico, comparadas à aninhada:

- `ativo=true` pode resultar em `OPERANDO`; `inativo=true` resulta em `PARADA` quando não há estado de maior prioridade. Emergência, alarme, manutenção e presença explícita de 24 V continuam respeitando a prioridade existente (`services/machineState.py:35`).
- Porta aberta + emergência produz `PORTA_ABERTA_EMERGENCIA`, título “Operação falha”, sem retirar a prioridade de `EMERGENCIA` (`services/machineState.py:18`).
- Ativo + inativo produz `ATIVIDADE_CONFLITANTE`, título “Sinais de atividade conflitantes”, e atividade fica falsa (`services/machineState.py:25`).
- `signal_outputs` inclui nove pares declarados: emergência/alarme, emergência/ativo, alarme/ativo, alarme/inativo, porta/alarme, ativo/porta, inativo/porta, ativo/motor e inativo/motor. Também interpreta sinais isolados, todos falsos, sinais ausentes e formato legado (`services/signalOutputs.py:10`).
- Corrente recebida gera saída informativa vinculada à atividade/inatividade, identifica simulação apenas quando `extra_signals.current_input.source == "simulated"` e preserva `0 A`. O backend não transforma esse número em prova de atividade nem confirma origem física (`services/signalOutputs.py:79`).
- As interpretações não são gravadas como nova condição operacional. São calculadas a partir de cada leitura, e as entradas originais são preservadas. O código não converte ausência de campo em sinal falso.

## Atual versus Ultron (1)

Além das diferenças acima, a atual reorganiza a ingestão em torno da máquina:

1. **Novo armazenamento por CNC.** `database/models.py:307` acrescenta `MachineEvent`/`machine_events` com sequência estável, `machine_id`, metadados opcionais do coletor e sinais. Em Ultron (1), as novas leituras são `Telemetry` ligadas a `Device`; a CNC depende do coletor para consultar o histórico. O mecanismo `CodeSequence` já existe em Ultron (1), portanto geração persistente de códigos não é novidade funcional desta atual.
2. **Novo endpoint independente de hardware.** `services/events.py:70` expõe `POST /api/events`, aceita UUID, código CNC ou alias numérico (`1` → `CNC-001`) e não exige cadastro de dispositivo/MAC. A rota de telemetria por dispositivo continua como adaptador em `services/telemetry.py:18`.
3. **Novas consultas coletivas.** `services/cncService.py:62` oferece `GET /api/cncs/statuses`; linha 69 oferece `GET /api/cncs/history` com paginação, filtro de máquina e intervalo. O backend de Ultron (1) consulta estado e histórico por CNC e não tem essas rotas coletivas.
4. **Presença e estado passam a ser da máquina.** `services/cncService.py:109` calcula comunicação por leitura/`cnc.last_seen`; a referência Ultron (1) usa presença do dispositivo associado.
5. **Histórico compatível preservado.** `services/eventRepository.py:14` unifica eventos atuais e telemetria anterior sem duplicar os já importados. `preserve_legacy_history`, linha 93, copia leituras legadas antes de remover ou realocar coletor. Os pontos de chamada estão em `services/deviceService.py:151` e `:162`. Ultron (1) bloqueia realocação quando existe histórico e exclui telemetria em cascata ao excluir dispositivo. Excluir a própria CNC continua removendo seus eventos em cascata.
6. **Autenticação de ingestão unificada.** `services/ingestAuth.py:7` aceita `X-API-Key` ou `X-Device-Key`, usa `INGEST_API_KEY` com fallback em `DEVICE_API_KEY` e comparação de tempo constante. Antes há somente a chave de dispositivo. Sem chave configurada, essa verificação não exige credencial.
7. **Idempotência reaproveitada e ampliada.** `services/events.py:21` concentra validação de timestamp e reenvio: reutilizar ID com conteúdo diferente retorna 409; reenvio idêntico não renova presença; leitura antiga não reverte o estado atual. Parte disso já existia na telemetria de Ultron (1), mas nesta versão é aplicada à ingestão por máquina e ao adaptador legado.
8. **Configuração do evento.** `config.py:9` passa a reconhecer `INGEST_API_KEY` e `EVENT_OFFLINE_TIMEOUT_SECONDS`; `services/clock.py:4` prioriza o timeout de evento e mantém fallback para o de dispositivo.
9. **Serviços extraídos.** `codeService.py` separa a função de geração de códigos já existente; `machineState.py` separa interpretação antes localizada em telemetria; `schemas/observation.py` passa a servir como observação interna comum.

No backend de Ultron (1), `testWifiFlow.py` existe e não aparece no backend atual; parte do escopo passa a ser coberta por testes de eventos, preservação e ingestão genérica. Isso é diferença de suíte, não evidência de que o firmware Wi-Fi inteiro foi removido.

## Atual versus HTTP, V3 e TCC

Estas três referências usam a árvore `SCOMPTEC- Back`, com `Main.py`, `Database`, `Schema`, `Services`, `create_admin.py` e nomes de teste com underscores. A atual usa `backend`, `main.py`, `database`, `schemas`, `services`, `createAdmin.py` e nomes em camelCase. Muitos diffs nessas referências são correções de caminho/importação e não funções inéditas.

- **MySQL continua sendo suportado.** O modelo relacional SQLAlchemy não foi substituído por outro banco. A atual acrescenta criação automática do banco MySQL inexistente antes de criar tabelas, apenas para o erro MySQL 1049 (`database/connection.py:33`). Erros de autenticação não são reinterpretados como banco ausente. HTTP/V3/TCC somente criam tabelas em um banco já existente.
- **JSON de configuração do backend.** HTTP/V3/TCC leem `.env`; a atual também lê `backend/config.json`, valida suas chaves e tipos e aplica prioridade ambiente → `.env` → JSON (`config.py:16`). O JSON não substitui o `.env` existente. O inventário da raiz do projeto não é o JSON carregado pelo backend.
- **SQLite para simulação.** A atual e HTTP têm opções de engine SQLite, conexão compartilhada para memória e foreign keys habilitadas. V3/TCC não têm essa adaptação de engine (`SCOMPTECHTTP/SCOMPTEC- Back/Database/Connection.py:18`; atual `database/connection.py:18`).
- **Isolamento de configuração na simulação.** Atual e HTTP ignoram `.env` quando `ULTRON_SIMULATION=true`; V3/TCC carregam `.env` incondicionalmente. A atual também ignora seu JSON nesse modo (`config.py:39`).
- **Tolerância de relógio e continuidade.** Atual e HTTP têm tolerância de até 60 s para horário de coleta futuro e reinício da duração do estado depois de lacuna de comunicação/coleta; V3/TCC não reiniciam a duração nessa condição. Idempotência e rejeição de timestamps futuros já existem nas referências, portanto não são novidade absoluta da atual.
- **Administração, login, registro e criptografia não são uma função nova.** Após alinhar imports/nomes, `authService`, `adminService`, `adminBootstrap`, schemas de administração e os mecanismos de segurança mantêm a lógica das referências HTTP/V3/TCC. A atual continua exigindo usuário nas ocorrências por máquina e perfil administrativo no roteador de administração. Não foi identificada uma reformulação geral de permissões.
- **Origem Electron.** Atual, aninhada, Ultron (1), HTTP e V3 incluem `scomptec://app` na lista CORS em código. O TCC não inclui essa origem em `Main.py:20`.
- **Dependências do backend mudaram de localização.** HTTP/V3/TCC têm `requirements.txt` e `requirements-dev.txt` próprios dentro de `SCOMPTEC- Back`; a atual usa o arquivo de requisitos na raiz do projeto. Comparar apenas a ausência dentro de `backend` produziria falsa impressão de remoção de dependências.

## Testes presentes, sem execução

Contagem de definições Python `test*` por AST; parametrizações podem produzir mais casos durante execução.

| Backend | Módulos `test*.py` | Definições `test*` |
|---|---:|---:|
| Atual | 8 | 60 |
| Aninhada | 7 | 50 |
| Ultron (1) | 7 | 42 |
| HTTP | 6 | 37 |
| V3 | 3 | 27 |
| TCC | 3 | 27 |

Os testes novos mais específicos são `testEvents.py:164` (combinações e prioridade), `:193` (corrente e ausência), `:217` (corrente inválida), `:223` (saídas atuais e históricas), `testSignalOutputs.py:56` (64 snapshots) e `testDatabaseBootstrap.py:21` (criação de banco MySQL).

## Limites

Este relatório identifica comportamento previsto pelo código. Não inspeciona dados de uma instalação MySQL em execução, não comprova ligação elétrica, não mede desempenho e não comprova aprovação de testes. Nenhuma cronologia entre pastas foi inferida de nome ou data de arquivo.
