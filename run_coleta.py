import os
import pandas as pd
from dotenv import load_dotenv
import logging
from typing import Dict, Any, Optional

from coleta.api_coleta_365scores import ThreeSixtyFiveScoresCollector, Config as ScraperConfig
from coleta.banco_dados import BancoDados

# --- Configuração de Logging ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def process_game_dataframes(game_data: Dict[str, Any]) -> Optional[Dict[str, pd.DataFrame]]:
    """
    Processa os dados brutos de um jogo e retorna um dicionário de DataFrames.
    Isolado para facilitar testes e manutenção.
    """
    if not game_data or "game_info" not in game_data or "game_statistics" not in game_data:
        logger.warning("Payload de dados do jogo está incompleto ou mal formatado. Pulando.")
        return None

    # Acessa os dados usando as chaves corretas retornadas pelo coletor
    game_info = game_data["game_info"]
    game_stats = game_data["game_statistics"]
    player_stats = game_data["player_statistics"]
    # --- Times ---
    home_team = game_info["homeCompetitor"]
    away_team = game_info["awayCompetitor"]

    # --- DataFrame de Jogo (será usado para inserir na tabela 'jogos') ---
    df_jogo = pd.DataFrame([{
        "api_url": ScraperConfig.build_url_from_id(game_info["id"]),
        "status": game_info["statusText"],
        "start_time": pd.to_datetime(game_info.get("startTime"), unit='s', utc=True),
        "home_score": game_info["scores"]["home"],
        "away_score": game_info["scores"]["away"],
        "raw_payload": game_data,
    }])

    # --- DataFrame de Estatísticas do Time ---
    stats_list = []
    for stat_group in game_stats:
        for stat in stat_group.get("members", []):
            # Ignora estatísticas que não são divididas por time (ex: Posse de Bola)
            if len(stat.get("results", [])) == 2:
                stats_list.append({
                    "team_api_id": home_team["id"],
                    "type": stat["name"],
                    "value": stat["results"][0],
                })
                stats_list.append({
                    "team_api_id": away_team["id"],
                    "type": stat["name"],
                    "value": stat["results"][1],
                })
    df_estatisticas_time = pd.DataFrame(stats_list)

    # --- DataFrames de Jogadores e Estatísticas de Jogadores ---
    players_list = []
    player_stats_list = []

    for member in player_stats:
        athlete = member.get("athlete", {})
        if not athlete:
            continue

        players_list.append({
            "api_id": athlete["id"],
            "name": athlete["name"],
            "short_name": athlete.get("shortName"),
            "position": athlete.get("positionName"),
            "jersey_num": athlete.get("jerseyNum"),
            "nationality": athlete.get("country", {}).get("name"),
            "team_api_id": member["competitorId"]
        })

        for stat in member.get("statistics", []):
            player_stats_list.append({
                "player_api_id": athlete["id"],
                "stat_name": stat["name"],
                "value": stat["value"]
            })

    df_jogadores = pd.DataFrame(players_list).drop_duplicates(subset=["api_id"])
    df_estatisticas_jogador = pd.DataFrame(player_stats_list)

    return {
        "jogo": df_jogo,
        "estatisticas_time": df_estatisticas_time,
        "jogadores": df_jogadores,
        "estatisticas_jogador": df_estatisticas_jogador,
    }


