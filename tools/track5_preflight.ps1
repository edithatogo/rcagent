[CmdletBinding()]
param(
    [Alias('ManifestAudit')][string]$Receipt,
    [string]$BlindingMap,
    [string]$ExpectedSha256,
    [string]$PythonExecutable = 'python'
)
$ErrorActionPreference = 'Stop'
# No fixture mode is exposed by a study-transition entry point.
$arguments = @((Join-Path $PSScriptRoot 'evaluation_preflight.py'), '--stage', 'scoring')
if ($Receipt) { $arguments += @('--receipt', $Receipt) }
if ($ExpectedSha256) { $arguments += @('--expected-sha256', $ExpectedSha256) }
& $PythonExecutable @arguments
# Live admission is disabled even if an interpreter shim returns success.
exit 1
