# Análise de firmware, ferramentas e inicialização

Data: 04/11/2026. Comparação estática, sem iniciar serviços, acessar banco ou gravar placa.

## Referências comparadas

- **Atual**: `C:\Users\pedro\OneDrive\Desktop\UltronScomptec-main`.
- **Aninhada**: `C:\Users\pedro\OneDrive\Desktop\UltronScomptec-main\UltronScomptec-main`.
- **Ultron (1)**: `C:\Users\pedro\OneDrive\Desktop\UltronScomptec-main (1)\UltronScomptec-main`.
- **HTTP**: `C:\Users\pedro\OneDrive\Desktop\SCOMPTECHTTP`.
- **V3**: `C:\Users\pedro\OneDrive\Desktop\SCOMPTECV3`.
- **TCC**: `C:\Users\pedro\OneDrive\Desktop\ps3youtube\ScompTecTCC-main`.

Não foram encontrados arquivos AGENTS.md nos diretórios de código examinados. Pastas de dependências e caches não foram usadas como evidência funcional. Os nomes acima identificam cópias, sem presumir a ordem cronológica entre elas.

## Mudança de finalidade do firmware

A diferença principal em relação a Ultron (1), HTTP, V3 e TCC é que a Atual **monitora uma CNC e não controla a mesa seletora**. A Atual não configura saídas de relé nem chama `digitalWrite` no perfil principal. As outras quatro cópias têm controle de esteira e desvios, sensores de altura/metal/queda, estados de classificação e contadores. Isso é uma mudança de aplicação, não apenas uma troca de nomes.

Evidências: Atual `firmware/optaCncMonitor/cncMonitor.cpp:8`, `:16`, `:36`; Ultron (1) `firmware/optaMesaMonitor/mesaControl.cpp:25`, `:182`, `:401`, `:411`; V3 `firmware/opta_mesa_monitor/Telemetry.cpp:25`–`:43` inclui alturas, rampas, saídas comandadas e contadores no payload. O arquivo principal passou de `optaMesaMonitor`/`opta_mesa_monitor` para `optaCncMonitor`.

A Aninhada já é um monitor sem atuação. Portanto a ausência de controle da mesa não é exclusiva da Atual quando a referência é a Aninhada.

## Entradas físicas: Atual contra Aninhada

| Entrada Opta | Atual | Aninhada |
|---|---|---|
| I1/A0 | `ativo` | `em_execucao` |
| I2/A1 | `inativo` | `pausa` |
| I3/A2 | `emergencia` | `parada` |
| I4/A3 | `motor_ligado` | `emergencia` |
| I5/A4 | `alarme` | `motor_ligado` |
| I6/A5 | `porta_aberta` | `automatico` |
| I7/A6 | Livre, não lida | `manual` |
| I8/A7 | Reservada para corrente, não lida | `alarme` |

Na Atual, somente os seis primeiros pinos são lidos digitalmente. Todos os oito ficam configurados como `INPUT`, mas I7/I8 não são lidos e I8 não tem leitura ADC. A máscara de polaridade é limitada a `0x3F`. O nome do perfil é `six_signals_current_reserved_v2`; o da Aninhada é `boolean_monitor_v1`.

O campo de compatibilidade `machine_active` também mudou: na Atual exige I1 ativo **e** I2 inativo falso; na Aninhada depende apenas de I1. Os seis booleanos continuam sendo serializados individualmente, inclusive em conflito.

Evidências: Atual `firmware/optaCncMonitor/signalProfile.h:6`–`:14`, `cncMonitor.cpp:18`, `:38`, `:43`, `telemetryPayload.h:10`–`:29`; Aninhada `firmware/optaCncMonitor/telemetryPayload.h:10`–`:26`.

O payload atual deixa de publicar `extra_signals.clp_inputs.D000..D007`. Em seu lugar informa `spare_input=I7` e `current_input` com entrada I8, unidade A, origem `unavailable` e `physical_enabled=false`. `analog_signals` permanece vazio no firmware. Portanto a Atual prepara o contrato de corrente, mas **não mede corrente física**.

As versões declaradas no código aberto são `opta-monitor-usb-2.1.0` ou `opta-monitor-wifi-2.1.0`, contra `2.0.0` na Aninhada (`config.h:52`–`:55`).

## Transporte e confiabilidade

| Cópia | Transporte do perfil principal |
|---|---|
| Atual | USB por padrão; Wi-Fi/HTTP selecionável na compilação |
| Aninhada | Mesmo seletor USB/HTTP e mesmo núcleo de transporte da Atual |
| Ultron (1) | HTTP, USB ou servidor Modbus TCP selecionáveis na compilação |
| HTTP | Wi-Fi/HTTP no firmware principal |
| V3 | USB, envio por fragmentos `CNC_CHUNK:` |
| TCC | Wi-Fi/HTTP, com ArduinoHttpClient e snapshot compartilhado |

