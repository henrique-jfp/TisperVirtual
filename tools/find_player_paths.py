import os
import importlib.util
import json

MODULE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'coleta', 'api_coleta_365scores.py'))
spec = importlib.util.spec_from_file_location("api_coleta_365scores", MODULE_PATH)
api_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(api_mod)
fetch_data = api_mod.fetch_data

gid = 4309082
url = f"https://webws.365scores.com/web/game/stats/?games={gid}"
data = fetch_data(url)

paths = []

def search(obj, path=''):
    if isinstance(obj, dict):
        for k,v in obj.items():
            if 'player' in k.lower():
                paths.append((path + '/' + k, v))
            search(v, path + '/' + k)
    elif isinstance(obj, list):
        for i, item in enumerate(obj[:10]):
            search(item, path + f'[{i}]')

search(data)
print('found paths:', len(paths))
for p, v in paths[:20]:
    t = type(v).__name__
    info = ''
    try:
        if isinstance(v, list) and v:
            info = f'list len {len(v)}; sample keys: {list(v[0].keys())[:20]}'
        elif isinstance(v, dict):
            info = f'dict keys: {list(v.keys())[:20]}'
        else:
            info = repr(v)[:200]
    except Exception:
        info = str(type(v))
    print(p, '->', t, info)

# also print some surrounding structure: statistics[?] entries
if isinstance(data.get('statistics'), list):
    for i, s in enumerate(data['statistics'][:5]):
        print('\nstatistics[{}] id/name:'.format(i), s.get('id'), s.get('name'), 'keys:', list(s.keys())[:20])

print('\ndone')
