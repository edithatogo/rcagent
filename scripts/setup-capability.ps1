[CmdletBinding()]
param(
    [ValidateSet('Preflight', 'Install')]
    [string]$Action = 'Preflight',
    [ValidateSet('validate')]
    [string]$Profile = 'validate',
    [string]$EnvironmentPath = '.venv',
    [switch]$AllowNetwork
)

$ErrorActionPreference = 'Stop'
$repositoryRoot = [System.IO.Path]::GetFullPath((Split-Path -Parent $PSScriptRoot))
$environmentFullPath = [System.IO.Path]::GetFullPath(
    (Join-Path $repositoryRoot $EnvironmentPath)
)
$repositoryBoundary = $repositoryRoot.TrimEnd(
    [System.IO.Path]::DirectorySeparatorChar,
    [System.IO.Path]::AltDirectorySeparatorChar
) + [System.IO.Path]::DirectorySeparatorChar

if (-not $environmentFullPath.StartsWith(
    $repositoryBoundary,
    [System.StringComparison]::OrdinalIgnoreCase
)) {
    throw 'Environment path must be a child of the repository.'
}
if (Test-Path -LiteralPath $environmentFullPath) {
    throw 'Refusing to modify an existing or unowned environment path.'
}

$registryPath = Join-Path $repositoryRoot 'conductor\capability-profiles.json'
$registry = Get-Content -LiteralPath $registryPath -Raw | ConvertFrom-Json
$profileRecord = $registry.profiles | Where-Object { $_.id -eq $Profile }
if (-not $profileRecord -or $profileRecord.status -ne 'implemented') {
    throw "Capability profile '$Profile' is not implemented."
}

$uvCommand = Get-Command uv -ErrorAction SilentlyContinue
$pythonCommand = Get-Command python -ErrorAction SilentlyContinue
$preflight = [ordered]@{
    schema_version = '1.0'
    action = $Action.ToLowerInvariant()
    profile = $Profile
    target = $environmentFullPath
    target_state = 'absent'
    uv_available = [bool]$uvCommand
    python_available = [bool]$pythonCommand
    network_authorized = [bool]$AllowNetwork
    telemetry = 'off'
    result = 'passed'
}

if ($Action -eq 'Preflight') {
    $preflight | ConvertTo-Json -Compress
    return
}
if (-not $AllowNetwork) {
    throw 'Installation may access package indexes; rerun with -AllowNetwork after reviewing egress.'
}
if (-not $uvCommand -and -not $pythonCommand) {
    throw 'Neither uv nor Python is available.'
}

function Invoke-CheckedNative {
    param([string]$Command, [string[]]$Arguments)
    & $Command @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Native command failed with exit code ${LASTEXITCODE}: $Command"
    }
}

if ($uvCommand) {
    Invoke-CheckedNative $uvCommand.Source @('venv', '--python', '3.13', $environmentFullPath)
} else {
    Invoke-CheckedNative $pythonCommand.Source @('-m', 'venv', $environmentFullPath)
}

$venvPython = Join-Path $environmentFullPath 'Scripts\python.exe'
if (-not (Test-Path -LiteralPath $venvPython)) {
    throw "Virtual environment creation failed: $venvPython"
}
if ($uvCommand) {
    Invoke-CheckedNative $uvCommand.Source @('pip', 'install', '--python', $venvPython, '-e', "$repositoryRoot[$Profile]")
} else {
    Invoke-CheckedNative $venvPython @('-m', 'pip', 'install', '--disable-pip-version-check', '-e', "$repositoryRoot[$Profile]")
}
Invoke-CheckedNative $venvPython @('-m', 'tools.validate_repository', '--root', $repositoryRoot)

$preflight.result = 'installed-and-verified'
$preflight | ConvertTo-Json -Compress
