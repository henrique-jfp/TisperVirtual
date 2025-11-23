import requests
import re
import json
from pathlib import Path

# carrega HEADERS/SESSION do coletor lendo o arquivo (não importa o pacote)
COLLECTOR_PATH = Path(r"c:\\TradeComigo\\coleta\\api_coleta_365scores.py")
txt = COLLECTOR_PATH.read_text(encoding='utf-8')
ua = re.search(r"'User-Agent'\s*:\s*['\"]([^'\"]+)['\"]", txt)
HEADERS = {
    'User-Agent': ua.group(1) if ua else 'Mozilla/5.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}
SESSION = requests.Session()
SESSION.headers.update(HEADERS)

TEST_URLS = [
    "https://www.365scores.com/game/?gameId=4309082",
    "https://www.365scores.com/game/?gameId=4309098",
]

for u in TEST_URLS:
    try:
        r = SESSION.get(u, headers=HEADERS, timeout=(5,15))
        print(f"URL: {u} - status {r.status_code} - length {len(r.text)}")
        txt = r.text[:5000]
        found = []
        for token in ('playersStats', 'players', '/web/game/stats', '/web/game/?', 'includePlayers'):
            if token in r.text:
                found.append(token)
        print(' Found tokens:', found)
        if 'window.__INITIAL_STATE__' in r.text:
            idx = r.text.find('window.__INITIAL_STATE__')
            excerpt = r.text[idx:idx+1000]
            print(' Has INITIAL_STATE snippet:', excerpt[:500])
    except Exception as e:
        print('Erro fetching', u, e)
