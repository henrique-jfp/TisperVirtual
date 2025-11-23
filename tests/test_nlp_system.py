#!/usr/bin/env python3
"""
Teste do sistema de processamento de linguagem natural para o tipster AI
"""

import requests
import json

def testar_nlp():
    """Testa diferentes tipos de perguntas no sistema NLP"""

    base_url = "http://127.0.0.1:8080/api/chat"

    # Testes de perguntas
    perguntas_teste = [
        "Quais jogos acontecem hoje?",
        "Quais são os próximos jogos do Flamengo?",
        "Como está o Palmeiras nas estatísticas?",
        "Qual a melhor aposta de hoje?",
        "Qual o histórico de Palmeiras x Corinthians?",
        "Como está o Gabigol jogando?",
        "Qual a classificação do campeonato?",
        "Qual a odd para vitória do Palmeiras contra o Corinthians?",
        "Conte-me sobre o jogo de hoje",
        "O que você recomenda para apostar hoje?"
    ]

    print("🧪 Testando sistema de processamento de linguagem natural...\n")

    for pergunta in perguntas_teste:
        try:
            response = requests.post(base_url, json={'prompt': pergunta}, timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"❓ Pergunta: {pergunta}")
                print(f"🤖 Resposta: {data.get('reply', 'Sem resposta')[:200]}...")
                print("-" * 80)
            else:
                print(f"❌ Erro na pergunta '{pergunta}': Status {response.status_code}")
        except Exception as e:
            print(f"❌ Erro na pergunta '{pergunta}': {str(e)}")

        print()

if __name__ == "__main__":
    testar_nlp()