#!/usr/bin/env python3
"""
Teste simples das melhorias com URL real
"""

import asyncio
import requests

async def test_url_real():
    """Testa com uma URL que sabemos que existe"""

    print("🧪 TESTANDO COM URL REAL")
    print("=" * 50)

    # URL de teste real (página do GitHub que sabemos que existe)
    test_url = "https://github.com/microsoft/vscode/blob/main/README.md"

    print(f"Testando URL: {test_url}")

    try:
        # Iniciar API Flask em background
        import subprocess
        import time

        print("🚀 Iniciando API Flask...")
        api_process = subprocess.Popen(['python', 'flask_api.py'], cwd='C:\\TradeComigo')

        # Aguardar API iniciar
        time.sleep(3)

        # Fazer requisição
        response = requests.post(
            'http://127.0.0.1:5000/api/smart-print',
            json={'url': test_url},
            timeout=60
        )

        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print("✅ Sucesso!")

            if 'data' in data:
                result = data['data']
                print(f"Content Type: {result.get('content_type')}")
                print(f"Title: {result.get('title', 'N/A')}")
                print(f"Confidence: {result.get('confidence', 'N/A')}")

                # Verificar link_info
                link_info = result.get('link_info', {})
                if link_info:
                    print(f"Link Info: {link_info}")

                # Verificar insert_result
                insert_result = data.get('insert_result')
                if insert_result:
                    print(f"Insert Status: {insert_result.get('status')}")

        else:
            print(f"❌ Erro: {response.text}")

    except Exception as e:
        print(f"❌ Erro: {e}")

    finally:
        # Parar API
        try:
            api_process.terminate()
            api_process.wait()
        except:
            pass

if __name__ == "__main__":
    asyncio.run(test_url_real())