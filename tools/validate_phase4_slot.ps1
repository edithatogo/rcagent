[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$SlotRoot,
    [Parameter(Mandatory=$true)][string]$ExpectedCondition,
    [Parameter(Mandatory=$true)][string]$ExpectedCase,
    [Parameter(Mandatory=$true)][string]$ExpectedRun
)

$ErrorActionPreference = 'Stop'
$slot = (Resolve-Path -LiteralPath $SlotRoot).Path
$failures = [System.Collections.Generic.List[string]]::new()

$required = @('raw-transcript.md','normalized-output.md','metadata.json','attestation.md','slot-receipt.json')
foreach ($name in $required) {
    $path = Join-Path $slot $name
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { $failures.Add("missing file: $name"); continue }
    if ((Get-Item -LiteralPath $path).Length -eq 0) { $failures.Add("empty file: $name") }
}

$metadataPath = Join-Path $slot 'metadata.json'
if (Test-Path -LiteralPath $metadataPath) {
    try { $metadata = Get-Content -LiteralPath $metadataPath -Raw | ConvertFrom-Json }
    catch { $failures.Add('metadata.json is invalid JSON'); $metadata = $null }
    if ($metadata) {
        foreach ($field in @('condition','case_id','run_id','model','harness','started_at','ended_at','operator')) {
            if (-not $metadata.PSObject.Properties.Name.Contains($field) -or [string]::IsNullOrWhiteSpace([string]$metadata.$field)) {
                $failures.Add("metadata missing: $field")
            }
        }
        if ($metadata.condition -ne $ExpectedCondition) { $failures.Add('condition does not match expected value') }
        if ($metadata.case_id -ne $ExpectedCase) { $failures.Add('case_id does not match expected value') }
        if ($metadata.run_id -ne $ExpectedRun) { $failures.Add('run_id does not match expected value') }
    }
}

$normalizedPath = Join-Path $slot 'normalized-output.md'
if (Test-Path -LiteralPath $normalizedPath) {
    $normalized = Get-Content -LiteralPath $normalizedPath -Raw
    $sections = [regex]::Matches($normalized, '(?m)^##\s+Section\s+[1-8]\s*:').Count
    if ($sections -ne 8) { $failures.Add("normalized output has $sections required sections; expected 8") }
}

$receiptPath = Join-Path $slot 'slot-receipt.json'
if (Test-Path -LiteralPath $receiptPath) {
    try { $receipt = Get-Content -LiteralPath $receiptPath -Raw | ConvertFrom-Json }
    catch { $failures.Add('slot-receipt.json is invalid JSON'); $receipt = $null }
    if ($receipt) {
        foreach ($name in @('raw-transcript.md','normalized-output.md','metadata.json','attestation.md')) {
            $entry = $receipt.files | Where-Object { $_.path -eq $name } | Select-Object -First 1
            if (-not $entry -or $entry.sha256 -notmatch '^[A-Fa-f0-9]{64}$') { $failures.Add("missing/invalid receipt hash: $name"); continue }
            if (Test-Path -LiteralPath (Join-Path $slot $name)) {
                $actual = (Get-FileHash -LiteralPath (Join-Path $slot $name) -Algorithm SHA256).Hash
                if ($actual -ne $entry.sha256.ToUpperInvariant()) { $failures.Add("hash mismatch: $name") }
            }
        }
    }
}

if ($failures.Count) {
    $failures | Sort-Object -Unique | ForEach-Object { Write-Output "QUARANTINE: $_" }
    exit 1
}
Write-Output "ADMIT: $ExpectedCondition/$ExpectedCase/$ExpectedRun"
