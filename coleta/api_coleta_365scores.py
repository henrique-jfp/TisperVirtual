import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import json
import time
import argparse
from typing import Dict, Any, List, Optional, Set
from supabase import create_client, Client

# Playwright opcional para fallback robusto via navegador headless
try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except Exception:
    PLAYWRIGHT_AVAILABLE = False

# --- Configurações ---
SUPABASE_URL: str = "https://nflmvptqgicabovfmnos.supabase.co"
SUPABASE_KEY: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5mbG12cHRxZ2ljYWJvdmZtbm9zIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM3NzEzNTAsImV4cCI6MjA3OTM0NzM1MH0.l-RuwMrLgQgfjp8XZQ7bpEwfKODo7qKEXOhGR49xJ9c"
COMPETITION_NAME: str = "Brasileirão - Série A"
SERIE_A_TEAM_IDS: List[int] = [1215, 1222, 1209, 1211, 1210, 1273, 1216, 1218, 1219, 1778, 1225, 8499, 1267, 1774, 1775, 1227, 1767, 1228, 1213, 1768]

# --- Conexão e Cabeçalhos ---
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
HEADERS: Dict[str, str] = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.365scores.com/",
}

# Reuse a session with retry strategy to avoid hangs and improve resilience
SESSION = requests.Session()
try:
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "POST"]
    )
except TypeError:
    # older urllib3 uses 'method_whitelist'
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        method_whitelist=["GET", "POST"]
    )
adapter = HTTPAdapter(max_retries=retry_strategy)
SESSION.mount("https://", adapter)
SESSION.mount("http://", adapter)

def fetch_data(url: str) -> Optional[Dict[str, Any]]:
    """Busca dados de uma URL da API de forma segura usando `SESSION` com retries.

    Usa timeout dividido (connect, read) e captura KeyboardInterrupt para permitir
    parada manual sem deixar a execução travada.
    """
    try:
        # timeout: (connect, read)
        response = SESSION.get(url, headers=HEADERS, timeout=(5, 15))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response is not None and e.response.status_code == 404:
            print(f"  [AVISO] Dados não encontrados (404 Not Found) para a URL: {url}")
        else:
            code = e.response.status_code if getattr(e, 'response', None) is not None else '??'
            print(f"  [ERRO HTTP] Falha ao conectar com a API ({code}) para a URL: {url} - {e}")
        return None
    except KeyboardInterrupt:
        # Permite Ctrl-C propagar para o loop superior para um shutdown limpo
        raise
    except Exception as e:
        print(f"  [ERRO GERAL] Falha ao conectar com a API para a URL: {url} - {e}")
        return None


def safe_upsert(table_name: str, rows: List[Dict[str, Any]], on_conflict: Optional[str] = None):
    """Tenta upsert simples; se falhar por ausência de constraint, faz fallback por linha (update->insert)."""
    if not rows:
        return
    # Se fornecido on_conflict, deduplicar linhas com base nas colunas de conflito
    cols = [c.strip() for c in on_conflict.split(',')] if on_conflict else []
    if cols:
        unique = {}
        fallback_rows = []
        for r in rows:
            try:
                key = tuple(r.get(c) for c in cols)
            except Exception:
                key = None
            # Se alguma das chaves for None, não podemos deduplicar com segurança — manter na lista
            if key and all(k is not None for k in key):
                if key not in unique:
                    unique[key] = r
            else:
                # use id() para manter única a entrada com chaves ausentes
                unique[id(r)] = r
        rows = list(unique.values())

    try:
        if on_conflict:
            supabase.table(table_name).upsert(rows, on_conflict=on_conflict).execute()
        else:
            supabase.table(table_name).upsert(rows).execute()
        return
    except Exception as e:
        print(f"  [WARN] upsert direto falhou para tabela '{table_name}': {e}. Fazendo fallback por linha.")
    for r in rows:
        try:
            # se temos colunas de conflito, tente update por essas colunas usando .match()
            if cols and all((k in r and r[k] is not None) for k in cols):
                match_dict = {k: r[k] for k in cols}
                try:
                    res = supabase.table(table_name).update(r).match(match_dict).execute()
                except Exception:
                    # alguns clientes podem não aceitar update(...).match(...) encadeado; tentar via table(...) primeiro
                    res = supabase.table(table_name).update(r).match(match_dict).execute()
                # se update afetou linhas, continue
                if getattr(res, 'data', None):
                    continue
            # senão tente insert
            supabase.table(table_name).insert(r).execute()
        except Exception as e2:
            print(f"    [ERRO] Falha ao salvar linha em '{table_name}': {e2}")


