import os
import importlib.util

MODULE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'coleta', 'api_coleta_365scores.py'))
spec = importlib.util.spec_from_file_location("api_coleta_365scores", MODULE_PATH)
api_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(api_mod)
fetch_data = api_mod.fetch_data

base = "https://webws.365scores.com/web/game/stats/?games={gid}"
params = [
    'includePlayers=1', 'includePlayers=true', 'withPlayers=1', 'withPlayers=true',
    'includePlayerStats=1', 'includePlayerStats=true', 'showPlayers=1', 'showPlayers=true',
    'detailed=true', 'extended=true', 'players=1', 'includeLineups=1', 'withLineups=1'
]

gid = 4309082
for p in params:
    url = base.format(gid=gid) + '&' + p
    print('\n->', url)
    data = fetch_data(url)
    if not data:
        print('  no data')
        continue
    # quick search for 'player' substring in keys or text
    s = str(data)
    if 'player' in s.lower():
        print('  FOUND player substring in response')
    else:
        print('  no player substring')

print('\n-- done')
