[CmdletBinding()]
param(
    [ValidateSet('Preflight', 'Install', 'Verify', 'Rollback', 'Uninstall')]
    [string]$Action = 'Preflight',
    [ValidateSet('validate')]
    [string]$Profile = 'validate',
    [string]$EnvironmentPath = '.venv',
    [switch]$AllowNetwork,
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
$repositoryRoot = [System.IO.Path]::GetFullPath((Split-Path -Parent $PSScriptRoot))
$environmentFullPath = [System.IO.Path]::GetFullPath((Join-Path $repositoryRoot $EnvironmentPath))
$repositoryBoundary = $repositoryRoot.TrimEnd(
    [System.IO.Path]::DirectorySeparatorChar,
    [System.IO.Path]::AltDirectorySeparatorChar
) + [System.IO.Path]::DirectorySeparatorChar
$markerName = '.safety-systems-capability.json'
$markerPath = Join-Path $environmentFullPath $markerName
$stateRoot = Join-Path $repositoryRoot '.capability-state'

if (-not $environmentFullPath.StartsWith($repositoryBoundary, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw 'Environment path must be a child of the repository.'
}

$registry = Get-Content -LiteralPath (Join-Path $repositoryRoot 'conductor\capability-profiles.json') -Raw | ConvertFrom-Json
$profileRecord = $registry.profiles | Where-Object { $_.id -eq $Profile }
if (-not $profileRecord -or $profileRecord.status -ne 'implemented') {
    throw "Capability profile '$Profile' is not implemented."
}

function Read-OwnershipMarker {
    if (-not (Test-Path -LiteralPath $markerPath -PathType Leaf)) { return $null }
    try { return Get-Content -LiteralPath $markerPath -Raw | ConvertFrom-Json }
    catch { throw 'Capability ownership marker is malformed.' }
}

function Test-OwnedTarget {
    param($Marker)
    if ($null -eq $Marker -or -not $Marker.installation_id) { return $false }
    $pairedPath = Join-Path (Join-Path $stateRoot 'ownership') "$($Marker.installation_id).json"
    if (-not (Test-Path -LiteralPath $pairedPath -PathType Leaf)) { return $false }
    try { $Paired = Get-Content -LiteralPath $pairedPath -Raw | ConvertFrom-Json }
    catch { return $false }
    return $Paired.installation_id -eq $Marker.installation_id -and
        $Paired.environment_path -eq $Marker.environment_path -and
        $Marker.schema_version -eq '1.0' -and
        $Marker.owner -eq 'safety-systems-workbench' -and
        $Marker.repository_root -eq $repositoryRoot -and
        $Marker.environment_path -eq $environmentFullPath -and
        $Marker.profile -eq $Profile
}

function Write-Receipt {
    param([string]$Result, [string]$TargetState, [bool]$NetworkUsed = $false)
    [ordered]@{
        schema_version = '1.0'
        action = $Action.ToLowerInvariant()
        result = $Result
        profile = $Profile
        environment_path = $environmentFullPath
        target_state = $TargetState
        network_authorized = [bool]$AllowNetwork
        network_used = $NetworkUsed
        telemetry = 'off'
    } | ConvertTo-Json -Compress
}

function Invoke-CheckedNative {
    param([string]$Command, [string[]]$Arguments)
    $nativeOutput = & $Command @Arguments 2>&1
    if ($LASTEXITCODE -ne 0) {
        $detail = ($nativeOutput | Select-Object -Last 1)
        throw "Native command failed with exit code ${LASTEXITCODE}: $Command ($detail)"
    }
}

$targetExists = Test-Path -LiteralPath $environmentFullPath -PathType Container
$marker = if ($targetExists) { Read-OwnershipMarker } else { $null }
$owned = $targetExists -and (Test-OwnedTarget $marker)
$targetState = if (-not $targetExists) { 'absent' } elseif ($owned) { 'owned' } else { 'unowned' }

if ($Action -eq 'Preflight') {
    $result = if ($targetState -eq 'unowned') { 'manual-review' } else { 'passed' }
    Write-Receipt $result $targetState
    if ($targetState -eq 'unowned') { exit 2 }
    return
}

if ($Action -eq 'Verify') {
    if (-not $owned) { Write-Receipt 'not-installed-or-unowned' $targetState; exit 2 }
    $venvPython = Join-Path $environmentFullPath 'Scripts\python.exe'
    if (-not (Test-Path -LiteralPath $venvPython -PathType Leaf)) {
        Write-Receipt 'invalid' $targetState
        exit 2
    }
    Invoke-CheckedNative $venvPython @('-c', "import importlib.metadata as m; assert m.version('safety-systems-workbench') == '0.0.0'; assert '$repositoryRoot'.lower() in (m.distribution('safety-systems-workbench').read_text('direct_url.json') or '').lower()")
    $currentRevision = (& git -C $repositoryRoot rev-parse HEAD).Trim()
    if ($LASTEXITCODE -ne 0 -or $marker.source_revision -ne $currentRevision) {
        Write-Receipt 'source-revision-mismatch' $targetState
        exit 2
    }
    Invoke-CheckedNative $venvPython @('-m', 'tools.validate_repository', '--root', $repositoryRoot)
    Write-Receipt 'verified' $targetState
    return
}

if ($Action -eq 'Rollback') {
    Write-Receipt 'rollback-unavailable-no-prior-state' $targetState
    exit 2
}

if ($Action -eq 'Uninstall') {
    if (-not $owned) { Write-Receipt 'refused-unowned' $targetState; exit 2 }
    Write-Receipt 'preview-only-removal-not-implemented' $targetState
    if (-not $DryRun) { exit 2 }
    return
}

if ($targetExists) { throw 'Refusing to modify an existing or unowned environment path.' }
if (-not $AllowNetwork) {
    throw 'Installation may access package indexes; rerun with -AllowNetwork after reviewing egress.'
}
$uvCommand = Get-Command uv -ErrorAction SilentlyContinue
$pythonCommand = Get-Command python -ErrorAction SilentlyContinue
if (-not $uvCommand -and -not $pythonCommand) { throw 'Neither uv nor Python is available.' }

if ($uvCommand) { Invoke-CheckedNative $uvCommand.Source @('venv', '--python', '3.13', $environmentFullPath) }
else { Invoke-CheckedNative $pythonCommand.Source @('-m', 'venv', $environmentFullPath) }

$venvPython = Join-Path $environmentFullPath 'Scripts\python.exe'
if (-not (Test-Path -LiteralPath $venvPython)) { throw "Virtual environment creation failed: $venvPython" }
if ($uvCommand) { Invoke-CheckedNative $uvCommand.Source @('pip', 'install', '--python', $venvPython, '-e', "$repositoryRoot[$Profile]") }
else { Invoke-CheckedNative $venvPython @('-m', 'pip', 'install', '--disable-pip-version-check', '-e', "$repositoryRoot[$Profile]") }
Invoke-CheckedNative $venvPython @('-m', 'tools.validate_repository', '--root', $repositoryRoot)

$installationId = [guid]::NewGuid().ToString('D')
$sourceRevision = (& git -C $repositoryRoot rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0) { throw 'Unable to resolve repository revision.' }
$ownership = [ordered]@{
    schema_version = '1.0'
    owner = 'safety-systems-workbench'
    installation_id = $installationId
    source_revision = $sourceRevision
    repository_root = $repositoryRoot
    environment_path = $environmentFullPath
    profile = $Profile
}
$ownership | ConvertTo-Json | Set-Content -LiteralPath $markerPath -Encoding utf8
$ownershipDirectory = Join-Path $stateRoot 'ownership'
New-Item -ItemType Directory -Path $ownershipDirectory -Force | Out-Null
$ownership | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $ownershipDirectory "$installationId.json") -Encoding utf8
Write-Receipt 'installed-and-verified' 'owned' $true
