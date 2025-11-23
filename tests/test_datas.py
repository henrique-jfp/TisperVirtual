#!/usr/bin/env python3
"""
Teste rápido das melhorias no NLP processor para datas
"""

from football_nlp_processor import FootballQueryProcessor

def test_datas():
    """Testa reconhecimento de perguntas sobre datas"""

    processor = FootballQueryProcessor()

    # Testes de perguntas sobre datas
    perguntas_data = [
        "qual dia é hoje",
        "que dia é hoje",
        "quando foi ontem",
        "qual dia foi ontem",
        "quando será amanhã",
        "qual dia será amanhã",
        "qual a tabela do campeonato brasileiro"
    ]

    print("🧪 TESTANDO RECONHECIMENTO DE DATAS")
    print("=" * 50)

    for pergunta in perguntas_data:
        print(f"\n❓ Pergunta: '{pergunta}'")

        # Classificar
        classificacao = processor.classify_query(pergunta)
        print(f"   📋 Tipo detectado: {classificacao['type']}")
        print(f"   🎯 Confiança: {classificacao['confidence']}")

        # Gerar resposta
        resposta = processor.generate_response(classificacao)
        print(f"   💬 Resposta: {resposta[:100]}...")

    print("\n" + "=" * 50)
    print("🏁 TESTE CONCLUÍDO")

if __name__ == "__main__":
    test_datas()