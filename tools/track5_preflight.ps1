[CmdletBinding()]
param(
    [string]$ManifestAudit,
    [string]$BlindingMap
)

$ErrorActionPreference = 'Stop'
$scriptRoot = if ($PSScriptRoot) { $PSScriptRoot } else { Split-Path -Parent $MyInvocation.MyCommand.Path }
if (-not $ManifestAudit) { $ManifestAudit = Join-Path $scriptRoot '..\evaluation\analysis\phase4-manifest-audit-receipt.md' }
if (-not $BlindingMap) { $BlindingMap = Join-Path $scriptRoot '..\evaluation\results\blinding-map.csv' }
$failures = @()

$audit = Get-Content -LiteralPath $ManifestAudit -Raw
if ($audit -match 'Slots eligible for blinding\s*\|\s*0\b') { $failures += 'Phase 4 reports zero eligible slots' }
if ($audit -match 'manifest is \*\*not complete\*\*') { $failures += 'Phase 4 manifest is incomplete' }

if (Test-Path -LiteralPath $BlindingMap) {
    $rows = Import-Csv -LiteralPath $BlindingMap
    if (@($rows).Count -eq 0) { $failures += 'Blinding map contains no admitted rows' }
} else { $failures += 'Blinding map is missing' }

if ($failures.Count) {
    $failures | ForEach-Object { Write-Output "BLOCKED: $_" }
    Write-Output 'Track 5 must not create blinding IDs, score rows, calculate IRR, or unblind.'
    exit 1
}
Write-Output 'PASS: Phase 4 admission preflight permits Track 5 start'
