import os
import importlib.util
import json

MODULE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'coleta', 'api_coleta_365scores.py'))
spec = importlib.util.spec_from_file_location("api_coleta_365scores", MODULE_PATH)
api_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(api_mod)
fetch_data = api_mod.fetch_data

game_ids = [4309082, 4309098, 4309116]

CANDIDATES = [
    "/web/game/stats/?games={}",
    "/web/game/details/?games={}",
    "/web/game/players/?games={}",
    "/web/game/playersStats/?games={}",
    "/web/game/players-statistics/?games={}",
    "/web/game/players-stats/?games={}",
    "/web/game/playerStats/?games={}",
    "/web/game/summary/?games={}",
]
BASE = "https://webws.365scores.com"


def contains_player_info(d):
    # search shallow and nested for 'player' occurrences
    if not d:
        return False
    if isinstance(d, dict):
        for k, v in d.items():
            if 'player' in k.lower():
                return True
            if isinstance(v, list) and v and isinstance(v[0], dict):
                # check keys of first element
                if any('player' in kk.lower() for kk in v[0].keys()):
                    return True
    return False

for gid in game_ids:
    print(f"\n--- probing game {gid} ---")
    for path_tpl in CANDIDATES:
        path = path_tpl.format(gid)
        url = BASE + path
        data = fetch_data(url)
        ok = False
        note = ''
        if data is None:
            note = 'no data (None or error)'
        else:
            # quick checks
            if contains_player_info(data):
                ok = True
                note = 'contains player key'
            else:
                # search nested for dicts that have key 'player'
                def search(obj, depth=0):
                    if depth>4:
                        return None
                    if isinstance(obj, dict):
                        for k,v in obj.items():
                            if 'player' in k.lower():
                                return k
                            res = search(v, depth+1)
                            if res:
                                return res
                    elif isinstance(obj, list):
                        for item in obj[:5]:
                            res = search(item, depth+1)
                            if res:
                                return res
                    return None
                res = search(data)
                if res:
                    ok = True
                    note = f'nested key: {res}'
                else:
                    note = 'no player keys found'
        print(f"  {path} -> {note}")

print('\n--- probe finished ---')
