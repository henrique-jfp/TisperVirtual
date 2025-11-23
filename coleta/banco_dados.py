import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class BancoDados:
    """
    GHOST: Classe para gerenciar a conexão e operações com o banco de dados.
    - Usa SQLAlchemy para ser agnóstico ao SGBD.
    - Conexão gerenciada por um pool.
    - Métodos robustos para inserção de DataFrames.
    """
    def __init__(self, db_url: str):
        """
        Inicializa a classe com a URL de conexão do banco de dados.
        Exemplo de URL (PostgreSQL): "postgresql://user:password@host:port/database"
        """
        self.db_url = db_url
        self.engine: Optional[Engine] = None

    def conectar(self):
        """Cria o motor de conexão com o banco de dados."""
        try:
            self.engine = create_engine(self.db_url, pool_pre_ping=True)
            # Testa a conexão
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

    def inserir_dataframe(self, df: pd.DataFrame, nome_tabela: str, if_exists: str = 'append'):
        """
        Insere um DataFrame em uma tabela do banco de dados.
        
        :param df: DataFrame a ser inserido.
        :param nome_tabela: Nome da tabela de destino.
        :param if_exists: Comportamento se a tabela já existir ('fail', 'replace', 'append').
                         'append' é o padrão para adicionar novos dados.
        """
        if self.engine is None:
            raise RuntimeError("Motor do banco de dados não inicializado. Chame conectar() primeiro.")
        if df.empty:
            logger.warning(f"DataFrame para a tabela '{nome_tabela}' está vazio. Nenhuma inserção será feita.")
            return

        try:
            with self.engine.begin() as connection: # Inicia uma transação
                df.to_sql(nome_tabela, connection, if_exists=if_exists, index=False)
                logger.info(f"{len(df)} registros inseridos/atualizados na tabela '{nome_tabela}'.")
        except SQLAlchemyError as e:
            logger.error(f"Erro ao inserir dados na tabela '{nome_tabela}': {e}")
            raise

    def criar_tabelas_iniciais(self):
        """
        Cria as tabelas 'partidas' e 'estatisticas' se elas não existirem.
        GHOST: SQL bruto para controle total sobre tipos de dados e chaves.
        """
        if self.engine is None:
            raise RuntimeError("Motor do banco de dados não inicializado.")

        criar_tabela_partidas = text("""
        CREATE TABLE IF NOT EXISTS partidas (
            id_partida VARCHAR(255) PRIMARY KEY,
            time_casa VARCHAR(255),
            time_fora VARCHAR(255),
            placar_casa INTEGER,
            placar_fora INTEGER,
            data_hora VARCHAR(255),
            liga VARCHAR(255),
            status VARCHAR(50)
        );
        """)

        criar_tabela_estatisticas = text("""
        CREATE TABLE IF NOT EXISTS estatisticas (
            id SERIAL PRIMARY KEY,
            id_partida VARCHAR(255) REFERENCES partidas(id_partida) ON DELETE CASCADE,
            tipo_estatistica VARCHAR(255),
            valor_casa INTEGER,
            valor_fora INTEGER,
            UNIQUE(id_partida, tipo_estatistica)
        );
        """)
        
        try:
            with self.engine.begin() as connection:
                connection.execute(criar_tabela_partidas)
                logger.info("Tabela 'partidas' verificada/criada com sucesso.")
                connection.execute(criar_tabela_estatisticas)
                logger.info("Tabela 'estatisticas' verificada/criada com sucesso.")
        except SQLAlchemyError as e:
            logger.error(f"Erro ao criar tabelas iniciais: {e}")
            raise

