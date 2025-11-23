import requests

url = 'http://127.0.0.1:8080/api/chat'

# Testar comando de estatísticas
data = {'prompt': 'estatísticas'}
try:
    response = requests.post(url, json=data, timeout=10)
    if response.status_code == 200:
        result = response.json()
        print('✅ Comando "estatísticas" funcionando!')
        print('Resposta:')
        print(result['reply'][:500] + '...' if len(result['reply']) > 500 else result['reply'])
    else:
        print(f'Erro HTTP: {response.status_code}')
        print(response.text)
except Exception as e:
    print(f'Erro: {e}')

print('\n' + '='*50)

# Testar comando específico de corners
data2 = {'prompt': 'corners'}
try:
    response2 = requests.post(url, json=data2, timeout=10)
    if response2.status_code == 200:
        result2 = response2.json()
        print('✅ Comando "corners" funcionando!')
        print('Resposta:')
        print(result2['reply'][:300] + '...' if len(result2['reply']) > 300 else result2['reply'])
    else:
        print(f'Erro HTTP: {response2.status_code}')
        print(response2.text)
except Exception as e:
    print(f'Erro: {e}')

print('\n' + '='*50)

# Testar ajuda
data3 = {'prompt': 'ajuda'}
try:
    response3 = requests.post(url, json=data3, timeout=10)
    if response3.status_code == 200:
        result3 = response3.json()
        print('✅ Comando "ajuda" funcionando!')
        print('Resposta:')
        print(result3['reply'])
    else:
        print(f'Erro HTTP: {response3.status_code}')
        print(response3.text)
except Exception as e:
    print(f'Erro: {e}')