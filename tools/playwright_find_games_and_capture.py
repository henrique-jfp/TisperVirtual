from playwright.sync_api import sync_playwright
import re
import json
from pathlib import Path
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--game', type=int, help='Game ID to capture')
args = parser.parse_args()

OUT = Path('./tools/playwright_captures')
OUT.mkdir(parents=True, exist_ok=True)

if args.game:
    URL = f'https://www.365scores.com/pt-br/football/brazil/brazil-serie-a/game/{args.game}'
else:
    URL = 'https://www.365scores.com/pt-br/football/brazil/brazil-serie-a/'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context()
    page = ctx.new_page()
    if args.game:
        gid = args.game
        print('Capturing for specific game', gid)
        captures = []
        def on_response(resp):
            try:
                url = resp.url
                if '/web/game' in url or '/web/game/stats' in url:
                    try:
                        text = resp.text()
                        obj = None
                        try:
                            obj = json.loads(text)
                        except Exception:
                            obj = text
                        captures.append({'url': url, 'status': resp.status, 'body': obj})
                    except Exception:
                        pass
            except Exception:
                pass
        page.on('response', on_response)
        # navigate to game page
        game_url = f'https://www.365scores.com/pt-br/football/brazil/brazil-serie-a/game/{gid}'
        try:
            page.goto(game_url, wait_until='networkidle', timeout=20000)
        except Exception:
            pass
        time.sleep(2)
        # try clicking stats
        for txt in ['Statistics', 'Stats', 'Lineups', 'Estatísticas', 'Escalações']:
            try:
                el = page.query_selector(f"text=/{txt}/i")
                if el:
                    try:
                        el.click(timeout=2000)
                    except Exception:
                        pass
                    time.sleep(1)
            except Exception:
                pass
        time.sleep(2)
        # save
        out = OUT / f'play_capture_brazil_{gid}.json'
        with out.open('w', encoding='utf-8') as f:
            json.dump(captures, f, ensure_ascii=False, indent=2)
        print('Saved captures to', out)
    else:
        page.goto(URL, wait_until='networkidle', timeout=20000)
        time.sleep(2)
        # coletar todos os hrefs
        hrefs = page.eval_on_selector_all('a[href]', "els => els.map(e => e.href)")
        candidates = []
        for h in hrefs:
            if '/game' in h or '/match' in h or 'gameId=' in h:
                m = re.search(r'gameId=(\d+)', h)
                if m:
                    candidates.append(m.group(1))
                else:
                    m2 = re.search(r'match/(\d+)', h)
                    if m2:
                        candidates.append(m2.group(1))
        candidates = list(dict.fromkeys(candidates))
        print('Found candidates:', candidates[:20])
        # try capture first candidate
        if candidates:
            gid = candidates[0]
            print('Capturing for', gid)
            captures = []
            def on_response(resp):
                try:
                    url = resp.url
                    if '/web/game' in url or '/web/game/stats' in url:
                        try:
                            text = resp.text()
                            obj = None
                            try:
                                obj = json.loads(text)
                            except Exception:
                                obj = text
                            captures.append({'url': url, 'status': resp.status, 'body': obj})
                        except Exception:
                            pass
                except Exception:
                    pass
            page.on('response', on_response)
            # navigate to game page
            game_url = f'https://www.365scores.com/game/?gameId={gid}'
            try:
                page.goto(game_url, wait_until='networkidle', timeout=20000)
            except Exception:
                pass
            time.sleep(2)
            # try clicking stats
            for txt in ['Statistics', 'Stats', 'Lineups']:
                try:
                    el = page.query_selector(f"text=/{txt}/i")
                    if el:
                        try:
                            el.click(timeout=2000)
                        except Exception:
                            pass
                        time.sleep(1)
                except Exception:
                    pass
            time.sleep(2)
            # save
            out = OUT / f'play_capture_dynamic_{gid}.json'
            with out.open('w', encoding='utf-8') as f:
                json.dump(captures, f, ensure_ascii=False, indent=2)
            print('Saved captures to', out)
        else:
            print('No candidates found on rendered page')
    try:
        ctx.close()
        browser.close()
    except Exception:
        pass
