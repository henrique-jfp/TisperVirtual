import importlib.util
import sys
from pathlib import Path
import traceback

# Carrega o módulo pelo caminho para reutilizar funções sem executar a CLI principal
spec = importlib.util.spec_from_file_location("api_coleta_365scores", Path("c:/TradeComigo/coleta/api_coleta_365scores.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

# Jogos de exemplo já utilizados nos testes anteriores
sample_game_ids = [4309082, 4309098, 4309116]

for gid in sample_game_ids:
    print(f"\n=== Testando jogo {gid} ===")
    try:
        mod.fetch_and_save_game_details(gid)
    except KeyboardInterrupt:
        print("Interrompido pelo usuário")
        break
    except Exception as e:
        print(f"Erro ao processar jogo {gid}: {e}")
        traceback.print_exc()
