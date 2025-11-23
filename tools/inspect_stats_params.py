import os
import importlib.util
import json

MODULE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'coleta', 'api_coleta_365scores.py'))
spec = importlib.util.spec_from_file_location("api_coleta_365scores", MODULE_PATH)
api_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(api_mod)
fetch_data = api_mod.fetch_data

params = ['includePlayers=1','withPlayers=1','includePlayerStats=1','showPlayers=1','detailed=true']
gid = 4309082
for p in params:
    url = f"https://webws.365scores.com/web/game/stats/?games={gid}&{p}"
    print('\n---', p, '---')
    d = fetch_data(url)
    if not d:
        print(' no data')
        continue
    # print top-level keys
    print(' top-level keys:', list(d.keys()))
    # look for 'players' keys
    def find_player_containers(obj, path=''):
        found = []
        if isinstance(obj, dict):
            for k,v in obj.items():
                if 'player' in k.lower() or 'players' in k.lower():
                    found.append((path+'/'+k, type(v).__name__, (len(v) if hasattr(v,'__len__') else 'N/A')))
                found += find_player_containers(v, path+'/'+k)
        elif isinstance(obj, list):
            for i,item in enumerate(obj[:10]):
                found += find_player_containers(item, path+f'[{i}]')
        return found
    res = find_player_containers(d)
    print(' found containers:', res[:10])
    # if there is a players list, print sample keys
    for path, t, count in res[:5]:
        try:
            # traverse path to get the object
            parts = [p for p in path.split('/') if p]
            cur = d
            for part in parts:
                if part.endswith(']') and '[' in part:
                    name, idx = part[:-1].split('[')
                    cur = cur.get(name)[int(idx)]
                else:
                    cur = cur.get(part)
            if isinstance(cur, list) and cur:
                print('  sample keys at', path, list(cur[0].keys())[:30])
        except Exception as e:
            pass
    # also print if 'games' contains hasLineups or hasMissingPlayers
    g0 = d.get('games',[{}])[0]
    print(' games[0] preview keys:', list(g0.keys())[:20])

print('\n--- done ---')
