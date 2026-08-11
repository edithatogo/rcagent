[CmdletBinding()]
param([string]$OutputPath)

$ErrorActionPreference='Stop'
$scriptRoot=if($PSScriptRoot){$PSScriptRoot}else{Split-Path -Parent $MyInvocation.MyCommand.Path}
$repo=(Resolve-Path (Join-Path $scriptRoot '..')).Path
if(-not $OutputPath){$OutputPath=Join-Path $repo 'evaluation\analysis\h0-quality-audit.csv'}
$root=(Resolve-Path (Join-Path $repo 'evaluation\results\H0-control-no-skill')).Path
$rows=foreach($f in Get-ChildItem $root -Recurse -File -Filter 'normalized-output.md'){
    $t=Get-Content $f.FullName -Raw
    $sections=[regex]::Matches($t,'(?m)^##\s+Section\s+[1-8]\s*:').Count
    $raw=Join-Path $f.DirectoryName 'raw-transcript.md'
    [pscustomobject]@{
        relative_path=$f.FullName.Substring($root.Length+1)
        raw_present=Test-Path $raw
        bytes=$f.Length
        section_count=$sections
        status=if($sections -eq 8 -and $f.Length -gt 0){'normalized-complete'}else{'normalized-incomplete'}
        admission_decision='not-admitted'
    }
}
$rows | Sort-Object relative_path | Export-Csv -LiteralPath $OutputPath -NoTypeInformation -Encoding utf8
$rows | Group-Object status | ForEach-Object {Write-Output "$($_.Name): $($_.Count)"}
Write-Output "AUDIT=$OutputPath"