Na Atual o seletor aceita apenas `ULTRON_TELEMETRY_USB=0/1`; USB é o padrão (`config.h:19`–`:29`). O script `tools/configurarTransmissao.py:14` aceita somente `http` e `usb`. Em Ultron (1) o script também aceita `modbus`, e `telemetry.cpp:23`–`:70` implementa servidor na porta 502, três coils e prioridade de emergência. A Atual removeu esse modo e não recebe comandos de modo da IHM por Modbus.

O transporte da Atual roda em thread separada, mantém a leitura das entradas fora do I/O e não segura o mutex durante escrita USB. Serial opera a 115200. O núcleo usa fila de 16 leituras, heartbeat de 1 s, expiração de 15 s, reconexão Wi-Fi de 5 s, timeout HTTP de 4 s e intervalo de retry de 1 s. As transições são enfileiradas e os retries HTTP reaproveitam o corpo/event_id. Falhas transitórias 408/429/5xx preservam pendência; erros permanentes descartam explicitamente; 404 provoca novo cadastro. A fila é em RAM e não garante preservação de toda transição durante interrupções.

Esses mecanismos **já existem na Aninhada**, com arquivos `telemetry.cpp`, `telemetryCore.h` e `httpResponse.h` idênticos byte a byte à Atual. HTTP e Ultron (1) também possuem núcleo com fila/retry, embora com outros snapshots. Não seria correto atribuir toda a confiabilidade exclusivamente à Atual.

Evidências Atual: `telemetry.cpp:19`–`:37`, `:86`–`:155`, `:164`; `config.h:57`–`:62`; `telemetryCore.h:68`–`:85`, `:126`. V3 `Telemetry.cpp:18`, `:49`–`:63` faz fragmentação de 32 bytes com intervalo de 5 ms; TCC `Telemetry.cpp:195`–`:227` mantém uma leitura pendente e reaproveita o mesmo corpo.

## Ponte USB e identidade

A Atual permite usar o ID lógico da máquina enviado pelo firmware, sobrescrever com `--machine-id` ou manter a compatibilidade por `--mac`/`--device-id`. O fluxo padrão publica em `/api/events`; não precisa cadastrar coletor por MAC. Ultron (1) só oferece `--mac`/`--device-id` e publica telemetria de dispositivo.

Atual `tools/ponteUsb.py:116`–`:155`, `:230`–`:235`; Ultron (1) `tools/ponteUsb.py:146`, `:220`–`:222`.

A opção `--stdout` da Atual emite JSON Lines e permite desacoplar aquisição e publicação. A chave HTTP da ponte dá preferência a `INGEST_API_KEY`, com compatibilidade `DEVICE_API_KEY`. São funcionalidades compartilhadas com a Aninhada, diferentes de Ultron (1)/HTTP/V3. A ponte continua entendendo `CNC_JSON:` e `CNC_CHUNK:` de dispositivos anteriores (`ponteUsb.py:28`–`:32`).

O acréscimo específico contra a Aninhada é preservar `analog_signals` e `extra_signals.current_input` ao converter o quadro USB em evento de máquina (`ponteUsb.py:134`–`:144`). Antes essa conversão descartava esses campos. O timestamp continua sendo UTC da recepção USB, estável nos retries, e não uma prova do horário de captura no hardware. A fila da ponte mantém no máximo uma leitura aguardando envio e a pendência expira após 15 s (`ponteUsb.py:19`, `:134`, `:167`, `:208`–`:211`, `:254`).

## Simulação e publicação

A Atual tem `tools/simuladorCnc.py`, que produz JSON Lines sem rede/hardware, e `tools/publicarEventos.py`, que publica essas linhas em `/api/events`. A Aninhada já tem os dois arquivos, mas seu simulador emite os oito sinais antigos e não oferece corrente/combinações.

Específico da Atual contra a Aninhada:

- Os seis sinais da tabela física substituem os oito antigos; o estado padrão passa de `em_execucao` para `ativo`.
- `--also` pode ser repetido para acionar sinais simultâneos.
- `--current` aceita corrente finita e não negativa em A, inclusive zero. O valor recebe origem `simulated`, entrada I8 e medição física desativada.
- Sem `--current`, o evento omite corrente; a ferramenta não inventa zero.

Evidência: `simuladorCnc.py:10`–`:28`, `:33`–`:42`. O publicador é idêntico ao da Aninhada; lê chave de ingestão/compatibilidade, usa header `X-API-Key`, rejeita JSON numérico não finito e encerra com erro ao falhar (`publicarEventos.py:13`, `:25`–`:37`).

Ultron (1)/HTTP usam `simuladorWifi.py`/`simulador_wifi.py`, simulando dispositivo/rede e publicando diretamente. Esse arquivo não está mais presente na Atual. V3 só tem ponte USB nos diretórios de ferramentas examinados; TCC não tem diretório tools no mesmo layout.

## Inicialização e configuração

`iniciarLocal.ps1` da Atual é idêntico ao da Aninhada. Ele mantém registro da pasta, PID, caminho do executável e horário de criação para reconhecer processos próprios; faz checagem de portas e disponibilidade HTTP; grava logs em `.local`; tem ações todos/backend/frontend/verificar/parar. Esses cuidados também existem em HTTP e Ultron (1), com caminhos antigos.

