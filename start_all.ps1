<#
.SYNOPSIS
Starts backend (uvicorn), frontend (Next.js) and optionally LM Studio for IA.

USAGE
  .\start_all.ps1        # starts backend and frontend
  .\start_all.ps1 -Frontend -Backend  # start subset
#>

param(
    [switch]$Backend,
    [switch]$Frontend,
    [switch]$All = $true
)

# Resolve script root (project root)
$root = $PSScriptRoot

if ($All -or $Backend) {
    $cmd = "Set-Location -LiteralPath '$root'; & '.\\.venv\\Scripts\\Activate.ps1'; python backend_server.py"
    Start-Process -FilePath pwsh -ArgumentList '-NoExit','-Command',$cmd -WindowStyle Normal
}

if ($All -or $Frontend) {
    $frontendPath = Join-Path $root 'frontend_next'
    $cmd = "Set-Location -LiteralPath '$frontendPath'; npm run dev"
    Start-Process -FilePath pwsh -ArgumentList '-NoExit','-Command',$cmd -WindowStyle Normal
}

# Open helpful browser tabs (best-effort)
try {
    # Start-Process 'http://localhost:3000/' -ErrorAction SilentlyContinue
    # Start-Process 'http://127.0.0.1:8000/docs' -ErrorAction SilentlyContinue
} catch {
    Write-Host 'Could not open browser tabs automatically.'
}

Write-Host 'Started requested services (check new PowerShell windows).' -ForegroundColor Green
