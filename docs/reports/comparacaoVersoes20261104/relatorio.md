# Relatório de diferenças entre as versões locais do SCOMPTEC

Data: **04/11/2026**. Versão de referência: `C:\Users\pedro\OneDrive\Desktop\UltronScomptec-main`.

## Resultado principal

Esta pasta tem **198 arquivos de projeto** e é **idêntica em caminhos e bytes ao conteúdo de `VERSÃOPRAMEXER.zip`**, localizado no Desktop. A confirmação usa SHA-256 de cada arquivo, com uma segunda conferência independente dos 198 arquivos. Os relatórios criados nesta análise e a cópia aninhada são considerados separadamente.

Ela é diferente das cinco outras pastas de projeto encontradas. A referência mais próxima é a pasta `UltronScomptec-main` que está **dentro desta própria pasta**: nessa comparação há **148 arquivos idênticos, 39 alterados e 11 adicionais**, sem arquivo exclusivo da cópia aninhada.

O diferencial mais específico desta versão é o perfil de **seis sinais**, com porta aberta, diagnósticos combinados, interpretações da API exibidas na dashboard e corrente opcional identificada como simulada. Contra as cópias da mesa seletora, a mudança é mais ampla: o firmware atual monitora CNC, enquanto aquelas cópias também comandam a mesa. Administração, login e o banco SQL já existiam nas outras versões.

**O código da aplicação, as configurações existentes e as outras cópias foram preservados.** Foram criados somente o material deste relatório em `docs/reports/comparacaoVersoes20261104/` e os arquivos de trabalho em `.local/comparacaoVersoes/`. Nenhum serviço, banco, instalação de dependência ou gravação de placa foi executado.

## Material entregue

- [Lista completa por arquivo, para todas as 11 comparações](C:/Users/pedro/OneDrive/Desktop/UltronScomptec-main/docs/reports/comparacaoVersoes20261104/diferencasPorArquivo.md)
- [Inventário verificável: caminhos, tamanhos, SHA-256, métricas de linhas e correspondências](C:/Users/pedro/OneDrive/Desktop/UltronScomptec-main/docs/reports/comparacaoVersoes20261104/inventarioComparativo.json)
- [Análise detalhada do backend, com evidências por arquivo e linha](C:/Users/pedro/OneDrive/Desktop/UltronScomptec-main/docs/reports/comparacaoVersoes20261104/analise-backend.md)
- [Análise detalhada do frontend, com evidências por arquivo e linha](C:/Users/pedro/OneDrive/Desktop/UltronScomptec-main/docs/reports/comparacaoVersoes20261104/analise-frontend.md)
- [Análise detalhada do firmware, ferramentas e inicialização](C:/Users/pedro/OneDrive/Desktop/UltronScomptec-main/docs/reports/comparacaoVersoes20261104/analise-firmware-tools.md)

## Cópias localizadas e escopo da busca

A busca percorreu as áreas acessíveis do perfil `C:\Users\pedro` e o disco `D:`, procurando nomes de projeto e arquivos compactados relacionados. Também foram inspecionados os níveis superiores de `C:`. Pastas do sistema, aplicativos instalados, caches e dependências não foram tratadas como outras versões do projeto. Atalhos recentes apontam para cópias; não são cópias adicionais.

Foram comparadas **seis pastas, contando a atual, e seis ZIPs**. São 12 inventários e 11 comparações contra a atual. Os nomes das pastas e as datas de arquivos não comprovam uma sequência de desenvolvimento.

