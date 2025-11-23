import os
from dotenv import load_dotenv
load_dotenv()
import requests

API_KEY = os.environ.get("API_FOOTBALL_KEY") or os.environ.get("RAPIDAPI_KEY") or os.environ.get("X_APISPORTS_KEY") or "b37e6fb1f944906c4156e0b4da160c62"
BASE_URL = "https://v3.football.api-sports.io"

# Default season (can be overridden via .env)
DEFAULT_SEASON = int(os.environ.get("DEFAULT_SEASON", 2025))

def _headers():
    if not API_KEY:
        return {}
    return {"x-apisports-key": API_KEY}

def buscar_ligas():
    """Busca ligas disponíveis na API-Football."""
    url = f"{BASE_URL}/leagues"
    try:
        response = requests.get(url, headers=_headers(), timeout=15)
    except requests.RequestException as e:
        print(f"Erro de conexão ao buscar ligas: {e}")
        return None
    if response.ok:
        try:
            return response.json()
        except Exception as e:
            print(f"Erro ao decodificar JSON em buscar_ligas: {e}")
            return None
    else:
        print(f"Erro ao buscar ligas: {response.status_code}")
        return None

def buscar_times_por_liga(id_liga, season=None):
    """Busca times de uma liga específica."""
    url = f"{BASE_URL}/teams"
    if season is None:
        season = DEFAULT_SEASON
    params = {"league": id_liga, "season": season}
    try:
        response = requests.get(url, headers=_headers(), params=params, timeout=15)
    except requests.RequestException as e:
        print(f"Erro de conexão ao buscar times: {e}")
        return None
    if response.ok:
        try:
            return response.json()
        except Exception as e:
            print(f"Erro ao decodificar JSON em buscar_times_por_liga: {e}")
            return None
    else:
        print(f"Erro ao buscar times: {response.status_code}")
        return None

def buscar_jogos_por_time(id_time, season=None):
    """Busca jogos de um time específico."""
    url = f"{BASE_URL}/fixtures"
    if season is None:
        season = DEFAULT_SEASON
    params = {"team": id_time, "season": season}
    try:
        response = requests.get(url, headers=_headers(), params=params, timeout=15)
    except requests.RequestException as e:
        print(f"Erro de conexão ao buscar jogos: {e}")
        return None
    if response.ok:
        try:
            return response.json()
        except Exception as e:
            print(f"Erro ao decodificar JSON em buscar_jogos_por_time: {e}")
            return None
    else:
        print(f"Erro ao buscar jogos: {response.status_code}")
        return None

if __name__ == "__main__":
    # Exemplo: Buscar ligas
    ligas = buscar_ligas()
    if ligas:
        print("Ligas disponíveis:")
        for liga in ligas['response'][:5]:
            print(f"{liga['league']['name']} - País: {liga['country']['name']}")

    # IDs ajustados para futebol brasileiro
    ID_LIGA_BRASILEIRAO_SERIE_A = 71  # Série A do Brasil
    ID_LIGA_BRASILEIRAO_SERIE_B = 72  # Série B do Brasil

    # Exemplo: Buscar times da Série A do Brasil
    times_serie_a = buscar_times_por_liga(ID_LIGA_BRASILEIRAO_SERIE_A)
    if times_serie_a:
        print("Times da Série A:")
        for time in times_serie_a['response'][:5]:
            print(f"{time['team']['name']} - Fundado em {time['team']['founded']}")

    # Exemplo: Buscar times da Série B do Brasil
    times_serie_b = buscar_times_por_liga(ID_LIGA_BRASILEIRAO_SERIE_B)
    if times_serie_b:
        print("Times da Série B:")
        for time in times_serie_b['response'][:5]:
            print(f"{time['team']['name']} - Fundado em {time['team']['founded']}")

    # Exemplo: Buscar jogos do Fluminense
    ID_TIME_FLUMINENSE = 136  # ID do Fluminense na API-Football
    jogos_fluminense = buscar_jogos_por_time(ID_TIME_FLUMINENSE)
    if jogos_fluminense:
        print("Jogos do Fluminense:")
        for jogo in jogos_fluminense['response'][:5]:
            print(f"{jogo['teams']['home']['name']} vs {jogo['teams']['away']['name']} - Data: {jogo['fixture']['date']}")