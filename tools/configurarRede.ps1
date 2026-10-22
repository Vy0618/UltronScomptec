param(
    [string]$BackendHost,
    [string]$DeviceKey = ''
)

$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
if (-not $BackendHost) {
    $candidates = @(Get-NetIPConfiguration | Where-Object {
        $_.NetAdapter.Status -eq 'Up' -and $_.IPv4DefaultGateway -and
        ($_.InterfaceAlias -match 'Wi-Fi|WiFi|Wireless|Sem Fio' -or $_.InterfaceDescription -match 'Wireless|Wi-Fi|802.11')
    })
    if ($candidates.Count -ne 1) {
        throw 'Nao foi possivel escolher o Wi-Fi. Consulte ipconfig e informe -BackendHost IPv4_DO_NOTEBOOK.'
    }
    $BackendHost = $candidates[0].IPv4Address.IPAddress
}
$address = $null
if (-not [System.Net.IPAddress]::TryParse($BackendHost, [ref]$address) -or
    $address.AddressFamily -ne [System.Net.Sockets.AddressFamily]::InterNetwork -or
    [System.Net.IPAddress]::IsLoopback($address) -or $BackendHost -eq '0.0.0.0' -or
    $BackendHost.StartsWith('169.254.')) {
    throw 'Informe um IPv4 valido do notebook no hotspot; nao use localhost, 0.0.0.0 ou o gateway do celular.'
}
if ($DeviceKey -match '[^\x20-\x7E]' -or $DeviceKey.Contains('"') -or $DeviceKey.Contains('\')) {
    throw 'A chave deve usar ASCII imprimivel sem aspas ou barra invertida.'
}
$header = Join-Path $projectRoot 'firmware\optaMesaMonitor\optaSecrets.h'
@"
#pragma once
// Gerado localmente. Notebook e Opta devem estar no hotspot maker.
#define ULTRON_WIFI_SSID "maker"
#define ULTRON_WIFI_PASSWORD "12345678"
#define ULTRON_BACKEND_HOST "$BackendHost"
#define ULTRON_DEVICE_API_KEY "$DeviceKey"
"@ | Set-Content -LiteralPath $header -Encoding ASCII
Write-Output "Configuracao criada para API em http://${BackendHost}:8000/api."
Write-Output 'A rede nao foi alterada. Confira que notebook e Opta estao conectados a maker.'
Write-Output 'Recompile e grave o firmware depois de mudar o IPv4. O arquivo local nao entra no ZIP.'