| ID | Origem exata | Arquivos de projeto |
|---|---|---:|
| ATUAL | `C:\Users\pedro\OneDrive\Desktop\UltronScomptec-main` | 198 |
| ANINHADA | `C:\Users\pedro\OneDrive\Desktop\UltronScomptec-main\UltronScomptec-main` | 187 |
| ULTRON_1 | `C:\Users\pedro\OneDrive\Desktop\UltronScomptec-main (1)\UltronScomptec-main` | 163 |
| HTTP | `C:\Users\pedro\OneDrive\Desktop\SCOMPTECHTTP` | 168 |
| V3 | `C:\Users\pedro\OneDrive\Desktop\SCOMPTECV3` | 149 |
| TCC | `C:\Users\pedro\OneDrive\Desktop\ps3youtube\ScompTecTCC-main` | 148 |
| ZIP_ULTRON_1 | `C:\Users\pedro\OneDrive\Desktop\UltronScomptec-main (1).zip` | 163 |
| ZIP_ULTRON | `C:\Users\pedro\OneDrive\Desktop\UltronScomptec-main.zip` | 187 |
| ZIP_MEXER | `C:\Users\pedro\OneDrive\Desktop\VERSÃOPRAMEXER.zip` | 198 |
| ZIP_TCC | `C:\Users\pedro\Downloads\ScompTecTCC-main.zip` | 147 |
| ZIP_V3 | `C:\Users\pedro\OneDrive\Desktop\BeeGuardDataset\ALERT\SCOMPTECV3-20261021T215457Z-1-001.zip` | 149 |
| ZIP_ALERT | `C:\Users\pedro\OneDrive\Desktop\BeeGuardDataset\ALERT\UltronScomptec-main.zip` | 163 |

Não é possível garantir ausência de outras cópias em áreas protegidas, contas de outros usuários, mídias desconectadas ou arquivos com nomes sem relação identificável com o projeto. Dois erros de varredura ocorreram dentro de `.tools` de SCOMPTECHTTP: um caminho de toolchain não encontrado e um diretório temporário sem acesso. Nenhum erro ocorreu nos arquivos de projeto incluídos nas comparações.

## Quantidade de diferenças

A direção é **outra cópia → atual**. A tabela alinha caminhos correspondentes, como `SCOMPTEC- Back` → `backend`, `Schema` → `schemas`, nomes PascalCase/snake_case → camelCase, monitor da mesa → monitor CNC e a imagem de login PNG → WebP. São correspondências de papel ou nome, sem afirmar uma renomeação histórica.

“Iguais em outro caminho” têm o mesmo SHA-256. “Alterados” incluem mudanças de implementação, imports, formatação e binários; esse número não representa uma quantidade de funcionalidades. A comparação literal de caminhos também consta no JSON, para que a reorganização de pastas não esconda nenhum arquivo.

| Referência | Iguais no mesmo caminho | Iguais em outro caminho | Alterados | Só na atual | Só na referência |
|---|---:|---:|---:|---:|---:|
| ANINHADA | 148 | 0 | 39 | 11 | 0 |
| ULTRON_1 | 71 | 1 | 85 | 41 | 6 |
| HTTP | 0 | 41 | 113 | 44 | 14 |
| V3 | 0 | 40 | 98 | 60 | 11 |
| TCC | 0 | 39 | 97 | 62 | 12 |
| ZIP_ULTRON_1 | 71 | 1 | 85 | 41 | 6 |
| ZIP_ULTRON | 148 | 0 | 39 | 11 | 0 |
| ZIP_MEXER | 198 | 0 | 0 | 0 | 0 |
| ZIP_TCC | 0 | 39 | 97 | 62 | 11 |
| ZIP_V3 | 0 | 40 | 98 | 60 | 11 |
| ZIP_ALERT | 71 | 1 | 85 | 41 | 6 |

### Quais cópias são realmente iguais

- **ATUAL = ZIP_MEXER:** os 198 arquivos são iguais.
- **ANINHADA = ZIP_ULTRON:** os 187 arquivos são iguais. O ZIP chamado apenas `UltronScomptec-main.zip` do Desktop contém outro perfil, não o mesmo conteúdo da pasta atual.
- **V3 = ZIP_V3:** os 149 arquivos são iguais.
- **ZIP_ULTRON_1 = ZIP_ALERT:** os dois arquivos ZIP também têm o mesmo conteúdo de projeto; são duplicatas entre si.
- **ULTRON_1 difere do ZIP_ULTRON_1 em seis arquivos**, embora ambos tenham 163 caminhos: `README.md`, `firmware/optaMesaMonitor/config.h`, `mesaControl.cpp`, `telemetry.cpp`, `telemetry.h` e `tools/configurarTransmissao.py`. A pasta extraída acrescenta o modo IHM Modbus TCP, com coils 0–2 e tratamento de emergência; o ZIP não contém essa implementação. Portanto a diferença de Modbus citada neste relatório se refere à pasta ULTRON_1.
- **TCC difere do ZIP_TCC por um arquivo adicional:** `explicacao_backend.txt`. Os outros 147 arquivos são iguais.

