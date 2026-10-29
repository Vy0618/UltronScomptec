param(
    [switch]$HostOnly,
    [string]$CliPath,
    [string]$ZigPath
)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$outputDir = Join-Path $root '.build\firmware'
$jsonInclude = Join-Path $root '.tools\arduino-user\libraries\ArduinoJson\src'
if (-not $ZigPath) { $ZigPath = Join-Path $root '.tools\zig\zig-windows-x86_64-0.13.0\zig.exe' }
if (-not $CliPath) {
    $cliCommand = Get-Command arduino-cli -ErrorAction SilentlyContinue
    if ($cliCommand) { $CliPath = $cliCommand.Source }
    else { $CliPath = Join-Path $env:LOCALAPPDATA 'Programs\Arduino IDE\resources\app\lib\backend\resources\arduino-cli.exe' }
}

function Run-Checked {
    param([string]$Executable, [string[]]$Arguments, [string]$Log)
    & $Executable @Arguments 2>&1 | Tee-Object -FilePath $Log
    if ($LASTEXITCODE -ne 0) { throw "Falha ($LASTEXITCODE): $Executable. Consulte $Log" }
}

$oldGlobalCache = $env:ZIG_GLOBAL_CACHE_DIR
$oldLocalCache = $env:ZIG_LOCAL_CACHE_DIR
$mappedDrive = $null
Push-Location -LiteralPath $root
try {
    if (-not (Test-Path -LiteralPath $ZigPath)) { throw 'Zig 0.13.0 ausente. Consulte README.md, secao 10 (Firmware do Opta WiFi); este script nao instala dependencias.' }
    if (-not (Test-Path -LiteralPath (Join-Path $jsonInclude 'ArduinoJson.h'))) { throw 'ArduinoJson 7.4.2 ausente em .tools/arduino-user/libraries. Consulte README.md, secao 10 (Firmware do Opta WiFi).' }
    New-Item -ItemType Directory -Force -Path $outputDir | Out-Null
    $env:ZIG_GLOBAL_CACHE_DIR = Join-Path $root '.build\zig-global'
    $env:ZIG_LOCAL_CACHE_DIR = Join-Path $root '.build\zig-local'
    Run-Checked $ZigPath @('c++','-std=c++17','-Wall','-Wextra','-Werror','-Ifirmware/tests/host','firmware/tests/host/testControl.cpp','-o',"$outputDir\test_control.exe") "$outputDir\compile-control.log"
    Run-Checked "$outputDir\test_control.exe" @() "$outputDir\test-control.log"
    Run-Checked $ZigPath @('c++','-std=c++17','-Wall','-Wextra','-Werror',"-I$jsonInclude",'firmware/tests/host/testtelemetry.cpp','-o',"$outputDir\test_telemetry.exe") "$outputDir\compile-telemetry.log"
    Run-Checked "$outputDir\test_telemetry.exe" @("$outputDir\telemetry-fixtures.json", "$outputDir\usb-fixture.txt", "$outputDir\monitor-usb-fixture.txt") "$outputDir\test-telemetry.log"

    if (-not $HostOnly) {
        if (-not (Test-Path -LiteralPath $CliPath)) { throw 'Arduino CLI ausente. Instale Arduino IDE 2/CLI ou informe -CliPath.' }
        if (-not (Test-Path -LiteralPath '.tools\arduino-data\packages\arduino\hardware\mbed_opta\4.6.0')) { throw 'Core arduino:mbed_opta@4.6.0 ausente. Consulte README.md, secao 10 (Firmware do Opta WiFi).' }
        # GCC 7 uses unnormalized relative include paths and exceeds MAX_PATH in
        # long OneDrive workspaces. A temporary drive keeps the installed core intact.
        foreach ($letter in @('U','V','W','X','Y','Z')) {
            if (-not (Test-Path "$letter`:\") -and -not (Get-PSDrive -Name $letter -ErrorAction SilentlyContinue)) {
                & subst.exe "$letter`:" $root
                if ($LASTEXITCODE -ne 0) { throw 'Nao foi possivel criar o mapeamento temporario de compilacao.' }
                $mappedDrive = "$letter`:"
                break
            }
        }
        if (-not $mappedDrive) { throw 'Nenhuma letra U: a Z: disponivel para o caminho curto temporario do GCC.' }
        $shortConfig = "directories:`n  data: $mappedDrive/.tools/arduino-data`n  downloads: $mappedDrive/.tools/arduino-downloads`n  user: $mappedDrive/.tools/arduino-user`n"
        Set-Content -LiteralPath '.tools\arduino-cli-short.yaml' -Value $shortConfig -Encoding ascii
        Run-Checked $CliPath @('compile','--fqbn','arduino:mbed_opta:opta','--config-file',"$mappedDrive\.tools\arduino-cli-short.yaml",'--build-path',"$mappedDrive\.build\firmware\opta-short","$mappedDrive\firmware\optaCncMonitor") "$outputDir\compile-opta.log"
    }
    Write-Output 'Firmware: verificacoes concluidas. Nenhum upload ou acesso ao hardware foi executado.'
}
catch { [Console]::Error.WriteLine($_.Exception.Message); exit 1 }
finally {
    if ($mappedDrive) { & subst.exe $mappedDrive /D | Out-Null }
    $env:ZIG_GLOBAL_CACHE_DIR = $oldGlobalCache
    $env:ZIG_LOCAL_CACHE_DIR = $oldLocalCache
    Pop-Location
}
exit 0
