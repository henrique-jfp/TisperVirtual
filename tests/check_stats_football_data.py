import requests

# Token da football-data.org
api_token = "54feb02d2567426191ebf5d40539a7ed"
headers = {"X-Auth-Token": api_token}

print("Verificando se football-data.org tem estatísticas detalhadas de jogos...")

# Obter um jogo específico para ver a estrutura completa
matches_url = "https://api.football-data.org/v4/competitions/BSA/matches"
params = {"status": "FINISHED", "limit": 1}  # Apenas 1 jogo
response = requests.get(matches_url, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()
    if data['matches']:
        match = data['matches'][0]
        print("Estrutura completa de um jogo:")
        print("Chaves principais:", list(match.keys()))
        print("\nScore:", match.get('score'))
        print("\nHome Team:", match.get('homeTeam'))
        print("\nAway Team:", match.get('awayTeam'))
        print("\nReferees:", match.get('referees', 'N/A'))
        print("\nBookings:", match.get('bookings', 'N/A'))
        print("\nGoals:", match.get('goals', 'N/A'))
        print("\nSubstitutions:", match.get('substitutions', 'N/A'))

        # Verificar se há estatísticas
        if 'statistics' in match:
            print("\nEstatísticas encontradas!")
            print(match['statistics'])
        else:
            print("\nNenhuma estatística detalhada encontrada no jogo.")
    else:
        print("Nenhum jogo encontrado.")
else:
    print(f"Erro: {response.status_code} - {response.text}")