## Diferenças específicas frente à cópia aninhada

Esta comparação isola o que mais caracteriza o conteúdo desta pasta. Tudo desta seção também distingue a atual do ZIP_ULTRON, porque esse ZIP é igual à aninhada.

### Sinais e entradas físicas

| Opta | Atual | Aninhada |
|---|---|---|
| I1/A0 | `ativo` | `em_execucao` |
| I2/A1 | `inativo` | `pausa` |
| I3/A2 | `emergencia` | `parada` |
| I4/A3 | `motor_ligado` | `emergencia` |
| I5/A4 | `alarme` | `motor_ligado` |
| I6/A5 | `porta_aberta` | `automatico` |
| I7/A6 | Livre, sem leitura | `manual` |
| I8/A7 | Corrente reservada, sem aquisição | `alarme` |

O código aberto passou de firmware 2.0.0/perfil `boolean_monitor_v1` para 2.1.0/perfil `six_signals_current_reserved_v2`. Somente I1–I6 são lidas digitalmente; I8 não é lida por ADC. O firmware publica corrente ausente, metadados de reserva e `physical_enabled=false`. Isso exige correspondência do CLP/cabeamento com o novo mapa: emergência e alarme mudaram de entrada.

O campo legado `machine_active` passa a exigir ativo e ausência de inativo. Os seis valores originais permanecem no evento mesmo em conflito.

Evidências: [firmware/optaCncMonitor/signalProfile.h](C:/Users/pedro/OneDrive/Desktop/UltronScomptec-main/firmware/optaCncMonitor/signalProfile.h:6), [firmware/optaCncMonitor/config.h](C:/Users/pedro/OneDrive/Desktop/UltronScomptec-main/firmware/optaCncMonitor/config.h:53), [firmware/optaCncMonitor/cncMonitor.cpp](C:/Users/pedro/OneDrive/Desktop/UltronScomptec-main/firmware/optaCncMonitor/cncMonitor.cpp:18) e [firmware/optaCncMonitor/telemetryPayload.h](C:/Users/pedro/OneDrive/Desktop/UltronScomptec-main/firmware/optaCncMonitor/telemetryPayload.h:10).

### Regras, diagnósticos e interpretações

- `ativo=true` indica operação; `inativo=true` impede operação. Um `ativo=false` explícito prevalece sobre aliases legados. Ausência de sinal continua “não informado”, sem deduzir o complemento.
- Emergência e alarme mantêm prioridade. Motor ligado isoladamente não comprova execução.
- Porta aberta + emergência gera **Operação falha**, mantendo `EMERGENCIA`.
- Ativo + inativo gera **Sinais de atividade conflitantes** e resulta em `PARADA` quando não há condição de maior prioridade.
- `signal_outputs` acrescenta código, nível, título, mensagem e sinais envolvidos. Interpreta pares, sinais isolados, ausência, leitura parcial, corrente e compatibilidade legada. Várias interpretações podem coexistir na mesma leitura.
- Status individual, consulta coletiva e histórico retornam essas interpretações. O histórico é calculado com cada leitura armazenada, sem copiar os sinais atuais.
- Mudanças de diagnóstico podem gerar aviso mesmo quando o estado resumido continua igual; a primeira carga não gera notificação de mudança. Interpretações informativas não geram avisos a cada consulta. A indisponibilidade preserva os últimos resultados e os identifica como antigos.

