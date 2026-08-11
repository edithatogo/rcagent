[CmdletBinding()]
param([string]$AuditPath)

$ErrorActionPreference = 'Stop'
$scriptRoot = if ($PSScriptRoot) { $PSScriptRoot } else { Split-Path -Parent $MyInvocation.MyCommand.Path }
if (-not $AuditPath) { $AuditPath = Join-Path $scriptRoot '..\evaluation\analysis\phase4-manifest-audit-receipt.md' }
$audit = Get-Content -LiteralPath $AuditPath -Raw
$blockers=@()
if ($audit -match 'Slots eligible for blinding\s*\|\s*0\b') { $blockers += 'zero eligible slots' }
if ($audit -match 'manifest is \*\*not complete\*\*') { $blockers += 'manifest incomplete' }
if ($audit -match 'sealed blinding map must remain unpopulated') { $blockers += 'blinding map must remain sealed/unpopulated' }
if ($blockers.Count) {
    $blockers | ForEach-Object { Write-Output "BLOCKED: $_" }
    Write-Output 'Phase 4 admission has not passed; Track 5 and Track 6 remain locked.'
    exit 1
}
Write-Output 'PASS: Phase 4 admission preflight passed; Track 5 may be considered for start.'
