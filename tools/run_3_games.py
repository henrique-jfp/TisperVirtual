import os
import importlib.util
import time

# Carrega dinamicamente o módulo collector
MODULE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'coleta', 'api_coleta_365scores.py'))
spec = importlib.util.spec_from_file_location("api_coleta_365scores", MODULE_PATH)
api_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(api_mod)

fetch_and_save_game_details = api_mod.fetch_and_save_game_details

GAME_IDS = [4309082, 4309098, 4309116]

for gid in GAME_IDS:
    print(f"\nExecutando coleta profunda para jogo {gid}")
    try:
        fetch_and_save_game_details(gid)
    except Exception as e:
        print(f"Erro ao processar {gid}: {e}")
    time.sleep(1)
print("\n--- Execução de 3 jogos concluída ---")
