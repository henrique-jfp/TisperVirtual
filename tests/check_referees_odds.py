import requests

# Token da football-data.org
api_token = "54feb02d2567426191ebf5d40539a7ed"
headers = {"X-Auth-Token": api_token}

print("Verificando árbitros e odds na football-data.org...")

# Obter um jogo específico
matches_url = "https://api.football-data.org/v4/competitions/BSA/matches"
params = {"status": "FINISHED", "limit": 1}
response = requests.get(matches_url, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()
    if data['matches']:
        match = data['matches'][0]
        print(f"Jogo: {match['homeTeam']['name']} vs {match['awayTeam']['name']}")
        print(f"Data: {match['utcDate'][:10]}")
        
        # Árbitros
        referees = match.get('referees', [])
        if referees:
            print("Árbitros:")
            for ref in referees:
                print(f"  - {ref['name']} ({ref.get('role', 'N/A')})")
        else:
            print("Árbitros: Nenhum listado.")
        
        # Odds
        odds = match.get('odds')
        if odds:
            print("\nOdds disponíveis:")
            print(f"  Home Win: {odds.get('homeWin', 'N/A')}")
            print(f"  Draw: {odds.get('draw', 'N/A')}")
            print(f"  Away Win: {odds.get('awayWin', 'N/A')}")
        else:
            print("\nOdds: Não disponíveis.")
    else:
        print("Nenhum jogo encontrado.")
else:
    print(f"Erro: {response.status_code} - {response.text}")