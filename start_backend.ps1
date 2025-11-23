$job = Start-Job -ScriptBlock { cd C:\TradeComigo; uvicorn api_server:app --host 127.0.0.1 --port 8000 }
Write-Host "Backend iniciado em background. Use Stop-Job para parar."