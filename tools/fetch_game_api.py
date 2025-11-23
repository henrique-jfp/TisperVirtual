import requests, json
url = 'https://api.365scores.com/web/game/?gameId=4467481'
headers = {'User-Agent':'Mozilla/5.0','Accept':'application/json'}
print('Fetching', url)
r = requests.get(url, headers=headers, timeout=20)
print('Status', r.status_code)
ct = r.headers.get('content-type')
print('Content-Type', ct)
try:
    j = r.json()
except Exception as e:
    print('Failed to parse JSON', e)
    j = None
if j is None:
    raise SystemExit(1)
print('Top-level keys:', list(j.keys()))
# check for likely player keys
candidates = ['lineups','players','squad','squads','rosters','teamPlayers','teamSquad']
found = [k for k in candidates if k in j]
print('Found candidate keys at top-level:', found)
open('tools/playwright_captures/game_api_4467481.json','w',encoding='utf-8').write(json.dumps(j, ensure_ascii=False))
print('Saved to tools/playwright_captures/game_api_4467481.json')
# also search nested dicts for these keys
import collections
matches = []
q = collections.deque([(None, j)])
while q:
    path, node = q.popleft()
    if isinstance(node, dict):
        for k, v in node.items():
            p = f"{path}.{k}" if path else k
            if k in candidates:
                matches.append(p)
            if isinstance(v, (dict, list)):
                q.append((p, v))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            p = f"{path}[{i}]" if path else f"[{i}]"
            if isinstance(v, (dict, list)):
                q.append((p, v))
print('Nested candidate key paths (first 50):')
for m in matches[:50]:
    print(' ', m)
print('Total nested matches:', len(matches))
