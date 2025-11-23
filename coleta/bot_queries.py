from supabase import create_client, Client
from typing import Dict, Any, Optional

# --- Configurações e Conexão ---
# Reutilize as mesmas credenciais do seu script de coleta
SUPABASE_URL: str = "https://nflmvptqgicabovfmnos.supabase.co"
SUPABASE_KEY: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5mbG12cHRxZ2ljYWJvdmZtbm9zIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM3NzEzNTAsImV4cCI6MjA3OTM0NzM1MH0.l-RuwMrLgQgfjp8XZQ7bpEwfKODo7qKEXOhGR49xJ9c"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_team_id_by_name(name: str) -> Optional[int]:
    """Busca o api_id de um time pelo nome."""
    try:
        response = supabase.table("times").select("api_id").ilike("name", f"%{name}%").limit(1).execute()
        if response.data:
            return response.data[0]['api_id']
        return None
    except Exception as e:
        print(f"[ERRO] ao buscar ID do time '{name}': {e}")
        return None

def get_last_game(team_name: str) -> Optional[Dict[str, Any]]:
    """
    Busca o último jogo CONCLUÍDO de um time específico, de forma bidirecional.
    """
    print(f"Buscando último jogo para: {team_name}")
    team_id = get_team_id_by_name(team_name)
    if not team_id:
        print(f"Time '{team_name}' não encontrado.")
        return None

    try:
        # A consulta precisa ser bidirecional (time pode ser mandante OU visitante)
        response = supabase.table("jogos").select("*, home_team:times!jogos_home_team_api_id_fkey(name), away_team:times!jogos_away_team_api_id_fkey(name)") \
            .filter("status", "eq", "Fim") \
            .or_(f"home_team_api_id.eq.{team_id},away_team_api_id.eq.{team_id}") \
            .order("start_time", desc=True) \
            .limit(1) \
            .execute()
        
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        print(f"[ERRO] ao buscar último jogo: {e}")
        return None

def get_head_to_head(team1_name: str, team2_name: str) -> Optional[Dict[str, Any]]:
    """
    Busca o último confronto direto entre dois times.
    """
    print(f"Buscando confronto direto: {team1_name} vs {team2_name}")
    team1_id = get_team_id_by_name(team1_name)
    team2_id = get_team_id_by_name(team2_name)

    if not team1_id or not team2_id:
        print("Um ou ambos os times não foram encontrados.")
        return None

    try:
        # A consulta verifica as duas combinações possíveis de mandante/visitante
        query = f"home_team_api_id.eq.{team1_id},away_team_api_id.eq.{team2_id}"
        inverse_query = f"home_team_api_id.eq.{team2_id},away_team_api_id.eq.{team1_id}"
        
        response = supabase.table("jogos").select("*, home_team:times!jogos_home_team_api_id_fkey(name), away_team:times!jogos_away_team_api_id_fkey(name)") \
            .or_(f"and({query}),and({inverse_query})") \
            .order("start_time", desc=True) \
            .limit(1) \
            .execute()

        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        print(f"[ERRO] ao buscar confronto direto: {e}")
        return None

if __name__ == '__main__':
    # --- Testes para verificar se a lógica está correta ---
    print("--- EXECUTANDO TESTES DE CONSULTA ---")

    # Teste 1: Último jogo do Fluminense
    last_flu_game = get_last_game("Fluminense")
    if last_flu_game:
        print("\nResultado [Último Jogo do Fluminense]:")
        print(f"  Data: {last_flu_game['start_time']}")
        print(f"  Jogo: {last_flu_game['home_team']['name']} {last_flu_game['home_team_score']} x {last_flu_game['away_team_score']} {last_flu_game['away_team']['name']}")
    else:
        print("\n[FALHA] Não foi possível encontrar o último jogo do Fluminense.")

    # Teste 2: Confronto direto Fluminense x Flamengo
    h2h_game = get_head_to_head("Fluminense", "Flamengo")
    if h2h_game:
        print("\nResultado [Confronto Fluminense x Flamengo]:")
        print(f"  Data: {h2h_game['start_time']}")
        print(f"  Jogo: {h2h_game['home_team']['name']} {h2h_game['home_team_score']} x {h2h_game['away_team_score']} {h2h_game['away_team']['name']}")
    else:
        print("\n[FALHA] Não foi possível encontrar o confronto entre Fluminense e Flamengo.")

    print("\n--- TESTES CONCLUÍDOS ---")
