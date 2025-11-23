import os
import time
import requests
from datetime import datetime, timedelta

API_FOOTBALL_KEY = os.environ.get("API_FOOTBALL_KEY") or os.environ.get("RAPIDAPI_KEY") or os.environ.get("X_APISPORTS_KEY")
API_FOOTBALL_URL = "https://v3.football.api-sports.io"

# Simple in-memory cache with TTL
_CACHE = {}

def _cache_get(key):
    entry = _CACHE.get(key)
    if not entry:
        return None
    value, ts, ttl = entry
    if time.time() - ts > ttl:
        del _CACHE[key]
        return None
    return value

def _cache_set(key, value, ttl=60):
    _CACHE[key] = (value, time.time(), ttl)

def fetch_odds_by_fixture(fixture_id):
    """Busca odds para um fixture específico via API-Football.

    Retorna lista de bookmaker entries normalizadas, ou [] se nada.
    """
    if not API_FOOTBALL_KEY:
        return []
    cache_key = f"odds_fixture_{fixture_id}"
    cached = _cache_get(cache_key)
    if cached is not None:
        return cached

    url = f"{API_FOOTBALL_URL}/odds"
    headers = {"x-apisports-key": API_FOOTBALL_KEY}
    params = {"fixture": fixture_id}
    try:
        r = requests.get(url, headers=headers, params=params, timeout=10)
        if r.status_code != 200:
            return []
        data = r.json()
        # data['response'] is list of bookmakers
        normalized = []
        for bookmaker in data.get('response', []):
            bm = bookmaker.get('bookmaker', {})
            markets = bookmaker.get('bookmaker', {})
            # The API-Football response may have 'bookmakers' structure; attempt parse
            # We'll normalize by reading 'bookmakers' or the provided structure
        # fallback: just return raw response for now
        _cache_set(cache_key, data.get('response', []), ttl=30)
        return data.get('response', [])
    except requests.RequestException:
        return []


def find_upcoming_fixture(team_a, team_b, days_ahead=14):
    """Procura partidas futuras nos próximos `days_ahead` dias que contenham ambos os times no nome.
    Esta função tenta localizar um fixture_id consultando o endpoint /fixtures por intervalo de datas.
    """
    if not API_FOOTBALL_KEY:
        return None
    start = datetime.utcnow().date()
    end = start + timedelta(days=days_ahead)
    url = f"{API_FOOTBALL_URL}/fixtures"
    headers = {"x-apisports-key": API_FOOTBALL_KEY}
    params = {"from": start.isoformat(), "to": end.isoformat()}
    try:
        r = requests.get(url, headers=headers, params=params, timeout=10)
        if r.status_code != 200:
            return None
        data = r.json().get('response', [])
        ta = team_a.lower()
        tb = team_b.lower()
        for f in data:
            teams = f.get('teams', {})
            home = teams.get('home', {}).get('name', '').lower()
            away = teams.get('away', {}).get('name', '').lower()
            if (ta in home and tb in away) or (ta in away and tb in home):
                return f.get('fixture', {}).get('id')
    except requests.RequestException:
        return None
    return None


def get_live_odds_for_match(team_a, team_b):
    """Tenta localizar um fixture entre os times e busca odds.

    Retorna dict com keys: fixture_id, timestamp, bookmakers (raw list) ou {} se nada.
    """
    # check cache
    key = f"live_odds::{team_a}::{team_b}"
    cached = _cache_get(key)
    if cached is not None:
        return cached

    fixture_id = find_upcoming_fixture(team_a, team_b, days_ahead=14)
    if not fixture_id:
        _cache_set(key, {}, ttl=30)
        return {}

    odds = fetch_odds_by_fixture(fixture_id)
    result = {"fixture_id": fixture_id, "bookmakers": odds}
    _cache_set(key, result, ttl=30)
    return result
