import json
import os
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import logging
from typing import Optional, List, Dict, Any
import hashlib

logger = logging.getLogger(__name__)

class BancoDados:
    """
    Classe para gerenciar a conexão e operações com o banco de dados,
    otimizada para o schema de dados de futebol, compatível com SQLite.
    """
    def __init__(self, db_url: str):
        if not db_url:
            raise ValueError("A URL do banco de dados (db_url) não pode ser vazia.")
        self.db_url = db_url
        self.engine: Optional[Engine] = None

    def conectar(self):
        """Cria o motor de conexão com o banco de dados."""
        try:
            # A URL para SQLite é simples: 'sqlite:///caminho/para/o/arquivo.db'
            self.engine = create_engine(
                self.db_url, pool_pre_ping=True
            )
            with self.engine.connect() as connection:
                logger.info("Conexão com o banco de dados estabelecida com sucesso.")
        except SQLAlchemyError as e:
            logger.error(f"Erro ao conectar com o banco de dados: {e}")
            self.engine = None
            raise
    
    def desconectar(self):
        """Fecha o motor de conexão."""
        if self.engine:
            self.engine.dispose()
            logger.info("Conexão com o banco de dados fechada.")
    
    def _execute_query(self, query: str, params: Optional[Dict] = None) -> List[Any]:
        """Helper para executar uma query SELECT e retornar resultados."""
        if self.engine is None:
            raise RuntimeError("Motor não inicializado. Chame conectar() primeiro.")
        try:
            with self.engine.connect() as connection:
                return self._execute_query_with_conn(connection, query, params)
        except SQLAlchemyError as e:
            logger.error(f"Erro ao executar a query: {query} | Erro: {e}")
            raise
    
    def _execute_query_with_conn(self, connection, query: str, params: Optional[Dict] = None) -> List[Any]:
        """Helper para executar uma query SELECT usando uma conexão existente."""
        try:
            result = connection.execute(text(query), params or {})
            return result.fetchall()
        except SQLAlchemyError as e:
            logger.error(f"Erro ao executar a query com conexão: {query} | Erro: {e}")
            raise
    
    def _execute_insert_returning_id(self, query: str, params: Dict) -> Optional[int]:
        """Helper para executar um INSERT e retornar o ID da linha criada."""
        if self.engine is None:
            raise RuntimeError("Motor não inicializado. Chame conectar() primeiro.")
        with self.engine.begin() as connection: # Inicia transação
            return self._execute_insert_returning_id_with_conn(connection, query, params)

    def _execute_insert_returning_id_with_conn(self, connection, query: str, params: Dict) -> Optional[int]:
        """Helper para executar um INSERT e retornar o ID da linha criada usando uma conexão existente."""
        try:
            result = connection.execute(text(query), params)
            row = result.fetchone()
            return row[0] if row else None
        except IntegrityError:
            logger.warning(f"Aviso de integridade, o item pode já existir. Query: {query}")
            # Em caso de corrida de condição, o item pode ter sido inserido
            # por outro processo. Retornamos None e o chamador deve re-verificar.
            return None
        except SQLAlchemyError as e:
            logger.error(f"Erro ao executar INSERT: {query} | Erro: {e}")
            raise
    
    def get_or_create(self, table_name: str, name_value: str, id_column: str, name_column: str = 'name', extra_cols: Optional[Dict] = None, connection=None) -> Optional[int]:
        """
        Verifica se um registro com o 'name_value' existe. Se sim, retorna o ID.
        Se não, cria o registro e retorna o novo ID.
        Pode receber uma conexão para participar de uma transação.
        """
        if self.engine is None:
            raise RuntimeError("Motor não inicializado. Chame conectar() primeiro.")

        # Determine which connection to use
        if connection:
            conn_to_use = connection
            managed_connection = False
        else:
            conn_to_use = self.engine.connect()
            conn_to_use.begin() # Start a transaction for this internal connection
            managed_connection = True

        try:
            # 1. Tenta buscar pelo nome (case-insensitive)
            select_query = f'SELECT {id_column} FROM {table_name} WHERE lower({name_column}) = :name'
            result = self._execute_query_with_conn(conn_to_use, select_query, {'name': name_value.lower()})
            if result:
                logger.debug(f"Registro encontrado em '{table_name}' para o nome '{name_value}': ID {result[0][0]}")
                return result[0][0]

            # 2. Se não encontrou, insere
            logger.info(f"Registro '{name_value}' não encontrado em '{table_name}'. Criando novo...")
            
            insert_cols = [name_column]
            insert_values = [f":{name_column}"]
            params = {name_column: name_value}

            if extra_cols:
                for col, val in extra_cols.items():
                    insert_cols.append(col)
                    insert_values.append(f":{col}")
                    params[col] = val

            insert_query = f"""
                INSERT INTO {table_name} ({', '.join(insert_cols)})
                VALUES ({', '.join(insert_values)})
                -- SQLite tem uma sintaxe ligeiramente diferente para ON CONFLICT
                -- e não suporta `lower(name)` diretamente no ON CONFLICT.
                -- A verificação case-insensitive já é feita na busca (SELECT).
                RETURNING {id_column}
            """

            new_id = self._execute_insert_returning_id_with_conn(conn_to_use, insert_query, params)
            
            if new_id:
                logger.info(f"Novo registro criado em '{table_name}' para '{name_value}' com ID: {new_id}")
                return new_id
            else:
                # Se new_id é None, pode ter havido um ON CONFLICT. Re-busca.
                logger.warning(f"Inserção não retornou ID para '{name_value}', possivelmente por concorrência ou ON CONFLICT. Re-buscando...")
                result = self._execute_query_with_conn(conn_to_use, select_query, {'name': name_value.lower()})
                return result[0][0] if result else None
        except Exception as e:
            if managed_connection:
                conn_to_use.rollback()
            raise
        finally:
            if managed_connection:
                conn_to_use.commit()
                conn_to_use.close()

    def get_or_create_competition(self, name: str, api_id: int, connection) -> Optional[int]:
        """Wrapper para get_or_create para a tabela 'competicoes' (schema em Português)."""
        return self.get_or_create('competicoes', name, 'id', name_column='nome', extra_cols={'api_id': api_id}, connection=connection)

    def get_or_create_team(self, name: str, api_id: int, country: Optional[str] = None, connection=None) -> Optional[int]:
        """Wrapper para get_or_create para a tabela 'times' (usa coluna 'nome')."""
        extra_cols = {'api_id': api_id}
        if country:
            extra_cols['pais'] = country
        return self.get_or_create('times', name, 'id', name_column='nome', extra_cols=extra_cols, connection=connection)

    @staticmethod
    def _generate_game_api_id(unique_string: str) -> int:
        """Gera um ID numérico de 63 bits a partir de uma string única (ex: URL ou ID da página)."""
        # Usamos SHA-256 para um hash robusto e pegamos os primeiros 16 caracteres hex
        hash_hex = hashlib.sha256(unique_string.encode('utf-8')).hexdigest()
        # Converte para inteiro e aplica um módulo para garantir que caiba em um bigint (63-bit para ser seguro)
        return int(hash_hex[:15], 16) & ((1 << 63) - 1)

    def insert_game(self, game_df: pd.DataFrame, competition_id: int, home_team_id: int, away_team_id: int, connection) -> Optional[int]:
        """
        Insere um novo jogo na tabela 'jogos' a partir de um DataFrame de jogo.
        Retorna o api_id do jogo inserido ou existente.
        """
        if game_df.empty:
            logger.warning("DataFrame de jogo vazio. Nenhuma inserção será feita.")
            return None

        game_row = game_df.iloc[0] # Expecting only one row for a single game

        game_api_id = self._generate_game_api_id(game_row['api_url'])
        
        # Verifica se o jogo já existe
        if self._execute_query_with_conn(connection, "SELECT api_id FROM jogos WHERE api_id = :api_id", {'api_id': game_api_id}):
            logger.warning(f"Jogo com API ID {game_api_id} (URL: {game_row['api_url']}) já existe. Pulando inserção.")
            return game_api_id

        query = """
            INSERT INTO jogos (api_id, competition_id, start_time, status, home_team_api_id, away_team_api_id, home_team_score, away_team_score, raw_payload)
            VALUES (:api_id, :competition_id, :start_time, :status, :home_team_api_id, :away_team_api_id, :home_team_score, :away_team_score, :raw_payload)
            RETURNING api_id
        """
        params = {
            'api_id': game_api_id,
            'competition_id': competition_id,
            'start_time': game_row['start_time'].isoformat(), # Convert Timestamp to string
            'status': game_row['status'],
            'home_team_api_id': home_team_id,
            'away_team_api_id': away_team_id,
            'home_team_score': game_row['home_score'],
            'away_team_score': game_row['away_score'],
            'raw_payload': json.dumps(game_row['raw_payload'], ensure_ascii=False) # Store raw_payload as JSON string
        }

        return self._execute_insert_returning_id_with_conn(connection, query, params)

    def check_if_game_exists(self, game_url: str) -> bool:
        """Verifica se um jogo com a dada URL (ou seu api_id gerado) já existe no banco."""
        game_api_id = self._generate_game_api_id(game_url)
        query = "SELECT 1 FROM jogos WHERE api_id = :api_id"
        result = self._execute_query(query, {'api_id': game_api_id})
        return bool(result)

    def inserir_dataframe(self, df: pd.DataFrame, nome_tabela: str, connection=None, if_exists: str = 'append', index: bool = False):
        """
        Insere um DataFrame em uma tabela do banco de dados.
        
        :param df: DataFrame a ser inserido.
        :param nome_tabela: Nome da tabela de destino.
        :param connection: Conexão SQLAlchemy a ser usada (para transações).
        :param if_exists: Comportamento se a tabela já existir ('fail', 'replace', 'append').
        :param index: Se deve escrever o índice do DataFrame como uma coluna.
        """
        if self.engine is None:
            raise RuntimeError("Motor do banco de dados não inicializado. Chame conectar() primeiro.")
        if df.empty:
            logger.warning(f"DataFrame para a tabela '{nome_tabela}' está vazio. Nenhuma inserção será feita.")
            return

        # Determine which connection to use
        if connection:
            conn_to_use = connection
            managed_connection = False
        else:
            conn_to_use = self.engine.connect()
            conn_to_use.begin() # Start a transaction for this internal connection
            managed_connection = True

        try:
            df.to_sql(nome_tabela, conn_to_use, if_exists=if_exists, index=index, method='multi')
            logger.info(f"{len(df)} registros inseridos na tabela '{nome_tabela}'.")
        except Exception as e:
            logger.error(f"Erro ao inserir dados na tabela '{nome_tabela}': {e}")
            if managed_connection:
                conn_to_use.rollback()
            raise
        finally:
            if managed_connection:
                conn_to_use.commit()
                conn_to_use.close()

