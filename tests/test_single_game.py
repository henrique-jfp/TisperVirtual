import sys
sys.path.append('coleta')
from api_coleta_365scores import fetch_and_save_game_details

# Testar apenas um jogo recente
game_id = 535273  # Jogo mais recente finalizado
print(f"Testando extração de detalhes para jogo {game_id}...")
fetch_and_save_game_details(game_id, dry_run=True)