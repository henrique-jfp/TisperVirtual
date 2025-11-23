import os
import importlib.util
import json

# carrega o módulo do coletor para usar fetch_data
MODULE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'coleta', 'api_coleta_365scores.py'))
spec = importlib.util.spec_from_file_location("api_coleta_365scores", MODULE_PATH)
api_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(api_mod)

fetch_data = api_mod.fetch_data

game_ids = [4309082, 4309098, 4309116]

for gid in game_ids:
    print('\n--- GAME', gid, '---')
    stats_url = f"https://webws.365scores.com/web/game/stats/?games={gid}"
    data = fetch_data(stats_url)
    if not data:
        print('  nenhum dado retornado (None)')
        continue
    keys = list(data.keys())
    print('  top-level keys:', keys)
    # inspect competitors
    comp = data.get('competitors')
    if isinstance(comp, list) and comp:
        print('  competitors[0] keys:', list(comp[0].keys()))
    # inspect games[0]
    g0 = None
    if isinstance(data.get('games'), list) and data.get('games'):
        g0 = data['games'][0]
        print('  games[0] keys:', list(g0.keys()))
    # inspect statistics / actualGameStatistics
    for k in ('statistics', 'actualGameStatistics'):
        if k in data:
            print(f"  has '{k}' key; type={type(data[k]).__name__}")
            try:
                if isinstance(data[k], dict):
                    subkeys = list(data[k].keys())[:10]
                    print(f"   {k} subkeys(sample):", subkeys)
                if isinstance(data.get('statistics'), list) and data.get('statistics'):
                    stat0 = data['statistics'][0]
                    print('   statistics[0] keys:', list(stat0.keys()))
                    # search for player-containing subkeys in stat0
                    for kk, vv in stat0.items():
                        if isinstance(vv, list) and vv and isinstance(vv[0], dict):
                            # show sample keys of first element
                            print(f"    stat0.{kk}[0] keys:", list(vv[0].keys())[:20])
            except Exception:
                pass
    # check playersStats or similar
    for candidate in ['playersStats', 'players', 'players_stats', 'playersStatsList', 'playersList']:
        if candidate in data:
            ps = data[candidate]
            print(f"  found key '{candidate}' with type {type(ps).__name__} and len {len(ps) if hasattr(ps,'__len__') else 'N/A'}")
            if isinstance(ps, list) and len(ps)>0:
                sample = ps[0]
                print('   sample keys:', list(sample.keys()))
            break
    else:
        # try to search nested for 'player' keys
        def find_players(obj, path=''):
            if isinstance(obj, dict):
                for k,v in obj.items():
                    if k.lower().startswith('player') or (isinstance(v, list) and v and isinstance(v[0], dict) and 'player' in v[0] if v else False):
                        print(f"  possible players container at path '{path + '/' + k}': type={type(v).__name__}")
                        try:
                            if isinstance(v, list) and v and isinstance(v[0], dict):
                                print('   sample keys:', list(v[0].keys()))
                        except Exception:
                            pass
                    find_players(v, path + '/' + k)
            elif isinstance(obj, list):
                for i, item in enumerate(obj[:3]):
                    find_players(item, path + f'[{i}]')
        find_players(data)
    # print small sample of JSON size
    try:
        s = json.dumps(data if isinstance(data, dict) else {}, ensure_ascii=False)
        print('  json length:', len(s))
    except Exception:
        pass

print('\n--- Inspeção concluída ---')
