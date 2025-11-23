import requests
import json

# Testar perguntas de data através da API
perguntas = [
    'qual dia é hoje',
    'quando foi ontem',
    'qual dia será amanhã'
]

print('🧪 TESTANDO API COM PERGUNTAS DE DATA')
print('=' * 50)

for pergunta in perguntas:
    try:
        response = requests.post('http://localhost:5000/api/chat', 
                               json={'prompt': pergunta},
                               timeout=10)

        if response.status_code == 200:
            data = response.json()
            resposta = data.get('reply', 'Sem resposta')
            print(f'❓ "{pergunta}"')
            print(f'💬 {resposta[:100]}...' if len(resposta) > 100 else f'💬 {resposta}')
            print()
        else:
            print(f'❌ Erro na API para "{pergunta}": {response.status_code}')

    except Exception as e:
        print(f'❌ Erro de conexão para "{pergunta}": {e}')
        print()