Evidências: [backend/services/machineState.py](C:/Users/pedro/OneDrive/Desktop/UltronScomptec-main/backend/services/machineState.py:4), [backend/services/signalOutputs.py](C:/Users/pedro/OneDrive/Desktop/UltronScomptec-main/backend/services/signalOutputs.py:23), [backend/services/cncService.py](C:/Users/pedro/OneDrive/Desktop/UltronScomptec-main/backend/services/cncService.py:125) e [frontend/src/services/monitoring.js](C:/Users/pedro/OneDrive/Desktop/UltronScomptec-main/frontend/src/services/monitoring.js:55).

### Corrente, simulador e ponte USB

A API de eventos aceita `analog_signals` e `extra_signals`. Corrente deve ser número finito e não negativo em ampères; `0 A` é válido e diferente de ausência. O número não determina o estado operacional.

O simulador muda para os seis sinais, usa `ativo` como padrão e acrescenta `--also` repetível e `--current`. A corrente gerada recebe origem `simulated`; sem esse argumento ela é omitida. Uma leitura posterior sem corrente não conserva o valor anterior. A ponte USB passa a preservar os campos analógicos e os metadados de corrente ao converter o quadro em evento por máquina.

Na interface, cartões, detalhes e gráfico identificam simulação. Dados recebidos sem origem física confirmada não são apresentados como medição física comprovada. **Esta versão não implementa a medição elétrica de corrente no Opta.**

### Dashboard

Surge o painel **Interações entre sinais**, com filtro por máquina e por nível, seis máquinas por página e duas interpretações por cartão. Os detalhes mostram todas as interpretações; cartões, alertas, histórico e modo TV também passam a exibi-las. O painel dos seis sinais é movido para o início dos detalhes e diferencia acionado, não acionado e não informado. O som de emergência passa a depender de aviso ainda não resolvido.

### Arquivos adicionais e volume por área

| Área | Arquivos alterados | Arquivos adicionais |
|---|---:|---:|
| Backend | 7 | 3 |
| Frontend | 15 | 5 |
| Firmware e testes C++ | 7 | 1 |
| Ferramentas e seus testes | 5 | 0 |
| Documentação | 3 | 1 |
| Raiz | 1 | 1 |
| Exemplos | 1 | 0 |
| **Total** | **39** | **11** |

Os 11 adicionais são:

- [backend/schemas/signalOutput.py](C:/Users/pedro/OneDrive/Desktop/UltronScomptec-main/backend/schemas/signalOutput.py)
- [backend/services/signalOutputs.py](C:/Users/pedro/OneDrive/Desktop/UltronScomptec-main/backend/services/signalOutputs.py)
- [backend/tests/testSignalOutputs.py](C:/Users/pedro/OneDrive/Desktop/UltronScomptec-main/backend/tests/testSignalOutputs.py)
- [docs/reports/sinaisOperacionaisCorrente.md](C:/Users/pedro/OneDrive/Desktop/UltronScomptec-main/docs/reports/sinaisOperacionaisCorrente.md)
- [firmware/optaCncMonitor/signalProfile.h](C:/Users/pedro/OneDrive/Desktop/UltronScomptec-main/firmware/optaCncMonitor/signalProfile.h)
- [frontend/src/components/signalOutputs/fleetSignalOutputs.jsx](C:/Users/pedro/OneDrive/Desktop/UltronScomptec-main/frontend/src/components/signalOutputs/fleetSignalOutputs.jsx)
- [frontend/src/components/signalOutputs/signalOutputList.jsx](C:/Users/pedro/OneDrive/Desktop/UltronScomptec-main/frontend/src/components/signalOutputs/signalOutputList.jsx)
- [frontend/src/services/cncSignals.test.js](C:/Users/pedro/OneDrive/Desktop/UltronScomptec-main/frontend/src/services/cncSignals.test.js)
- [frontend/src/services/signalOutputs.js](C:/Users/pedro/OneDrive/Desktop/UltronScomptec-main/frontend/src/services/signalOutputs.js)
- [frontend/src/services/signalOutputs.test.js](C:/Users/pedro/OneDrive/Desktop/UltronScomptec-main/frontend/src/services/signalOutputs.test.js)
- [Main.pdf](C:/Users/pedro/OneDrive/Desktop/UltronScomptec-main/Main.pdf)

