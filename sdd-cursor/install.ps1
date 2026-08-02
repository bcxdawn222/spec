# SDD for Cursor installer: copy .cursor/, AGENTS.md, scripts/, templates/, references/ into target project
param(
    [string]$Target = ""
)

$ErrorActionPreference = "Stop"
$src = $PSScriptRoot

if (-not $Target) {
    $Target = (Get-Location).Path
}

if (-not (Test-Path "$src\.cursor")) {
    Write-Error "Cannot find $src\.cursor - run this script from the sdd-cursor directory"
}

$targets = @(".cursor", "AGENTS.md", "scripts", "templates", "references")
foreach ($t in $targets) {
    $from = Join-Path $src $t
    $to = Join-Path $Target $t
    if (Test-Path $from) {
        Copy-Item $from $to -Recurse -Force
        Write-Host "[OK] $t -> $to"
    }
}

Write-Host ""
Write-Host "Installed to: $Target"
Write-Host "Restart Cursor, then type /spec in the project to see the commands."
Write-Host "Smoke test: python scripts/sdd.py status"