import time
import os
import importlib.util

# Carrega dinamicamente o módulo `api_coleta_365scores.py` pelo caminho para evitar problemas de import
MODULE_PATH = os.path.join(os.path.dirname(__file__), '..', 'coleta', 'api_coleta_365scores.py')
MODULE_PATH = os.path.abspath(MODULE_PATH)
spec = importlib.util.spec_from_file_location("api_coleta_365scores", MODULE_PATH)
api_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(api_mod)

fetch_data = api_mod.fetch_data
fetch_and_save_game_details = api_mod.fetch_and_save_game_details

BASE_URL = "https://webws.365scores.com"
TEAM_ID = 1216  # Fluminense (assumido a partir da lista de IDs)
COMPETITION_NAME = "Brasileir\u00e3o - S\u00e9rie A"


def collect_team_game_ids(team_id: int) -> list:
    page_path = f"/web/games/results/?appTypeId=5&langId=31&timezoneName=America/Sao_Paulo&userCountryId=21&competitors={team_id}&showOdds=true&includeTopBettingOpportunity=1&topBookmaker=156"
    collected = {}
    while page_path:
        url = page_path if page_path.startswith("http") else (BASE_URL + page_path)
        print(f"Buscando página: {url}")
        data = fetch_data(url)
        if not data or not data.get("games"):
            break
        for g in data.get("games", []):
            if not g: continue
            if COMPETITION_NAME in g.get("competitionDisplayName", "") or True:
                gid = g.get("id")
                if gid:
                    collected[gid] = g
        paging = data.get("paging") or {}
        next_page = paging.get("nextPage")
        if next_page:
            page_path = next_page
            time.sleep(1)
        else:
            break
    return sorted(collected.keys())


if __name__ == '__main__':
    print("Iniciando: coleta profunda para o Fluminense (team_id=%s)" % TEAM_ID)
    game_ids = collect_team_game_ids(TEAM_ID)
    print(f"Jogos encontrados para o time {TEAM_ID}: {len(game_ids)}")
    for i, gid in enumerate(game_ids, start=1):
        print(f"\n[{i}/{len(game_ids)}] Coletando detalhes para jogo ID: {gid}")
        try:
            fetch_and_save_game_details(gid)
        except Exception as e:
            print(f"  [ERRO] Exceção ao processar jogo {gid}: {e}")
        time.sleep(1)
    print("\n--- Coleta profunda Fluminense concluída ---")
