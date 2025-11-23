#!/usr/bin/env python3
"""
Script de teste para a rota /api/smart-print
"""

import requests
import json

def test_smart_print():
    """Testa a rota /api/smart-print"""

    # URL de teste - notícia sobre Flamengo
    test_url = "https://ge.globo.com/futebol/times/flamengo/noticia/2024/01/20/flamengo-testa-time-misto-contra-o-volta-redonda.ghtml"

    # Fazer requisição
    try:
        response = requests.post(
            'http://127.0.0.1:5000/api/smart-print',
            json={'url': test_url},
            timeout=60
        )

        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")

if __name__ == "__main__":
    test_smart_print()