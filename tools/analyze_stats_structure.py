import json
from pathlib import Path

P = Path(r"c:\TradeComigo\tools\playwright_captures\stats_direct_365531214467481.json")
obj = json.loads(P.read_text(encoding='utf-8'))

matches = []

def walk(o, path):
    if isinstance(o, dict):
        # check if dict itself looks like a player
        keys = set(o.keys())
        if {'id','name'} <= keys and ('teamId' in keys or 'competitorId' in keys or 'team' in keys):
            matches.append((path, o))
        for k,v in o.items():
            walk(v, path + [k])
    elif isinstance(o, list):
        for i, item in enumerate(o[:50]):
            walk(item, path + [f'[{i}]'])

walk(obj, [])

print('Matches found:', len(matches))
for i, (p, sample) in enumerate(matches[:10]):
    print('\n--- Match', i+1, 'path=','/'.join(p))
    # print a compact view
    for k in ('id','name','playerId','player','teamId','position'):
        if k in sample:
            print(f'  {k}:', sample.get(k))
    # show full sample keys
    print('  keys:', list(sample.keys())[:30])

# If none found, try to find lists that contain player-like dicts
if not matches:
    def find_lists(o, path):
        if isinstance(o, dict):
            for k,v in o.items():
                find_lists(v, path + [k])
        elif isinstance(o, list):
            # inspect first element
            if o:
                first = o[0]
                if isinstance(first, dict):
                    keys = set(first.keys())
                    if any(x in keys for x in ('player','playerId','player_id','id','name')):
                        print('Candidate list at path:', '/'.join(path), 'first keys:', list(first.keys())[:30])
                for i,item in enumerate(o[:20]):
                    find_lists(item, path + [f'[{i}]'])
    find_lists(obj, [])

print('\nDone')
