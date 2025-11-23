import re
from supabase import create_client

# Extrai SUPABASE_URL e SUPABASE_KEY diretamente do arquivo do coletor
def extract_credentials(path):
    url = None
    key = None
    with open(path, 'r', encoding='utf-8') as f:
        for raw_line in f:
            line = raw_line.strip()
            if line.startswith('SUPABASE_URL') and ('"' in line or "'" in line):
                # pega entre as primeiras aspas
                parts = line.split('"')
                if len(parts) >= 3:
                    url = parts[1]
                else:
                    parts = line.split("'")
                    if len(parts) >= 3:
                        url = parts[1]
            if line.startswith('SUPABASE_KEY') and ('"' in line or "'" in line):
                parts = line.split('"')
                if len(parts) >= 3:
                    key = parts[1]
                else:
                    parts = line.split("'")
                    if len(parts) >= 3:
                        key = parts[1]
            if url and key:
                break
    return url, key

SUPABASE_URL, SUPABASE_KEY = extract_credentials(r"c:\\TradeComigo\\coleta\\api_coleta_365scores.py")
if not SUPABASE_URL or not SUPABASE_KEY:
    raise SystemExit("Não foi possível extrair SUPABASE_URL/SUPABASE_KEY do coletor")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def count_table(table_name):
    try:
        # Tenta via REST (PostgREST) para obter o count exato através do header 'Content-Range'
        import requests
        url = SUPABASE_URL.rstrip('/') + f"/rest/v1/{table_name}?select=*"
        headers = {
            'apikey': SUPABASE_KEY,
            'Authorization': f'Bearer {SUPABASE_KEY}',
            'Accept': 'application/json',
            'Prefer': 'count=exact'
        }
        r = requests.get(url, headers=headers, timeout=(5, 15))
        if r.status_code != 200:
            print(f"{table_name}: HTTP {r.status_code} ao consultar REST - {r.text[:200]}")
            return
        cr = r.headers.get('Content-Range') or r.headers.get('content-range')
        if cr:
            # formato esperado: items start-end/total
            parts = cr.split('/')
            if len(parts) == 2:
                total = parts[1]
                print(f"{table_name}: total = {total} (via Content-Range)")
                return
        # fallback: contar itens retornados (pode estar limitado)
        try:
            data = r.json()
            print(f"{table_name}: {len(data)} linhas retornadas (via JSON)")
        except Exception:
            print(f"{table_name}: resposta OK mas não foi possível parsear JSON")
    except Exception as e:
        print(f"Erro ao consultar {table_name}: {e}")

if __name__ == '__main__':
    for t in ('eventos_jogo', 'jogadores', 'estatisticas_jogador'):
        count_table(t)
    print('\nVerificando outras tabelas relacionadas...')
    for t in ('jogos', 'jogos_processados', 'raw_game_data'):
        count_table(t)

    # Inspecionar raw_game_data para alguns jogos processados (amostra)
    sample_ids = [4309082, 4309098, 4309116, 9176256, 712887]
    print('\nInspecionando raw_game_data para alguns jogos (verifica presença de dados de jogador)...')
    import requests, json
    for gid in sample_ids:
        url = SUPABASE_URL.rstrip('/') + f"/rest/v1/raw_game_data?jogo_api_id=eq.{gid}&select=stats_json,details_json"
        headers = {
            'apikey': SUPABASE_KEY,
            'Authorization': f'Bearer {SUPABASE_KEY}',
            'Accept': 'application/json'
        }
        try:
            r = requests.get(url, headers=headers, timeout=(5,15))
            if r.status_code != 200:
                print(f"  jogo {gid}: HTTP {r.status_code} ao buscar raw_game_data")
                continue
            arr = r.json()
            if not arr:
                print(f"  jogo {gid}: nenhum raw_game_data encontrado")
                continue
            row = arr[0]
            stats = row.get('stats_json')
            details = row.get('details_json')
            has_players = False
            snippet = None
            for s in (stats, details):
                if not s:
                    continue
                try:
                    obj = json.loads(s)
                except Exception:
                    continue
                # procura chaves comuns
                if isinstance(obj, dict):
                    if 'players' in obj or 'playersStats' in obj or 'competitors' in obj:
                        has_players = True
                        snippet = list(obj.keys())[:5]
                        break
                elif isinstance(obj, list) and obj:
                    snippet = [type(obj[0]).__name__]
            print(f"  jogo {gid}: has_players={has_players}; snippet_keys={snippet}")
            if not has_players:
                # imprime um pequeno trecho do stats_json para inspeção (limite 1000 chars)
                excerpt = (stats or details or '')[:1000]
                print(f"    excerpt: {excerpt[:500]!r}... (truncado)")
        except Exception as e:
            print(f"  jogo {gid}: erro ao buscar raw_game_data: {e}")
