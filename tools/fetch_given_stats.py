import requests
import json
import argparse
import re
from pathlib import Path

DEFAULT_HEADERS = {
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
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0'
}

OUT_DIR = Path('tools/playwright_captures')
OUT_DIR.mkdir(parents=True, exist_ok=True)


def has_player_data(obj):
    if not obj:
        return False
    if isinstance(obj, dict) and obj.get('playersStats'):
        return True
    def _search(o):
        if isinstance(o, dict):
            for k, v in o.items():
                kl = k.lower()
                if kl in ("players", "playerstats", "playersstats") and isinstance(v, list) and v:
                    return True
                if _search(v):
                    return True
        elif isinstance(o, list):
            for item in o:
                if isinstance(item, dict):
                    if any(x in item for x in ("player", "playerId", "player_id", "id")):
                        return True
                if _search(item):
                    return True
        return False
    return _search(obj)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', required=True)
    args = parser.parse_args()
    url = args.url
    print('Fetching URL:', url)
    try:
        r = requests.get(url, headers=DEFAULT_HEADERS, timeout=(5,20))
        print('HTTP', r.status_code)
        text = r.text
        # try parse json
        try:
            obj = r.json()
            print('JSON top-level type:', type(obj).__name__)
            # dump small summary
            summary = {}
            if isinstance(obj, dict):
                summary['keys'] = list(obj.keys())[:20]
            elif isinstance(obj, list) and obj:
                if isinstance(obj[0], dict):
                    summary['sample_keys'] = list(obj[0].keys())[:20]
            print('Summary keys/sample_keys:', summary)
            found_players = has_player_data(obj)
            print('has_player_data:', found_players)
            out = OUT_DIR / f'stats_direct_{re.sub(r"[^0-9]","", url)}.json'
            with out.open('w', encoding='utf-8') as f:
                json.dump(obj, f, ensure_ascii=False, indent=2)
            print('Saved JSON to', out)
        except Exception as e:
            print('Response not JSON or parse failed:', e)
            snippet = text[:1000]
            print('Snippet:', snippet)
    except Exception as e:
        print('Request failed:', e)

if __name__ == '__main__':
    main()
