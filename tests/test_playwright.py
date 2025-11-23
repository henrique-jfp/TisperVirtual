import sys
sys.path.append('coleta')
from api_coleta_365scores import fetch_game_via_playwright

# Testar Playwright para um jogo recente
game_id = 535273
print(f"Testando Playwright para jogo {game_id}...")
result = fetch_game_via_playwright(game_id, timeout=15)
if result:
    print("Encontrou dados!")
    print(f"Tipo de dados: {type(result)}")
    if isinstance(result, dict):
        print(f"Chaves principais: {list(result.keys())}")
        # Verificar se tem dados de jogadores
        from api_coleta_365scores import has_player_data
        if has_player_data(result):
            print("✅ TEM DADOS DE JOGADORES!")
        else:
            print("❌ Não tem dados de jogadores")
else:
    print("❌ Não encontrou dados")