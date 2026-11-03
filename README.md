# SCOMPTEC

Monitoramento de máquinas CNC com Arduino Opta, API FastAPI, MySQL e dashboard React. Exibe estados, alertas e histórico a partir dos sinais disponibilizados pela IHM/CLP.

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

Requisitos: **Python 3.10+**, **Node.js 22.12+ com npm** e **MySQL 8**. Para usar o Opta, instale também o **Arduino CLI**.

Execute os comandos na raiz do projeto. Os exemplos usam Linux/Bash; as diferenças do Windows estão abaixo.

### Dependências

No Ubuntu/Mint/Debian, com Node.js e npm já instalados:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip build-essential mysql-server mysql-client curl jq
sudo systemctl enable --now mysql
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
npm --prefix frontend ci
```

### Banco e configuração

Entre no MySQL como administrador (`sudo mysql`) e crie o usuário da aplicação:

```sql
CREATE USER 'scomptec'@'127.0.0.1' IDENTIFIED BY 'SENHA_PRIVADA';
GRANT ALL PRIVILEGES ON cnc_monitor.* TO 'scomptec'@'127.0.0.1';
```

Copie os modelos somente se os arquivos locais ainda não existirem:

```bash
cp -n backend/config.example.json backend/config.json
cp -n frontend/.env.example frontend/.env
```

Em `backend/config.json`, ajuste `DATABASE_URL` e troque `AUTH_SECRET`:

```text
mysql+pymysql://scomptec:SENHA_PRIVADA@127.0.0.1:3306/cnc_monitor?charset=utf8mb4
```

Codifique caracteres especiais da senha na URL (`@` → `%40`, por exemplo). A API cria o banco e as tabelas na primeira inicialização.

Em `frontend/.env`:

```dotenv
VITE_API_BASE_URL=http://127.0.0.1:8000/api
VITE_USE_MOCKS=false
```

A configuração do backend segue esta prioridade: **ambiente → `backend/.env` → `backend/config.json`**. Reinicie API e frontend após mudar suas configurações. O [configuracao.json](configuracao.json) da raiz é apenas um inventário de parâmetros.

<details>
<summary>Setup no Windows (PowerShell)</summary>

Instale Python, Node.js/npm, MySQL 8 e, para o hardware, Arduino CLI. Crie o usuário no MySQL com o SQL acima, usando `mysql -u root -p`.

```powershell
py -3 -m venv .venv
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
npm --prefix frontend ci
if (-not (Test-Path backend/config.json)) { Copy-Item backend/config.example.json backend/config.json }
if (-not (Test-Path frontend/.env)) { Copy-Item frontend/.env.example frontend/.env }
```

Ajuste os arquivos conforme indicado acima. Nos comandos Python deste guia, substitua `.venv/bin/python` por `& .\.venv\Scripts\python.exe` e use a porta serial real, como `COM4`.

Para iniciar API e dashboard com o launcher:

```powershell
.\iniciarLocal.ps1
# Para encerrar os processos iniciados pelo launcher:
.\iniciarLocal.ps1 -Acao parar
```

A ponte USB deve ser iniciada separadamente.

</details>

## Executar

### 1. Iniciar a API

```bash
.venv/bin/python -m uvicorn main:app --app-dir backend --host 127.0.0.1 --port 8000
```

Confirme em `http://127.0.0.1:8000/api/health`: o retorno esperado é `{"status":"ok","database":"ok"}`. A documentação interativa fica em `http://127.0.0.1:8000/docs`.

### 2. Cadastrar a máquina

Em outro terminal, consulte os cadastros existentes antes de criar um novo:

```bash
API=http://127.0.0.1:8000/api
curl --fail-with-body -sS "$API/cncs" | jq

# Para cadastrar uma máquina nova:
curl --fail-with-body -sS -X POST "$API/cncs" \
  -H 'Content-Type: application/json' \
  -d '{"name":"Máquina 01","description":"Monitoramento IHM/CLP"}' | jq
```

