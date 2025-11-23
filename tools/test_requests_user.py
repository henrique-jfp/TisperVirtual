import time
import json
import requests
from typing import Any, Dict

# headers based on your curl samples
HEADERS: Dict[str, str] = {
    'accept': '*/*',
    'accept-language': 'pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'origin': 'https://www.365scores.com',
    'referer': 'https://www.365scores.com/',
    'sec-ch-ua': '"Chromium";v="142", "Microsoft Edge";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0',
}

URLS = [
    'https://webws.365scores.com/web/standings/?appTypeId=5&langId=31&timezoneName=America/Sao_Paulo&userCountryId=21&competitions=113&live=false&isPreview=true&stageNum=1&seasonNum=75&lastUpdateId=5468179236',
    'https://webws.365scores.com/web/games/current/?appTypeId=5&langId=31&timezoneName=America/Sao_Paulo&userCountryId=21&competitions=113&showOdds=true&topBookmaker=161&lastUpdateId=5468211019',
    'https://webws.365scores.com/web/trends/?appTypeId=5&langId=31&timezoneName=America/Sao_Paulo&userCountryId=21&competition=113&isTop=true&topBookmaker=161',
    'https://webws.365scores.com/web/relatedEntities/?appTypeId=5&langId=31&timezoneName=America/Sao_Paulo&userCountryId=21&competitions=113',
    'https://webws.365scores.com/web/games/predictions/?appTypeId=5&langId=31&timezoneName=America/Sao_Paulo&userCountryId=21&competitions=113&topBookmaker=161&lastUpdateId=5468155980',
    'https://webws.365scores.com/web/athletes/?appTypeId=5&langId=31&timezoneName=America/Sao_Paulo&userCountryId=21&athletes=48242&fullDetails=true&topBookmaker=161',
    'https://webws.365scores.com/web/games/current/?appTypeId=5&langId=31&timezoneName=America/Sao_Paulo&userCountryId=21&competitors=1215&showOdds=true&includeTopBettingOpportunity=1&topBookmaker=161',
    'https://webws.365scores.com/web/game/?appTypeId=5&langId=31&timezoneName=America/Sao_Paulo&userCountryId=21&gameId=4380286&topBookmaker=161',
]


def has_player_data(stats_obj: Any) -> bool:
    if not stats_obj:
        return False
    if isinstance(stats_obj, dict) and stats_obj.get('playersStats'):
        return True

    def _search(o: Any) -> bool:
        if isinstance(o, dict):
            for k, v in o.items():
                kl = k.lower()
                if kl in ('players', 'playerstats', 'playersstats') and isinstance(v, list) and v:
                    return True
                if _search(v):
                    return True
        elif isinstance(o, list):
            for item in o:
                if isinstance(item, dict):
                    if any(x in item for x in ('player', 'playerId', 'player_id', 'id')):
                        return True
                if _search(item):
                    return True
        return False

    return _search(stats_obj)


session = requests.Session()

results = []
for i, url in enumerate(URLS, start=1):
    print(f"\n[{i}] GET {url}")
    try:
        t0 = time.time()
        r = session.get(url, headers=HEADERS, timeout=(5, 15))
        dt = int((time.time() - t0) * 1000)
        code = r.status_code
        print(f"  status={code} time={dt}ms len={len(r.content)}")
        is_json = False
        top_keys = None
        player_flag = False
        snippet = None
        try:
            j = r.json()
            is_json = True
            if isinstance(j, dict):
                top_keys = list(j.keys())[:20]
            else:
                top_keys = type(j).__name__
            player_flag = has_player_data(j)
            snippet = json.dumps(j, ensure_ascii=False)[:800]
        except Exception:
            snippet = (r.text or '')[:800]
        print(f"  json={is_json} top_keys={top_keys} has_player_data={player_flag}")
        if snippet:
            print(f"  snippet: {snippet[:400]}{('...' if len(snippet)>400 else '')}")
        results.append({'url': url, 'status': code, 'time_ms': dt, 'is_json': is_json, 'top_keys': top_keys, 'has_player_data': player_flag})
    except Exception as e:
        print(f"  [ERROR] {e}")
    time.sleep(0.5)

print('\n--- SUMMARY ---')
for r in results:
    print(f"{r['url']} -> {r['status']} json={r['is_json']} players={r['has_player_data']}")