O README foi ampliado com o setup local primeiro, exemplos de injeção de sinais, corrente, simulação, testes integrados e orientações web/Electron. Os guias de integração, equipe e explicação também foram ajustados. `Main.pdf` foi acrescentado como referência do ladder anterior; ele não comprova o novo mapa de seis sinais.

## Diferenças adicionais frente às outras pastas

Os recursos desta seção já estão presentes na aninhada, salvo indicação de outra referência.

### Backend e persistência

- O fluxo principal passa a usar eventos **por máquina**, com `MachineEvent`, `POST /api/events`, UUID/código/alias numérico e sem necessidade de MAC ou coletor cadastrado.
- `GET /api/cncs/statuses` retorna a frota em uma consulta. `GET /api/cncs/history` oferece histórico global paginado por máquina e período.
- Presença e estado são calculados para a máquina. O adaptador de telemetria por dispositivo continua disponível.
- Histórico legado e novo é preservado quando se remove ou realoca um coletor. ULTRON_1 bloqueia realocação com histórico e remove sua telemetria em cascata ao excluir o dispositivo. Excluir a própria CNC continua removendo seus eventos.
- A chave de ingestão aceita `X-API-Key` ou `X-Device-Key`, com `INGEST_API_KEY` e fallback `DEVICE_API_KEY`. Sem chave configurada, essa validação não exige credencial. Idempotência, conflitos 409 e rejeição de leituras futuras já existiam parcialmente na telemetria antiga; a atual aplica as regras ao fluxo genérico por máquina.
- Contra HTTP/V3/TCC, as cópias Ultron acrescentam `backend/config.json` e criação automática de banco MySQL inexistente. A prioridade é ambiente → `.env` → JSON. `configuracao.json` da raiz é inventário e não carrega a configuração da aplicação.
- SQLite isolado e ignorar `.env` na simulação **já existem no HTTP**; distinguem a atual de V3/TCC. A atual também ignora seu JSON na simulação.
- Login, cadastro, criptografia, usuários administrativos, ocorrências, regras, auditoria e exportação **já existem nas outras pastas**. Muitos arquivos desses módulos mudaram só de nomes/imports. As cópias antigas já usam backend SQL; o manifesto legado da raiz não prova uma migração exclusiva de MongoDB nesta versão.

### Frontend, navegação e consultas

- Monitoramento da frota por `/cncs/statuses`, sem consultar todos os coletores e o histórico/utilização de cada máquina a cada rodada. Histórico e utilização são carregados pelos componentes que precisam deles.
- Histórico global de 30 itens por página, com snapshot do horário final. O filtro de status atua somente na página recebida. Detalhes carregam até 100 leituras; utilização da frota usa concorrência limitada a quatro chamadas.
- Cache limitado, cancelamento, timeout de 10 s, pausa com aba oculta e bloqueio de consultas simultâneas. O intervalo de 5 s após terminar a rodada já existia nas outras cópias.
- Páginas e layouts carregados sob demanda, tratamento de erro de rota, gráficos adiados e relógio compartilhado para durações.
- Página `/recuperar-senha` passa a existir e orienta procurar o administrador; não há envio automático de e-mail implementado.
- Login troca PNG por WebP para desktop e celular e melhora identificação dos campos. Busca do cabeçalho, notificações, conta/logout, Escape, foco e navegação móvel receberam implementação/ajustes.
- Lista de máquinas tem paginação de 24 itens; resumo da dashboard limita oito máquinas e nove eventos recentes. Menu móvel controla rolagem e foco; CSS inclui alvos de toque e redução de movimento.
- A interface específica da mesa, com altura, metal, rampas, contadores e comandos O1/O2/O3, dá lugar ao monitor CNC. A página de dispositivos se torna **Coletores opcionais** e deixa de mostrar a mesma tabela de métricas de gateway.
- Tema claro e seletor claro/escuro distinguem a atual de HTTP/V3/TCC, mas já estão em ULTRON_1. Preservação de alertas durante falha da API já existe em HTTP/ULTRON_1; V3/TCC limpavam a lista.
- Configuração de API distingue web de Electron: URL relativa `/api` na web, absoluta no desktop; build web usa `/`, Electron usa `./`, e há `build:electron`. O protocolo local `scomptec://app` já existe em HTTP/V3/ULTRON_1; diferencia essas cópias do TCC.