Guarde o `id` (UUID) e o `code` retornados. O Opta envia `machine_id: "1"` por padrão, que resolve para **`CNC-001`**. Códigos excluídos não são reutilizados; para outro código, informe `--machine-id` na ponte. O fluxo USB dispensa cadastro de dispositivo ou MAC.

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
.venv/bin/python tools/ponteUsb.py --porta /dev/ttyACM0 --api http://127.0.0.1:8000/api
```

Para outra máquina, acrescente `--machine-id CNC-002` com o código correto. A mensagem `HTTP confirmado` indica que a API aceitou o evento. No Linux, permissão negada na serial pode exigir inclusão no grupo `dialout` e novo login.

Se configurar `INGEST_API_KEY` no backend, forneça a mesma chave no ambiente da ponte. Ela lê `backend/.env`, mas não `backend/config.json`.

### 5. Abrir a dashboard

Em outro terminal:

```bash
npm --prefix frontend run dev -- --host 127.0.0.1 --port 5173 --strictPort
```

Acesse **http://127.0.0.1:5173/dashboard**. Detalhes da máquina: `/maquinas/CNC-001`; modo TV: `/tv`. Ative os sinais na IHM/CLP e compare os estados na dashboard. Mantenha API, ponte e frontend em execução; encerre com `Ctrl+C`.

Para acesso por outro computador, ajuste o endereço de escuta dos serviços, `VITE_API_BASE_URL` e `CORS_ORIGINS` para o IP/origem usados na rede.

## Eventos e consultas

A API aceita eventos de qualquer produtor, inclusive `curl` ou simulador:

```json
{"machine_id":"CNC-001","states":{"em_execucao":true,"alarme":false}}
```

Cada envio representa um snapshot completo: estados ausentes ficam não informados. `event_id` e `timestamp` são opcionais. Reenvios com a mesma chave e conteúdo não duplicam registros nem renovam presença; conteúdo diferente retorna 409. Leituras antigas não revertem o estado atual.

Sem eventos novos por 90 s, o estado passa a `SEM_COMUNICACAO`. Uma observação antiga recebida recentemente pode aparecer como `DADOS_DESATUALIZADOS`. Ajuste o timeout com `EVENT_OFFLINE_TIMEOUT_SECONDS` (mínimo 10 s).

| Método | Rota | Uso |
|---|---|---|
| POST / GET | `/api/cncs` | Cadastrar / listar máquinas |
| GET / PUT / DELETE | `/api/cncs/{uuid}` | Consultar / editar / excluir |
| GET | `/api/cncs/{uuid}/status` | Estados e última comunicação |
| GET | `/api/cncs/{uuid}/history?page=1&limit=50` | Histórico paginado |
| GET | `/api/cncs/{uuid}/utilization` | Utilização nas últimas 24 h |
| POST | `/api/events` | Enviar estados |

Excluir uma máquina remove seu histórico. Trocar ou remover um coletor preserva os eventos da máquina. Os endpoints `/api/devices/...` continuam disponíveis para integrações anteriores.

## Testar sem hardware

Após o setup das dependências, encerre a API habitual e inicie uma instância com SQLite separado na mesma porta:

```bash
mkdir -p .local
ULTRON_SIMULATION=true DATABASE_URL=sqlite:///./.local/testes-locais.db \
ADMIN_EMAIL= ADMIN_PASSWORD= INGEST_API_KEY= DEVICE_API_KEY= \
EVENT_OFFLINE_TIMEOUT_SECONDS=10 \
.venv/bin/python -m uvicorn main:app --app-dir backend --host 127.0.0.1 --port 8000
```

Cadastre a máquina conforme o passo 2 e, com o código retornado, publique estados continuamente:

```bash
set -o pipefail
.venv/bin/python tools/simuladorCnc.py --machine-id CNC-001 --state cycle --count -1 \
  | .venv/bin/python tools/publicarEventos.py --api http://127.0.0.1:8000/api
```

Abra o frontend normalmente. Pare o simulador para observar o timeout de 10 s. Também é possível enviar o [evento de exemplo](examples/machine-event.json) por `curl`, ajustando o ID da máquina. No Windows, `iniciarLocal.ps1 -Simular` inicia API e frontend com SQLite separado.

## Autenticação e administração

Configure `ADMIN_EMAIL` e `ADMIN_PASSWORD` juntos no backend (senha de 8–128 caracteres), com `ADMIN_NAME` opcional, e reinicie a API. A conta será criada ou atualizada. Entre pelo login normal e acesse `/admin` para gerenciar usuários, ocorrências, limites e histórico administrativo.

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
