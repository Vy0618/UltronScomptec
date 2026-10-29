# SCOMPTEC — IHM/CLP → Opta → servidor

O fluxo principal é **IHM/CLP → Arduino Opta → laptop/servidor**. O servidor recebe os estados pela serial, grava os eventos no MySQL e disponibiliza as informações à dashboard. A dashboard usa apenas o ID da máquina e os estados recebidos; não depende de acesso direto ao Opta ou à IHM/CLP.

## Índice

- [1. Como o fluxo principal funciona](#1-como-o-fluxo-principal-funciona)
- [2. Instalação e configuração](#2-instalação-e-configuração)
- [3. Setup e execução do fluxo completo](#3-setup-e-execução-do-fluxo-completo)
  - [Upload do código no Opta](#33-upload-do-código-no-opta)
- [4. Criar, listar, consultar, modificar e excluir máquinas](#4-criar-listar-consultar-modificar-e-excluir-máquinas)
- [5. Testes automatizados e diagnóstico](#5-testes-automatizados-e-diagnóstico)
- [6. Responsividade da dashboard](#6-responsividade-da-dashboard)
- [7. Testes locais sem hardware](#7-testes-locais-sem-hardware)
- [8. Persistência e compatibilidade](#8-persistência-e-compatibilidade)

Execute os comandos na raiz do projeto. Os exemplos principais usam Linux/Bash; as diferenças do Windows estão indicadas. Use um terminal separado para cada processo que permanece em execução.

## 1. Como o fluxo principal funciona

```text
IHM / CLP: estados D000–D007
         │ sinais digitais
         ▼
Arduino Opta: entradas I1–I8, ID padrão "1"
         │ serial USB, 115200, quadros CNC_JSON
         ▼
Laptop / servidor
  ponteUsb.py → POST /api/events → API FastAPI → MySQL
                                      ▲
                                      │ consultas HTTP e respostas JSON
                                      ▼
                             Dashboard React/Vite
```

1. **IHM/CLP:** disponibiliza os oito sinais booleanos da máquina ou da simulação. D000–D007 são os nomes dos sinais da IHM/CLP; não são pinos de saída do Arduino.
2. **Opta:** lê I1–I8, aplica a polaridade/filtro configurados e guarda o último snapshot em RAM. Não comanda relés ou atuadores.
3. **Serial:** o firmware envia a primeira amostra, alterações de estado e heartbeat a cada segundo. Cada linha começa com `CNC_JSON:` e contém o ID da máquina, sequência, uptime e o payload dos sinais.
4. **Ponte no servidor:** `tools/ponteUsb.py` lê a porta USB, usa o ID recebido e transforma `payload.digital_signals` em `states`. Ela envia o evento à API por HTTP. O horário atribuído pela ponte representa a recepção USB, não necessariamente o instante elétrico da mudança.
5. **API e banco:** a API resolve a máquina cadastrada, valida o evento e grava `machine_events` no MySQL. Mantém também o resumo operacional e o horário da última recepção em `cncs`.
6. **Dashboard:** consulta a API imediatamente e agenda outra rodada 5 s após terminar a anterior. Exibe máquinas, estados, histórico e alertas; não abre serial nem consulta o hardware. O banco é acessado pela API, não pelo navegador. Não há WebSocket ativo no fluxo atual.

### Mapeamento dos sinais

| IHM/CLP | Entrada Opta | Pino Arduino | Estado enviado à aplicação |
|---|---|---|---|
| D000 | I1 | A0 | `em_execucao` |
| D001 | I2 | A1 | `pausa` |
| D002 | I3 | A2 | `parada` |
| D003 | I4 | A3 | `emergencia` |
| D004 | I5 | A4 | `motor_ligado` |
| D005 | I6 | A5 | `automatico` |
| D006 | I7 | A6 | `manual` |
| D007 | I8 | A7 | `alarme` |

O padrão é nível alto ativo. `ULTRON_INPUT_ACTIVE_LOW_MASK` e `INPUT_FILTER_MS` em [config.h](firmware/optaCncMonitor/config.h) ajustam inversão e filtro. O firmware lê os pinos a cada passagem do loop, com pausa nominal de 1 ms; não há garantia de capturar pulsos menores que o intervalo real de aquisição. A indicação de emergência é para monitoramento.

Os valores e a fila do Opta ficam em RAM: não sobrevivem a uma queda de energia. A fila comporta até 16 amostras, com expiração em 15 s; a ponte mantém uma leitura em envio e a mais recente em espera. Interrupções podem perder transições, embora novas amostras permitam recuperar o estado atual.

### Identificação da máquina e contrato da API

O firmware transmite `machine_id: "1"` por padrão. A API interpreta `"1"` como o código **`CNC-001`** e procura a máquina cadastrada. O ID `"1"` não é o UUID interno do banco. A API também aceita o código completo ou o UUID no evento.

```json
{
  "machine_id": "1",
  "states": {
    "em_execucao": true,
    "pausa": false,
    "parada": false,
    "emergencia": false,
    "motor_ligado": true,
    "automatico": true,
    "manual": false,
    "alarme": false
  }
}
```

O endpoint é `POST /api/events`. Cada evento é um snapshot completo: campos ausentes ficam não informados e não são mesclados automaticamente com o anterior. Nomes de estados adicionais também são preservados.

`event_id` e `timestamp` são opcionais. Sem eles, cada POST cria uma leitura com horário do servidor. Reenvio com a mesma chave e conteúdo não duplica nem renova presença; conteúdo diferente com a mesma chave retorna 409. Máquina desconhecida retorna 404; contrato inválido ou booleanos como strings retornam 422. Observações antigas entram no histórico sem reverter o estado mais recente.

O resumo operacional reconhece emergência, alarme e execução, além das condições mantidas por compatibilidade; pausa e modos continuam disponíveis como booleanos independentes. Sem eventos novos pelo timeout, a máquina aparece como `SEM_COMUNICACAO`; recepção recente com observação antiga pode aparecer como `DADOS_DESATUALIZADOS`. O timeout padrão é 90 s.

### Separação de responsabilidades

O fluxo físico principal usa IHM/CLP e Opta. A aplicação continua independente da origem: `curl`, arquivo ou simulador podem enviar o mesmo contrato para testar API, banco e dashboard. MySQL é o banco da instalação; SQLite pode ser escolhido para testes isolados.

O contexto é monitorar falhas de CNC Mitsubishi M60, M70 e M80 por uma aquisição pouco invasiva. O perfil atual observa booleanos e não implementa protocolo proprietário ou códigos internos de erro desses comandos. A ligação física deve corresponder às interfaces autorizadas da instalação.

## 2. Instalação e configuração


Requisitos: Python 3.10+, Node.js 22.12+ e npm, MySQL 8 e Arduino CLI. O firmware usa o core `arduino:mbed_opta` e ArduinoJson. O arquivo [requirements.txt](requirements.txt) reúne as dependências Python.

### Linux (Mint/Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip build-essential mysql-server mysql-client curl jq
sudo systemctl enable --now mysql
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
npm --prefix frontend ci
```

Instale Node.js e disponibilize o Arduino CLI no `PATH`. Se o executável já estiver em `.tools/arduino-cli-linux/arduino-cli`, o procedimento de gravação da seção 3 também aceita esse caminho. A instalação do core e da biblioteca está junto dos comandos de gravação.

### Windows (PowerShell)

Instale Python, Node.js/npm, MySQL 8 e Arduino CLI. Deixe `py`, `node`, `npm` e `arduino-cli` acessíveis no terminal.

```powershell
py -3 -m venv .venv
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
npm --prefix frontend ci
```

### Banco e URLs da aplicação

No MySQL do **computador host**, entre como administrador (`sudo mysql` no Linux; `mysql -u root -p` no Windows) e crie somente o usuário da aplicação, com permissão para criar o banco configurado:

```sql
CREATE USER 'scomptec'@'127.0.0.1' IDENTIFIED BY 'SENHA_PRIVADA';
GRANT ALL PRIVILEGES ON cnc_monitor.* TO 'scomptec'@'127.0.0.1';
```

Copie os modelos apenas se as configurações locais ainda não existirem; depois edite as cópias. Se já houver arquivos configurados, preserve-os:

| Linux | Windows PowerShell |
|---|---|
| `cp -n backend/config.example.json backend/config.json` | `if (-not (Test-Path backend/config.json)) { Copy-Item backend/config.example.json backend/config.json }` |
| `cp -n frontend/.env.example frontend/.env` | `if (-not (Test-Path frontend/.env)) { Copy-Item frontend/.env.example frontend/.env }` |

Em `backend/config.json`, configure `DATABASE_URL` como `mysql+pymysql://scomptec:SENHA_PRIVADA@127.0.0.1:3306/cnc_monitor?charset=utf8mb4`; a API criará `cnc_monitor` na primeira inicialização. Troque também `AUTH_SECRET` e, se quiser login administrativo inicial, defina `ADMIN_EMAIL` e `ADMIN_PASSWORD` juntos. Codifique caracteres especiais da senha dentro da URL (`@` → `%40`, por exemplo). Em `frontend/.env`, use:

```dotenv
VITE_API_BASE_URL=http://127.0.0.1:8000/api
VITE_USE_MOCKS=false
```

Se `backend/.env` existir, seus valores prevalecem sobre `backend/config.json`. Reinicie a API após alterar a configuração e o Vite após alterar `frontend/.env`. Se a porta 8000 estiver ocupada, use outra porta na API e ajuste a URL do frontend e da ponte; no modo HTTP, ajuste também `BACKEND_PORT` em `firmware/optaCncMonitor/config.h` e regrave o Opta.

O backend lê ambiente do processo, depois `backend/.env` e depois `backend/config.json`, sem substituir valores de maior prioridade. O [configuracao.json](configuracao.json) da raiz é um inventário; não é carregado automaticamente. A ponte lê o ambiente e `backend/.env`, mas não lê `backend/config.json`: se houver `INGEST_API_KEY` somente no JSON, informe a mesma chave no ambiente da ponte.

## 3. Setup e execução do fluxo completo

### 3.1 Iniciar a API — terminal 1

Com o MySQL ativo e `backend/config.json` configurado:

```bash
.venv/bin/python -m uvicorn main:app \
  --app-dir backend --host 127.0.0.1 --port 8000
```

No Windows:

```powershell
& .\.venv\Scripts\python.exe -m uvicorn main:app --app-dir backend --host 127.0.0.1 --port 8000
```

Em outro terminal, confirme o banco e a API:

```bash
curl --fail-with-body -sS http://127.0.0.1:8000/api/health | jq
```

O esperado é `{"status":"ok","database":"ok"}`. Também é possível inspecionar as rotas em `http://127.0.0.1:8000/docs`.

### 3.2 Cadastrar ou localizar a máquina — terminal 2

Use os comandos da seção 4. Em um banco novo, o primeiro cadastro gera `CNC-001`, correspondente ao ID padrão `"1"` do firmware. Em um banco existente, consulte os códigos antes de cadastrar: o contador não reutiliza códigos excluídos. Para associar o Opta a outro código ou UUID, use `--machine-id` ao iniciar a ponte ou altere `ULTRON_MACHINE_ID` no firmware e regrave.

Não é necessário cadastrar um dispositivo ou MAC para o fluxo serial principal.

### 3.3 Upload do código no Opta

Upload é a gravação do firmware na placa. Execute os comandos a partir da raiz do projeto; o firmware usa serial USB e ID padrão `"1"`.

Conecte o Opta por USB e pare qualquer ponte ou monitor serial que esteja usando essa porta. No Linux, selecione o CLI instalado ou o executável local do projeto:

```bash
if command -v arduino-cli >/dev/null 2>&1; then
  ARDUINO_CLI=arduino-cli
else
  ARDUINO_CLI=.tools/arduino-cli-linux/arduino-cli
fi

"$ARDUINO_CLI" version
"$ARDUINO_CLI" core update-index
"$ARDUINO_CLI" core install arduino:mbed_opta@4.6.0
"$ARDUINO_CLI" lib install ArduinoJson@7.4.2
"$ARDUINO_CLI" board list
```

Se nenhum dos executáveis existir, instale o Arduino CLI antes de continuar. Substitua `/dev/ttyACM0` pela porta listada e grave o transporte USB:

```bash
python3 tools/configurarTransmissao.py \
  --transporte usb --porta /dev/ttyACM0 --cli "$ARDUINO_CLI"
```

O script limpa a pasta de artefatos do transporte selecionado, compila os fontes de [optaCncMonitor](firmware/optaCncMonitor) e só depois grava a placa. Essa limpeza evita o erro `multiple build artifacts found` causado por binários de sketches antigos. Para compilar sem gravar, troque `--porta /dev/ttyACM0` por `--somente-compilar`. Após a gravação, confira a porta novamente; ela pode mudar.

No Windows, com `arduino-cli` no PATH:

```powershell
arduino-cli core update-index
arduino-cli core install arduino:mbed_opta@4.6.0
arduino-cli lib install ArduinoJson@7.4.2
arduino-cli board list
& .\.venv\Scripts\python.exe tools/configurarTransmissao.py --transporte usb --porta COM4
```

Use a porta realmente listada, no lugar de `COM4`.

#### Compilação e upload diretamente pelo Arduino CLI

O script acima já executa compilação e upload. Para executar essas etapas separadamente, use os comandos abaixo depois de instalar o core e a biblioteca. Mantenha a ponte serial e o monitor serial fechados durante a gravação.

Linux/Bash, usando `ARDUINO_CLI` definido anteriormente:

```bash
"$ARDUINO_CLI" board list

"$ARDUINO_CLI" compile \
  --fqbn arduino:mbed_opta:opta \
  --build-property compiler.cpp.extra_flags=-DULTRON_TELEMETRY_USB_OVERRIDE=1 \
  --output-dir .build/firmware/opta-usb \
  firmware/optaCncMonitor

# Execute o upload somente se a compilação concluir com sucesso.
"$ARDUINO_CLI" upload \
  --fqbn arduino:mbed_opta:opta \
  --port /dev/ttyACM0 \
  --input-dir .build/firmware/opta-usb
```

Windows/PowerShell, com `arduino-cli` no PATH:

```powershell
arduino-cli board list

arduino-cli compile --fqbn arduino:mbed_opta:opta --build-property "compiler.cpp.extra_flags=-DULTRON_TELEMETRY_USB_OVERRIDE=1" --output-dir .build/firmware/opta-usb firmware/optaCncMonitor

# Execute o upload somente se a compilação concluir com sucesso.
arduino-cli upload --fqbn arduino:mbed_opta:opta --port COM4 --input-dir .build/firmware/opta-usb
```

Substitua a porta pelo valor retornado por `board list`. O upload usa o binário gerado em `.build/firmware/opta-usb`; alterações no código exigem nova compilação antes de gravar. Após o upload, liste as portas novamente e inicie a ponte conforme a seção 3.4.

### 3.4 Iniciar a coleta serial — terminal 3

```bash
.venv/bin/python tools/ponteUsb.py --listar-portas
.venv/bin/python tools/ponteUsb.py \
  --porta /dev/ttyACM0 --api http://127.0.0.1:8000/api
```

A ponte usa o ID `"1"` enviado pelo firmware. Para substituí-lo sem regravar, informe a máquina escolhida:

```bash
.venv/bin/python tools/ponteUsb.py \
  --porta /dev/ttyACM0 --machine-id CNC-002 --api http://127.0.0.1:8000/api
```

No Windows:

```powershell
& .\.venv\Scripts\python.exe tools/ponteUsb.py --porta COM4 --api http://127.0.0.1:8000/api
```

Se a API exigir chave, defina a mesma `INGEST_API_KEY` no ambiente da ponte. No Linux, permissão negada na serial pode exigir adicionar o usuário ao grupo `dialout` com `sudo usermod -aG dialout "$USER"` e fazer novo login. Diagnósticos como `HTTP confirmado` mostram que a API aceitou o envio.

### 3.5 Iniciar a dashboard — terminal 4

```bash
VITE_USE_MOCKS=false VITE_API_BASE_URL=http://127.0.0.1:8000/api \
npm --prefix frontend run dev -- --host 127.0.0.1 --port 5173 --strictPort
```

No Windows:

```powershell
$env:VITE_USE_MOCKS='false'
$env:VITE_API_BASE_URL='http://127.0.0.1:8000/api'
npm --prefix frontend run dev -- --host 127.0.0.1 --port 5173 --strictPort
```

Abra `http://127.0.0.1:5173/dashboard`. A máquina deve aparecer após o cadastro; os estados chegam depois que a ponte publica eventos. A tela de detalhes usa o código legível: `http://127.0.0.1:5173/maquinas/CNC-001`.

Ative os sinais na IHM/CLP, confira `HTTP confirmado` na ponte e compare os estados retornados por `/api/cncs/{uuid}/status` com a dashboard. Sem novos eventos, o estado muda pelo timeout. Mantenha API, ponte e frontend ativos durante a coleta.

Para acessar a interface de outro computador, a API e o frontend precisam escutar em endereços acessíveis, `VITE_API_BASE_URL` deve apontar para o IP do servidor e `CORS_ORIGINS` deve incluir a origem real do frontend. O Opta continua conectado por USB ao computador que executa a ponte.

## 4. Criar, listar, consultar, modificar e excluir máquinas

Os comandos abaixo são Linux/Bash e usam `curl` e `jq`, a partir da raiz. A API deve estar rodando. As rotas de cadastro chamam as máquinas de `cncs`; nome e descrição são editáveis, enquanto UUID e código são gerados pelo servidor.

```bash
API=http://127.0.0.1:8000/api
mkdir -p .local
```

### Criar uma máquina

```bash
curl --fail-with-body -sS -X POST "$API/cncs" \
  -H 'Content-Type: application/json' \
  -d '{"name":"Máquina 01","description":"Monitoramento IHM/CLP → Opta → servidor"}' \
  -o .local/maquina-criada.json

jq '{id, code, name, description}' .local/maquina-criada.json
MACHINE_ID=$(jq -er '.id' .local/maquina-criada.json)
MACHINE_CODE=$(jq -er '.code' .local/maquina-criada.json)
```

Guarde o UUID em `MACHINE_ID`: ele é usado nos comandos de consulta, edição e exclusão. Cada POST cria uma máquina nova; não repita o cadastro para reenviar estados de uma máquina existente.

### Listar máquinas

```bash
curl --fail-with-body -sS "$API/cncs" | jq
```

Para selecionar uma máquina já cadastrada por seu código, substitua `CNC-001` e execute:

```bash
MACHINE_ID=$(
  curl --fail-with-body -sS "$API/cncs" \
    | jq -er '.[] | select(.code == "CNC-001") | .id'
)
```

Se não houver resultado, cadastre a máquina ou escolha um código existente antes de continuar. Em um terminal novo, carregue novamente o UUID pelo comando acima ou pelo arquivo salvo no cadastro.

### Consultar uma máquina e seus dados

```bash
curl --fail-with-body -sS "$API/cncs/$MACHINE_ID" | jq
curl --fail-with-body -sS "$API/cncs/$MACHINE_ID/status" | jq
curl --fail-with-body -sS "$API/cncs/$MACHINE_ID/history?page=1&limit=50" | jq
curl --fail-with-body -sS "$API/cncs/$MACHINE_ID/utilization" | jq
```

### Modificar uma máquina

```bash
curl --fail-with-body -sS -X PUT "$API/cncs/$MACHINE_ID" \
  -H 'Content-Type: application/json' \
  -d '{"name":"Centro de usinagem 01","description":"CNC Mitsubishi M70 — bancada de monitoramento"}' | jq
```

Pode enviar apenas `name` ou apenas `description`. O cadastro não altera os estados operacionais: eles são atualizados pelos eventos recebidos.

### Enviar um estado sem hardware para conferir o cadastro

A aplicação aceita o mesmo evento que a ponte envia, permitindo verificar API, MySQL e dashboard sem depender da bancada:

```bash
jq -n --arg machine_id "$MACHINE_ID" '{
  machine_id: $machine_id,
  states: {em_execucao: true, pausa: false, parada: false, emergencia: false,
           motor_ligado: true, automatico: true, manual: false, alarme: false}
}' | curl --fail-with-body -sS -X POST "$API/events" \
  -H 'Content-Type: application/json' --data-binary @- | jq
```

Se `INGEST_API_KEY` estiver configurada, acrescente `-H "X-API-Key: $INGEST_API_KEY"` ao POST, com a variável definida no terminal. A [seção 7](#7-testes-locais-sem-hardware) oferece um ambiente SQLite isolado e exemplos de pipelines.

### Excluir uma máquina

Este comando remove o cadastro e seu histórico de eventos. Use o UUID da máquina que deseja excluir:

```bash
curl --fail-with-body -sS -X DELETE "$API/cncs/$MACHINE_ID" -w 'HTTP %{http_code}\n'
```

A resposta esperada é HTTP 204, sem corpo JSON. Confirme a remoção com a listagem. Apagar e cadastrar novamente gera outro UUID e outro código; não reutiliza automaticamente o ID `"1"` do Opta.

## 5. Testes automatizados e diagnóstico

Execute a partir da raiz. Os testes Python usam SQLite isolado; não validam o MySQL nem o equipamento físico.

| Verificação | Linux | Windows PowerShell |
|---|---|---|
| API e ponte | `ULTRON_SIMULATION=true DATABASE_URL=sqlite:// ADMIN_EMAIL= ADMIN_PASSWORD= DEVICE_API_KEY= .venv/bin/python -m pytest -q backend/tests tools/tests` | `.\tools\testarProjeto.ps1` (também testa frontend) |
| Frontend | `npm --prefix frontend test` | `npm --prefix frontend test` |
| Lint | `npm --prefix frontend run lint` | `npm --prefix frontend run lint` |
| Build | `npm --prefix frontend run build` | `npm --prefix frontend run build` |
| API em execução | `curl -f http://127.0.0.1:8000/api/health` | `Invoke-RestMethod http://127.0.0.1:8000/api/health` |
| Compilar Opta sem gravar | `python3 tools/configurarTransmissao.py --transporte usb --somente-compilar` | `& .\.venv\Scripts\python.exe tools/configurarTransmissao.py --transporte usb --somente-compilar` |

O teste opcional de concorrência MySQL exige um banco local separado cujo nome comece com `ultron_test` e a variável `ULTRON_TEST_MYSQL_URL`. O teste USB físico exige Opta conectado, ponte ativa e confirmação de `HTTP confirmado` no terminal. Pare os processos em primeiro plano com `Ctrl+C`.

## 6. Responsividade da dashboard

Comandos para Linux/Bash.

Este teste verifica a adaptação do layout a diferentes tamanhos de tela usando dados demonstrativos, sem depender do backend ou do Opta. Os comandos devem ser executados na raiz do projeto, com o ambiente `.venv` já criado conforme a seção 2.

**1. Preparar o frontend e o navegador de teste**

```bash
npm --prefix frontend ci
.venv/bin/python -m pip install playwright
.venv/bin/python -m playwright install chromium
```

A instalação utiliza a biblioteca oficial [Playwright para Python](https://playwright.dev/python/docs/library).

**2. Iniciar a dashboard no primeiro terminal**

```bash
VITE_USE_MOCKS=true npm --prefix frontend run dev -- \
  --host 127.0.0.1 --port 5174 --strictPort
```

Acesse `http://127.0.0.1:5174/dashboard`. Mantenha esse terminal aberto durante o teste. A porta 5174 precisa estar livre; `--strictPort` impede iniciar silenciosamente em outra porta.

**3. Executar o teste em outro terminal, também na raiz do projeto**

O script verifica celular, tablet, notebook e desktop, incluindo os pontos de mudança do layout. Salva capturas da página inteira, do menu quando disponível e um relatório JSON.

```bash
.venv/bin/python - <<'PY'
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

output = Path(".local/testes/responsividade")
output.mkdir(parents=True, exist_ok=True)

sizes = [
    (320, 568),
    (390, 844),
    (639, 900),
    (640, 900),
    (767, 1024),
    (768, 1024),
    (1023, 768),
    (1024, 768),
    (1366, 768),
    (1920, 1080),
]

results = []

with sync_playwright() as p:
    browser = p.chromium.launch()

    for width, height in sizes:
        context = browser.new_context(
            viewport={"width": width, "height": height},
            locale="pt-BR",
            reduced_motion="reduce",
        )
        page = context.new_page()
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))

        page.goto(
            "http://127.0.0.1:5174/dashboard",
            wait_until="domcontentloaded",
        )
        page.get_by_text(
            "Status da Operação CNC:", exact=True
        ).wait_for(state="visible")

        page.screenshot(
            path=str(output / f"dashboard-{width}x{height}.png"),
            full_page=True,
            animations="disabled",
        )

        dimensions = page.evaluate("""() => ({
            viewport: document.documentElement.clientWidth,
            content: Math.max(
                document.documentElement.scrollWidth,
                document.body.scrollWidth
            )
        })""")

        overflow = dimensions["content"] > dimensions["viewport"] + 1

        menu = page.get_by_role("button", name="Abrir menu", exact=True)
        menu_tested = menu.is_visible()
        if menu_tested:
            menu.click()
            page.screenshot(
                path=str(output / f"menu-{width}x{height}.png"),
                full_page=True,
                animations="disabled",
            )

        result = {
            "resolucao": f"{width}x{height}",
            "rolagem_horizontal": overflow,
            "menu_aberto_para_inspecao": menu_tested,
            "erros_javascript": list(errors),
            "aprovado": not overflow and not errors,
        }
        results.append(result)

        label = "OK" if result["aprovado"] else "FALHOU"
        print(f"{label}: {width}x{height}")
        context.close()

    browser.close()

(output / "resultado.json").write_text(
    json.dumps(results, ensure_ascii=False, indent=2),
    encoding="utf-8",
)
print(f"\nCapturas e relatório: {output.resolve()}")
raise SystemExit(0 if all(r["aprovado"] for r in results) else 1)
PY
```

**4. Abrir as capturas e o relatório**

```bash
xdg-open .local/testes/responsividade
cat .local/testes/responsividade/resultado.json
```

O resultado automático identifica rolagem horizontal na página e erros JavaScript, retornando código de saída 1 se houver falha. A abertura do menu é registrada para inspeção, mas sua usabilidade não é validada automaticamente. Nas imagens, confira textos cortados, sobreposição de componentes, gráficos legíveis e acesso ao menu. Um resultado `OK` não substitui essa inspeção visual e não mede desempenho, tempo de resposta da API ou comunicação com o Opta.

Ao terminar, encerre a instância demonstrativa com `Ctrl+C` no primeiro terminal.

## 7. Testes locais sem hardware

Comandos para Linux/Bash, executados na raiz do projeto. Nenhum Opta, IHM, CLP ou cadastro de coletor é necessário.

**1. Iniciar a API isolada no primeiro terminal**

```bash
mkdir -p .local
ULTRON_SIMULATION=true DATABASE_URL=sqlite:///./.local/testes-locais.db \
EVENT_OFFLINE_TIMEOUT_SECONDS=10 INGEST_API_KEY= DEVICE_API_KEY= \
CORS_ORIGINS=http://127.0.0.1:5175,http://localhost:5175 \
ADMIN_EMAIL= ADMIN_PASSWORD= \
.venv/bin/python -m uvicorn main:app \
  --app-dir backend --host 127.0.0.1 --port 8001
```

**2. Cadastrar a máquina no segundo terminal**

`jq` extrai o UUID retornado pela API. Instale as ferramentas com `sudo apt install curl jq` se necessário.

```bash
API=http://127.0.0.1:8001/api
curl --fail-with-body -sS "$API/health" | jq

MACHINE_ID=$(
  curl --fail-with-body -sS -X POST "$API/cncs" \
    -H 'Content-Type: application/json' \
    -d '{"name":"Estação de teste","description":"Eventos independentes de hardware"}' \
  | jq -er '.id'
)
echo "$MACHINE_ID"
```

**3. Enviar os estados**

```bash
jq -n --arg machine_id "$MACHINE_ID" '{
  machine_id: $machine_id,
  states: {
    em_execucao: true, pausa: false, parada: false, emergencia: false,
    motor_ligado: true, automatico: true, manual: false, alarme: false
  }
}' | curl --fail-with-body -sS -X POST "$API/events" \
  -H 'Content-Type: application/json' --data-binary @- | jq
```

Para testar um alarme, envie outro snapshot:

```bash
jq -n --arg machine_id "$MACHINE_ID" '{
  machine_id: $machine_id,
  states: {em_execucao: false, alarme: true, emergencia: false}
}' | curl --fail-with-body -sS -X POST "$API/events" \
  -H 'Content-Type: application/json' --data-binary @- | jq
```

Os outros campos não enviados ficam não informados no snapshot atual. Para enviar um arquivo, altere o `machine_id` em [examples/machine-event.json](examples/machine-event.json) e execute:

```bash
curl --fail-with-body -sS -X POST "$API/events" \
  -H 'Content-Type: application/json' --data-binary @examples/machine-event.json | jq
```

**4. Consultar, editar e listar as máquinas**

```bash
curl --fail-with-body -sS "$API/cncs" | jq
curl --fail-with-body -sS "$API/cncs/$MACHINE_ID" | jq
curl --fail-with-body -sS "$API/cncs/$MACHINE_ID/status" | jq
curl --fail-with-body -sS "$API/cncs/$MACHINE_ID/history?limit=50" | jq
curl --fail-with-body -sS "$API/cncs/$MACHINE_ID/utilization" | jq

curl --fail-with-body -sS -X PUT "$API/cncs/$MACHINE_ID" \
  -H 'Content-Type: application/json' -d '{"name":"Estação 01"}' | jq
```

**5. Gerar eventos e compor programas por pipes**

O simulador apenas escreve JSON Lines em stdout. Ele não abre serial, não cadastra máquina e não acessa a API. O publicador apenas lê stdin e faz os POSTs; respostas vão para stdout e erros para stderr.

```bash
# Gerar oito eventos para um arquivo, sem rede nem hardware.
.venv/bin/python tools/simuladorCnc.py --machine-id "$MACHINE_ID" \
  --state cycle --count 8 --interval 0 > .local/eventos.jsonl

# Publicar o arquivo na API.
.venv/bin/python tools/publicarEventos.py --api "$API" < .local/eventos.jsonl

# Produzir e publicar continuamente; interrompa com Ctrl+C.
set -o pipefail
.venv/bin/python tools/simuladorCnc.py --machine-id "$MACHINE_ID" \
  --state cycle --count -1 \
  | .venv/bin/python tools/publicarEventos.py --api "$API"
```

Eventos gerados incluem `event_id` e horário de observação. Reenviar o mesmo arquivo preserva os IDs e não duplica registros; uma leitura antiga não substitui o estado mais recente. Reenvios idênticos não renovam a presença da máquina. Um evento com mesma chave e conteúdo diferente retorna 409. JSON inválido ou booleanos escritos como strings retornam 422.

**6. Abrir a dashboard em outro terminal**

```bash
VITE_USE_MOCKS=false VITE_API_BASE_URL=http://127.0.0.1:8001/api \
npm --prefix frontend run dev -- --host 127.0.0.1 --port 5175 --strictPort
```

Abra `http://127.0.0.1:5175/dashboard`. O acompanhamento depende apenas dos eventos recebidos. O ID identifica a máquina, independentemente de quantos produtores enviem seus estados.

**7. Verificar a ausência de novos eventos**

Pare os produtores e execute no terminal com as variáveis:

```bash
sleep 11
curl --fail-with-body -sS "$API/cncs/$MACHINE_ID/status" \
  | jq '{status, online, states, last_seen}'
```

Com o timeout de 10 s deste roteiro, o estado será `SEM_COMUNICACAO` e os últimos estados continuarão disponíveis. Uma observação antiga recebida agora pode resultar em `DADOS_DESATUALIZADOS`; receber e observar são horários distintos.

**8. Limpar a máquina de teste**

A exclusão da máquina remove seu histórico. Remover um coletor opcional não remove nem transfere os eventos da máquina.

```bash
curl --fail-with-body -sS -X DELETE "$API/cncs/$MACHINE_ID" -w 'HTTP %{http_code}\n'
```

Pare API e frontend com `Ctrl+C` nos respectivos terminais. MySQL continua como banco da instalação; estes comandos escolhem explicitamente SQLite para isolamento.

## 8. Persistência e compatibilidade

Os eventos novos são gravados em `machine_events`, diretamente ligados à máquina. Essa tabela é criada na inicialização, sem alterar as colunas da tabela antiga. Leituras preexistentes em `telemetry` continuam disponíveis por uma camada de compatibilidade. A aplicação não exige migração destrutiva nem apaga o histórico anterior.

Os endpoints `/api/devices/...` permanecem como adaptadores opcionais. Sua telemetria é convertida para eventos de máquina. O campo antigo `gateway_online` continua na resposta por compatibilidade; a dashboard usa `online`, calculado pela chegada de novos eventos, sem consultar a situação do coletor.

`INGEST_API_KEY` e `X-API-Key` são os nomes genéricos para autenticação de ingestão. `EVENT_OFFLINE_TIMEOUT_SECONDS` define quanto tempo sem novos eventos torna a máquina desatualizada/offline; sem ele, o nome antigo `DEVICE_OFFLINE_TIMEOUT_SECONDS` é usado. Reinicie a API após alterar essas configurações.
