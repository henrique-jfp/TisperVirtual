import requests
from datetime import datetime
from supabase import create_client, Client
from typing import List, Dict, Any, Optional

# Config Supabase (mesmo do coletor existente)
SUPABASE_URL = "https://nflmvptqgicabovfmnos.supabase.co:443"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5mbG12cHRxZ2ljYWJvdmZtbm9zIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM3NzEzNTAsImV4cCI6MjA3OTM0NzM1MH0.l-RuwMrLgQgfjp8XZQ7bpEwfKODo7qKEXOhGR49xJ9c"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Token da football-data.org
API_TOKEN = "54feb02d2567426191ebf5d40539a7ed"
HEADERS = {"X-Auth-Token": API_TOKEN}

def safe_upsert(table_name: str, rows: List[Dict[str, Any]], on_conflict: Optional[str] = None):
    """Upsert seguro, igual ao coletor existente."""
    if not rows:
        return
    cols = [c.strip() for c in on_conflict.split(',')] if on_conflict else []
    if cols:
        unique = {}
        for r in rows:
            try:
                key = tuple(r.get(c) for c in cols)
            except Exception:
                key = None
            if key and all(k is not None for k in key):
                if key not in unique:
                    unique[key] = r
            else:
                unique[id(r)] = r
        rows = list(unique.values())

    try:
        if on_conflict:
            supabase.table(table_name).upsert(rows, on_conflict=on_conflict).execute()
        else:
            supabase.table(table_name).upsert(rows).execute()
        return
    except Exception as e:
        print(f"  [WARN] Upsert direto falhou para '{table_name}': {e}. Fazendo fallback.")
        for r in rows:
            try:
                if cols and all(r.get(c) is not None for c in cols):
                    match_dict = {c: r[c] for c in cols}
                    supabase.table(table_name).update(r).match(match_dict).execute()
                else:
                    supabase.table(table_name).insert(r).execute()
            except Exception as e2:
                print(f"    [ERRO] Falha ao salvar linha em '{table_name}': {e2}")

def save_matches_to_db(matches, source="football_data", dry_run=False):
    """Salva jogos no banco, evitando duplicatas por api_id."""
    games_to_save = []
    for match in matches:
        home_team = match['homeTeam']['name']
        away_team = match['awayTeam']['name']
        date = match['utcDate'][:10]
        score_home = match['score'].get('fullTime', {}).get('home')
        score_away = match['score'].get('fullTime', {}).get('away')
        status = match['status']
        
        games_to_save.append({
            "api_id": match['id'],  # ID da football-data como PK
            "start_time": match['utcDate'],
            "status": status,
            "home_team_score": score_home,
            "away_team_score": score_away
        })
    
    if dry_run:
        print(f"[DRY-RUN] Salvaria {len(games_to_save)} jogos.")
        for g in games_to_save[:3]:
            print(f"  {g['api_id']}: {g['start_time'][:10]} - Status: {g['status']}")
    else:
        safe_upsert("jogos", games_to_save, on_conflict="api_id")
        print(f"Salvos {len(games_to_save)} jogos no banco.")

def save_standings_to_db(standings, season=2024, dry_run=False):
    """Salva classificação em tabela 'classificacao'."""
    standings_to_save = []
    for team in standings:
        standings_to_save.append({
            "season": season,
            "position": team['position'],
            "team_name": team['team']['name'],
            "points": team['points'],
            "played_games": team['playedGames'],
            "won": team['won'],
            "draw": team['draw'],
            "lost": team['lost'],
            "goals_for": team['goalsFor'],
            "goals_against": team['goalsAgainst'],
            "goal_difference": team['goalDifference']
        })
    
    if dry_run:
        print(f"[DRY-RUN] Salvaria classificação de {len(standings_to_save)} times.")
        for s in standings_to_save[:5]:
            print(f"  {s['position']}. {s['team_name']} - {s['points']} pts")
    else:
        safe_upsert("classificacao", standings_to_save, on_conflict="season,position")
        print(f"Salva classificação de {len(standings_to_save)} times.")

def save_scorers_to_db(scorers, season=2024, dry_run=False):
    """Atualiza jogadores com gols/assists totais da temporada."""
    players_to_update = []
    for scorer in scorers:
        player_name = scorer['player']['name']
        goals = scorer['goals']
        assists = scorer.get('assists', 0)
        
        players_to_update.append({
            "name": player_name,
            "season_goals": goals,
            "season_assists": assists
        })
    
    if dry_run:
        print(f"[DRY-RUN] Atualizaria {len(players_to_update)} jogadores com stats da temporada.")
        for p in players_to_update[:5]:
            print(f"  {p['name']} - {p['season_goals']}G, {p['season_assists']}A")
    else:
        # Atualiza jogadores existentes por name
        for p in players_to_update:
            try:
                supabase.table("jogadores").update({
                    "season_goals": p['season_goals'],
                    "season_assists": p['season_assists']
                }).eq("name", p['name']).execute()
            except Exception as e:
                print(f"Erro ao atualizar {p['name']}: {e}")
        print(f"Tentativa de atualização de {len(players_to_update)} jogadores.")

def get_standings():
    """Busca a tabela atualizada do Brasileirão Série A."""
    url = "https://api.football-data.org/v4/competitions/BSA/standings"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        return data['standings'][0]['table']
    else:
        print(f"Erro ao buscar tabela: {response.status_code}")
        return []

def get_scorers(limit=10):
    """Busca artilheiros e assistentes (top limit)."""
    url = "https://api.football-data.org/v4/competitions/BSA/scorers"
    params = {"limit": limit}
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['scorers']
    else:
        print(f"Erro ao buscar artilheiros: {response.status_code}")
        return []

def get_all_match_scores(status="FINISHED"):
    """Busca placares de todos os jogos (finalizados ou agendados)."""
    url = "https://api.football-data.org/v4/competitions/BSA/matches"
    params = {"status": status}
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['matches']
    else:
        print(f"Erro ao buscar jogos: {response.status_code}")
        return []

def search_future_games():
    """Busca jogos futuros (agendados)."""
    return get_all_match_scores(status="SCHEDULED")

# Exemplos de uso
if __name__ == "__main__":
    print("=== SALVANDO DADOS NO BANCO (HÍBRIDO) ===")
    
    # Salva todos os jogos finalizados (evitando duplicatas)
    matches = get_all_match_scores("FINISHED")
    save_matches_to_db(matches, dry_run=False)
    
    # Salva próximos jogos
    future_games = search_future_games()
    save_matches_to_db(future_games, dry_run=False)
    
    # Salva classificação atual
    standings = get_standings()
    save_standings_to_db(standings, dry_run=False)
    
    # Salva artilheiros
    scorers = get_scorers(50)  # Top 50
    save_scorers_to_db(scorers, dry_run=False)
    
    print("Dados básicos salvos! Agora podemos focar em extrair stats de jogadores do 365scores.")
    print("Para relacionar, usaremos data/time dos jogos como chave.")