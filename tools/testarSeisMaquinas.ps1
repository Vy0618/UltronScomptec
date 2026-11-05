param(
    [ValidateNotNullOrEmpty()]
    [string]$Api = 'http://127.0.0.1:8000/api',
    [ValidateRange(0, 10000)]
    [int]$Rodadas = 30,
    [ValidateRange(0, 3600)]
    [int]$IntervaloSegundos = 2,
    [string]$Chave = $(if ($env:INGEST_API_KEY) { $env:INGEST_API_KEY } else { $env:DEVICE_API_KEY })
)

$ErrorActionPreference = 'Stop'
$apiBase = $Api.Trim().TrimEnd('/')
$headers = @{}
if (-not [string]::IsNullOrEmpty($Chave)) { $headers['X-API-Key'] = $Chave }

function Invoke-TestApi([string]$Method, [string]$Path, [hashtable]$Body) {
    $request = @{
        Uri = $apiBase + $Path
        Method = $Method
        Headers = $headers
        TimeoutSec = 10
        ErrorAction = 'Stop'
    }
    if ($PSBoundParameters.ContainsKey('Body')) {
        $request.ContentType = 'application/json; charset=utf-8'
        $request.Body = [System.Text.Encoding]::UTF8.GetBytes(($Body | ConvertTo-Json -Depth 8 -Compress))
    }
    try {
        Invoke-RestMethod @request
    } catch {
        $statusCode = $null
        if ($_.Exception.Response) { $statusCode = [int]$_.Exception.Response.StatusCode }
        if ($statusCode -eq 401) {
            throw 'A API recusou a chave (HTTP 401). Informe -Chave com a INGEST_API_KEY ou DEVICE_API_KEY configurada no backend.'
        }
        if ($statusCode) { throw "A chamada $Method $Path falhou (HTTP $statusCode). Confira a API e os dados enviados." }
        throw 'Nao foi possivel acessar a API. Confira o endereco -Api e se o backend esta em execucao.'
    }
}

function New-TestStates([string[]]$ActiveSignals) {
    $states = [ordered]@{
        ativo = $false
        inativo = $false
        emergencia = $false
        motor_ligado = $false
        porta_aberta = $false
        alarme = $false
    }
    foreach ($signal in $ActiveSignals) { $states[$signal] = $true }
    return $states
}

$existing = Invoke-TestApi 'Get' '/cncs'
$existing = @($existing)
$machines = @()
$created = 0
foreach ($number in 1..6) {
    $name = 'CNC teste {0:00}' -f $number
    $machine = $existing | Where-Object { $_.name -ceq $name } | Select-Object -First 1
    if ($null -eq $machine) {
        $machine = Invoke-TestApi 'Post' '/cncs' @{
            name = $name
            description = 'Maquina de teste da frota; eventos simulados por tools/testarSeisMaquinas.ps1.'
        }
        $existing += $machine
        $created++
    }
    $machines += $machine
}
Write-Output ('Maquinas de teste: 6; novas: {0}; reutilizadas: {1}.' -f $created, (6 - $created))
$machines | Format-Table code, name -AutoSize

$scenarios = @(
    (New-TestStates @('ativo', 'motor_ligado'))
    (New-TestStates @('inativo'))
    (New-TestStates @('emergencia'))
    (New-TestStates @('alarme'))
    (New-TestStates @('ativo', 'motor_ligado', 'porta_aberta'))
    (New-TestStates @('emergencia', 'porta_aberta'))
)
$sent = 0
for ($round = 1; $round -le $Rodadas; $round++) {
    for ($index = 0; $index -lt $machines.Count; $index++) {
        $scenario = $scenarios[($index + $round - 1) % $scenarios.Count]
        Invoke-TestApi 'Post' '/events' @{
            machine_id = $machines[$index].id
            states = $scenario
            event_id = [Guid]::NewGuid().ToString()
            extra_signals = @{ source = 'simulated'; scenario = 'teste-frota' }
        } | Out-Null
        $sent++
    }
    Write-Output ('Rodada {0}/{1}: 6 eventos enviados.' -f $round, $Rodadas)
    if ($round -lt $Rodadas -and $IntervaloSegundos -gt 0) { Start-Sleep -Seconds $IntervaloSegundos }
}
Write-Output ('Eventos enviados nesta execucao: {0}.' -f $sent)

$historySummary = foreach ($machine in $machines) {
    $machineId = [Uri]::EscapeDataString([string]$machine.id)
    $history = Invoke-TestApi 'Get' ("/cncs/$machineId/history?limit=1")
    [pscustomobject]@{ code = $machine.code; name = $machine.name; total = $history.total }
}
Write-Output 'Historico por maquina (inclui eventos de execucoes anteriores):'
$historySummary | Format-Table code, name, total -AutoSize
