#!/usr/bin/env python3
"""
Teste simples da API Smart Print
"""

import requests
import time

def test_api():
    # Aguardar um pouco para garantir que a API esteja pronta
    time.sleep(2)

    try:
        # Testar a rota root primeiro
        response = requests.get('http://127.0.0.1:5000/', timeout=5)
        print(f"Root endpoint: {response.status_code}")

        # Testar smart-print
        test_url = "https://ge.globo.com/futebol/times/flamengo/noticia/2024/01/20/flamengo-testa-time-misto-contra-o-volta-redonda.ghtml"

        print(f"Testando URL: {test_url}")
        response = requests.post(
            'http://127.0.0.1:5000/api/smart-print',
            json={'url': test_url},
            timeout=60
        )

        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print("✅ Sucesso!")
            print(f"Message: {data.get('message', 'N/A')}")
            if 'data' in data:
                print(f"Content Type: {data['data'].get('content_type', 'N/A')}")
                print(f"Confidence: {data['data'].get('confidence', 'N/A')}")
        else:
            print(f"❌ Erro: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Erro de conexão: {e}")

if __name__ == "__main__":
    test_api()