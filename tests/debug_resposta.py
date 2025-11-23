from football_nlp_processor import FootballQueryProcessor

# Testar geração de resposta diretamente
processor = FootballQueryProcessor()

perguntas = [
    'qual dia é hoje',
    'quando foi ontem',
    'qual dia será amanhã'
]

print('🧪 DEBUG: GERAÇÃO DE RESPOSTA DIRETA')
print('=' * 50)

for pergunta in perguntas:
    classificacao = processor.classify_query(pergunta)
    resposta = processor.generate_response(classificacao, None)
    print(f'❓ "{pergunta}"')
    print(f'💬 {resposta[:150]}...' if len(resposta) > 150 else f'💬 {resposta}')
    print()