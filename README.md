# SCOMPTEC — guia rápido

Execute os comandos na raiz do projeto. Troque senhas, IPs e portas de exemplo pelos valores do seu ambiente. Use um terminal separado para cada processo que permanece em execução.

## 1. Resumo da arquitetura

```text
Mesa seletora → Arduino Opta WiFi ── HTTP/Wi-Fi ───────────→ API FastAPI → MySQL → React/Vite
                             └────── USB serial → ponte Python ┘
Simulador Python ─────────────────────── HTTP ──────────────→ API FastAPI → SQLite → React/Vite
```

O Opta controla a mesa localmente; a API apenas recebe leituras. HTTP e USB são modos exclusivos, escolhidos ao gravar o firmware. No modo HTTP, Opta e computador devem estar na mesma rede. No modo USB, a ponte roda no computador conectado ao Opta. O frontend consulta a API por HTTP. Ao iniciar, a API cria o banco MySQL configurado se ele não existir e cria suas tabelas ausentes; não migra tabelas existentes.

## 2. Instalação e configuração

Requisitos: Python 3.10+, Node.js 22.12+ e npm. Para USB/HTTP com Opta, instale MySQL 8, Arduino CLI, o core `arduino:mbed_opta` e ArduinoJson. O arquivo [requirements.txt](requirements.txt) reúne as dependências Python.

### Linux (Mint/Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip build-essential mysql-server mysql-client
sudo systemctl enable --now mysql
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
npm --prefix frontend ci
```

Instale Node.js e Arduino CLI se ainda não estiverem no `PATH`. Para gravar o Opta:

```bash
arduino-cli core update-index
arduino-cli core install arduino:mbed_opta@4.6.0
arduino-cli lib install ArduinoJson@7.4.2
arduino-cli board list
```

### Windows (PowerShell)

Instale Python, Node.js/npm, MySQL 8 e Arduino CLI. Deixe `py`, `node`, `npm` e `arduino-cli` acessíveis no terminal.

```powershell
py -3 -m venv .venv
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
npm --prefix frontend ci
arduino-cli core update-index
arduino-cli core install arduino:mbed_opta@4.6.0
arduino-cli lib install ArduinoJson@7.4.2
arduino-cli board list
```

### Banco e URLs para uso com Opta

No MySQL do **computador host**, entre como administrador (`sudo mysql` no Linux; `mysql -u root -p` no Windows) e crie somente o usuário da aplicação, com permissão para criar o banco configurado:

```sql
CREATE USER 'scomptec'@'127.0.0.1' IDENTIFIED BY 'SENHA_PRIVADA';
GRANT ALL PRIVILEGES ON cnc_monitor.* TO 'scomptec'@'127.0.0.1';
```

Copie os modelos e edite as cópias locais:

| Linux | Windows PowerShell |
|---|---|
| `cp backend/config.example.json backend/config.json` | `Copy-Item backend/config.example.json backend/config.json` |
| `cp frontend/.env.example frontend/.env` | `Copy-Item frontend/.env.example frontend/.env` |

Em `backend/config.json`, configure `DATABASE_URL` como `mysql+pymysql://scomptec:SENHA_PRIVADA@127.0.0.1:3306/cnc_monitor?charset=utf8mb4`; a API criará `cnc_monitor` na primeira inicialização. Troque também `AUTH_SECRET` e, se quiser login administrativo inicial, defina `ADMIN_EMAIL` e `ADMIN_PASSWORD` juntos. Codifique caracteres especiais da senha dentro da URL (`@` → `%40`, por exemplo). Em `frontend/.env`, use:

```dotenv
VITE_API_BASE_URL=http://127.0.0.1:8000/api
VITE_USE_MOCKS=false
```

Se `backend/.env` existir, seus valores prevalecem sobre `backend/config.json`. Reinicie a API após alterar a configuração e o Vite após alterar `frontend/.env`. Se a porta 8000 estiver ocupada, use outra porta na API e ajuste a URL do frontend e da ponte; no modo HTTP, ajuste também `BACKEND_PORT` em `firmware/optaMesaMonitor/config.h` e regrave o Opta.

## 3. Colocar o sistema para rodar

Abra o dashboard em `http://127.0.0.1:5173/dashboard`. Nas instalações com MySQL, confirme a API em `http://127.0.0.1:8000/api/health` antes de iniciar o frontend ou a ponte.

### A. Simulação local, sem Opta ou MySQL

O simulador usa SQLite isolado. No Linux:

```bash
mkdir -p .local
ULTRON_SIMULATION=true DATABASE_URL=sqlite:///./.local/simulation.db \
  .venv/bin/python -m uvicorn main:app --app-dir backend --host 127.0.0.1 --port 8000
# Em outro terminal:
npm --prefix frontend run dev -- --host 127.0.0.1
# Em um terceiro terminal:
.venv/bin/python tools/simuladorWifi.py --api http://127.0.0.1:8000/api --apenas-stream --stream-seconds -1
```

No Windows, o inicializador prepara o SQLite e abre API e frontend; inicie o simulador em outro terminal:

```powershell
.\iniciarLocal.ps1 -Simular
& .\.venv\Scripts\python.exe tools/simuladorWifi.py --api http://127.0.0.1:8000/api --apenas-stream --stream-seconds -1
# Depois do teste:
.\iniciarLocal.ps1 -Acao parar
```

Se iniciar os processos Windows em terminais separados, use `$env:ULTRON_SIMULATION='true'` e `$env:DATABASE_URL='sqlite:///./.local/simulation.db'` no terminal da API. A simulação não testa sensores, relés nem conexão física.

### B. Opta por USB serial

Use o MySQL e as URLs da seção 2. Grave o modo USB com o Opta conectado. No Linux:

```bash
arduino-cli board list
python3 tools/configurarTransmissao.py --transporte usb --porta /dev/ttyACM0
.venv/bin/python -m uvicorn main:app --app-dir backend --host 127.0.0.1 --port 8000
# Em outro terminal:
npm --prefix frontend run dev -- --host 127.0.0.1
# Em outro terminal, após conferir a porta:
.venv/bin/python tools/ponteUsb.py --listar-portas
.venv/bin/python tools/ponteUsb.py --porta /dev/ttyACM0 --mac AA:BB:CC:DD:EE:FF --api http://127.0.0.1:8000/api
```

No Windows, troque a porta `COM4` pela listada; mantenha API, frontend e ponte em terminais separados:

```powershell
arduino-cli board list
& .\.venv\Scripts\python.exe tools/configurarTransmissao.py --transporte usb --porta COM4
& .\.venv\Scripts\python.exe -m uvicorn main:app --app-dir backend --host 127.0.0.1 --port 8000
# Em outro terminal:
npm --prefix frontend run dev -- --host 127.0.0.1
# Em outro terminal:
& .\.venv\Scripts\python.exe tools/ponteUsb.py --listar-portas
& .\.venv\Scripts\python.exe tools/ponteUsb.py --porta COM4 --mac AA:BB:CC:DD:EE:FF --api http://127.0.0.1:8000/api
```

Use o **MAC real do Opta** no primeiro cadastro; para manter um cadastro existente, troque `--mac AA:BB:CC:DD:EE:FF` por `--device-id UUID_EXISTENTE`. A porta pode mudar após gravar. No Linux, se faltar permissão na serial, adicione o usuário ao grupo `dialout` (`sudo usermod -aG dialout "$USER"`) e faça novo login. Se configurar `DEVICE_API_KEY` no backend, defina o mesmo valor no ambiente da ponte antes de iniciá-la (`export DEVICE_API_KEY=...` no Linux; `$env:DEVICE_API_KEY='...'` no PowerShell).

### C. Opta por HTTP/Wi-Fi

Use o MySQL e as URLs da seção 2. Computador e Opta devem estar na **mesma rede**. Descubra o IPv4 do computador (`ip -4 addr show` no Linux; `ipconfig` no Windows). Crie `firmware/optaMesaMonitor/optaSecrets.h`:

```cpp
#pragma once
#define ULTRON_WIFI_SSID "NOME_DA_REDE"
#define ULTRON_WIFI_PASSWORD "SENHA_DA_REDE"
#define ULTRON_BACKEND_HOST "192.168.1.20"
#define ULTRON_DEVICE_API_KEY ""
```

Troque `192.168.1.20` pelo IP do computador, nunca por `127.0.0.1`. A chave deve ser igual a `DEVICE_API_KEY` no backend, se definida. Libere a entrada TCP 8000 no firewall do computador. O Opta acessa a **API**, enquanto o MySQL pode continuar restrito a `127.0.0.1:3306`.

Linux, em terminais separados:

```bash
arduino-cli board list
python3 tools/configurarTransmissao.py --transporte http --porta /dev/ttyACM0
.venv/bin/python -m uvicorn main:app --app-dir backend --host 0.0.0.0 --port 8000
# Em outro terminal:
npm --prefix frontend run dev -- --host 127.0.0.1
```

Windows, em terminais separados:

```powershell
arduino-cli board list
& .\.venv\Scripts\python.exe tools/configurarTransmissao.py --transporte http --porta COM4
& .\.venv\Scripts\python.exe -m uvicorn main:app --app-dir backend --host 0.0.0.0 --port 8000
# Em outro terminal:
npm --prefix frontend run dev -- --host 127.0.0.1
```

Confira `http://192.168.1.20:8000/api/health` de outro aparelho da rede. No dashboard, confirme cadastro do Opta, leituras e sinais da mesa. Teste uma peça por vez: não metálica → reta; metálica pequena → queda 1; metálica média/grande → queda 2. Compare comandos exibidos e movimento físico. Para acessar o dashboard em outro computador, use `VITE_API_BASE_URL=http://192.168.1.20:8000/api`, inclua `http://192.168.1.20:5173` em `CORS_ORIGINS`, inicie o Vite com `--host 0.0.0.0` e libere a porta 5173.

## 4. Comandos para testar

Execute a partir da raiz. Os testes Python usam SQLite isolado; não validam o MySQL nem o equipamento físico.

| Verificação | Linux | Windows PowerShell |
|---|---|---|
| API e ponte | `ULTRON_SIMULATION=true DATABASE_URL=sqlite:// ADMIN_EMAIL= ADMIN_PASSWORD= DEVICE_API_KEY= .venv/bin/python -m pytest -q backend/tests tools/tests` | `.\tools\testarProjeto.ps1` (também testa frontend) |
| Frontend | `npm --prefix frontend test` | `npm --prefix frontend test` |
| Lint | `npm --prefix frontend run lint` | `npm --prefix frontend run lint` |
| Build | `npm --prefix frontend run build` | `npm --prefix frontend run build` |
| API em execução | `curl -f http://127.0.0.1:8000/api/health` | `Invoke-RestMethod http://127.0.0.1:8000/api/health` |
| Compilar Opta sem gravar | `python3 tools/configurarTransmissao.py --transporte http --somente-compilar` | `& .\.venv\Scripts\python.exe tools/configurarTransmissao.py --transporte http --somente-compilar` |

O teste opcional de concorrência MySQL exige um banco local separado cujo nome comece com `ultron_test` e a variável `ULTRON_TEST_MYSQL_URL`. O teste USB físico exige Opta conectado, ponte ativa e confirmação de `HTTP confirmado` no terminal. Pare os processos em primeiro plano com `Ctrl+C`.