def table_has_column(table_name: str, column_name: str) -> bool:
    """Verifica de forma prática se a tabela exposta pelo Supabase/PostgREST possui a coluna.

    Faz uma tentativa de `select` por essa coluna; se PostgREST reclamar (PGRST204), assumimos que não existe.
    """
    try:
        # limit 0 teria sido ideal, mas a API do supabase client pode não aceitar; limit 1 é suficiente.
        res = supabase.table(table_name).select(column_name).limit(1).execute()
        # Se a chamada não lançou, a coluna provavelmente existe
        return True
    except Exception as e:
        # Mensagens do supabase/PostgREST contêm PGRST204 quando a coluna não existe
        msg = str(e)
        if 'PGRST204' in msg or "Could not find the '" in msg or 'schema cache' in msg:
            return False
        # em caso de qualquer outro erro, não arriscar — logamos e retornamos False
        print(f"  [WARN] Verificação de coluna falhou para {table_name}.{column_name}: {e}")
        return False


def has_player_data(stats_obj: Any) -> bool:
    """Detecta de forma robusta se a estrutura de `stats` contém dados por jogador."""
    if not stats_obj:
        return False
    # caso óbvio
    if isinstance(stats_obj, dict) and stats_obj.get("playersStats"):
        return True

    # busca recursiva por listas/dicionários que parecem conter dados de jogador
    def _search(o: Any) -> bool:
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

    return _search(stats_obj)


def fetch_game_via_playwright(game_id: int, timeout: int = 12) -> Optional[Dict[str, Any]]:
    """Usa Playwright para carregar a página pública do jogo e capturar respostas XHR
    que contenham `/web/game` ou `/web/game/stats` com dados de jogador.

    Retorna o JSON quando encontrado ou None.
    """
    if not PLAYWRIGHT_AVAILABLE:
        raise RuntimeError("Playwright não está disponível. Instale com: pip install playwright; playwright install")

    result_json = None
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent=HEADERS.get('User-Agent'))
            page = context.new_page()

            # coletar respostas relevantes
            responses = []

            def handle_response(response):
                try:
                    url = response.url
                    if '/web/game' in url or '/web/game/stats' in url:
                        try:
                            text = response.text()
                            # tenta parsear JSON
                            import json as _json
                            obj = _json.loads(text)
                            responses.append(obj)
                        except Exception:
                            pass
                except Exception:
                    pass

            page.on('response', handle_response)

            # Navega para a página do jogo — usamos a rota pública genérica
            # A URL pública costuma ser algo como /match/ ou /game; tentamos múltiplas.
            candidate_urls = [
                f"https://www.365scores.com/game/?gameId={game_id}",
                f"https://www.365scores.com/match/{game_id}",
                f"https://www.365scores.com/en/match/{game_id}",
                f"https://www.365scores.com/pt/match/{game_id}",
            ]
            for u in candidate_urls:
                try:
                        page.goto(u, wait_until='networkidle', timeout=timeout*1000)
                except Exception:
                    # ignora timeouts e tenta próxima
                    pass

                # aguarda algumas respostas para que XHRs sejam capturados
                import time as _time
                _time.sleep(2)

                # Tenta interagir com a página: clicar na aba de estatísticas/lineups para forçar XHRs
                try:
                    # possíveis textos que ativam a aba de estatísticas
                    candidates = ['Statistics', 'Stats', 'Lineups', 'Line-ups', 'Line ups']
                    for txt in candidates:
                        try:
                            el = page.query_selector(f"text=/{txt}/i")
                            if el:
                                el.click(timeout=2000)
                                _time.sleep(1)
                        except Exception:
                            pass
                except Exception:
                    pass

                # espera mais tempo para XHRs aparecerem
                _time.sleep(3)
            # aguarda algumas respostas para que XHRs sejam capturados
            import time as _time
            _time.sleep(2)

            # procura o primeiro objeto que parece conter dados de jogador
            for obj in responses:
                if has_player_data(obj):
                    result_json = obj
                    break

            # cleanup
            try:
                context.close()
                browser.close()
            except Exception:
                pass
    except Exception as e:
        print(f"  [ERRO] fetch_game_via_playwright: {e}")

    return result_json