### Firmware e transportes

O firmware atual e o aninhado monitoram entradas e não comandam os relés. ULTRON_1/HTTP/V3/TCC contêm controle de esteira, desvios e classificação de peças. A mudança de finalidade elimina essas funções de atuação do firmware principal atual.

| Referência | Comunicação principal observada |
|---|---|
| Atual e aninhada | USB por padrão, HTTP/Wi-Fi selecionável na compilação |
| ULTRON_1 em pasta | HTTP, USB ou IHM Modbus TCP; três coils, porta 502 |
| ZIP_ULTRON_1 e ZIP_ALERT | HTTP ou USB; sem a implementação Modbus da pasta |
| HTTP | Wi-Fi/HTTP |
| V3 | USB com quadros fragmentados `CNC_CHUNK:` |
| TCC | Wi-Fi/HTTP com ArduinoHttpClient |

A atual mantém thread de transporte separada, fila limitada, heartbeat, expiração e retry. Esses mecanismos já estão na aninhada; HTTP/ULTRON_1 também possuem parte desse núcleo. A fila em RAM não garante retenção de todas as transições. Os dois arquivos de código/configuração do ESP32 de referência (`.ino` e `platformio.ini`) foram preservados byte a byte nas seis pastas, com mudança de localização nas cópias Ultron; os README auxiliares não foram todos preservados.

### Inicialização e ferramentas

O launcher atual é igual ao da aninhada. Usa logs e controle de processos da própria pasta, verifica portas/saúde e permite iniciar, consultar ou parar os serviços. HTTP/ULTRON_1 já têm cuidados semelhantes; V3/TCC usam `iniciar.cmd` com terminais separados.

Na atual, `-Simular` inicia API/SQLite e frontend, mas **não inicia o produtor**. HTTP/ULTRON_1 iniciam simulador de dispositivo automaticamente. `simuladorWifi.py` foi substituído no fluxo atual por simulador de eventos JSON Lines + publicador HTTP. A ponte aceita identidade lógica, `--stdout` e compatibilidade com quadros/identidades antigos. O seletor atual compila `optaCncMonitor`, oferece HTTP/USB e limpa a pasta de exportação antes do build.

`iniciarLocal.ps1`, `requirements.txt`, `configuracao.json`, configuração de rede/transporte e os scripts gerais de ensaio são iguais entre atual e aninhada.

### Dependências e testes presentes

Os intervalos de dependências diretas e de desenvolvimento do frontend são iguais nas seis pastas. O lockfile atual é igual ao da aninhada e ULTRON_1; contra HTTP/V3/TCC há 56 entradas diferentes. Entre as resoluções fixadas estão Vite 8.2.1 → 8.3.5, Electron 43.4.1 → 43.8.3 e electron-builder 26.15.3 → 26.18.0. Isso descreve os arquivos, sem comprovar a versão instalada.

O manifesto Python da raiz atual consolida API SQL, ponte, testes e referências MongoDB. Nas cópias antigas, parte das dependências está em manifestos dentro do backend e das ferramentas.

| Pasta | Módulos de teste do backend | Definições Python `test*` | Arquivos frontend `*.test.js` |
|---|---:|---:|---:|
| Atual | 8 | 60 | 7 |
| Aninhada | 7 | 50 | 5 |
| ULTRON_1 | 7 | 42 | 4 |
| HTTP | 6 | 37 | 4 |
| V3 | 3 | 27 | 3 |
| TCC | 3 | 27 | 3 |

Parametrizações podem gerar mais casos que a quantidade de definições. Há novos cenários de seis sinais, corrente, ausência, diagnósticos e interpretações; a suíte específica de Wi-Fi/simulador antigo deixa de estar no mesmo fluxo. A presença desses testes não comprova aprovação. Os registros de testes existentes em `docs/reports` são relatos anteriores; não foram reproduzidos nesta análise.

