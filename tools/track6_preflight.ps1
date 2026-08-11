[CmdletBinding()]
param([string]$ClaimsBoundary)

$ErrorActionPreference = 'Stop'
$scriptRoot = if ($PSScriptRoot) { $PSScriptRoot } else { Split-Path -Parent $MyInvocation.MyCommand.Path }
if (-not $ClaimsBoundary) { $ClaimsBoundary = Join-Path $scriptRoot '..\evaluation\analysis\track6-claims-boundary.md' }
$failures = @()
if (-not (Test-Path -LiteralPath $ClaimsBoundary -PathType Leaf)) { $failures += 'Track 6 claims-boundary file is missing' }
else {
    $text = Get-Content -LiteralPath $ClaimsBoundary -Raw
    if ($text -match '(?i)blocked|pending|wait') { $failures += 'Track 5 closure is not evidenced; Track 6 remains gated' }
}
if ($failures.Count) {
    $failures | ForEach-Object { Write-Output "BLOCKED: $_" }
    Write-Output 'Track 6 must not unblind, calculate final statistics, publish visualisations, or make final claims.'
    exit 1
}
Write-Output 'PASS: Track 5 closure preflight permits Track 6 start'