def try_player_endpoints(game_id: int):
    """Tenta múltiplos endpoints conhecidos que frequentemente retornam listas de jogadores.

    Retorna (json_obj, endpoint_url) no primeiro encontrado que contenha dados por jogador,
    ou (None, None) se nenhum foi encontrado.
    """
    candidates = [
        f"https://webws.365scores.com/web/game/players/?games={game_id}",
        f"https://webws.365scores.com/web/game/playersStats/?games={game_id}",
        f"https://webws.365scores.com/web/game/playerStats/?games={game_id}",
        f"https://webws.365scores.com/web/game/players-stats/?games={game_id}",
        f"https://webws.365scores.com/web/game/lineups/?games={game_id}",
        f"https://webws.365scores.com/web/game/lineups/?gameId={game_id}",
        f"https://webws.365scores.com/web/game/stats/?games={game_id}&includePlayers=1&includePlayerStats=1",
        f"https://api.365scores.com/web/game/stats/?games={game_id}&includePlayers=1&includePlayerStats=1",
    ]

    for url in candidates:
        try:
            sd = fetch_data(url)
            if sd:
                if has_player_data(sd):
                    return sd, url
        except Exception:
            # ignora e tenta próxima
            pass
    return None, None

def mark_processing_status(game_id: int, status_type: str, details: Optional[str] = None):
    """Marca o status de processamento do jogo na tabela `jogos_processados`.

    Não cria a tabela automaticamente — execute o DDL fornecido no Supabase.
    """
    try:
        existing = supabase.table("jogos_processados").select("jogo_api_id").eq("jogo_api_id", game_id).execute()
        payload = {"jogo_api_id": game_id, "status": status_type, "details": details}
        if existing and getattr(existing, "data", None):
            supabase.table("jogos_processados").update(payload).eq("jogo_api_id", game_id).execute()
        else:
            supabase.table("jogos_processados").insert(payload).execute()
    except Exception as err:
        print(f"  [ERRO] Falha ao marcar processing status para jogo {game_id}: {err}")

def run_collect_games(dry_run: bool = False):
    """
    FASE 1: Coleta Ampla.
    Varre todos os times da Série A para descobrir e salvar os IDs de todos os jogos do campeonato.
    """
    print("--- EXECUTANDO: Coleta Ampla de Jogos ---")
    
    for team_id in SERIE_A_TEAM_IDS:
        print(f"\nBuscando jogos para o time ID: {team_id}")
        base_url = "https://webws.365scores.com"
        # Parâmetros recomendados encontrados: timezoneName, userCountryId, showOdds, includeTopBettingOpportunity, topBookmaker
        page_path = f"/web/games/results/?appTypeId=5&langId=31&timezoneName=America/Sao_Paulo&userCountryId=21&competitors={team_id}&showOdds=true&includeTopBettingOpportunity=1&topBookmaker=156"

        collected_games: Dict[int, Dict[str, Any]] = {}
        while page_path:
            url = page_path if page_path.startswith("http") else (base_url + page_path)
            data = fetch_data(url)
            if not data or not data.get("games"):
                if not collected_games:
                    print(f"  Nenhum jogo encontrado para o time {team_id} na página {url}.")
                break

            for game in data["games"]:
                if not game: continue
                if COMPETITION_NAME in game.get("competitionDisplayName", ""):
                    gid = game.get("id")
                    if gid:
                        collected_games[gid] = game

            # Avança para a próxima página, se houver
            paging = data.get("paging") or {}
            next_page = paging.get("nextPage")
            if next_page:
                page_path = next_page
                time.sleep(1)
            else:
                break

        games_to_save: List[Dict[str, Any]] = [
            {
                "api_id": g.get("id"),
                "competition": g.get("competitionDisplayName"),
                "start_time": g.get("startTime"),
                "status": g.get("statusText"),
                "home_team_score": int(g.get("homeCompetitor", {}).get("score")) if g.get("homeCompetitor", {}).get("score") is not None else None,
                "away_team_score": int(g.get("awayCompetitor", {}).get("score")) if g.get("awayCompetitor", {}).get("score") is not None else None,
            }
            for g in collected_games.values()
        ]

        if games_to_save:
            if dry_run:
                print(f"  [DRY-RUN] Inseriria {len(games_to_save)} jogos básicos: {[g['api_id'] for g in games_to_save[:5]]}...")
            else:
                try:
                    print(f"  Salvando/Atualizando {len(games_to_save)} jogos básicos...")
                    supabase.table("jogos").upsert(games_to_save, on_conflict="api_id").execute()
                except Exception as e:
                    print(f"  [ERRO] Falha ao salvar jogos básicos: {e}")
        else:
            print(f"  Nenhum jogo do {COMPETITION_NAME} encontrado para o time {team_id}.")

        time.sleep(1)
    print("\n--- Coleta Ampla de Jogos Concluída ---")