# Exemplo de como usar (será chamado pelo processador)
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    
    # A URL deve vir de uma variável de ambiente no código real
    DATABASE_URL = os.environ.get("DATABASE_URL")
    if not DATABASE_URL:
        print("Variável de ambiente DATABASE_URL não definida. Defina-a com a string de conexão (ex: sqlite:///db/tradecomigo.sqlite3).")
    else:
        db = BancoDados(DATABASE_URL)
        try:
            db.conectar()
            
            # 1. Testar get_or_create para uma competição
            comp_name = "Brasileirão Série Z"
            comp_id = db.get_or_create('competitions', comp_name, 'id')
            print(f"ID para '{comp_name}': {comp_id}")

            # 2. Testar get_or_create para um time
            team_name = "Gemini FC"
            team_id = db.get_or_create('times', team_name, 'api_id')
            print(f"ID para '{team_name}': {team_id}")
            
            # 3. Testar inserção de jogo
            home_id = db.get_or_create('times', 'Time da Casa FC', 'api_id')
            away_id = db.get_or_create('times', 'Visitante EC', 'api_id')
            
            if home_id and away_id and comp_id:
                game_info = {
                    'url': 'https://www.flashscore.com/jogo/unico/12345',
                    'competition_id': comp_id,
                    'start_time': '2025-01-01 20:00:00',
                    'home_team_id': home_id,
                    'away_team_id': away_id,
                    'home_score': 2,
                    'away_score': 1
                }
                game_id = db.insert_game(game_info)
                print(f"Jogo inserido com ID: {game_id}")

                if game_id:
                    # 4. Testar inserção de estatísticas em massa
                    stats_data = [
                        {'jogo_api_id': game_id, 'team_api_id': home_id, 'type': 'Posse de bola', 'value': '60%'},
                        {'jogo_api_id': game_id, 'team_api_id': away_id, 'type': 'Posse de bola', 'value': '40%'},
                        {'jogo_api_id': game_id, 'team_api_id': home_id, 'type': 'Finalizações', 'value': '15'},
                        {'jogo_api_id': game_id, 'team_api_id': away_id, 'type': 'Finalizações', 'value': '8'},
                    ]
                    stats_df = pd.DataFrame(stats_data)
                    db.inserir_dataframe(stats_df, 'estatisticas_time')
                    print("Estatísticas inseridas com sucesso.")

        finally:
            db.desconectar()