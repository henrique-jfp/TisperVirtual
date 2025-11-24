from typing import Dict, Any, Optional
import os
from dotenv import load_dotenv
from coleta.banco_dados import BancoDados

# Carrega variáveis de ambiente
load_dotenv()

# Define a URL do banco, preferindo SQLITE local se não houver DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///" + os.path.join(os.path.dirname(__file__), "..", "db", "tradecomigo.sqlite3"))

# Instancia e conecta o wrapper do banco
db = BancoDados(DATABASE_URL)
try:
    db.conectar()
except Exception as e:
    print(f"[ERRO] ao conectar com o banco local: {e}")


def get_team_id_by_name(name: str) -> Optional[int]:
    """Busca o ID primário do time pelo nome (case-insensitive)."""
    try:
        query = "SELECT id, api_id, nome FROM times WHERE lower(nome) LIKE :pattern LIMIT 1"
        pattern = f"%{name.lower()}%"
        rows = db._execute_query(query, {'pattern': pattern})
        if rows:
            return rows[0][0]  # id (PK)
        return None
    except Exception as e:
        print(f"[ERRO] ao buscar ID do time '{name}': {e}")
        return None


def get_last_game(team_name: str) -> Optional[Dict[str, Any]]:
    """Retorna o último jogo com status 'finalizado' para o time informado."""
    print(f"Buscando último jogo para: {team_name}")
    team_id = get_team_id_by_name(team_name)
    if not team_id:
        print(f"Time '{team_name}' não encontrado.")
        return None

    try:
        query = (
            "SELECT j.* FROM jogos j "
            "WHERE (j.time_casa_id = :team_id OR j.time_fora_id = :team_id) AND j.status = 'finalizado' "
            "ORDER BY j.data_hora DESC LIMIT 1"
        )
        rows = db._execute_query(query, {'team_id': team_id})
        if not rows:
            return None
        row = rows[0]
        # Converter row para dict simples (nome das colunas não retornadas pelo fetchall()).
        # Para simplicidade, retornamos um mapping mínimo.
        return {
            'id': row[0],
            'api_id': row[1],
            'data_hora': row[4] if len(row) > 4 else None,
            'gols_casa': row[10] if len(row) > 10 else None,
            'gols_fora': row[11] if len(row) > 11 else None,
            'status': row[15] if len(row) > 15 else None,
        }
    except Exception as e:
        print(f"[ERRO] ao buscar último jogo: {e}")
        return None


def get_head_to_head(team1_name: str, team2_name: str) -> Optional[Dict[str, Any]]:
    """Busca o último confronto direto entre dois times."""
    print(f"Buscando confronto direto: {team1_name} vs {team2_name}")
    team1_id = get_team_id_by_name(team1_name)
    team2_id = get_team_id_by_name(team2_name)

    if not team1_id or not team2_id:
        print("Um ou ambos os times não foram encontrados.")
        return None

    try:
        query = (
            "SELECT j.* FROM jogos j WHERE "
            "(j.time_casa_id = :t1 AND j.time_fora_id = :t2) OR (j.time_casa_id = :t2 AND j.time_fora_id = :t1) "
            "ORDER BY j.data_hora DESC LIMIT 1"
        )
        rows = db._execute_query(query, {'t1': team1_id, 't2': team2_id})
        if not rows:
            return None
        row = rows[0]
        return {
            'id': row[0],
            'api_id': row[1],
            'data_hora': row[4] if len(row) > 4 else None,
            'gols_casa': row[10] if len(row) > 10 else None,
            'gols_fora': row[11] if len(row) > 11 else None,
            'status': row[15] if len(row) > 15 else None,
        }
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
