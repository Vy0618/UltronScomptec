param(
    [switch]$Simular,
    [ValidateSet('todos', 'backend', 'frontend', 'verificar', 'parar')]
    [string]$Acao = 'todos',
    [ValidateRange(1024, 65535)][int]$PortaApi = 8000,
    [ValidateRange(1024, 65535)][int]$PortaDashboard = 5173
)

$ErrorActionPreference = 'Stop'
$projectRoot = $PSScriptRoot
$localDir = Join-Path $projectRoot '.local'
$statePath = Join-Path $localDir 'processos.json'
New-Item -ItemType Directory -Force -Path $localDir | Out-Null

function Read-State {
    if (Test-Path -LiteralPath $statePath) {
        $saved = Get-Content -LiteralPath $statePath -Raw | ConvertFrom-Json
        if ($saved.root -ne $projectRoot) { throw 'Arquivo de processos pertence a outra pasta.' }
        return $saved
    }
    return $null
}

function Is-OwnedProcess($entry) {
    $process = Get-Process -Id $entry.id -ErrorAction SilentlyContinue
    return $process -and $process.Path -eq $entry.executable -and `
        $process.StartTime.ToUniversalTime().Ticks -eq [long]$entry.startedTicks
}

function Stop-OwnedProcess($entry) {
    if (Is-OwnedProcess $entry) {
        # O launcher Python de um venv no Windows pode ter um processo filho.
        & (Join-Path $env:SystemRoot 'System32\taskkill.exe') /PID $entry.id /T /F | Out-Null
        if ($LASTEXITCODE -ne 0) {
            Start-Sleep -Milliseconds 500
            if (Is-OwnedProcess $entry) { throw ('Falha ao encerrar ' + $entry.name) }
        }
        Write-Output ('Encerrado: ' + $entry.name)
    }
}

if ($Acao -eq 'parar') {
    $saved = Read-State
    if ($saved) {
        foreach ($entry in @($saved.processes)) {
            Stop-OwnedProcess $entry
        }
        Remove-Item -LiteralPath $statePath
    }
    Write-Output 'Processos locais registrados por este projeto encerrados.'
    exit 0
}

$python = Join-Path $projectRoot '.venv\Scripts\python.exe'
if ($Acao -ne 'frontend' -and -not (Test-Path -LiteralPath $python)) {
    throw 'Crie .venv e instale requirements.txt da raiz antes de iniciar.'
}
$nodeCommand = Get-Command node.exe -ErrorAction SilentlyContinue
$node = if ($nodeCommand) { $nodeCommand.Source } else {
    Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe'
}
$vite = Join-Path $projectRoot 'frontend\node_modules\vite\bin\vite.js'
if ($Acao -ne 'backend' -and (-not (Test-Path -LiteralPath $node) -or -not (Test-Path -LiteralPath $vite))) {
    throw 'Instale Node.js e as dependencias do frontend com npm ci.'
}
if ($Acao -ne 'frontend') {
    & $python -c 'import uvicorn,fastapi,sqlalchemy,pymysql,email_validator,dotenv'
    if ($LASTEXITCODE -ne 0) { throw 'Dependencias Python incompletas.' }
}
if ($Acao -eq 'verificar') {
    Write-Output 'Python, dependencias do backend, Node.js e Vite encontrados.'
    exit 0
}

$saved = Read-State
$entries = @()
if ($saved) { $entries = @($saved.processes | Where-Object { Is-OwnedProcess $_ }) }
$previousIds = @($entries | ForEach-Object { $_.id })

function Save-State {
    @{ root = $projectRoot; processes = @($script:entries) } | ConvertTo-Json -Depth 4 |
        Set-Content -LiteralPath $statePath -Encoding UTF8
}

function Start-LocalProcess([string]$Name, [string]$Executable, [string[]]$Arguments, [string]$Directory = $projectRoot) {
    if (@($script:entries | Where-Object { $_.name -eq $Name }).Count) {
        throw "O processo $Name ja esta registrado. Use -Acao parar antes de reiniciar."
    }
    $argumentLine = ($Arguments | ForEach-Object { '"' + $_ + '"' }) -join ' '
    $process = Start-Process -FilePath $Executable -ArgumentList $argumentLine -WorkingDirectory $Directory `
        -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $localDir "$Name.log") `
        -RedirectStandardError (Join-Path $localDir "$Name.err.log")
    $script:entries += @{ name = $Name; id = $process.Id; executable = $Executable;
        startedTicks = $process.StartTime.ToUniversalTime().Ticks }
    Save-State
    Write-Output ("Iniciado: $Name (PID " + $process.Id + ')')
}

function Assert-PortFree([int]$Port) {
    $client = New-Object System.Net.Sockets.TcpClient
    try {
        $pending = $client.BeginConnect('127.0.0.1', $Port, $null, $null)
        if ($pending.AsyncWaitHandle.WaitOne(500) -and $client.Connected) {
            throw "A porta $Port ja esta ocupada. Nenhum processo existente foi encerrado."
        }
    } finally { $client.Dispose() }
}

function Wait-Http([string]$Url) {
    for ($attempt = 0; $attempt -lt 30; $attempt++) {
        try {
            $response = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 2
            if ($response.StatusCode -eq 200) { return }
        } catch { Start-Sleep -Milliseconds 500 }
    }
    throw "Servico nao respondeu em $Url. Consulte os logs em .local."
}

$apiUrl = "http://127.0.0.1:$PortaApi/api"
if ($PortaApi -eq $PortaDashboard) { throw 'API e dashboard precisam de portas diferentes.' }
if ($Acao -in @('todos', 'backend')) { Assert-PortFree $PortaApi }
if ($Acao -in @('todos', 'frontend')) { Assert-PortFree $PortaDashboard }
$environmentNames = @('NO_PROXY', 'VITE_API_BASE_URL', 'VITE_USE_MOCKS', 'PYTHONUNBUFFERED', 'DATABASE_URL', 'DEVICE_OFFLINE_TIMEOUT_SECONDS', 'ADMIN_EMAIL', 'ADMIN_PASSWORD', 'DEVICE_API_KEY', 'INGEST_API_KEY', 'EVENT_OFFLINE_TIMEOUT_SECONDS', 'ULTRON_SIMULATION', 'CORS_ORIGINS')
$previousEnvironment = @{}
foreach ($name in $environmentNames) { $previousEnvironment[$name] = [Environment]::GetEnvironmentVariable($name, 'Process') }
try {
$env:NO_PROXY = 'localhost,127.0.0.1'
$env:VITE_API_BASE_URL = $apiUrl
$env:VITE_USE_MOCKS = 'false'
$env:PYTHONUNBUFFERED = '1'
$localOrigins = @("http://127.0.0.1:$PortaDashboard", "http://localhost:$PortaDashboard")
if ($env:CORS_ORIGINS) { $localOrigins += $env:CORS_ORIGINS.Split(',') }
$env:CORS_ORIGINS = ($localOrigins | Select-Object -Unique) -join ','
if ($Simular) {
    $env:ULTRON_SIMULATION = 'true'
    $dbFile = (Join-Path $localDir 'simulacao.db').Replace('\', '/')
    $env:DATABASE_URL = 'sqlite:///' + $dbFile
    $env:DEVICE_OFFLINE_TIMEOUT_SECONDS = '10'
    $env:EVENT_OFFLINE_TIMEOUT_SECONDS = '10'
    # A simulacao nao herda conta administrativa ou chave de uma instalacao real.
    $env:ADMIN_EMAIL = ''
    $env:ADMIN_PASSWORD = ''
    $env:DEVICE_API_KEY = ''
    $env:INGEST_API_KEY = ''
}

if ($Acao -in @('todos', 'backend')) {
    Start-LocalProcess 'backend' $python @('-m', 'uvicorn', 'main:app', '--app-dir', 'backend', '--host', '0.0.0.0', '--port', "$PortaApi")
    Wait-Http "$apiUrl/health"
}
if ($Acao -in @('todos', 'frontend')) {
    Start-LocalProcess 'dashboard' $node @($vite, '--host', '127.0.0.1', '--port', "$PortaDashboard", '--strictPort') -Directory (Join-Path $projectRoot 'frontend')
    Wait-Http "http://127.0.0.1:$PortaDashboard"
}
if ($Simular -and $Acao -in @('todos', 'backend')) {
    Write-Output 'TESTE LOCAL: SQLite separado e timeout de 10 s. Cadastre uma maquina e envie eventos por curl ou pipeline; nenhum coletor e iniciado.'
}
Write-Output "Dashboard: http://127.0.0.1:$PortaDashboard/dashboard"
Write-Output "API: $apiUrl/health"
Write-Output "Opta: use o IPv4 Wi-Fi deste notebook, porta $PortaApi; a API escuta em 0.0.0.0."
Write-Output 'Logs: .local. Para encerrar: .\iniciarLocal.ps1 -Acao parar'
} catch {
    foreach ($entry in @($script:entries | Where-Object { $_.id -notin $previousIds })) { Stop-OwnedProcess $entry }
    $script:entries = @($script:entries | Where-Object { $_.id -in $previousIds -and (Is-OwnedProcess $_) })
    Save-State
    throw
} finally {
    foreach ($name in $environmentNames) { [Environment]::SetEnvironmentVariable($name, $previousEnvironment[$name], 'Process') }
}
