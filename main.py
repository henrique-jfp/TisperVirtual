import asyncio
import logging
import os
import yaml
import argparse
from dotenv import load_dotenv
from coleta.navegador import Navegador
from coleta.captura_xhr import CapturaXHR
from coleta.processador import ProcessadorDados
from coleta.banco_dados import BancoDados
from typing import Dict, Any

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# GHOST: Configuração centralizada de logging para consistência.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def carregar_config(path: str = "config.yaml") -> Dict[str, Any]:
    """Carrega o arquivo de configuração YAML."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logger.error(f"Arquivo de configuração '{path}' não encontrado.")
        raise
    except yaml.YAMLError as e:
        logger.error(f"Erro ao parsear o arquivo YAML '{path}': {e}")
        raise

async def executar_alvo(config_alvo: Dict[str, Any]):
    """







    GHOST: Orquestra o processo completo para um alvo específico.
    Coleta -> Processamento -> Persistência.
    """




    logger.info(f"Iniciando execução para o alvo: {config_alvo.get('descricao', 'Sem descrição')}")
    




    # --- Configuração ---
    DB_URL = os.getenv("DATABASE_URL")
    if not DB_URL:
        logger.error("A variável de ambiente DATABASE_URL não está definida. Adicione-a ao seu arquivo .env.")
        return

    dados_capturados = []
    
    # --- Fase 1: Coleta ---



    try:
        async with Navegador(headless=True) as navegador:
            await navegador.navegar_para(config_alvo['url'])
            await navegador.esperar_por_seletor(config_alvo['seletores']['espera_inicial'])

            capturador = CapturaXHR(navegador)

            async def acao_definida():
                if navegador.page:
                    logger.info(f"Executando ação: Clicar no seletor '{config_alvo['seletores']['acao_clique']}'")
                    await navegador.page.click(config_alvo['seletores']['acao_clique'])
                    await navegador.esperar_por_seletor(config_alvo['seletores']['espera_pos_acao'])

            await capturador.capturar_durante_acao(acao_definida, url_filtros=config_alvo['filtros_url'])
            
            dados_capturados = capturador.obter_capturas()
            capturador.salvar_capturas(dados_capturados, nome_base=config_alvo['nome_base_arquivo'])
    except Exception as e:
        logger.critical(f"Falha crítica na fase de coleta: {e}")
        return # Interrompe a execução se a coleta falhar

    # --- Fase 2: Processamento e Persistência ---
    if dados_capturados:
        logger.info("Iniciando fase de processamento e persistência...")
        

        processador = ProcessadorDados(pasta_entrada="dados_raw")
        dados_brutos = processador.carregar_todos_jsons()
        df_partidas = processador.normalizar_partidas(dados_brutos)
        df_estatisticas = processador.normalizar_estatisticas(dados_brutos)


        db = BancoDados(db_url=DB_URL)
        try:
            db.conectar()
            db.criar_tabelas_iniciais()
            








            # GHOST: A estratégia 'append' com chaves primárias/únicas é uma forma
            # simples e eficaz de evitar duplicatas sem lógica complexa de 'upsert'.
            db.inserir_dataframe(df_partidas, "partidas", if_exists='append')
            db.inserir_dataframe(df_estatisticas, "estatisticas", if_exists='append')

        except Exception as e:
            logger.critical(f"Falha crítica na operação com o banco de dados: {e}")
        finally:
            db.desconectar()
            
        logger.info("Processamento e persistência concluídos.")
    else:
        logger.warning("Nenhum dado foi capturado. As fases de processamento e persistência foram ignoradas.")

def main():
    """
    Ponto de entrada principal. Parseia argumentos da linha de comando
    e executa o alvo de coleta correspondente.
    """
    config = carregar_config()
    alvos_disponiveis = list(config.get('alvos', {}).keys())

    parser = argparse.ArgumentParser(description="Motor de extração de dados web.")
    parser.add_argument(
        "alvo", 
        help="O nome do alvo a ser executado, conforme definido em config.yaml.",
        choices=alvos_disponiveis
    )
    args = parser.parse_args()
    
    config_alvo_selecionado = config['alvos'][args.alvo]
    
    asyncio.run(executar_alvo(config_alvo_selecionado))

if __name__ == "__main__":

    main()