## Inconsistências internas relevantes nesta versão

1. **ZIP interno do firmware desatualizado.** `firmware/archives/optaCncMonitor.zip` tem o perfil 2.0.0 de oito sinais, não contém `signalProfile.h` e é idêntico ao arquivo da aninhada. A pasta aberta tem 2.1.0/seis sinais. O seletor de compilação usa a pasta aberta, mas compilar o ZIP manualmente produz outro mapa de entradas.
2. **Inventário central parcialmente antigo.** `configuracao.json` continua igual ao da aninhada e ainda descreve firmware 2.0.0, perfil `boolean_monitor_v1`, sinais antigos e simulador com padrão `em_execucao`/oito estados. O código usa 2.1.0, seis sinais e padrão `ativo`. O arquivo é declarativo e não altera a aplicação por si só.
3. **OpenAPI exportado incompleto.** `docs/reference/openapi.json` não contém `/api/events`, `/api/cncs/statuses` nem `/api/cncs/history`, embora as rotas estejam no código atual. Não representa integralmente o contrato atual.
4. **Referências históricas com oito sinais.** `docs/reports/testesCncLocal.md` relata validação de 29/10 com oito entradas; o `Main.pdf` também representa o ladder anterior. Ambos exigem leitura no seu contexto histórico. O relatório `sinaisOperacionaisCorrente.md` descreve o perfil de seis sinais e registra limites de validação física.
5. **Link de contexto sem destino nesta cópia.** O README aponta para `docs/CONTEXTO_PROJETO.md`, mas esse arquivo não está presente no inventário atual.

Essas divergências foram registradas e preservadas, pois o pedido é comparar e relatar.

Evidências: [configuracao.json](C:/Users/pedro/OneDrive/Desktop/UltronScomptec-main/configuracao.json:305), [configuracao.json](C:/Users/pedro/OneDrive/Desktop/UltronScomptec-main/configuracao.json:476), [docs/reference/openapi.json](C:/Users/pedro/OneDrive/Desktop/UltronScomptec-main/docs/reference/openapi.json:8), [docs/reports/testesCncLocal.md](C:/Users/pedro/OneDrive/Desktop/UltronScomptec-main/docs/reports/testesCncLocal.md:19).

## Arquivos locais, dependências instaladas e limites

SCOMPTECHTTP tem ambientes e artefatos que não existem nas demais árvores com a mesma estrutura: `.venv`, `node_modules`, `.build`, `.tools`, `.local`, `dist`, `.vite` e caches Python. Foram contabilizados **58.531 arquivos acessíveis** nessas categorias, somando **3.625.504.814 bytes (cerca de 3,63 GB decimais)**. A contagem é parcial somente nos dois diretórios de `.tools` com erro citados antes. A presença desses arquivos não comprova que a instalação funciona ou está em execução.

Essas categorias foram separadas do código; seus totais e tamanhos constam no JSON. Não foram produzidos diffs de bibliotecas instaladas, logs, bancos ou binários de toolchain. Também foram excluídos metadados Git, caches de editor e os próprios arquivos desta análise. A cópia aninhada foi inventariada como projeto separado, evitando duplicar seus arquivos dentro da atual.

Não foram encontrados arquivos locais `.env`, `backend/config.json` ou `optaSecrets.h` junto aos arquivos de projeto incluídos; os modelos de configuração foram comparados. Nenhum valor de credencial foi reproduzido no relatório.

A comparação identifica conteúdo e comportamento previsto pelo código. Não estabelece autoria, datas de cada alteração, ordem de commits ou desempenho medido. A pasta atual não contém repositório `.git` acessível para reconstruir esse histórico. Não houve consulta ao banco em uso, teste de navegador, execução de suíte ou ensaio elétrico.

O inventário completo permite consultar **cada diferença de arquivo**, inclusive conteúdo preservado em outro caminho e itens sem correspondência. SHA-256 prova igualdade de bytes; a interpretação funcional está fundamentada nas análises de backend, frontend e firmware anexas.
