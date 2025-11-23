import requests
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Teste da API-Football
api_key = os.environ.get("API_FOOTBALL_KEY")
if not api_key:
    print("❌ API_FOOTBALL_KEY não encontrada")
    print("Variáveis de ambiente disponíveis:", list(os.environ.keys()))
    exit(1)

print("🔑 Chave da API encontrada")

# Testar classificação
url = "https://v3.football.api-sports.io/standings"
headers = {"x-apisports-key": api_key}
params = {"league": 71, "season": 2023}  # Temporada 2023 (disponível no plano gratuito)

print("📊 Testando classificação (temporada 2024)...")
response = requests.get(url, headers=headers, params=params, timeout=10)

if response.status_code == 200:
    data = response.json()
    standings = data.get('response', [])
    if standings:
        league_standings = standings[0].get('league', {}).get('standings', [])
        print(f"✅ Classificação obtida: {len(league_standings)} grupos")
        if league_standings:
            # standings[0] é o grupo principal
            for i, team_data in enumerate(league_standings[0][:5], 1):
                team_name = team_data.get('team', {}).get('name', 'N/A')
                points = team_data.get('points', 0)
                print(f"  {i}º {team_name} - {points} pts")
    else:
        print("❌ Nenhum dado de classificação encontrado")
        print("Resposta da API:", data)
else:
    print(f"❌ Erro na API: {response.status_code} - {response.text}")

# Testar jogos futuros
print("\n⚽ Testando jogos futuros...")
url = "https://v3.football.api-sports.io/fixtures"
params = {
    "league": 71,
    "season": 2023,
    "status": "NS",  # Not Started
    "next": 10  # Próximos 10 jogos
}

response = requests.get(url, headers=headers, params=params, timeout=10)

if response.status_code == 200:
    data = response.json()
    fixtures = data.get('response', [])
    print(f"✅ Jogos futuros obtidos: {len(fixtures)} jogos")
    for fixture in fixtures[:3]:
        teams = fixture.get('teams', {})
        home = teams.get('home', {}).get('name', 'N/A')
        away = teams.get('away', {}).get('name', 'N/A')
        fixture_date = fixture.get('fixture', {}).get('date', 'N/A')
        print(f"  {home} x {away} - {fixture_date[:10]}")
else:
    print(f"❌ Erro na API: {response.status_code} - {response.text}")