def run_collect_details(reprocess_no_events: bool = False, dry_run: bool = False):
    """
    FASE 2: Coleta Profunda.
    Busca e salva os detalhes (estatísticas, jogadores, etc.) apenas para os jogos que ainda não foram processados.
    """
    print("--- EXECUTANDO: Coleta Profunda de Detalhes ---")

    try:
        all_games_response = supabase.table("jogos").select("api_id").execute()
        all_game_ids = {item['api_id'] for item in all_games_response.data}

        processed_game_ids: Set[int] = set()
        # Tenta ler `jogos_processados` (mais confiável). Se não existir, faz fallback para eventos_jogo.
        try:
            resp = supabase.table("jogos_processados").select("jogo_api_id,status").execute()
            skip_statuses = {"PROCESSED"}
            if not reprocess_no_events:
                skip_statuses.add("NO_EVENTS")
            processed_game_ids = {item['jogo_api_id'] for item in (resp.data or []) if item.get('status') in skip_statuses}
            print(f"Usando 'jogos_processados' para pular IDs com status: {skip_statuses}")
        except Exception:
            # fallback antigo
            resp2 = supabase.table("eventos_jogo").select("jogo_api_id").execute()
            processed_game_ids = {item['jogo_api_id'] for item in (resp2.data or [])}

        print(f"Total de jogos no banco: {len(all_game_ids)}")
        print(f"Jogos a pular (já processados): {len(processed_game_ids)}")

        games_to_process = sorted(list(all_game_ids - processed_game_ids))

        if not games_to_process:
            print("Todos os jogos já possuem detalhes. Nenhuma ação necessária.")
            return

        print(f"Iniciando coleta de detalhes para {len(games_to_process)} novos jogos...")
        for i, game_id in enumerate(games_to_process):
            print(f"\nProcessando jogo {i+1}/{len(games_to_process)} (ID: {game_id})...")
            fetch_and_save_game_details(game_id, dry_run=dry_run)
            time.sleep(1)

    except Exception as e:
        print(f"[ERRO FATAL] na coleta de detalhes: {e}")

    print("\n--- Coleta Profunda de Detalhes Concluída ---")


