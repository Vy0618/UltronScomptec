param(
    [switch]$Firmware
)

$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$frontendRoot = Join-Path $projectRoot 'frontend'
$logsRoot = Join-Path $projectRoot '.local\testes'
$runId = Get-Date -Format 'yyyyMMdd-HHmmss-fff'
$runDir = Join-Path $logsRoot $runId
New-Item -ItemType Directory -Force -Path $runDir | Out-Null
$results = [System.Collections.Generic.List[object]]::new()

function Find-Node {
    $command = Get-Command node.exe -ErrorAction SilentlyContinue
    if ($command) { return $command.Source }
    $bundled = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe'
    if (Test-Path -LiteralPath $bundled) { return $bundled }
    return $null
}

function Find-Npm([string]$Node) {
    if (-not $Node) { return $null }
    $command = Get-Command npm.cmd -ErrorAction SilentlyContinue
    if ($command) {
        $globalCli = Join-Path (Split-Path -Parent $command.Source) 'node_modules\npm\bin\npm-cli.js'
        if (Test-Path -LiteralPath $globalCli) { return @{ executable = $Node; prefix = @($globalCli) } }
        return @{ executable = $command.Source; prefix = @() }
    }
    $localCli = Join-Path $projectRoot '.tools\npm\package\bin\npm-cli.js'
    if (Test-Path -LiteralPath $localCli) { return @{ executable = $Node; prefix = @($localCli) } }
    return $null
}

function Invoke-Check([string]$Name, [string]$Executable, [string[]]$Arguments, [string]$WorkingDirectory, [string]$Unavailable) {
    $logPath = Join-Path $runDir ($Name + '.log')
    $timer = [System.Diagnostics.Stopwatch]::StartNew()
    $exitCode = 127
    Write-Output ("`nExecutando: " + $Name)
    if (-not $Executable -or -not (Test-Path -LiteralPath $Executable)) {
        $message = if ($Unavailable) { $Unavailable } else { 'Executavel nao encontrado.' }
        $message | Tee-Object -FilePath $logPath
    } else {
        Push-Location -LiteralPath $WorkingDirectory
        try {
            # Native stderr and nonzero exit codes are recorded, then the next check runs.
            $ErrorActionPreference = 'Continue'
            $PSNativeCommandUseErrorActionPreference = $false
            & $Executable @Arguments 2>&1 | Tee-Object -FilePath $logPath
            $exitCode = $LASTEXITCODE
            if ($null -eq $exitCode) { $exitCode = 1 }
        } catch {
            $_ | Out-String | Tee-Object -FilePath $logPath -Append
            $exitCode = 1
        } finally {
            Pop-Location
        }
    }
    $timer.Stop()
    $result = [pscustomobject]@{
        nome = $Name
        resultado = if ($exitCode -eq 0) { 'APROVADO' } else { 'FALHOU' }
        codigo = $exitCode
        segundos = [Math]::Round($timer.Elapsed.TotalSeconds, 2)
        log = $logPath
    }
    $script:results.Add($result)
    Write-Output ($result.resultado + ': ' + $Name + ' (codigo ' + $exitCode + ')')
}

$python = Join-Path $projectRoot '.venv\Scripts\python.exe'
$node = Find-Node
$npm = Find-Npm $node
$envNames = @('DATABASE_URL', 'ADMIN_EMAIL', 'ADMIN_PASSWORD', 'DEVICE_API_KEY', 'PYTHONDONTWRITEBYTECODE', 'VITE_USE_MOCKS', 'ULTRON_SIMULATION')
$previousEnvironment = @{}
foreach ($name in $envNames) { $previousEnvironment[$name] = [Environment]::GetEnvironmentVariable($name, 'Process') }

try {
    # Tests use in-memory SQLite and never inherit a configured production database.
    $env:DATABASE_URL = 'sqlite://'
    $env:ULTRON_SIMULATION = 'true'
    $env:ADMIN_EMAIL = ''
    $env:ADMIN_PASSWORD = ''
    $env:DEVICE_API_KEY = ''
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:VITE_USE_MOCKS = 'false'
    if ($Firmware) {
        # Host tests generate the C++ telemetry fixture consumed by the API suite.
        $firmwareScript = Join-Path $projectRoot 'firmware\testarFirmware.ps1'
        $shell = if (Test-Path -LiteralPath (Join-Path $PSHOME 'pwsh.exe')) { Join-Path $PSHOME 'pwsh.exe' } else { Join-Path $PSHOME 'powershell.exe' }
        if (Test-Path -LiteralPath $firmwareScript) {
            Invoke-Check 'firmware' $shell @('-NoProfile', '-NonInteractive', '-ExecutionPolicy', 'Bypass', '-File', $firmwareScript) $projectRoot ''
        } else {
            Invoke-Check 'firmware' $null @() $projectRoot 'firmware/testarFirmware.ps1 nao foi encontrado; os testes de firmware nao foram executados.'
        }
    }
    Invoke-Check 'python' $python @('-B', '-u', '-m', 'pytest', '-q', '-p', 'no:cacheprovider', '--basetemp', (Join-Path $runDir 'pytest-temp'), 'backend/tests', 'tools/tests') $projectRoot 'Crie .venv e instale requirements.txt da raiz antes de testar.'
    foreach ($task in @('test', 'lint', 'build')) {
        $executable = if ($npm) { $npm.executable } else { $null }
        $arguments = if ($npm) { @($npm.prefix) + @('run', $task) } else { @() }
        Invoke-Check ('frontend-' + $task) $executable $arguments $frontendRoot 'Instale Node.js e disponibilize npm global ou .tools/npm/package/bin/npm-cli.js. Este script nao instala dependencias.'
    }
} finally {
    foreach ($name in $envNames) { [Environment]::SetEnvironmentVariable($name, $previousEnvironment[$name], 'Process') }
}

$failed = @($results | Where-Object { $_.codigo -ne 0 })
$summary = [pscustomobject]@{
    execucao = $runId
    projeto = $projectRoot
    firmwareSolicitado = [bool]$Firmware
    aprovado = $failed.Count -eq 0
    verificacoes = @($results.ToArray())
}
$summary | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $runDir 'resumo.json') -Encoding UTF8
$summary | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $logsRoot 'ultimo-resumo.json') -Encoding UTF8
$results | Format-Table nome, resultado, codigo, segundos -AutoSize | Out-String |
    Tee-Object -FilePath (Join-Path $runDir 'resumo.txt')
Write-Output ('Logs e resumo: ' + $runDir)
if ($failed.Count) { exit 1 }
exit 0
