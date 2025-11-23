import requests

# API-Football key fornecida pelo usuário
api_key = "b37e6fb1f944906c4156e0b4da160c62"
headers = {
    "X-RapidAPI-Key": api_key,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

# Primeiro, obter fixtures do Brasileirão Série A (liga 71, temporada 2024)
fixtures_url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
params = {
    "league": 71,
    "season": 2024,
    "status": "FT"  # Jogos finalizados
}

print("Buscando fixtures do Brasileirão Série A...")
response = requests.get(fixtures_url, headers=headers, params=params)

if response.status_code == 200:
    fixtures_data = response.json()
    print(f"Encontrados {len(fixtures_data['response'])} jogos.")
    
    # Pegar o primeiro jogo finalizado
    if fixtures_data['response']:
        fixture = fixtures_data['response'][0]
        fixture_id = fixture['fixture']['id']
        home_team = fixture['teams']['home']['name']
        away_team = fixture['teams']['away']['name']
        print(f"Testando jogo: {home_team} vs {away_team} (ID: {fixture_id})")
        
        # Agora, buscar estatísticas de jogadores para esse jogo
        players_url = f"https://api-football-v1.p.rapidapi.com/v3/fixtures/players"
        players_params = {"fixture": fixture_id}
        
        print("Buscando estatísticas de jogadores...")
        players_response = requests.get(players_url, headers=headers, params=players_params)
        
        if players_response.status_code == 200:
            players_data = players_response.json()
            print("Dados de jogadores encontrados!")
            print("Estrutura da resposta:")
            print(players_data)
        else:
            print(f"Erro ao buscar jogadores: {players_response.status_code} - {players_response.text}")
    else:
        print("Nenhum jogo encontrado.")
else:
    print(f"Erro ao buscar fixtures: {response.status_code} - {response.text}")