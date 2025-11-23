import requests
import re
import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_WS = "https://webws.365scores.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.365scores.com/",
}

OUTPUT_DIR = Path("./tools/playwright_captures")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


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


def fetch_stats_variants(game_id):
    variants = [
        "&includePlayers=1&includePlayerStats=1",
        "&withPlayers=1&includePlayerStats=1",
        "&includePlayers=1&detailed=true",
        "&showPlayers=1",
        "",
    ]
    last = None
    for p in variants:
        url = f"{BASE_WS}/web/game/stats/?games={game_id}&appTypeId=5&langId=31&timezoneName=America/Sao_Paulo&userCountryId=21" + p
        try:
            r = requests.get(url, headers=HEADERS, timeout=(5,15))
            if r.status_code == 200:
                try:
                    obj = r.json()
                except Exception:
                    obj = None
                last = obj
                if obj and has_player_data(obj):
                    return obj, url
        except Exception:
            pass
        time.sleep(0.3)
    return last, None


def discover_games(limit=20):
    # tenta obter jogos do endpoint current; se falhar, usa results sem filtros
    candidates = []
    try:
        url = f"{BASE_WS}/web/games/current/?appTypeId=5&langId=31&timezoneName=America/Sao_Paulo&userCountryId=21"
        r = requests.get(url, headers=HEADERS, timeout=(5,15))
        if r.status_code == 200:
            data = r.json()
            games = data.get('games') if isinstance(data, dict) else []
            for g in games:
                gid = g.get('id')
                if gid and gid not in candidates:
                    candidates.append(gid)
    except Exception:
        pass
    # fallback: broad search via page results for big competitions
    if len(candidates) < limit:
        try:
            # buscar sem competitor para pegar feed amplo
            url = f"{BASE_WS}/web/games/results/?appTypeId=5&langId=31&timezoneName=America/Sao_Paulo&userCountryId=21"
            r = requests.get(url, headers=HEADERS, timeout=(5,15))
            if r.status_code == 200:
                data = r.json()
                for g in data.get('games', [])[:limit*2]:
                    gid = g.get('id')
                    if gid and gid not in candidates:
                        candidates.append(gid)
        except Exception:
            pass
    return candidates[:limit]


def capture_via_playwright(game_id, out_path):
    captures = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(user_agent=HEADERS['User-Agent'])
        page = ctx.new_page()
        def on_response(response):
            try:
                url = response.url
                if '/web/game' in url or '/web/game/stats' in url:
                    try:
                        text = response.text()
                        parsed = None
                        try:
                            parsed = json.loads(text)
                        except Exception:
                            parsed = text
                        captures.append({'url': url, 'status': response.status, 'body': parsed})
                    except Exception:
                        pass
            except Exception:
                pass
        page.on('response', on_response)
        tried = False
        candidate_urls = [
            f"https://www.365scores.com/game/?gameId={game_id}",
            f"https://www.365scores.com/match/{game_id}",
            f"https://www.365scores.com/en/match/{game_id}",
            f"https://www.365scores.com/pt/match/{game_id}",
        ]
        for u in candidate_urls:
            try:
                page.goto(u, wait_until='networkidle', timeout=15000)
                tried = True
            except Exception:
                pass
        time.sleep(1)
        # tentar clicar em abas de estatísticas
        for txt in ['Statistics', 'Stats', 'Lineups', 'Line ups', 'Line-ups']:
            try:
                el = page.query_selector(f"text=/{txt}/i")
                if el:
                    try:
                        el.click(timeout=2000)
                    except Exception:
                        pass
                    time.sleep(0.8)
            except Exception:
                pass
        time.sleep(2)
        # coletar também conteúdo inicial se houver
        try:
            content = page.content()
            captures.append({'url': 'page_content', 'status': 200, 'body': content[:100000]})
        except Exception:
            pass
        try:
            ctx.close()
            browser.close()
        except Exception:
            pass
    # salvar captures
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(captures, f, ensure_ascii=False, indent=2)
    return captures


if __name__ == '__main__':
    print('Descobrindo jogos candidatos...')
    # Tenta descobrir jogos por times da Série A (lista no coletor)
    try:
        txt = Path(r"c:\\TradeComigo\\coleta\\api_coleta_365scores.py").read_text(encoding='utf-8')
        m = re.search(r"SERIE_A_TEAM_IDS\s*[:=].*\[(.*?)\]", txt, re.S)
        team_ids = []
        if m:
            inner = m.group(1)
            for num in re.findall(r"(\d+)", inner):
                team_ids.append(num)
    except Exception:
        team_ids = []

    games = []
    if team_ids:
        for tid in team_ids:
            try:
                url = f"{BASE_WS}/web/games/results/?appTypeId=5&langId=31&timezoneName=America/Sao_Paulo&userCountryId=21&competitors={tid}&showOdds=true&includeTopBettingOpportunity=1&topBookmaker=156"
                r = requests.get(url, headers=HEADERS, timeout=(5,15))
                if r.status_code == 200:
                    data = r.json()
                    for g in data.get('games', []):
                        gid = g.get('id')
                        if gid and gid not in games:
                            games.append(gid)
            except Exception:
                pass
            if len(games) >= 20:
                break
    if not games:
        games = discover_games(limit=20)
    print('Encontrados candidatos:', games)
    for gid in games:
        print('\nTestando gameId=', gid)
        sd, url = fetch_stats_variants(gid)
        if sd and has_player_data(sd):
            print('Encontrado via API stat variant!', gid, 'url=', url)
            out = OUTPUT_DIR / f'play_capture_{gid}.json'
            print('Capturando via Playwright e salvando em', out)
            captures = capture_via_playwright(gid, out)
            print('Salvou capturas, resumo: total responses=', len(captures))
            # também salvar sd
            with open(OUTPUT_DIR / f'stats_response_{gid}.json', 'w', encoding='utf-8') as f:
                json.dump(sd, f, ensure_ascii=False, indent=2)
            break
        else:
            print('Não encontrado via API para', gid, ' — tentando Playwright capture para inspeção (pode não conter players)')
            out = OUTPUT_DIR / f'play_capture_{gid}.json'
            captures = capture_via_playwright(gid, out)
            print('Capturas salvas em', out, 'responses:', len(captures))
            # inspeciona se algum capture tem players
            found = False
            for c in captures:
                try:
                    body = c.get('body')
                    if isinstance(body, dict) and has_player_data(body):
                        found = True
                        with open(OUTPUT_DIR / f'stats_response_playwright_{gid}.json', 'w', encoding='utf-8') as f:
                            json.dump(body, f, ensure_ascii=False, indent=2)
                        print('Encontrado players via Playwright response for', gid)
                        break
                except Exception:
                    pass
            if found:
                break
    print('\nBusca finalizada.')
