[CmdletBinding()]
param(
    [ValidateSet('validate', 'test')]
    [string]$Profile = 'validate',
    [string]$EnvironmentPath = '.venv'
)

$ErrorActionPreference = 'Stop'
$repositoryRoot = Split-Path -Parent $PSScriptRoot
$environmentFullPath = [System.IO.Path]::GetFullPath(
    (Join-Path $repositoryRoot $EnvironmentPath)
)

if (-not $environmentFullPath.StartsWith(
    [System.IO.Path]::GetFullPath($repositoryRoot),
    [System.StringComparison]::OrdinalIgnoreCase
)) {
    throw "Environment path must remain inside the repository."
}

$pythonCommand = Get-Command python -ErrorAction Stop
& $pythonCommand.Source -m venv $environmentFullPath

$venvPython = Join-Path $environmentFullPath 'Scripts\python.exe'
if (-not (Test-Path -LiteralPath $venvPython)) {
    throw "Virtual environment creation failed: $venvPython"
}

& $venvPython -m pip install --disable-pip-version-check --upgrade pip
& $venvPython -m pip install --disable-pip-version-check -e "$repositoryRoot[$Profile]"
& $venvPython -m tools.validate_repository --root $repositoryRoot

Write-Output "Installed and verified capability profile '$Profile'."
