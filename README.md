# SCOMPTEC

Monitoramento de máquinas CNC com Arduino Opta, API FastAPI, MySQL e dashboard React. Exibe estados, alertas e histórico a partir dos sinais disponibilizados pela IHM/CLP.

## Acesso administrativo

Credenciais configuradas para a conta administrativa desta instalação. A API cria ou atualiza essa conta ao iniciar em modo normal.

| Campo | Valor |
|---|---|
| Login | http://127.0.0.1:5173/login |
| E-mail | ` admin@empresa.com.br ` |
| Senha | ` SUBSTITUA_POR_SENHA_ADMINISTRATIVA ` |
| Painel administrativo | http://127.0.0.1:5173/admin |

O launcher com `-Simular` não importa essas credenciais nem cria automaticamente a conta administrativa. Para uma conta de teste, consulte [Autenticação e administração](#autenticação-e-administração).

## Sumário

- [Acesso administrativo](#acesso-administrativo)
- [Funcionamento](#funcionamento)
  - [Sinais e regras da aplicação](#sinais-e-regras-da-aplicação)
  - [Interpretações na dashboard](#interpretações-na-dashboard)
  - [Mapeamento físico atual do Opta](#mapeamento-físico-atual-do-opta)
  - [Corrente na entrada I8](#corrente-na-entrada-i8)
- [Setup](#setup)
  - [Dependências no Linux](#dependências-no-linux)
  - [Dependências no Windows](#dependências-no-windows)
  - [Configuração do frontend](#configuração-do-frontend)
- [1) Setup para testes locais](#1-setup-para-testes-locais)
  - [a) Setup e inicialização](#a-setup-e-inicialização)
    - [Linux / Bash](#linux--bash)
    - [Windows / PowerShell](#windows--powershell)
  - [b) Lista de comandos úteis](#b-lista-de-comandos-úteis)
- [2) Setup para teste integrado com o CLP](#2-setup-para-teste-integrado-com-o-clp)
  - [Preparar os sinais do CLP](#preparar-os-sinais-do-clp)
  - [Setup e inicialização no Linux](#setup-e-inicialização-no-linux)
    - [1. Configurar MySQL e backend](#1-configurar-mysql-e-backend)
    - [2. Iniciar a API e cadastrar a máquina](#2-iniciar-a-api-e-cadastrar-a-máquina)
    - [3. Gravar o Opta](#3-gravar-o-opta)
    - [4. Iniciar a ponte USB](#4-iniciar-a-ponte-usb)
    - [5. Abrir a dashboard](#5-abrir-a-dashboard)
  - [Setup e inicialização no Windows (PowerShell)](#setup-e-inicialização-no-windows-powershell)
- [Acesso e distribuição da dashboard](#acesso-e-distribuição-da-dashboard)
  - [Acesso pela rede](#acesso-pela-rede)
  - [Hospedagem web](#hospedagem-web)
  - [Aplicativo desktop (Electron)](#aplicativo-desktop-electron)
- [Eventos e consultas](#eventos-e-consultas)
- [Autenticação e administração](#autenticação-e-administração)
- [Testes](#testes)
- [Estrutura e referências](#estrutura-e-referências)

## Funcionamento

```text
IHM/CLP → Opta → USB → ponte Python → API → MySQL
                                      ↑
                                Dashboard React
```

1. A IHM/CLP disponibiliza os seis sinais digitais do perfil configurado.
2. O Opta lê as entradas e envia estados pela serial USB a 115200 baud, nas mudanças e com heartbeat de 1 s.
3. `tools/ponteUsb.py` converte as leituras em eventos e envia para `POST /api/events`.
4. A API valida e grava os eventos por máquina no MySQL.
5. A dashboard consulta a API; cada nova rodada começa 5 s após a anterior terminar.

### Sinais e regras da aplicação

O perfil atual da aplicação acompanha seis sinais booleanos independentes:

| Chave em `states` | Significado |
|---|---|
| `ativo` | Atividade da máquina informada pelo produtor |
| `inativo` | Inatividade informada pelo produtor |
| `emergencia` | Emergência acionada |
| `motor_ligado` | Motor ligado; isoladamente não significa execução |
| `alarme` | Alarme / erro |
| `porta_aberta` | Porta aberta |

Com os seis parâmetros da IHM em `false` (0), o status é `OPERANDO`. Qualquer um desses parâmetros em `true` (1) leva a `EMERGENCIA`, inclusive `ativo`, `inativo`, `motor_ligado` e `porta_aberta`. A interpretação prioritária em `signal_outputs` identifica todos os parâmetros em 1 pelo nome e pela chave. Quando todos voltam a 0, a emergência é encerrada. Os valores recebidos são preservados; um sinal ausente continua **não informado** e uma leitura incompleta não confirma que todos estão em 0. Os tratamentos de comunicação, tensão dedicada e atividade no formato legado continuam disponíveis.

As consultas de status individual e coletivo também retornam `diagnostics`, calculados a partir da mesma leitura:

- `porta_aberta=true` + `emergencia=true`: **Operação falha**, mantendo o estado `EMERGENCIA`.
- `ativo=true` + `inativo=true`: **Sinais de atividade conflitantes**, com estado `EMERGENCIA` pela regra dos parâmetros da IHM.

Os diagnósticos aparecem nos detalhes, cartões e alertas. Uma nova combinação gera notificação mesmo quando o estado resumido continua igual. Em perda de comunicação, o último diagnóstico é identificado como antigo; os valores recebidos são preservados. A primeira carga não cria notificações de mudança.

### Interpretações na dashboard

O painel **Interações entre sinais** mostra saídas calculadas pela API em `signal_outputs`, com código, nível, título, mensagem e sinais envolvidos. Há filtros por máquina e por nível (**Informativo**, **Atenção**, **Crítico**), com seis máquinas por página e duas interpretações resumidas por cartão. Os detalhes mostram todas as saídas; cartões, alertas, histórico e modo TV também exibem interpretações.

Na dashboard, o gráfico de setores **Principais causas de falhas** aparece abaixo do gráfico de alertas, com cores por parâmetro, legenda, quantidades e percentuais. Ambos usam o mesmo período de 8, 12 ou 24 horas e as máquinas do contexto selecionado. A API agrega os novos acionamentos em `failure_causes` por hora: leituras repetidas de um sinal continuamente acionado não aumentam a contagem; causas simultâneas contam separadamente. Após uma lacuna superior ao timeout, um sinal acionado inicia uma nova ocorrência observada. Os dados vêm do histórico completo do período, sem limitar a contagem às últimas leituras da dashboard.

As combinações da [tabela do relatório](docs/reports/sinaisOperacionaisCorrente.md#resultado-das-interações-entre-sinais) continuam gerando saídas, assim como corrente simulada e leitura parcial. A classificação operacional segue a regra atual da IHM descrita acima; o relatório registra as interpretações anteriores. Mais de uma regra pode corresponder à mesma leitura. As saídas não modificam os sinais recebidos e não acionam relés. As consultas de status e histórico usam a mesma interpretação; o histórico é calculado a partir de cada leitura armazenada, sem copiar o estado atual.

Uma alteração de sinais atualiza o painel mesmo sem mudança de status. As notificações existentes continuam ligadas a mudanças de estado e aos dois diagnósticos específicos; interpretações informativas não geram notificações a cada atualização. Em perda de comunicação, os últimos resultados são identificados como antigos.

### Mapeamento físico atual do Opta

O perfil `six_signals_current_reserved_v3` (firmware USB/HTTP 2.1.1) segue o mapa da IHM informado para esta instalação. A tabela descreve a ligação sequencial esperada de Q0.0–Q0.5 a I1–I6; a ligação elétrica e a polaridade ainda precisam ser conferidas na bancada. O `Main.pdf` representa o mapeamento anterior, com oito redes `%M0.0`–`%M0.7` → `%Q0.0`–`%Q0.7`, sem porta aberta, e não comprova essa ligação atual.

| Saída IHM/CLP esperada | Indicação na IHM | Opta | Pino | Chave em `states` / finalidade |
|---|---|---|---|---|
| Q0.0 | Em execução | I1 | A0 | `ativo` |
| Q0.1 | Parada | I2 | A1 | `inativo` |
| Q0.2 | Emergência | I3 | A2 | `emergencia` |
| Q0.3 | Motor ligado | I4 | A3 | `motor_ligado` |
| Q0.4 | Porta aberta | I5 | A4 | `porta_aberta` |
| Q0.5 | Alerta erro | I6 | A5 | `alarme` |
| — | — | I7 | A6 | Reserva livre |
| — | — | I8 | A7 | Corrente em A, medição física desativada |

O firmware apenas monitora entradas. Polaridade e filtros ficam em [config.h](firmware/optaCncMonitor/config.h). As filas são limitadas e ficam em RAM; interrupções podem perder transições. O perfil atual observa booleanos e não implementa protocolos proprietários Mitsubishi ou controle de atuadores. Nomes legados de execução (`em_execucao`/`ciclo`/`cycle`) continuam aceitos pela aplicação; o histórico e outros sinais recebidos são preservados.

### Corrente na entrada I8

I8/A7 fica configurada como entrada reservada. O firmware não executa leitura digital ou ADC nessa porta e não publica uma corrente fictícia. Sem sensor e calibração, `analog_signals` permanece vazio e a dashboard mostra **NÃO INFORMADO**, distinguindo ausência de valor de uma corrente válida de `0 A`. A reserva aparece em `extra_signals.current_input`, com unidade `A`, origem `unavailable` e `physical_enabled=false`.

A API aceita o campo opcional `analog_signals.current`, com número finito e não negativo em ampères, além de `extra_signals` para identificar a origem. Para simular uma corrente, com a API e a máquina já cadastradas, pare outro produtor que esteja enviando snapshots para essa CNC e execute:

```bash
.venv/bin/python tools/simuladorCnc.py --machine-id CNC-001 --state ativo --current 12.5 --count -1 --interval 1 \
  | .venv/bin/python tools/publicarEventos.py --api http://127.0.0.1:8000/api --key=
```

No PowerShell:

```powershell
& .\.venv\Scripts\python.exe tools/simuladorCnc.py --machine-id CNC-001 --state ativo --current 12.5 --count -1 --interval 1 |
  & .\.venv\Scripts\python.exe tools/publicarEventos.py --api http://127.0.0.1:8000/api --key=
```

Troque `12.5` pelo valor desejado, inclusive `0`. O comando marca a origem como `simulated`; cartões, detalhes e gráfico identificam a simulação. Uma leitura posterior sem corrente volta a indicar valor não informado, sem carregar o número anterior. A reserva de I8 não configura saídas de relé e não habilita uma medição física sem sensor.

Para usar os **sinais reais da IHM/Opta** com uma corrente virtual fixa, acrescente a simulação na própria ponte USB:

```powershell
& .\.venv\Scripts\python.exe tools/ponteUsb.py --listar-portas
# Use a porta do Opta e o código da CNC cadastrada:
& .\.venv\Scripts\python.exe tools/ponteUsb.py --porta COM4 --machine-id CNC-001 --simular-corrente
```

`--simular-corrente` usa **24 A** como valor padrão. Para escolher outro valor, inclusive zero, use `--corrente 18.2` ou `--corrente 0` no lugar dessa opção. O valor é fixo: a troca é feita pelo argumento, sem mudança automática pelos sinais. Interrompa a ponte com `Ctrl+C` antes de iniciá-la com outro valor. Sem ambas as opções, a ponte mantém o comportamento normal de corrente ausente ou recebida.

Essa opção acrescenta apenas `analog_signals.current` à mesma leitura recebida, marcada como `simulated` e `physical_enabled=false`. Os seis sinais, seu mapeamento e suas regras permanecem os recebidos do Opta; não é necessário regravar a placa para mudar o valor virtual. Uma corrente já recebida, inclusive zero e o alias `corrente`, ou um sensor declarado fisicamente habilitado têm prioridade e não são substituídos. Use somente essa ponte para a CNC em teste; um simulador separado enviaria outro snapshot sobre os sinais reais.

Para **trocar somente a corrente por comando, sem reiniciar a ponte a cada troca**, inicie a ponte com `--arquivo-corrente`. Execute os comandos na raiz do projeto e use um arquivo diferente para cada máquina.

Linux, no terminal da ponte:

```bash
.venv/bin/python tools/ponteUsb.py --porta /dev/ttyACM0 --machine-id CNC-001 --arquivo-corrente .local/corrente-CNC-001.txt
```

Em outro terminal, injete o valor desejado:

```bash
printf '12.5\n' > .local/corrente-CNC-001.txt
```

Windows / PowerShell, no terminal da ponte:

```powershell
& .\.venv\Scripts\python.exe tools/ponteUsb.py --porta COM4 --machine-id CNC-001 --arquivo-corrente .local/corrente-CNC-001.txt
```

Em outro terminal:

```powershell
Set-Content -Path .local/corrente-CNC-001.txt -Value '12.5' -Encoding ascii
```

A ponte cria a pasta do arquivo, lê o número a cada nova leitura USB e envia a corrente junto dos sinais reais. Use ponto decimal e um valor não negativo, inclusive `0`. A dashboard atualiza na consulta seguinte. Um arquivo ausente ou inválido mantém a última corrente válida; antes do primeiro valor válido, a corrente continua não informada, ou usa `--corrente` / `--simular-corrente` se fornecidos. Retries mantêm o valor da leitura original. Sem novas leituras USB, o comando não cria eventos nem faz a máquina parecer online.

## Setup

Escolha o método de acordo com o que deseja executar:

| Método | Origem dos dados | Banco | Requisitos adicionais |
|---|---|---|---|
| [1) Testes locais](#1-setup-para-testes-locais) | Simulador Python → publicador HTTP | SQLite em arquivo local | Nenhum hardware ou servidor MySQL |
| [2) Teste integrado com CLP/Opta](#2-setup-para-teste-integrado-com-o-clp) | IHM/CLP → Opta → USB → ponte Python | MySQL 8 | Opta, cabo USB de dados e Arduino CLI |

Os dois métodos usam **Python 3.10+** e **Node.js 22.12+ com npm**. Faça a preparação comum abaixo e depois siga somente o método escolhido. Execute todos os comandos na raiz do repositório; mantenha essa pasta também nos novos terminais.

### Dependências no Linux

No Ubuntu/Mint/Debian, com Node.js e npm já instalados:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip build-essential curl jq
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
npm --prefix frontend ci
```

### Dependências no Windows

Com Python e Node.js/npm instalados, abra o PowerShell na raiz do projeto:

```powershell
py -3 -m venv .venv
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
npm --prefix frontend ci
```

Os exemplos principais abaixo usam Bash. Cada método inclui seu procedimento em PowerShell; não é necessário ativar o ambiente virtual.

### Configuração do frontend

Copie o modelo somente se o arquivo local ainda não existir.

Linux:

```bash
cp -n frontend/.env.example frontend/.env
```

Windows:

```powershell
if (-not (Test-Path frontend/.env)) { Copy-Item frontend/.env.example frontend/.env }
```

Confira estes valores em `frontend/.env`, inclusive se o arquivo já existia:

```dotenv
VITE_API_BASE_URL=/api
VITE_USE_MOCKS=false
```

Mantenha `VITE_USE_MOCKS=false` também na simulação: os dados simulados devem passar pela API e pelo banco. No desenvolvimento, o Vite encaminha `/api` para `http://127.0.0.1:8000`. Reinicie o frontend após alterar o `.env`.

<a id="testar-sem-hardware"></a>

## 1) Setup para testes locais

Este modo testa API, SQLite e dashboard com sinais produzidos por comandos. Não exige CLP, Opta, Arduino CLI ou servidor MySQL. Faça primeiro a [preparação comum](#setup); os exemplos usam o ambiente virtual sem precisar ativá-lo.

### a) Setup e inicialização

#### Linux / Bash

Use três terminais na raiz do repositório. Se a porta 8000 já estiver ocupada por uma API do projeto, encerre essa instância antes de iniciar o teste.

**Terminal 1 — API e banco SQLite isolado:**

```bash
mkdir -p .local
ULTRON_SIMULATION=true DATABASE_URL=sqlite:///./.local/simulacao.db \
ADMIN_EMAIL= ADMIN_PASSWORD= INGEST_API_KEY= DEVICE_API_KEY= \
EVENT_OFFLINE_TIMEOUT_SECONDS=10 \
.venv/bin/python -m uvicorn main:app --app-dir backend --host 127.0.0.1 --port 8000
```

`ULTRON_SIMULATION=true` impede a leitura de `backend/.env` e `backend/config.json`. O arquivo `.local/simulacao.db` é criado automaticamente, preserva os dados entre execuções e não usa o MySQL da instalação. Conta administrativa e chaves de ingestão ficam vazias apenas nesse processo.

**Terminal 2 — dashboard:**

```bash
npm --prefix frontend run dev -- --host 127.0.0.1 --port 5173 --strictPort
```

Confirme `VITE_API_BASE_URL=/api` e `VITE_USE_MOCKS=false` em `frontend/.env`. O Vite encaminha as chamadas à API local na porta 8000.

**Terminal 3 — conferir serviços e cadastrar a máquina:**

```bash
API=http://127.0.0.1:8000/api
curl --fail-with-body -sS "$API/health" | jq
curl --fail-with-body -sS "$API/cncs" | jq

# Somente se precisar de uma máquina nova:
curl --fail-with-body -sS -X POST "$API/cncs" \
  -H 'Content-Type: application/json' \
  -d '{"name":"CNC simulada","description":"Teste local sem hardware"}' | jq
```

A saúde esperada é `{"status":"ok","database":"ok"}`. Anote o `id` (UUID) e o `code` retornados. Os comandos abaixo usam `CNC-001`: substitua pelo código real. Reutilize uma CNC existente quando possível; códigos excluídos não são reutilizados.

Abra **http://127.0.0.1:5173/dashboard** e execute um produtor da [lista de comandos](#b-lista-de-comandos-úteis) no terceiro terminal. API, frontend e produtor devem permanecer em execução. As interpretações aparecem no painel **Interações entre sinais**, nos detalhes `/maquinas/CNC-001`, no histórico `/historico` e no modo `/tv`. A documentação da API fica em **http://127.0.0.1:8000/docs**.

#### Windows / PowerShell

Depois de instalar as dependências e configurar o frontend, inicie API e dashboard com o launcher:

```powershell
.\iniciarLocal.ps1 -Simular
$api = 'http://127.0.0.1:8000/api'
Invoke-RestMethod "$api/health"
Invoke-RestMethod "$api/cncs"

# Somente se precisar de uma máquina nova:
$body = @{ name = 'CNC simulada'; description = 'Teste local sem hardware' } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "$api/cncs" -ContentType 'application/json' -Body $body
```

O launcher inicia API e frontend em segundo plano, usa `.local/simulacao.db` e timeout de 10 s. Ele **não inicia o produtor de eventos**: use os comandos da próxima seção com o código cadastrado. Logs ficam em `.local`.

Abra **http://127.0.0.1:5173/dashboard**. Para encerrar, use `Ctrl+C` no produtor e depois:

```powershell
.\iniciarLocal.ps1 -Acao parar
```

### b) Lista de comandos úteis

Mantenha API e frontend abertos. Execute somente **um produtor por CNC** e interrompa-o com `Ctrl+C` antes de escolher outra combinação. Cada evento substitui o snapshot completo da máquina; não há mescla com a leitura anterior.

No Bash, defina esta função no terminal de injeção:

```bash
set -o pipefail
MACHINE_CODE=CNC-001
API=http://127.0.0.1:8000/api

enviar_sinais() {
  .venv/bin/python tools/simuladorCnc.py --machine-id "$MACHINE_CODE" --count -1 --interval 1 "$@" \
    | .venv/bin/python tools/publicarEventos.py --api "$API" --key=
}
```

No PowerShell, use a função equivalente:

```powershell
$codigoMaquina = 'CNC-001'
$api = 'http://127.0.0.1:8000/api'

function Enviar-Sinais {
  & .\.venv\Scripts\python.exe tools/simuladorCnc.py --machine-id $codigoMaquina --count -1 --interval 1 @args |
    & .\.venv\Scripts\python.exe tools/publicarEventos.py --api $api --key=
}
```

Escolha um exemplo da tabela. No PowerShell, substitua `enviar_sinais` por `Enviar-Sinais`, mantendo os argumentos:

| Objetivo | Comando Bash | Resultado esperado |
|---|---|---|
| Atividade com motor ligado | `enviar_sinais --state ativo --also motor_ligado` | `EMERGENCIA`; identifica `ativo` e `motor_ligado`. |
| Máquina inativa | `enviar_sinais --state inativo` | `EMERGENCIA`; identifica `inativo`. |
| Alarme durante atividade | `enviar_sinais --state ativo --also alarme` | `EMERGENCIA`; identifica `ativo` e `alarme`. |
| Emergência | `enviar_sinais --state emergencia` | `EMERGENCIA`; “Emergência acionada”. |
| Operação falha | `enviar_sinais --state porta_aberta --also emergencia` | `EMERGENCIA`; diagnóstico “Operação falha”. |
| Atividade conflitante | `enviar_sinais --state ativo --also inativo` | `EMERGENCIA`; diagnóstico “Sinais de atividade conflitantes”. |
| Atividade com porta aberta | `enviar_sinais --state ativo --also porta_aberta` | `EMERGENCIA`; identifica `ativo` e `porta_aberta`. |
| Corrente simulada | `enviar_sinais --state ativo --current 12.5` | `12.5 A`, identificada como simulada. |
| Corrente zero | `enviar_sinais --state inativo --current 0` | `0 A` é um valor válido, diferente de não informado. |
| Voltar a não informar corrente | `enviar_sinais --state ativo` | A próxima leitura omite corrente; o valor anterior não é reutilizado. |
| Alternar os seis sinais | `enviar_sinais --state cycle --interval 5` | Um sinal acionado por vez; todas as leituras ficam no histórico. |
| Publicar uma única leitura | `enviar_sinais --state ativo --count 1` | Envia um evento e encerra. Após 10 s sem novo evento, ocorre timeout. |

O simulador só gera JSON Lines; o publicador envia cada linha à API. `--also` é repetível. `--count -1` mantém a emissão até `Ctrl+C`; `--count 6` limita a seis eventos. `--key=` é próprio deste teste sem chave e evita herdar credenciais de ingestão do ambiente.

Para testar uma frota no Windows, com a API já iniciada, use:

```powershell
# Cadastra ou reutiliza CNC teste 01 até CNC teste 06:
.\tools\testarSeisMaquinas.ps1 -Rodadas 0
# Acrescenta 30 leituras por máquina, 180 no total, em aproximadamente um minuto:
.\tools\testarSeisMaquinas.ps1 -Rodadas 30 -IntervaloSegundos 2
```

O comando reutiliza os cadastros de teste pelo nome, usa seus UUIDs reais e acrescenta histórico sem apagar registros. Os seis cenários se alternam entre as máquinas: execução com motor, parada, emergência, alarme, execução com porta aberta e emergência com porta aberta. Cada evento contém os seis booleanos e metadados de simulação; a corrente permanece ausente. O horário é atribuído pela API no recebimento. O resumo final mostra o total persistido de cada máquina, incluindo execuções anteriores. No histórico da dashboard, clique em **Atualizar histórico** para incluir leituras geradas depois que a página foi aberta.

`-Api` permite alterar o endereço da API. Se a ingestão exigir chave, informe `-Chave` ou configure `INGEST_API_KEY`/`DEVICE_API_KEY` no ambiente do terminal. Cadastro e histórico mantêm o fluxo de autenticação existente.

Para enviar um snapshot com todos os seis sinais explicitamente desacionados, pare o produtor e use:

```bash
curl --fail-with-body -sS -X POST "$API/events" \
  -H 'Content-Type: application/json' \
  -d '{"machine_id":"CNC-001","states":{"ativo":false,"inativo":false,"emergencia":false,"motor_ligado":false,"alarme":false,"porta_aberta":false}}' | jq
```

No PowerShell:

```powershell
$body = @{
  machine_id = $codigoMaquina
  states = @{ ativo = $false; inativo = $false; emergencia = $false; motor_ligado = $false; alarme = $false; porta_aberta = $false }
} | ConvertTo-Json -Depth 4
Invoke-RestMethod -Method Post -Uri "$api/events" -ContentType 'application/json' -Body $body
```

O resultado é `PARADA`, com a interpretação “Nenhum sinal acionado”. Isso não fabrica `inativo=true`. Atualize o `machine_id` do exemplo Bash se seu código for diferente.

Para consultar estados, interpretações e histórico pelo terminal:

```bash
curl --fail-with-body -sS "$API/cncs/statuses" \
  | jq '.[] | {code, status, states, signal_outputs, analog_signals}'
curl --fail-with-body -sS "$API/cncs/history?page=1&limit=10" | jq
```

```powershell
Invoke-RestMethod "$api/cncs/statuses" | ConvertTo-Json -Depth 10
Invoke-RestMethod "$api/cncs/history?page=1&limit=10" | ConvertTo-Json -Depth 10
```

Para testar a perda de comunicação, interrompa somente o produtor e aguarde 10 s mais a próxima consulta da dashboard. O estado passa a `SEM_COMUNICACAO`, e as interpretações ficam marcadas como antigas. Reinicie o produtor para recuperar a comunicação. Para testar indisponibilidade da API, mantenha a página aberta, encerre a API e depois inicie-a novamente com o mesmo comando de simulação.

### Histórico reconstruído de quatro horas

O banco MySQL fica fora do repositório Git. Para transportar o histórico reconstruído de **Siemens S7-300** e **Siemens S7-1200**, o projeto inclui `data/demo/historicoQuatroHoras.json`: uma janela de 04/11/2026, das 18:08:31 às 22:08:31 de Brasília, com 1.021 registros. Esse arquivo contém somente o plano desse histórico, sem usuários ou credenciais, e pode acompanhar o código no Git.

Com o MySQL e a API já em execução, importe em outro computador pela raiz do projeto:

```powershell
& .\.venv\Scripts\python.exe tools/reconstruirHistorico.py --plano .\data\demo\historicoQuatroHoras.json --aplicar
```

A ferramenta cria os dois cadastros que estiverem faltando, reutiliza nomes existentes e preserva os demais registros. Reexecutar o mesmo plano não duplica seus eventos. A origem do lote permanece `reconstructed`. O arquivo cobre apenas esse conjunto de quatro horas; um backup completo do MySQL requer uma exportação separada.

## 2) Setup para teste integrado com o CLP

Use este caminho para testar IHM/CLP → Opta → USB → ponte Python → API → MySQL → dashboard. Faça a [preparação comum](#setup), instale MySQL 8 e deixe `arduino-cli` no PATH.

### Preparar os sinais do CLP

O firmware espera a ligação sequencial Q0.0→I1=ativo (Em execução), Q0.1→I2=inativo (Parada), Q0.2→I3=emergência, Q0.3→I4=motor ligado, Q0.4→I5=porta aberta e Q0.5→I6=alarme (Alerta erro). I7 fica livre; I8/A7 permanece reservada para corrente, sem leitura física. Confira a ligação e a polaridade contra o [mapeamento do firmware](#mapeamento-físico-atual-do-opta) antes do ensaio. O `Main.pdf` descreve o ladder anterior e não confirma o vínculo atual.

Cadastre a CNC antes de iniciar a ponte. Mantenha somente um produtor de snapshots por máquina: pare o simulador ao testar os sinais do CLP. Encerre a API SQLite de teste antes de iniciar a API MySQL na mesma porta. No PowerShell, pare o launcher com `-Acao parar` antes de reiniciá-lo sem `-Simular`.

### Setup e inicialização no Linux

#### 1. Configurar MySQL e backend

No Ubuntu/Mint/Debian:

```bash
sudo apt install mysql-server mysql-client
sudo systemctl enable --now mysql
```

Entre no MySQL como administrador (`sudo mysql`) e crie o usuário da aplicação:

```sql
CREATE USER 'scomptec'@'127.0.0.1' IDENTIFIED BY 'SENHA_PRIVADA';
GRANT ALL PRIVILEGES ON cnc_monitor.* TO 'scomptec'@'127.0.0.1';
```

Copie o modelo somente se o arquivo local ainda não existir:

```bash
cp -n backend/config.example.json backend/config.json
```

Em `backend/config.json`, ajuste `DATABASE_URL` e troque `AUTH_SECRET`:

```text
mysql+pymysql://scomptec:SENHA_PRIVADA@127.0.0.1:3306/cnc_monitor?charset=utf8mb4
```

Codifique caracteres especiais da senha na URL (`@` → `%40`, por exemplo). A API cria o banco e as tabelas na primeira inicialização. Use as credenciais da sua instalação e mantenha-as nos arquivos locais do backend.

A configuração do backend segue esta prioridade: **ambiente → `backend/.env` → `backend/config.json`**. Reinicie API e frontend após mudar suas configurações. O [configuracao.json](configuracao.json) da raiz é apenas um inventário de parâmetros.

Se `backend/.env` já definir `DATABASE_URL` ou `AUTH_SECRET`, ajuste os valores nesse arquivo, pois eles prevalecem sobre o JSON.

#### 2. Iniciar a API e cadastrar a máquina

```bash
.venv/bin/python -m uvicorn main:app --app-dir backend --host 127.0.0.1 --port 8000
```

Confirme em `http://127.0.0.1:8000/api/health`: o retorno esperado é `{"status":"ok","database":"ok"}`. A documentação interativa fica em `http://127.0.0.1:8000/docs`.

Em outro terminal, consulte os cadastros existentes antes de criar um novo:

```bash
API=http://127.0.0.1:8000/api
curl --fail-with-body -sS "$API/cncs" | jq

# Para cadastrar uma máquina nova:
curl --fail-with-body -sS -X POST "$API/cncs" \
  -H 'Content-Type: application/json' \
  -d '{"name":"Máquina 01","description":"Monitoramento IHM/CLP"}' | jq
```

Guarde o `id` (UUID) e o `code` retornados, ou reutilize os de uma máquina já cadastrada. Os exemplos seguintes usam **`CNC-001`**: substitua-o pelo código real. Códigos excluídos não são reutilizados. O fluxo USB dispensa cadastro de dispositivo ou MAC.

#### 3. Gravar o Opta

Com `arduino-cli` no PATH, conecte a placa e feche a ponte ou qualquer monitor que esteja usando a serial:

```bash
arduino-cli core update-index
arduino-cli core install arduino:mbed_opta@4.6.0
arduino-cli lib install ArduinoJson@7.4.2
arduino-cli board list
.venv/bin/python tools/configurarTransmissao.py --transporte usb --porta /dev/ttyACM0
```

Use a porta listada para sua placa. O script compila e depois grava; para compilar sem upload, substitua `--porta /dev/ttyACM0` por `--somente-compilar`. Se o CLI estiver instalado localmente, informe `--cli .tools/arduino-cli-linux/arduino-cli`. A porta pode mudar após a gravação.

#### 4. Iniciar a ponte USB

```bash
.venv/bin/python tools/ponteUsb.py --listar-portas
.venv/bin/python tools/ponteUsb.py --porta /dev/ttyACM0 --machine-id CNC-001 --api http://127.0.0.1:8000/api
```

Use a porta e o código identificados nos passos anteriores. Sem `--machine-id`, a ponte usa o ID enviado pelo firmware: o padrão `"1"` resolve para `CNC-001`. A mensagem `HTTP confirmado` indica que a API aceitou o evento. No Linux, permissão negada na serial pode exigir inclusão no grupo `dialout` e novo login.

Se configurar `INGEST_API_KEY` no backend, forneça a mesma chave no ambiente da ponte. Ela lê `backend/.env`, mas não `backend/config.json`.

#### 5. Abrir a dashboard

Em outro terminal:

```bash
npm --prefix frontend run dev -- --host 127.0.0.1 --port 5173 --strictPort
```

Acesse **http://127.0.0.1:5173/dashboard**. Detalhes da máquina: `/maquinas/CNC-001`; modo TV: `/tv`. Ative os sinais na IHM/CLP e compare os estados e as mensagens no painel **Interações entre sinais**. Teste um sinal por vez e depois as combinações documentadas, comparando também os seis valores nos detalhes da CNC. Mantenha API, ponte e frontend em execução; encerre com `Ctrl+C`.

### Setup e inicialização no Windows (PowerShell)

Após a preparação comum, instale e inicie MySQL 8 e instale Arduino CLI. Abra `mysql -u root -p` e execute o SQL do [passo 1](#1-configurar-mysql-e-backend). Prepare `backend/config.json` e ajuste `DATABASE_URL` e `AUTH_SECRET` conforme esse mesmo passo:

```powershell
if (-not (Test-Path backend/config.json)) { Copy-Item backend/config.example.json backend/config.json }
```

Inicie API e dashboard, confira a saúde e liste as máquinas:

```powershell
.\iniciarLocal.ps1
$api = 'http://127.0.0.1:8000/api'
Invoke-RestMethod "$api/health"
Invoke-RestMethod "$api/cncs"
```

Se precisar de uma máquina nova, cadastre-a e anote `id` e `code`:

```powershell
$body = @{ name = 'Maquina 01'; description = 'Monitoramento IHM/CLP' } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "$api/cncs" -ContentType 'application/json' -Body $body
```

Conecte o Opta e, com a serial livre, compile e grave usando a porta indicada por `board list` (`COM4` é um exemplo):

```powershell
arduino-cli core update-index
arduino-cli core install arduino:mbed_opta@4.6.0
arduino-cli lib install ArduinoJson@7.4.2
arduino-cli board list
& .\.venv\Scripts\python.exe tools/configurarTransmissao.py --transporte usb --porta COM4
& .\.venv\Scripts\python.exe tools/ponteUsb.py --listar-portas
& .\.venv\Scripts\python.exe tools/ponteUsb.py --porta COM4 --machine-id CNC-001 --api http://127.0.0.1:8000/api
```

Substitua `CNC-001` pelo código cadastrado e confirme a porta após a gravação. Abra **http://127.0.0.1:5173/dashboard**. A ponte permanece nesse terminal; o launcher executa API e frontend em segundo plano, com logs em `.local`.

Para encerrar, use `Ctrl+C` na ponte e depois:

```powershell
.\iniciarLocal.ps1 -Acao parar
```

## Acesso e distribuição da dashboard

As opções abaixo atendem aos dois métodos de setup.

### Acesso pela rede

Para acessar por computador ou celular na mesma rede, mantenha `VITE_API_BASE_URL=/api` e inicie o Vite com `--host 0.0.0.0`. Abra `http://IP_DO_COMPUTADOR:5173/dashboard` no outro aparelho. O proxy de desenvolvimento encaminha `/api` para a API local na porta 8000; a API pode continuar escutando em `127.0.0.1`. Se houver um endereço absoluto antigo em `frontend/.env`, substitua-o por `/api` e reinicie o Vite.

```bash
npm --prefix frontend run dev -- --host 0.0.0.0 --port 5173 --strictPort
```

Encerre o frontend anterior antes de usar a mesma porta. No Windows, o launcher inicia a dashboard apenas em loopback e define uma URL absoluta para a API. Para acessar pelo celular, pare o launcher, inicie somente a API com `.\iniciarLocal.ps1 -Acao backend` (acrescente `-Simular` para SQLite) e execute o comando npm acima separadamente, com `frontend/.env` configurado para `/api`. Permita o acesso à porta 5173 no firewall da rede local.

### Hospedagem web

Na hospedagem web, execute `npm --prefix frontend run build`, sirva `frontend/dist` e configure o servidor HTTP para encaminhar `/api/` ao FastAPI e devolver `index.html` nas rotas da aplicação (como `/maquinas/CNC-001`). Use HTTPS, compressão e cache dos assets com hash; o HTML deve ser revalidado para receber versões novas. `vite preview` é usado para conferência local, não para hospedagem de produção. Se a API estiver em outro domínio, configure sua URL absoluta em `VITE_API_BASE_URL` e a origem web em `CORS_ORIGINS`.

### Aplicativo desktop (Electron)

Para Electron, `npm --prefix frontend run build:electron` gera caminhos relativos e `npm --prefix frontend run electron:build` também prepara o instalador. O endereço padrão da API desktop é `http://127.0.0.1:8000/api`; informe uma URL absoluta alcançável para usar um servidor remoto. Reinicie a API junto com a atualização do frontend: o monitoramento utiliza as consultas coletivas e as interpretações `signal_outputs` descritas abaixo.

## Eventos e consultas

A API aceita eventos de qualquer produtor, inclusive `curl` ou simulador:

```json
{"machine_id":"CNC-001","states":{"ativo":true,"inativo":false,"emergencia":false,"motor_ligado":true,"alarme":false,"porta_aberta":false}}
```

Cada envio representa um snapshot completo: estados ausentes ficam não informados. `event_id` e `timestamp` são opcionais. Reenvios com a mesma chave e conteúdo não duplicam registros nem renovam presença; conteúdo diferente retorna 409. Leituras antigas não revertem o estado atual.

Por padrão, sem eventos novos por 90 s, o estado passa a `SEM_COMUNICACAO`; o setup de simulação reduz esse tempo para 10 s. Uma observação antiga recebida recentemente pode aparecer como `DADOS_DESATUALIZADOS`. Ajuste o timeout com `EVENT_OFFLINE_TIMEOUT_SECONDS` (mínimo 10 s).

| Método | Rota | Uso |
|---|---|---|
| POST / GET | `/api/cncs` | Cadastrar / listar máquinas |
| GET | `/api/cncs/statuses` | Estados e `signal_outputs` da frota em uma requisição |
| GET | `/api/cncs/history?page=1&limit=30` | Histórico global paginado; aceita `machine_id`, `start` e `end` |
| GET / PUT / DELETE | `/api/cncs/{uuid}` | Consultar / editar / excluir |
| GET | `/api/cncs/{uuid}/status` | Estados, interpretações e última comunicação |
| GET | `/api/cncs/{uuid}/history?page=1&limit=50` | Histórico paginado |
| GET | `/api/cncs/{uuid}/utilization` | Utilização nas últimas 24 h |
| POST | `/api/events` | Enviar estados |

Excluir uma máquina remove seu histórico. Trocar ou remover um coletor preserva os eventos da máquina. Os endpoints `/api/devices/...` continuam disponíveis para integrações anteriores.

## Autenticação e administração

Configure `ADMIN_EMAIL` e `ADMIN_PASSWORD` juntos no backend (senha de 8–128 caracteres), com `ADMIN_NAME` opcional, e reinicie a API. A conta será criada ou atualizada. Entre pelo login normal e acesse `/admin` para gerenciar usuários, ocorrências, limites e histórico administrativo.

Na simulação iniciada manualmente, os arquivos de configuração do backend são ignorados: para criar uma conta de teste, defina essas variáveis no comando de inicialização da API no lugar dos valores vazios do exemplo. O launcher com `-Simular` mantém a conta administrativa vazia.

Cadastro público não concede perfil administrativo. Os limites salvos são usados no resumo administrativo de desvios; outros painéis mantêm seus próprios critérios. Veja o [guia de administração](docs/guides/administracao.md).

## Testes

```bash
ULTRON_SIMULATION=true DATABASE_URL=sqlite:// ADMIN_EMAIL= ADMIN_PASSWORD= \
INGEST_API_KEY= DEVICE_API_KEY= EVENT_OFFLINE_TIMEOUT_SECONDS= DEVICE_OFFLINE_TIMEOUT_SECONDS=90 \
.venv/bin/python -m pytest -q backend/tests tools/tests
npm --prefix frontend test
npm --prefix frontend run lint
npm --prefix frontend run build
```

No Windows, use `tools/testarProjeto.ps1`; `-Firmware` inclui os testes C++ e a compilação para a placa. `-FirmwareHostOnly` executa os testes C++ sem exigir o core da placa ou gravar o Opta. Ambos aceitam `-ZigPath` e `-ArduinoJsonInclude` para ferramentas já instaladas; a segunda opção aponta para a pasta `src` do ArduinoJson 7.4.2. O compilador de host esperado é Zig 0.13.0. `-CliPath` permite indicar o Arduino CLI para a compilação de placa.

```powershell
.\tools\testarProjeto.ps1
# Com as ferramentas de host instaladas:
.\tools\testarProjeto.ps1 -FirmwareHostOnly -ZigPath 'C:\ferramentas\zig\zig.exe' -ArduinoJsonInclude 'C:\ferramentas\ArduinoJson\src'
```

Os testes Python usam SQLite isolado. Concorrência MySQL exige `ULTRON_TEST_MYSQL_URL` apontando para um banco local separado com nome iniciado em `ultron_test`. Testes de software não validam a ligação elétrica ou o hardware físico.

O [teste de navegador e responsividade](docs/guides/testesResponsividade.md) verifica o build de produção com dados simulados, navegação, paginação, menus, cabeçalho, falha/recuperação da API e tamanhos de celular a desktop.

## Estrutura e referências

```text
backend/    API, persistência e testes
frontend/   Dashboard React e Electron
firmware/   Aquisição no Opta e testes C++
tools/      Ponte USB, simulador e scripts
docs/       Guias, contexto técnico e relatórios
legacy/     Referências de versões anteriores
```

- [Contrato de eventos e guia da equipe](docs/guides/guiaEquipe.md)
- [Integração com IHM/CLP e Opta](docs/guides/integracaoOpta.md)
- [Teste de responsividade](docs/guides/testesResponsividade.md)
- [Relatório de sinais operacionais e corrente](docs/reports/sinaisOperacionaisCorrente.md)
