import requests

# Token da football-data.org
api_token = "54feb02d2567426191ebf5d40539a7ed"
headers = {"X-Auth-Token": api_token}

print("Verificando o que a football-data.org oferece gratuitamente...")

# 1. Placares de jogos (últimos jogos)
print("\n1. Placares de jogos (últimos 3 finalizados):")
matches_url = "https://api.football-data.org/v4/competitions/BSA/matches"
params = {"status": "FINISHED", "limit": 3}
response = requests.get(matches_url, headers=headers, params=params)
if response.status_code == 200:
    data = response.json()
    for match in data['matches']:
        home = match['homeTeam']['name']
        away = match['awayTeam']['name']
        score = f"{match['score']['fullTime']['home']} - {match['score']['fullTime']['away']}"
        date = match['utcDate'][:10]
        print(f"  {date}: {home} {score} {away}")
else:
    print("Erro ao buscar placares.")

# 2. Próximos jogos
print("\n2. Próximos jogos (próximos 3 agendados):")
params = {"status": "SCHEDULED", "limit": 3}
response = requests.get(matches_url, headers=headers, params=params)
if response.status_code == 200:
    data = response.json()
    for match in data['matches']:
        home = match['homeTeam']['name']
        away = match['awayTeam']['name']
        date = match['utcDate'][:10]
        print(f"  {date}: {home} vs {away}")
else:
    print("Erro ao buscar próximos jogos.")

# 3. Tabela do Brasileiro
print("\n3. Tabela do Brasileiro (Top 5):")
standings_url = "https://api.football-data.org/v4/competitions/BSA/standings"
response = requests.get(standings_url, headers=headers)
if response.status_code == 200:
    data = response.json()
    table = data['standings'][0]['table'][:5]
    for team in table:
        pos = team['position']
        name = team['team']['name']
        pts = team['points']
        print(f"  {pos}. {name} - {pts} pts")
else:
    print("Erro ao buscar tabela.")

# 4. Artilheiros
print("\n4. Artilheiros (Top 5):")
scorers_url = "https://api.football-data.org/v4/competitions/BSA/scorers"
params = {"limit": 5}
response = requests.get(scorers_url, headers=headers, params=params)
if response.status_code == 200:
    data = response.json()
    for scorer in data['scorers']:
        name = scorer['player']['name']
        team = scorer['team']['name']
        goals = scorer['goals']
        assists = scorer.get('assists', 'N/A')  # Verificar se há assists
        print(f"  {name} ({team}) - {goals} gols, {assists} assists")
else:
    print("Erro ao buscar artilheiros.")

print("\nResumo: Sim para placares, próximos jogos, tabela e artilheiros. Para assists, verifique se aparece 'N/A' ou um número.")