def fetch_and_save_game_details(game_id: int, dry_run: bool = False):
    """
    Busca e salva todos os detalhes de um único jogo.
    """
    # Prioriza a chamada ao endpoint `/web/game/` (contém payload rico do jogo)
    game_page_url = (
        f"https://webws.365scores.com/web/game/?appTypeId=5&langId=31&timezoneName=America/Sao_Paulo"
        f"&userCountryId=21&gameId={game_id}&topBookmaker=161"
    )

    # Estatísticas: base com parâmetros comuns; tentaremos variantes que costumam liberar jogadores
    base_stats_url = (
        f"https://webws.365scores.com/web/game/stats/?games={game_id}"
        f"&appTypeId=5&langId=31&timezoneName=America/Sao_Paulo&userCountryId=21"
    )

    # Opcional: buscar detalhes individuais do atleta para enriquecer `jogadores` (desativado por padrão)
    FETCH_ATHLETE_DETAILS = False

    # Primeiro tente o endpoint /web/game/?gameId=...
    game_page_data = fetch_data(game_page_url)

    # Tenta múltiplas variações de parâmetros que, empiricamente, liberam dados de jogadores
    stats_param_variants = [
        "&includePlayers=1&includePlayerStats=1",
        "&withPlayers=1&includePlayerStats=1",
        "&includePlayers=1&detailed=true",
        "&showPlayers=1",
        "",
    ]

    stats_data = None
    used_params: Optional[str] = None
    used_endpoint: Optional[str] = None
    last_non_none = None

    # Se o endpoint /web/game/ já retornou dados úteis (lineups/events), trate como 'details'
    details_data = None
    if game_page_data and isinstance(game_page_data, dict) and game_page_data.get("game"):
        # normalize to look like previous 'details' shape
        details_data = {"games": [game_page_data.get("game")]} if game_page_data.get("game") else None
        # if lineups/events exist directly on game, we can consider it as providing details
        if details_data and (details_data["games"][0].get("lineups") or details_data["games"][0].get("events")):
            used_endpoint = "game"

    # Caso não tenha sido suficiente, probe o endpoint de stats com variantes — priorizando a variante com players
    if not used_endpoint:
        for p in stats_param_variants:
            url = base_stats_url + p
            sd = fetch_data(url)
            if sd:
                last_non_none = sd
                if has_player_data(sd):
                    stats_data = sd
                    used_params = p
                    used_endpoint = "stats"
                    break
        # se nada encontrou players, usa o último retorno válido (mesmo sem players)
        if not stats_data:
            stats_data = last_non_none

    # Se ainda não encontrou dados de jogador, tente uma sondagem mais agressiva com combinações de parâmetros
    if stats_data and not has_player_data(stats_data):
        aggressive_variants = []
        appTypeIds = [5, 1]
        langIds = [31, 1]
        userCountryIds = [21, 1]
        include_players_flags = ["&includePlayers=1&includePlayerStats=1", "&withPlayers=1&includePlayerStats=1", "&includePlayers=1&detailed=true", "&showPlayers=1", ""]
        topBookmakers = [161, 156, 0]
        for a in appTypeIds:
            for l in langIds:
                for uc in userCountryIds:
                    for pf in include_players_flags:
                        for tb in topBookmakers:
                            s = f"&appTypeId={a}&langId={l}&timezoneName=America/Sao_Paulo&userCountryId={uc}{pf}&topBookmaker={tb}"
                            aggressive_variants.append(s)

        for p in aggressive_variants:
            url = f"https://webws.365scores.com/web/game/stats/?games={game_id}" + p
            sd = fetch_data(url)
            if sd and has_player_data(sd):
                stats_data = sd
                used_params = p
                used_endpoint = "stats_aggressive"
                print(f"  [INFO] Variante agressiva encontrou dados com params: {p}")
                break

        # Se ainda sem dados por jogador, tente endpoints alternativos conhecidos (players/playersStats/lineups)
        if stats_data and not has_player_data(stats_data):
            try:
                sd_alt, alt_url = try_player_endpoints(game_id)
                if sd_alt:
                    stats_data = sd_alt
                    used_endpoint = f"alt_endpoint:{alt_url}"
                    print(f"  [INFO] Endpoint alternativo encontrou dados de jogador: {alt_url}")
            except Exception:
                pass

    # 'stats' é a fonte primária dos dados de jogador; 'details' (ou /web/game) é complementar
    # Se recebemos `stats_data` mas ele não contém dados por jogador, tentamos fallback via Playwright
    if stats_data and not has_player_data(stats_data):
        if PLAYWRIGHT_AVAILABLE:
            try:
                print("  [INFO] stats_data presente mas sem dados de jogador — tentando fallback via Playwright...")
                browser_result = fetch_game_via_playwright(game_id)
                if browser_result and has_player_data(browser_result):
                    stats_data = browser_result
                    used_endpoint = "playwright"
                    print("  [INFO] Fallback via Playwright encontrou dados de jogador.")
                else:
                    print("  [WARN] Fallback via Playwright não encontrou dados de jogador.")
            except Exception as e:
                print(f"  [ERRO] Fallback Playwright falhou: {e}")

    if not stats_data and not details_data:
        print(f"  [AVISO] Faltam dados de 'stats' e 'game' para o jogo {game_id}. Marcando como falha.")
        # Antes de falhar, tentamos um fallback robusto via navegador (Playwright)
        if PLAYWRIGHT_AVAILABLE:
            try:
                print("  [INFO] Tentando fallback via Playwright (navegador) para capturar stats de jogador...")
                browser_result = fetch_game_via_playwright(game_id)
                if browser_result and has_player_data(browser_result):
                    stats_data = browser_result
                    used_endpoint = "playwright"
                    print("  [INFO] Fallback via Playwright encontrou dados de jogador.")
                else:
                    print("  [WARN] Fallback via Playwright não trouxe dados de jogador.")
            except Exception as e:
                print(f"  [ERRO] Fallback Playwright falhou: {e}")
        else:
            print("  [WARN] Playwright não disponível. Para ativar, instale: 'pip install playwright' e execute 'playwright install'.")

        if not stats_data and not details_data:
            mark_processing_status(game_id, "FAILED_STATS_COLLECTION", details=None)
            return

    teams_to_save: List[Dict[str, Any]] = []
    players_to_save: List[Dict[str, Any]] = []
    player_stats_to_save: List[Dict[str, Any]] = []
    team_stats_to_save: List[Dict[str, Any]] = []
    lineups_to_save: List[Dict[str, Any]] = []
    events_to_save: List[Dict[str, Any]] = []

    def safe_dump(obj: Any) -> str:
        try:
            return json.dumps(obj, ensure_ascii=False)
        except Exception:
            return "{}"

    def mark_event_status(status_type: str):
        # Deprecated: manter wrapper compatível com chamadas antigas, mas usar jogos_processados
        mark_processing_status(game_id, status_type)

    # Processar Times e Estatísticas de Times
    if stats_data and stats_data.get("competitors"):
        for team_raw in stats_data["competitors"]:
            teams_to_save.append({"api_id": team_raw.get("id"), "name": team_raw.get("name")})
            if team_raw.get("statistics"):
                for stat_name, stat_value in team_raw["statistics"].items():
                    team_stats_to_save.append({
                        "jogo_api_id": game_id,
                        "team_api_id": team_raw.get("id"),
                        "type": stat_name,
                        "value": stat_value
                    })

    # Processar Jogadores e Estatísticas de Jogadores
    if stats_data and has_player_data(stats_data):
        # Caso comum: payloads de 'lineups' possuem top-level `members` com `athleteId` e `stats` por member
        if isinstance(stats_data, dict) and stats_data.get("members") and isinstance(stats_data.get("members"), list):
            for member in stats_data.get("members", []):
                athlete_id = member.get("athleteId") or member.get("id")
                if not athlete_id:
                    continue

                players_to_save.append({
                    "api_id": athlete_id,
                    "name": member.get("name"),
                    "short_name": member.get("shortName"),
                    "jersey_number": member.get("jerseyNumber"),
                    "team_api_id": member.get("competitorId") or member.get("competitorNum") or member.get("teamId"),
                })

                # registra escalação a partir do payload de members
                lineups_to_save.append({
                    "jogo_api_id": game_id,
                    "player_api_id": athlete_id,
                    "team_api_id": member.get("competitorId") or member.get("competitorNum") or member.get("teamId"),
                    "is_starter": True if member.get("status") == 1 else False,
                    "status": member.get("statusText"),
                    "position": member.get("positionName") or (member.get("position") and member.get("position").get("name") if isinstance(member.get("position"), dict) else None),
                })

                # normaliza estatísticas por jogador (cada member pode ter lista 'stats')
                for s in member.get("stats", []):
                    player_stats_to_save.append({
                        "jogo_api_id": game_id,
                        "player_api_id": athlete_id,
                        "team_api_id": member.get("competitorId") or member.get("competitorNum") or member.get("teamId"),
                        "stat_type": s.get("type"),
                        "stat_name": s.get("name"),
                        "value": s.get("value"),
                    })
        else:
            # Fallback: tenta localizar listas com players em estruturas variadas
            player_stats_list = stats_data.get("playersStats") or []
            if not player_stats_list:
                def _find_lists(o: Any):
                    found = []
                    if isinstance(o, dict):
                        for k, v in o.items():
                            if isinstance(v, list):
                                # só consideramos listas candidatas se os itens aparentam ser jogadores
                                # Endurecido: exige pelo menos 'jerseyNumber' E pelo menos um de 'athleteId', 'playerId', 'position', 'shortName'
                                def is_player_like(item):
                                    if not isinstance(item, dict):
                                        return False
                                    has_jersey = 'jerseyNumber' in item
                                    has_optional = any(x in item for x in ('athleteId', 'playerId', 'position', 'shortName'))
                                    has_name = 'name' in item  # Evita stats puras que têm 'name' mas não são players
                                    return has_jersey and has_optional and has_name
                                if all(is_player_like(i) for i in v):
                                    found.append(v)
                            else:
                                found.extend(_find_lists(v))
                    elif isinstance(o, list):
                        for i in o:
                            found.extend(_find_lists(i))
                    return found

                lists = _find_lists(stats_data)
                if lists:
                    player_stats_list = lists[0]

            for player_stat in player_stats_list:
                player_raw = player_stat.get("player") or player_stat.get("playerRaw") or player_stat
                # heurística endurecida: identificar se o item parece ser um jogador (exige jerseyNumber + pelo menos um opcional)
                def is_player_like(item):
                    if not isinstance(item, dict):
                        return False
                    has_jersey = 'jerseyNumber' in item
                    has_optional = any(k in item for k in ('athleteId', 'playerId', 'position', 'shortName'))
                    return has_jersey and has_optional
                if not is_player_like(player_raw):
                    # pula items que não parecem representar jogadores
                    continue

                athlete_id = player_raw.get("athleteId") or player_raw.get("id") or player_stat.get("playerId") or player_stat.get("id")
                if not athlete_id:
                    continue

                players_to_save.append({
                    "api_id": athlete_id,
                    "name": player_raw.get("name") or player_stat.get("name"),
                })

                # normaliza stats em formatos dict/list
                stats_blob = player_stat.get("stats") or player_stat
                if isinstance(stats_blob, dict):
                    for k, v in stats_blob.items():
                        if k in ("player", "playerId", "athleteId"): continue
                        player_stats_to_save.append({
                            "jogo_api_id": game_id,
                            "player_api_id": athlete_id,
                            "stat_name": str(k),
                            "value": str(v) if v is not None else None,
                        })
                elif isinstance(stats_blob, list):
                    for s in stats_blob:
                        name = s.get("name") or s.get("stat") or s.get("type")
                        val = s.get("value") or s.get("v")
                        if name:
                            player_stats_to_save.append({
                                "jogo_api_id": game_id,
                                "player_api_id": athlete_id,
                                "stat_name": str(name),
                                "value": str(val) if val is not None else None,
                            })

    game_details = None
    if details_data and details_data.get("games"):
        game_details = details_data["games"][0]
    elif details_data is None and game_page_data and isinstance(game_page_data, dict) and game_page_data.get("game"):
        # fallback: normalize if we didn't convert above
        game_details = game_page_data.get("game")

    # Processar Escalações (somente se 'details' estiver disponível)
    if game_details and game_details.get("lineups"):
        for lineup in game_details["lineups"]:
            team_id = lineup.get("competitorId")
            for member in lineup.get("members", []):
                athlete_id = member.get("athleteId") or member.get("id")
                lineups_to_save.append({
                    "jogo_api_id": game_id,
                    "player_api_id": athlete_id,
                    "team_api_id": team_id,
                    "is_starter": lineup.get("isStarter", False),
                    "position": member.get("positionName")
                })

    # Processar Eventos do Jogo (somente se 'details' estiver disponível) ou se `stats_data.chartEvents` existir
    if (game_details and game_details.get("events")) or (stats_data and isinstance(stats_data, dict) and stats_data.get("chartEvents") and stats_data.get("chartEvents").get("events")):
        events_source = []
        if game_details and game_details.get("events"):
            events_source.extend(game_details.get("events") or [])
        if stats_data and isinstance(stats_data, dict) and stats_data.get("chartEvents") and stats_data.get("chartEvents").get("events"):
            events_source.extend(stats_data.get("chartEvents").get("events") or [])

        for event in events_source:
            # Normaliza tipos: alguns campos vêm como strings com decimais ("10.0").
            def _to_int_maybe(v):
                if v is None:
                    return None
                try:
                    if isinstance(v, int):
                        return v
                    fv = float(v)
                    return int(fv)
                except Exception:
                    try:
                        return int(str(v))
                    except Exception:
                        return None

            event_key = event.get("id") or event.get("key") or event.get("eventId")
            events_to_save.append({
                "api_id": _to_int_maybe(event_key),
                "jogo_api_id": game_id,
                "type": event.get("name") or event.get("type"),
                "minute": _to_int_maybe(event.get("time") or event.get("gameTime") or event.get("minute")),
                "player_api_id": _to_int_maybe(event.get("playerId")),
                "team_api_id": _to_int_maybe(event.get("competitorId") or event.get("competitorNum") or event.get("competitor")),
                "detail": event
            })

    # Salvar dados no banco
    # Normaliza player_stats_to_save: pode conter dicts com múltiplas chaves
    normalized_player_stats: List[Dict[str, Any]] = []
    for rec in player_stats_to_save:
        jogo = rec.get("jogo_api_id")
        pid = rec.get("player_api_id")
        teamid = rec.get("team_api_id") or rec.get("team")
        # se rec tem chave 'stats' como dict/list
        stats_blob = rec.get("stats") or {}
        if isinstance(stats_blob, dict):
            for k, v in stats_blob.items():
                normalized_player_stats.append({
                    "jogo_api_id": jogo,
                    "player_api_id": pid,
                    "team_api_id": teamid,
                    "stat_name": str(k),
                    "value": str(v) if v is not None else None,
                })
        elif isinstance(stats_blob, list):
            for s in stats_blob:
                name = s.get("name") or s.get("stat") or s.get("type")
                val = s.get("value") or s.get("v")
                if name:
                    normalized_player_stats.append({
                        "jogo_api_id": jogo,
                        "player_api_id": pid,
                        "team_api_id": teamid,
                        "stat_name": str(name),
                        "value": str(val) if val is not None else None,
                    })
        else:
            # Caso rec contenha pares diretos além de jogo/player
            for k, v in rec.items():
                if k in ("jogo_api_id", "player_api_id", "team_api_id", "team", "stats"): continue
                normalized_player_stats.append({
                    "jogo_api_id": jogo,
                    "player_api_id": pid,
                    "team_api_id": teamid,
                    "stat_name": str(k),
                    "value": str(v) if v is not None else None,
                })

    if dry_run:
        print(f"  [DRY-RUN] Resumo do que seria inserido para jogo {game_id}:")
        print(f"    - Times: {len(teams_to_save)} ({[t['name'] for t in teams_to_save[:3]]}...)" if teams_to_save else "    - Times: 0")
        print(f"    - Jogadores: {len(players_to_save)} ({[p['name'] for p in players_to_save[:3]]}...)" if players_to_save else "    - Jogadores: 0")
        print(f"    - Estatísticas de time: {len(team_stats_to_save)}")
        print(f"    - Estatísticas de jogador: {len(normalized_player_stats)}")
        print(f"    - Escalações: {len(lineups_to_save)}")
        print(f"    - Eventos: {len(events_to_save)}")
        print(f"  [DRY-RUN] Nenhum dado salvo no banco.")
        return

    try:

        # Filtra eventos sem `api_id` — o DB exige NOT NULL em `eventos_jogo.api_id`.
        if events_to_save:
            orig_count = len(events_to_save)
            events_to_save = [e for e in events_to_save if e.get('api_id') is not None]
            filtered_count = len(events_to_save)
            if filtered_count < orig_count:
                print(f"  [WARN] {orig_count - filtered_count} eventos sem 'api_id' removidos antes do insert.")

        if events_to_save:
            # Protege contra inserções de colunas desconhecidas no PostgREST/Supabase
            # (ex: quando o DB ainda não possui a coluna 'detail').
            if not table_has_column('eventos_jogo', 'detail'):
                # remove campo 'detail' de todos os eventos se a coluna não existe
                for ev in events_to_save:
                    if 'detail' in ev:
                        ev.pop('detail', None)

            safe_upsert("eventos_jogo", events_to_save, on_conflict="api_id")
            # marca como processado após salvar eventos
            details_note = None
            if used_endpoint == "game":
                details_note = "game_endpoint"
            else:
                details_note = f"stats{used_params or ''}"
            mark_processing_status(game_id, "PROCESSED", details=details_note)
        else:
            # Marca o jogo como processado mesmo sem eventos para não reprocessar
            # inclui nos detalhes quais parâmetros/endpoint (se houver) foram usados para obter stats
            details_note = None
            if used_endpoint == "game":
                details_note = "game_endpoint"
            else:
                details_note = f"stats{used_params or ''}"
            mark_processing_status(game_id, "NO_EVENTS", details=details_note)
        print(f"  Detalhes do jogo {game_id} salvos com sucesso.")
    except Exception as e:
        print(f"  [ERRO] Falha ao salvar detalhes do jogo {game_id}: {e}")
        try:
            # Marca como falha para evitar retentativas
            mark_event_status("DB_SAVE_ERROR")
        except Exception as inner_e:
            print(f"  [ERRO CRÍTICO] Falha ao marcar jogo {game_id} como 'DB_SAVE_ERROR': {inner_e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Coletor de dados do 365Scores para o Brasileirão.")
    parser.add_argument(
        "fase",
        choices=["jogos", "detalhes", "games", "details"],
        help="A fase da coleta a ser executada: 'jogos'/'games' para a coleta ampla, 'detalhes'/'details' para a coleta profunda."
    )
    parser.add_argument(
        "--reprocess-no-events",
        action="store_true",
        help="Se fornecido, reprocessa jogos anteriormente marcados como NO_EVENTS (útil para tentar novos parâmetros)."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Modo de teste: parseia e mostra o que seria inserido, mas não salva no banco de dados."
    )
    args = parser.parse_args()

    if args.fase in ("jogos", "games"):
        run_collect_games(dry_run=args.dry_run)
    elif args.fase in ("detalhes", "details"):
        run_collect_details(getattr(args, 'reprocess_no_events', False), dry_run=args.dry_run)
