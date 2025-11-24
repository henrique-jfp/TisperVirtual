#!pwsh
<#
start_all.ps1
Inicia backend e frontend em janelas separadas do PowerShell.

Comportamento:
- Se existir `.venv\Scripts\Activate.ps1` no root, ativa o virtualenv antes de rodar o backend.
- Backend: executa `python -u run_coleta.py` no diretório do projeto.
- Frontend: se existir `frontend_next/package.json`, executa `npm run dev` dentro de `frontend_next`.

Uso:
Abra um PowerShell na raiz do repositório e execute:
    .\start_all.ps1

Observações:
- Adapte os comandos `python` / `npm run dev` conforme seu fluxo (uvicorn/flask/next etc.).
#>

$root = Split-Path -Parent $MyInvocation.MyCommand.Path

# Backend command (ativa .venv se existir)
$venvActivate = Join-Path $root ".venv\Scripts\Activate.ps1"
if (Test-Path $venvActivate) {
    $backendCmd = "& '$venvActivate'; cd '$root'; python -u run_coleta.py"
} else {
    $backendCmd = "cd '$root'; python -u run_coleta.py"
}

# Frontend command (se existir frontend_next with package.json)
$frontendDir = Join-Path $root 'frontend_next'
if (Test-Path (Join-Path $frontendDir 'package.json')) {
    $frontendCmd = "cd '$frontendDir'; npm run dev"
} else {
    $frontendCmd = "Write-Host 'frontend_next/package.json não encontrado. Pulei o start do front.'; Start-Sleep -Seconds 10"
}

Write-Host "Iniciando backend..."
Start-Process -FilePath pwsh -ArgumentList @('-NoExit','-Command',$backendCmd)

Write-Host "Iniciando frontend..."
Start-Process -FilePath pwsh -ArgumentList @('-NoExit','-Command',$frontendCmd)

Write-Host "Comandos enviados. Verifique as janelas do PowerShell abertas para logs."
