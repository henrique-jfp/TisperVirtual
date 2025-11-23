#!/usr/bin/env python3
"""
Teste direto do sistema de processamento de linguagem natural
"""

from football_nlp_processor import FootballQueryProcessor
from football_tipster_ai import FootballTipsterAI

def testar_nlp_direto():
    """Testa o processamento NLP diretamente"""

    # Inicializar processadores
    nlp_processor = FootballQueryProcessor()
    tipster_ai = FootballTipsterAI()

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

    print("🧪 Testando sistema de processamento de linguagem natural (direto)...\n")

    for pergunta in perguntas_teste:
        try:
            print(f"❓ Pergunta: {pergunta}")

            # Classificar a query
            classification = nlp_processor.classify_query(pergunta)
            print(f"   📋 Classificação: {classification['type']} (confiança: {classification['confidence']})")
            if classification['entities']:
                print(f"   🏷️  Entidades: {classification['entities']}")

            # Simular dados de resposta (dados mock)
            mock_data = None
            if classification['type'] == 'jogos_hoje':
                mock_data = {'jogos': [
                    {'hora': '16:00', 'casa': 'Flamengo', 'fora': 'Palmeiras', 'estadio': 'Maracanã'},
                    {'hora': '18:30', 'casa': 'Corinthians', 'fora': 'São Paulo', 'estadio': 'Neo Química'}
                ]}
            elif classification['type'] == 'classificacao':
                mock_data = {'classificacao': [
                    {'nome': 'Palmeiras', 'pontos': 45},
                    {'nome': 'Flamengo', 'pontos': 42},
                    {'nome': 'Botafogo', 'pontos': 38}
                ]}
            elif classification['type'] == 'melhor_aposta':
                mock_data = {'recomendacoes': [
                    {'jogo': 'Flamengo x Palmeiras', 'tipo': 'Ambos Marcam', 'odd': 1.85, 'confianca': 'Alta'}
                ]}

            # Gerar resposta
            resposta = nlp_processor.generate_response(classification, mock_data)
            print(f"🤖 Resposta: {resposta[:150]}...")
            print("-" * 80)

        except Exception as e:
            print(f"❌ Erro na pergunta '{pergunta}': {str(e)}")

        print()

if __name__ == "__main__":
    testar_nlp_direto()