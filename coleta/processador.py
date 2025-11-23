import pandas as pd
import json
import os
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ProcessadorDados:
    """
    GHOST: Classe refatorada para modularidade e clareza.
    - Lógica de normalização dividida em métodos privados e específicos.
    - Tratamento de erro mais granular.
    - Foco em transformar diferentes "schemas" de JSON em um formato canônico.
    """
    def __init__(self, pasta_entrada: str = "dados_raw"):
        self.pasta_entrada = pasta_entrada

    def _carregar_json(self, filepath: str) -> Optional[Dict[str, Any]]:
        """Carrega um único arquivo JSON."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Erro ao carregar ou decodificar {filepath}: {e}")
            return None

    def carregar_todos_jsons(self) -> List[Dict[str, Any]]:
        """Carrega todos os arquivos JSON da pasta de entrada."""
        dados_validos = []
        if not os.path.isdir(self.pasta_entrada):
            logger.error(f"Diretório de entrada não encontrado: {self.pasta_entrada}")
            return []
        for filename in os.listdir(self.pasta_entrada):
            if filename.endswith('.json'):
                filepath = os.path.join(self.pasta_entrada, filename)
                dados = self._carregar_json(filepath)
                if dados:
                    dados_validos.append(dados)
        logger.info(f"Carregados {len(dados_validos)} arquivos JSON de '{self.pasta_entrada}'.")
        return dados_validos
            
    def _normalizar_de_lista_flashscore(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Normaliza dados de uma lista de partidas do Flashscore."""
        partidas = []
        for match in data:
            if isinstance(match, dict) and ('home_team' in match or 'away_team' in match):
                partida = {
                    'id_partida': match.get('id') or match.get('match_id'),
                    'time_casa': match.get('home_team'),
                    'time_fora': match.get('away_team'),
                    'placar_casa': match.get('home_score'),
                    'placar_fora': match.get('away_score'),
                    'data_hora': match.get('date'),
                    'liga': match.get('league'),
                    'status': match.get('status')
                }
                if partida['id_partida']:
                    partidas.append(partida)
        return partidas

    def _normalizar_de_objeto_365scores(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Normaliza dados do objeto de resposta da API do 365scores."""
        partidas = []
        for match in data.get("Games", []):
            if isinstance(match, dict):
                partida = {
                    'id_partida': match.get('ID'),
                    'time_casa': match.get('HomeCompetitor', {}).get('Name'),
                    'time_fora': match.get('AwayCompetitor', {}).get('Name'),
                    'placar_casa': match.get('Scores', {}).get('Home'),
                    'placar_fora': match.get('Scores', {}).get('Away'),
                    'data_hora': match.get('StartTime'),
                    'liga': match.get('LeagueName'),
                    'status': match.get('StatusText')
                }
                if partida['id_partida']:
                    partidas.append(partida)
        return partidas

    def _normalizar_de_html(self, item: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Tenta extrair dados de partidas de um payload HTML.
        GHOST: Lógica de parsing de HTML isolada. Frágil por natureza,
        mas agora contida em seu próprio método.
        """
        html_content = item.get('data', {}).get('html', '')
        if not html_content:
            return []

        soup = BeautifulSoup(html_content, 'html.parser')
        title = soup.find('title')
        if not title or '|' not in title.get_text():
            return []

        try:
            title_text = title.get_text()
            first_part, second_part, *_ = title_text.split('|')

            score_part = first_part.strip().split()
            teams_part = second_part.strip().split(' v ')

            if len(score_part) < 3 or len(teams_part) < 2:
                return []

            home_team = teams_part[0].strip()
            away_team_date = teams_part[1].split()
            away_team = away_team_date[0].strip()
            date = ' '.join(away_team_date[1:])
            score = score_part[1]
            placar_casa, placar_fora = score.split('-')

            url = item.get('url', '')
            id_partida = url.split('mid=')[-1] if 'mid=' in url else url.split('?')[0].split('/')[-2]

            return [{
                'id_partida': id_partida,
                'time_casa': home_team,
                'time_fora': away_team,
                'placar_casa': placar_casa,
                'placar_fora': placar_fora,
                'data_hora': date,
                'liga': None,
                'status': 'finished'
            }]
        except (ValueError, IndexError) as e:
            logger.debug(f"Não foi possível parsear o título HTML: '{title.get_text()}'. Erro: {e}")
            return []

    def normalizar_partidas(self, dados_brutos: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Normaliza dados de partidas de várias fontes (listas, dicts, html) em um DataFrame.
        GHOST: Adicionada lógica para rotear para o parser correto baseado na URL.
        """
        partidas = []
        for item in dados_brutos:
            url_captura = item.get('url', '')
            data = item.get('data', {})

            if 'flashscore' in url_captura:
                if isinstance(data, list):
                    partidas.extend(self._normalizar_de_lista_flashscore(data))
                elif isinstance(data, dict):
                    if 'matches' in data and isinstance(data['matches'], list):
                        partidas.extend(self._normalizar_de_lista_flashscore(data['matches']))
                    elif 'html' in data:
                        partidas.extend(self._normalizar_de_html(item))

            elif '365scores' in url_captura:
                if isinstance(data, dict):
                    partidas.extend(self._normalizar_de_objeto_365scores(data))

        if not partidas:
            logger.warning("Nenhuma partida encontrada para normalizar.")
            return pd.DataFrame()

        df = pd.DataFrame(partidas).drop_duplicates(subset=['id_partida']).reset_index(drop=True)
        logger.info(f"Normalizadas {len(df)} partidas únicas.")
        return df

    def normalizar_estatisticas(self, dados_brutos: List[Dict[str, Any]]) -> pd.DataFrame:
        """Normaliza estatísticas de partidas em um DataFrame."""
        estatisticas = []
        for item in dados_brutos:
            data = item.get('data', {})
            if isinstance(data, dict):
                match_id = data.get('match_id')
                if not match_id:
                    continue
                for stat in data.get('stats', []):
                    estatisticas.append({
                        'id_partida': match_id,
                        'tipo_estatistica': stat.get('type'),
                        'valor_casa': stat.get('home_value'),
                        'valor_fora': stat.get('away_value')
                    })

        if not estatisticas:
            logger.warning("Nenhuma estatística encontrada para normalizar.")
            return pd.DataFrame()

        df = pd.DataFrame(estatisticas).drop_duplicates().reset_index(drop=True)
        logger.info(f"Normalizadas {len(df)} estatísticas.")
        return df

    def processar_e_salvar(self, pasta_saida: str = "dados_processados"):
        """
        Processa todos os dados brutos e salva os DataFrames resultantes em arquivos CSV.
        """
        os.makedirs(pasta_saida, exist_ok=True)
        dados_brutos = self.carregar_todos_jsons()

        if not dados_brutos:
            logger.warning("Nenhum dado bruto para processar. Encerrando.")
            return
        df_partidas = self.normalizar_partidas(dados_brutos)
        if not df_partidas.empty:
            path = os.path.join(pasta_saida, "partidas.csv")
            df_partidas.to_csv(path, index=False)
            logger.info(f"Dados de partidas salvos em: {path}")

        df_estatisticas = self.normalizar_estatisticas(dados_brutos)
        if not df_estatisticas.empty:
            path = os.path.join(pasta_saida, "estatisticas.csv")
            df_estatisticas.to_csv(path, index=False)
            logger.info(f"Dados de estatísticas salvos em: {path}")
