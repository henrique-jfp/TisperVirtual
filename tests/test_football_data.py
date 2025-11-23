import requests

# Token da football-data.org fornecido pelo usuário
api_token = "54feb02d2567426191ebf5d40539a7ed"
headers = {"X-Auth-Token": api_token}

print("Testando football-data.org para o Brasileirão Série A...")

# 1. Obter informações da competição
competition_url = "https://api.football-data.org/v4/competitions/BSA"
print(f"Buscando competição: {competition_url}")
response = requests.get(competition_url, headers=headers)

if response.status_code == 200:
    comp_data = response.json()
    print("Competição encontrada:")
    print(f"Nome: {comp_data['name']}")
    print(f"País: {comp_data['area']['name']}")
    print(f"Temporada atual: {comp_data['currentSeason']['startDate']} - {comp_data['currentSeason']['endDate']}")
    print(f"Rodada atual: {comp_data.get('currentSeason', {}).get('currentMatchday', 'N/A')}")
    print()

    # 2. Obter jogos recentes (última rodada)
    matches_url = "https://api.football-data.org/v4/competitions/BSA/matches"
    params = {"status": "FINISHED", "limit": 10}  # Últimos 10 jogos finalizados
    print(f"Buscando jogos: {matches_url}")
    matches_response = requests.get(matches_url, headers=headers, params=params)

    if matches_response.status_code == 200:
        matches_data = matches_response.json()
        print(f"Encontrados {len(matches_data['matches'])} jogos recentes.")
        for match in matches_data['matches'][:3]:  # Mostrar apenas os 3 primeiros
            home = match['homeTeam']['name']
            away = match['awayTeam']['name']
            score = f"{match['score']['fullTime']['home']} - {match['score']['fullTime']['away']}"
            date = match['utcDate'][:10]
            print(f"  {date}: {home} {score} {away}")
        print()

        # 3. Obter classificação
        standings_url = "https://api.football-data.org/v4/competitions/BSA/standings"
        print(f"Buscando classificação: {standings_url}")
        standings_response = requests.get(standings_url, headers=headers)

        if standings_response.status_code == 200:
            standings_data = standings_response.json()
            table = standings_data['standings'][0]['table'][:5]  # Top 5
            print("Top 5 da classificação:")
            for team in table:
                pos = team['position']
                name = team['team']['name']
                pts = team['points']
                print(f"  {pos}. {name} - {pts} pts")
            print()

            # 4. Obter artilheiros
            scorers_url = "https://api.football-data.org/v4/competitions/BSA/scorers"
            params = {"limit": 5}
            print(f"Buscando artilheiros: {scorers_url}")
            scorers_response = requests.get(scorers_url, headers=headers, params=params)

            if scorers_response.status_code == 200:
                scorers_data = scorers_response.json()
                print("Top 5 artilheiros:")
                for scorer in scorers_data['scorers']:
                    name = scorer['player']['name']
                    team = scorer['team']['name']
                    goals = scorer['goals']
                    print(f"  {name} ({team}) - {goals} gols")
            else:
                print(f"Erro ao buscar artilheiros: {scorers_response.status_code}")
        else:
            print(f"Erro ao buscar classificação: {standings_response.status_code}")
    else:
        print(f"Erro ao buscar jogos: {matches_response.status_code}")
else:
    print(f"Erro ao buscar competição: {response.status_code} - {response.text}")