def save_game_data(db: BancoDados, game_api_id: str, raw_data: Dict[str, Any], competition_id: int):
    """
    Orquestra o processamento e salvamento de todos os dados de um único jogo.
    """
    logger.info(f"Processando e salvando dados para o jogo com API ID: {game_api_id}")
    
    # 1. Processar dados brutos em DataFrames
    dataframes = process_game_dataframes(raw_data)
    if not dataframes:
        raise ValueError("Falha ao processar os dados brutos em DataFrames.")

    # Extrair informações essenciais do payload
    game_info = raw_data["game_info"]
    home_team_data = game_info["homeCompetitor"]
    away_team_data = game_info["awayCompetitor"]

    # Iniciar uma transação para garantir a atomicidade
    with db.engine.begin() as connection:
        # 2. Garantir que a competição e os times existam e obter seus IDs
        comp_id = db.get_or_create_competition(
            name=ScraperConfig.COMPETITION_NAME,
            api_id=competition_id,
            connection=connection
        )
        home_team_id = db.get_or_create_team(
            name=home_team_data["name"],
            api_id=home_team_data["id"],
            country=home_team_data.get("country", {}).get("name"),
            connection=connection
        )
        away_team_id = db.get_or_create_team(
            name=away_team_data["name"],
            api_id=away_team_data["id"],
            country=away_team_data.get("country", {}).get("name"),
            connection=connection
        )

        # 3. Inserir o jogo e obter o ID primário
        game_df = dataframes["jogo"]
        game_id = db.insert_game(
            game_df=game_df,
            competition_id=comp_id,
            home_team_id=home_team_id,
            away_team_id=away_team_id,
            connection=connection
        )
        logger.info(f"Jogo inserido com ID: {game_id}")

        # 4. Inserir/Atualizar jogadores
        # O método `inserir_dataframe` com `if_exists='append'` e PK definida lida com o upsert
        db.inserir_dataframe(dataframes["jogadores"], "jogadores", connection=connection, if_exists='append', index=False)
        logger.info(f"Foram processados {len(dataframes['jogadores'])} registros de jogadores.")
        
        # 5. Inserir estatísticas (agora com o ID do jogo)
        stats_time_df = dataframes["estatisticas_time"]
        stats_time_df["jogo_id"] = game_id
        db.inserir_dataframe(stats_time_df, "estatisticas_time", connection=connection, if_exists='append', index=False)
        
        stats_jog_df = dataframes["estatisticas_jogador"]
        stats_jog_df["jogo_id"] = game_id
        db.inserir_dataframe(stats_jog_df, "estatisticas_jogador", connection=connection, if_exists='append', index=False)
        logger.info("Estatísticas do jogo e dos jogadores foram salvas.")

def run():
    """
    Orquestra o processo completo de coleta e armazenamento de dados.
    """
    load_dotenv()
    
    # Define o caminho para o banco de dados SQLite local
    db_path = os.path.join(os.path.dirname(__file__), 'tradecomigo.db')
    DATABASE_URL = f"sqlite:///{db_path}"
    logger.info(f"Usando banco de dados SQLite em: {db_path}")

    collector = ThreeSixtyFiveScoresCollector()
    db = BancoDados(DATABASE_URL)
    # Com SQLite, o fallback REST não é mais o foco principal.
    fallback_available = False 

    # Tenta conectar ao banco via SQL
    try:
        db.conectar()
    except Exception as e:
        logger.critical(f"Não foi possível conectar ao banco de dados local SQLite: {e}. Abortando.")
        return

    try:
        # 1. Obter todos os IDs de jogos da competição configurada
        game_ids = collector.get_all_game_ids()
        if not game_ids:
            logger.warning("Nenhum ID de jogo encontrado pela API. Encerrando.")
            return

        logger.info(f"Encontrados {len(game_ids)} jogos para processar.")

        # 2. Processar cada jogo
        for i, game_api_id in enumerate(sorted(list(game_ids))):
            logger.info(f"--- Processando Jogo {i+1}/{len(game_ids)} (API ID: {game_api_id}) ---")

            # Construir URL para verificação e logging
            game_url = ScraperConfig.build_url_from_id(game_api_id)

            # Verificar se a URL do jogo já foi processada com sucesso
            already_exists = False
            if getattr(db, 'engine', None):
                already_exists = db.check_if_game_exists(game_url)
            if already_exists:
                logger.info(f"Jogo com URL {game_url} já existe no banco. Pulando.")
                continue

            try:
                # Obter dados brutos da API
                raw_data = collector.get_full_data_for_game(game_api_id)
                if not raw_data:
                    logger.warning(f"Não foi possível obter dados para o jogo {game_api_id}. Pulando.")
                    continue

                # Se há engine SQL ativa, tenta salvar no banco relacional
                if getattr(db, 'engine', None):
                    save_game_data(db, game_api_id, raw_data, ScraperConfig.COMPETITION_ID)
                    logger.info(f"Jogo {game_api_id} processado e salvo com sucesso no banco de dados.")
                else:
                    logger.error('Conexão com o banco de dados não está disponível. Dados não foram salvos.')

            except Exception as e:
                logger.error(f"Erro ao processar ou salvar dados do jogo {game_api_id}: {e}", exc_info=True)

    except Exception as e:
        logger.critical(f"Ocorreu um erro crítico no orquestrador: {e}", exc_info=True)
    finally:
        if 'db' in locals() and db.engine:
            db.desconectar()
            logger.info("Execução finalizada.")


if __name__ == "__main__":
    run()
