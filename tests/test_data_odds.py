#!/usr/bin/env python3
"""
Teste das funcionalidades de data e odds do sistema NLP
"""

from football_nlp_processor import FootballQueryProcessor

def testar_data_e_odds():
    """Testa as funcionalidades de data e odds"""

    processor = FootballQueryProcessor()

    print("🗓️ Teste de Contexto de Data:")
    print(f"Data atual: {processor.get_data_atual_formatada()}")
    print(f"Dia da semana: {processor.get_dia_semana()}")
    print()

    print("💰 Teste de Odds:")
    times_teste = [
        ("Flamengo", "Palmeiras"),
        ("Corinthians", "São Paulo"),
        ("Vasco", "Botafogo")
    ]

    for time1, time2 in times_teste:
        print(f"\n🏆 Odds para {time1} x {time2}:")
        odds = processor.buscar_odds_jogo(time1, time2)
        if odds:
            print(f"  Casa ({time1}): {odds['casa']}")
            print(f"  Empate: {odds['empate']}")
            print(f"  Fora ({time2}): {odds['fora']}")
            print(f"  Fonte: {odds['fonte']}")
            print(f"  Atualizado: {odds['atualizado_em']}")
        else:
            print("  ❌ Não foi possível obter odds")

    print("\n🤖 Teste de Respostas com Contexto de Data:")

    # Simula algumas perguntas
    perguntas_teste = [
        "Quais jogos acontecem hoje?",
        "Qual a classificação do campeonato?",
        "Qual a melhor aposta de hoje?"
    ]

    for pergunta in perguntas_teste:
        print(f"\n❓ Pergunta: {pergunta}")
        classification = processor.classify_query(pergunta)
        resposta = processor.generate_response(classification, None)
        print(f"🤖 Resposta: {resposta[:150]}...")

if __name__ == "__main__":
    testar_data_e_odds()