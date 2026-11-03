# SCOMPTEC

Monitoramento de máquinas CNC com Arduino Opta, API FastAPI, MySQL e dashboard React. Exibe estados, alertas e histórico a partir dos sinais disponibilizados pela IHM/CLP.

## Sumário

- [Funcionamento](#funcionamento)
- [Setup](#setup)
  - [Dependências no Linux](#dependências-no-linux)
  - [Dependências no Windows](#dependências-no-windows)
  - [Configuração do frontend](#configuração-do-frontend)
- [Método 1: setup com o Opta](#método-1-setup-com-o-opta)
  - [1. Configurar MySQL e backend](#1-configurar-mysql-e-backend)
  - [2. Iniciar a API e cadastrar a máquina](#2-iniciar-a-api-e-cadastrar-a-máquina)
  - [3. Gravar o Opta](#3-gravar-o-opta)
  - [4. Iniciar a ponte USB](#4-iniciar-a-ponte-usb)
  - [5. Abrir a dashboard](#5-abrir-a-dashboard)
  - [Opta no Windows (PowerShell)](#opta-no-windows-powershell)
- [Método 2: setup com simulação local](#método-2-setup-com-simulação-local)
  - [1. Iniciar a API com SQLite](#1-iniciar-a-api-com-sqlite)
  - [2. Cadastrar a máquina simulada](#2-cadastrar-a-máquina-simulada)
  - [3. Publicar eventos simulados](#3-publicar-eventos-simulados)
  - [4. Abrir a dashboard e conferir os estados](#4-abrir-a-dashboard-e-conferir-os-estados)
  - [Simulação no Windows (PowerShell)](#simulação-no-windows-powershell)
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

1. A IHM/CLP disponibiliza oito sinais digitais.
2. O Opta lê as entradas e envia estados pela serial USB a 115200 baud, nas mudanças e com heartbeat de 1 s.
3. `tools/ponteUsb.py` converte as leituras em eventos e envia para `POST /api/events`.
4. A API valida e grava os eventos por máquina no MySQL.
5. A dashboard consulta a API; cada nova rodada começa 5 s após a anterior terminar.

| IHM/CLP | Opta | Pino | Estado |
|---|---|---|---|
| D000 | I1 | A0 | `em_execucao` |
| D001 | I2 | A1 | `pausa` |
| D002 | I3 | A2 | `parada` |
| D003 | I4 | A3 | `emergencia` |
| D004 | I5 | A4 | `motor_ligado` |
| D005 | I6 | A5 | `automatico` |
| D006 | I7 | A6 | `manual` |
| D007 | I8 | A7 | `alarme` |

O firmware apenas monitora entradas. Polaridade e filtros ficam em [config.h](firmware/optaCncMonitor/config.h). As filas são limitadas e ficam em RAM; interrupções podem perder transições. O perfil atual observa booleanos e não implementa protocolos proprietários Mitsubishi ou controle de atuadores.

## Setup

Escolha o método de acordo com o que deseja executar:

| Método | Origem dos dados | Banco | Requisitos adicionais |
|---|---|---|---|
| [Com o Opta](#método-1-setup-com-o-opta) | IHM/CLP → Opta → USB → ponte Python | MySQL 8 | Opta, cabo USB de dados e Arduino CLI |
| [Simulação local](#método-2-setup-com-simulação-local) | Simulador Python → publicador HTTP | SQLite em arquivo local | Nenhum hardware ou servidor MySQL |

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

## Método 1: setup com o Opta

Use este caminho para coletar os sinais da IHM/CLP pelo Opta conectado via USB ao computador que executa a ponte Python. Além da preparação comum, instale MySQL 8 e deixe `arduino-cli` disponível no PATH. Para Windows, siga [Opta no Windows](#opta-no-windows-powershell).

### 1. Configurar MySQL e backend

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

### 2. Iniciar a API e cadastrar a máquina

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

### 3. Gravar o Opta

Com `arduino-cli` no PATH, conecte a placa e feche a ponte ou qualquer monitor que esteja usando a serial:

```bash
arduino-cli core update-index
arduino-cli core install arduino:mbed_opta@4.6.0
arduino-cli lib install ArduinoJson@7.4.2
arduino-cli board list
.venv/bin/python tools/configurarTransmissao.py --transporte usb --porta /dev/ttyACM0
```

Use a porta listada para sua placa. O script compila e depois grava; para compilar sem upload, substitua `--porta /dev/ttyACM0` por `--somente-compilar`. Se o CLI estiver instalado localmente, informe `--cli .tools/arduino-cli-linux/arduino-cli`. A porta pode mudar após a gravação.

### 4. Iniciar a ponte USB

```bash
.venv/bin/python tools/ponteUsb.py --listar-portas
.venv/bin/python tools/ponteUsb.py --porta /dev/ttyACM0 --machine-id CNC-001 --api http://127.0.0.1:8000/api
```

Use a porta e o código identificados nos passos anteriores. Sem `--machine-id`, a ponte usa o ID enviado pelo firmware: o padrão `"1"` resolve para `CNC-001`. A mensagem `HTTP confirmado` indica que a API aceitou o evento. No Linux, permissão negada na serial pode exigir inclusão no grupo `dialout` e novo login.

Se configurar `INGEST_API_KEY` no backend, forneça a mesma chave no ambiente da ponte. Ela lê `backend/.env`, mas não `backend/config.json`.

### 5. Abrir a dashboard

Em outro terminal:

```bash
npm --prefix frontend run dev -- --host 127.0.0.1 --port 5173 --strictPort
```

Acesse **http://127.0.0.1:5173/dashboard**. Detalhes da máquina: `/maquinas/CNC-001`; modo TV: `/tv`. Ative os sinais na IHM/CLP e compare os estados na dashboard. Mantenha API, ponte e frontend em execução; encerre com `Ctrl+C`.

### Opta no Windows (PowerShell)

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

<a id="testar-sem-hardware"></a>

## Método 2: setup com simulação local

Este caminho executa API, banco SQLite e dashboard no computador. O simulador gera os mesmos envelopes `machine_id`/`states` aceitos do Opta, e o publicador os envia para `POST /api/events`.

Após a [preparação comum](#setup), siga os passos abaixo. Não é necessário configurar MySQL, gravar firmware ou iniciar a ponte USB. Para Windows, siga [Simulação no Windows](#simulação-no-windows-powershell).

### 1. Iniciar a API com SQLite

Encerre uma API que já esteja usando a porta 8000. Em um terminal dedicado:

```bash
mkdir -p .local
ULTRON_SIMULATION=true DATABASE_URL=sqlite:///./.local/simulacao.db \
ADMIN_EMAIL= ADMIN_PASSWORD= INGEST_API_KEY= DEVICE_API_KEY= \
EVENT_OFFLINE_TIMEOUT_SECONDS=10 \
.venv/bin/python -m uvicorn main:app --app-dir backend --host 127.0.0.1 --port 8000
```

`ULTRON_SIMULATION=true` impede a leitura de `backend/.env` e `backend/config.json`; as variáveis acima selecionam o banco de simulação e deixam conta administrativa e chaves de ingestão vazias nesse processo. O arquivo `.local/simulacao.db` é criado automaticamente e preserva os dados entre execuções. Ele é separado do MySQL da instalação.

Em outro terminal, confirme a API e o banco:

```bash
curl --fail-with-body -sS http://127.0.0.1:8000/api/health | jq
```

O retorno esperado é `{"status":"ok","database":"ok"}`. A documentação interativa fica em **http://127.0.0.1:8000/docs**.

### 2. Cadastrar a máquina simulada

A ingestão exige uma máquina existente. Liste os registros e crie um somente se necessário:

```bash
API=http://127.0.0.1:8000/api
curl --fail-with-body -sS "$API/cncs" | jq

# Execute apenas para cadastrar uma nova máquina simulada:
curl --fail-with-body -sS -X POST "$API/cncs" \
  -H 'Content-Type: application/json' \
  -d '{"name":"CNC simulada","description":"Simulacao local sem hardware"}' | jq
```

Anote o `id` e o `code` retornados. Nos próximos comandos, substitua `CNC-001` pelo código real; mesmo no SQLite, os códigos excluídos não são reutilizados.

### 3. Publicar eventos simulados

Em outro terminal, inicie a geração contínua de eventos:

```bash
set -o pipefail
.venv/bin/python tools/simuladorCnc.py --machine-id CNC-001 --state cycle --count -1 --interval 5 \
  | .venv/bin/python tools/publicarEventos.py --api http://127.0.0.1:8000/api --key=
```

O simulador escreve JSON Lines em stdout; o publicador lê esse fluxo e envia cada evento à API. `--state cycle` alterna os oito sinais, ativando um por vez a cada 5 s. `--count -1` mantém a geração até `Ctrl+C`. O publicador imprime a resposta de cada envio; `--key=` evita herdar uma chave de ingestão do ambiente nesta simulação sem chave.

Para manter um sinal ativo, troque `--state cycle` por `--state em_execucao`, `--state alarme` ou `--state emergencia`. Para uma sequência finita, use `--count 8`. Cada envio é um snapshot completo dos oito sinais.

### 4. Abrir a dashboard e conferir os estados

Em outro terminal:

```bash
npm --prefix frontend run dev -- --host 127.0.0.1 --port 5173 --strictPort
```

Abra **http://127.0.0.1:5173/dashboard** e confira `/maquinas/CNC-001`, `/historico` e `/tv`, ajustando o código na URL. A interface consulta os estados a cada rodada de aproximadamente 5 s; os eventos ficam no histórico da API.

Com a API e o frontend ainda abertos, pare o simulador com `Ctrl+C`: após 10 s sem eventos, a API informa `SEM_COMUNICACAO`, exibido na próxima consulta da dashboard. Reinicie o pipeline para recuperar a comunicação. Encerre API e frontend com `Ctrl+C` nos respectivos terminais.

### Simulação no Windows (PowerShell)

Após a preparação comum, inicie os serviços com:

```powershell
.\iniciarLocal.ps1 -Simular
$api = 'http://127.0.0.1:8000/api'
Invoke-RestMethod "$api/health"
Invoke-RestMethod "$api/cncs"
```

O launcher inicia API e frontend em segundo plano, usa `.local/simulacao.db`, ignora a configuração local do backend e define timeout de 10 s. Ele não inicia o produtor de eventos.

Se a máquina ainda não existir, cadastre-a e anote `id` e `code`:

```powershell
$body = @{ name = 'CNC simulada'; description = 'Simulacao local sem hardware' } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "$api/cncs" -ContentType 'application/json' -Body $body
```

Com o código retornado no lugar de `CNC-001`, execute o pipeline no PowerShell:

```powershell
& .\.venv\Scripts\python.exe tools/simuladorCnc.py --machine-id CNC-001 --state cycle --count -1 --interval 5 |
  & .\.venv\Scripts\python.exe tools/publicarEventos.py --api http://127.0.0.1:8000/api --key=
```

Abra **http://127.0.0.1:5173/dashboard**. Para testar a perda de comunicação, use `Ctrl+C` no pipeline e mantenha os serviços abertos. Para encerrar API e frontend:

```powershell
.\iniciarLocal.ps1 -Acao parar
```

Antes de trocar entre simulação e MySQL pelo launcher, execute `-Acao parar` e inicie novamente com ou sem `-Simular`. Os logs dos serviços ficam em `.local`.

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

Para Electron, `npm --prefix frontend run build:electron` gera caminhos relativos e `npm --prefix frontend run electron:build` também prepara o instalador. O endereço padrão da API desktop é `http://127.0.0.1:8000/api`; informe uma URL absoluta alcançável para usar um servidor remoto. Reinicie a API junto com a atualização do frontend: o monitoramento utiliza as novas consultas coletivas abaixo.

## Eventos e consultas

A API aceita eventos de qualquer produtor, inclusive `curl` ou simulador:

```json
{"machine_id":"CNC-001","states":{"em_execucao":true,"alarme":false}}
```

Cada envio representa um snapshot completo: estados ausentes ficam não informados. `event_id` e `timestamp` são opcionais. Reenvios com a mesma chave e conteúdo não duplicam registros nem renovam presença; conteúdo diferente retorna 409. Leituras antigas não revertem o estado atual.

Por padrão, sem eventos novos por 90 s, o estado passa a `SEM_COMUNICACAO`; o setup de simulação reduz esse tempo para 10 s. Uma observação antiga recebida recentemente pode aparecer como `DADOS_DESATUALIZADOS`. Ajuste o timeout com `EVENT_OFFLINE_TIMEOUT_SECONDS` (mínimo 10 s).

| Método | Rota | Uso |
|---|---|---|
| POST / GET | `/api/cncs` | Cadastrar / listar máquinas |
| GET | `/api/cncs/statuses` | Estados da frota em uma requisição, sem carregar histórico |
| GET | `/api/cncs/history?page=1&limit=30` | Histórico global paginado; aceita `machine_id`, `start` e `end` |
| GET / PUT / DELETE | `/api/cncs/{uuid}` | Consultar / editar / excluir |
| GET | `/api/cncs/{uuid}/status` | Estados e última comunicação |
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

No Windows, use `tools/testarProjeto.ps1`; `-Firmware` inclui verificações do firmware. Os testes Python usam SQLite isolado. Concorrência MySQL exige `ULTRON_TEST_MYSQL_URL` apontando para um banco local separado com nome iniciado em `ultron_test`. Testes de software não validam a ligação elétrica ou o hardware físico.

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
- [Contexto técnico do projeto](docs/CONTEXTO_PROJETO.md)