Contra Ultron (1)/HTTP, as mudanças relevantes são:

- Pastas e módulos agora são `backend`, `frontend` e `main:app`, em vez de `SCOMPTEC- Back`, `scomptec-cnc front 2` e `Main:app`.
- `-Simular` usa SQLite separado e timeout de 10 s, mas **não inicia um produtor de eventos automaticamente**. Ultron (1) e HTTP iniciam um simulador de dispositivo em segundo plano.
- Inclui `INGEST_API_KEY`, `EVENT_OFFLINE_TIMEOUT_SECONDS` e `CORS_ORIGINS` no ambiente temporário; limpa a chave de ingestão na simulação; adiciona as origens locais da dashboard ao CORS.
- A API inicia em `0.0.0.0`; a dashboard em `127.0.0.1`, com URL absoluta da API. Esse detalhe já existe no launcher HTTP/Ultron (1).

Evidências Atual: `iniciarLocal.ps1:15`–`:36`, `:85`–`:112`, `:123`–`:156`; Ultron (1) `iniciarLocal.ps1:151` e HTTP `iniciar-local.ps1:151`. V3 e TCC usam `iniciar.cmd`, abrem terminais separados com backend `--reload` e frontend npm; o encerramento é manual com Ctrl+C (V3 `iniciar.cmd:45`–`:64`, TCC `iniciar.cmd:44`–`:63`).

O script `configurarTransmissao.py` atual limpa a pasta de exportação antes de compilar, evitando que binários de sketches diferentes permaneçam na mesma pasta de upload; essa preparação não existe em Ultron (1). Ele compila o novo `optaCncMonitor`, aceita caminho do CLI/configuração e opção apenas compilar. É idêntico ao da Aninhada (`configurarTransmissao.py:32`–`:53`).

Os arquivos `tools/configurarRede.ps1`, `tools/testarOpta.ps1`, `tools/testarProjeto.ps1`, `requirements.txt` e `configuracao.json` são idênticos entre Atual e Aninhada.

O `requirements.txt` atual consolida API SQL, ponte USB, testes e dependências MongoDB legadas. Nos projetos HTTP/V3/TCC, o requirements da raiz ainda lista bibliotecas legadas, mas `SCOMPTEC- Back/requirements.txt` já contém SQLAlchemy/PyMySQL. Portanto a diferença de manifesto da raiz **não demonstra uma migração exclusiva de MongoDB para SQL nesta cópia**.

## Verificações presentes no código

Contra a Aninhada, os testes atuais de firmware foram alterados para seis sinais, para ignorar I7/I8, manter saídas intactas e serializar a reserva de corrente. Os testes de simulador/ponte receberam casos de corrente e combinações simultâneas. A rotina de navegador recebeu dados e verificações para os seis sinais, corrente simulada, diagnósticos e painel de interações.

Evidências: `firmware/tests/host/testControl.cpp:19`–`:37`; `testTelemetry.cpp:31`–`:59`; `tools/tests/testEventTools.py`; `tools/tests/testPonteUsb.py`; `tools/testarFrontend.py:19`, `:34`–`:61`, `:104`–`:107`, `:117`.

`tools/testarProjeto.ps1` já executa pytest, frontend test/lint/build e, opcionalmente, firmware, com logs por execução e SQLite isolado. A Atual e a Aninhada têm o mesmo script; contra Ultron (1), foram acrescentadas as variáveis de isolamento ligadas a ingestão/eventos (`testarProjeto.ps1:74`–`:99`). Isso descreve os testes existentes, **não resultados de uma execução nesta análise**. O teste de navegador importa o interpretador do backend para construir respostas simuladas; a validação visual não é, isoladamente, uma implementação independente das regras da API.

## Inconsistência interna comprovada: ZIP de firmware desatualizado

`firmware/archives/optaCncMonitor.zip` da Atual é idêntico ao da Aninhada (SHA-256 iniciado por `90e3abcf57ad`). O ZIP contém 12 arquivos do perfil **2.0.0 com oito sinais**, não contém `signalProfile.h` e ainda lê I1–I8 e publica `em_execucao`, `pausa`, `parada`, `emergencia`, `motor_ligado`, `automatico`, `manual`, `alarme` e `clp_inputs.D000..D007`.

Já a pasta aberta contém o perfil **2.1.0 com seis sinais**. Assim, o conteúdo arquivado não representa o firmware principal atual. O script de compilação usa a pasta aberta (`configurarTransmissao.py:37`), mas compilar manualmente a partir do ZIP produz outro mapeamento. Nenhum arquivo foi corrigido nesta análise.

## Conteúdo preservado

O firmware ESP32 de referência é byte a byte igual entre as seis cópias examinadas; mudou a posição para `firmware/legacy/esp32CncMonitor` na Atual/Aninhada/Ultron (1). No grupo Atual/Aninhada, os transportes, filtros básicos, parser HTTP, scripts de rede/transporte/ensaio e dependências principais também permanecem iguais. As alterações exclusivas da Atual concentram-se no perfil de seis sinais, reserva de corrente, preservação desses campos na ponte, simulador e cobertura de testes/validação correspondente.
