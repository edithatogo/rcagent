[CmdletBinding()]
param([string]$OutputPath)

$ErrorActionPreference = 'Stop'
$scriptRoot = if ($PSScriptRoot) { $PSScriptRoot } else { Split-Path -Parent $MyInvocation.MyCommand.Path }
$repoRoot = (Resolve-Path (Join-Path $scriptRoot '..')).Path
if (-not $OutputPath) { $OutputPath = Join-Path $repoRoot 'evaluation\analysis\h0-h1-run-manifest.csv' }

$conditions = @(
    @{ id='H0'; root='evaluation\results\H0-control-no-skill' },
    @{ id='H1'; root='evaluation\results\H1-claude-code-sonnet' }
)
$rows = foreach ($condition in $conditions) {
    $root = (Resolve-Path (Join-Path $repoRoot $condition.root)).Path
    foreach ($file in Get-ChildItem -LiteralPath $root -Recurse -File -Filter 'raw-transcript.md') {
        $text = Get-Content -LiteralPath $file.FullName -Raw
        $fields = [ordered]@{
            condition_id = [bool]($text -match '(?im)^\s*(?:condition(?:\s+id)?)\s*[:|]')
            case_id = [bool]($text -match '(?im)^\s*(?:case(?:\s+id)?)\s*[:|]')
            run_number = [bool]($text -match '(?im)^\s*(?:run(?:\s+(?:id|number))?)\s*[:|]')
            model_id = [bool]($text -match '(?im)^\s*(?:model(?:\s+id)?)\s*[:|]')
            harness = [bool]($text -match '(?im)^\s*harness(?:\s+(?:name|version))?\s*[:|]')
            temperature = [bool]($text -match '(?im)^\s*temperature\s*[:|]')
            started_at = [bool]($text -match '(?im)^\s*(?:timestamp\s+start|start\s+time|started_at)\s*[:|]')
            ended_at = [bool]($text -match '(?im)^\s*(?:timestamp\s+end|end\s+time|ended_at)\s*[:|]')
            endpoint = [bool]($text -match '(?im)^\s*(?:api\s+endpoint|endpoint)\s*[:|]')
        }
        $errorMarker = [bool]($text -match '(?im)^\s*#{0,3}\s*(?:authentication\s+error|api\s+error|error)\b|\b(?:401|403)\s+(?:unauthorized|forbidden)\b|invalid\s+api\s+key|rate\s+limit\s+(?:error|exceeded)')
        $missing = @($fields.GetEnumerator() | Where-Object { -not $_.Value } | ForEach-Object { $_.Key })
        $status = if ($file.Length -eq 0) { 'empty' } elseif ($errorMarker) { 'error' } elseif ($missing.Count) { 'metadata-incomplete' } else { 'candidate-complete' }
        [pscustomobject]@{
            condition = $condition.id
            relative_path = $file.FullName.Substring($root.Length + 1)
            bytes = $file.Length
            status = $status
            error_marker = $errorMarker
            missing_fields = ($missing -join ';')
            admission_decision = 'not-admitted'
        }
    }
}
$rows | Sort-Object condition,relative_path | Export-Csv -LiteralPath $OutputPath -NoTypeInformation -Encoding utf8
$rows | Group-Object condition,status | Sort-Object Name | ForEach-Object { Write-Output "$($_.Name): $($_.Count)" }
Write-Output "MANIFEST=$OutputPath"
