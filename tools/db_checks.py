import os
import importlib.util

# Carrega o módulo collector para obter o objeto 'supabase' já configurado
MODULE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'coleta', 'api_coleta_365scores.py'))
spec = importlib.util.spec_from_file_location("api_coleta_365scores", MODULE_PATH)
api_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(api_mod)

supabase = api_mod.supabase

game_ids = [4309082, 4309098, 4309116]
print("Consultas para jogos:", game_ids)

# Jogadores count
try:
    res = supabase.table("jogadores").select("api_id").in_("api_id", game_ids).execute()
    jogadores = getattr(res, 'data', []) or []
    print(f"jogadores encontrados (api_id in list): {len(jogadores)}")
except Exception as e:
    print("Erro ao consultar jogadores:", e)

# Estatísticas por jogador
try:
    res2 = supabase.table("estatisticas_jogador").select("jogo_api_id").in_("jogo_api_id", game_ids).execute()
    stats = getattr(res2, 'data', []) or []
    print(f"estatisticas_jogador linhas encontradas: {len(stats)}")
except Exception as e:
    print("Erro ao consultar estatisticas_jogador:", e)

# Jogos processados
try:
    res3 = supabase.table("jogos_processados").select("*").in_("jogo_api_id", game_ids).execute()
    proc = getattr(res3, 'data', []) or []
    print("\njogos_processados rows:")
    for r in proc:
        print(r)
    if not proc:
        print("  (nenhuma linha encontrada)")
except Exception as e:
    print("Erro ao consultar jogos_processados:", e)
