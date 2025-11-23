from football_nlp_processor import FootballQueryProcessor

# Testar classificação de perguntas de data
processor = FootballQueryProcessor()

perguntas = [
    'qual dia é hoje',
    'quando foi ontem',
    'qual dia será amanhã'
]

print('🧪 DEBUG: CLASSIFICAÇÃO DE PERGUNTAS DE DATA')
print('=' * 50)

for pergunta in perguntas:
    classificacao = processor.classify_query(pergunta)
    print(f'❓ "{pergunta}"')
    print(f'   📋 Tipo: {classificacao["type"]}')
    print(f'   🎯 Confiança: {classificacao["confidence"]}')
    print()