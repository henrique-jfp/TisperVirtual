@echo off
echo Iniciando TradeComigo - Frontend + Backend
echo.

echo [1/2] Iniciando backend da API...
start "Chat API Backend" cmd /k "cd /d C:\TradeComigo && .\venv\Scripts\python.exe chat_api.py"

timeout /t 3 /nobreak > nul

echo [2/2] Iniciando frontend Next.js...
cd frontend_next
npm run dev

pause