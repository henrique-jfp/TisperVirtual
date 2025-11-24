import requests
import json
import time
import logging
from typing import Dict, Any, List, Optional, Set

# --- Configuração de Logging ---
# Configura um logger para exibir informações claras sobre o processo de coleta.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Configurações Principais ---
class Config:
    """
    Contém as configurações estáticas para o coletor, como URLs, IDs e cabeçalhos.
    """
    BASE_URL: str = "https://webws.365scores.com/web"
    HEADERS: Dict[str, str] = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://www.365scores.com/",
    }
    
    # IDs para o Campeonato Brasileiro Série A
    COMPETITION_ID: int = 113
    COMPETITION_NAME: str = "Brasileirão - Série A"
    
    # Lista de IDs dos times da Série A. Usada para garantir que todos os jogos sejam encontrados.
    # Esta lista pode ser atualizada anualmente.
    SERIE_A_TEAM_IDS: List[int] = [
        1215, 1222, 1209, 1211, 1210, 1273, 1216, 1218, 1219, 1778, 
        1225, 8499, 1267, 1774, 1775, 1227, 1767, 1228, 1213, 1768
    ]

    # Parâmetros padrão para as requisições, garantindo consistência.
    DEFAULT_PARAMS: Dict[str, Any] = {
        "appTypeId": 5,
        "langId": 31,
        "timezoneName": "America/Sao_Paulo",
        "userCountryId": 21,
    }

    @staticmethod
    def build_url_from_id(game_id: int) -> str:
        """Constrói uma URL de jogo a partir do ID.
        Esta é uma URL canônica para identificar o jogo, não necessariamente a URL da API.
        """
        return f"https://www.365scores.com/pt-br/football/game/{game_id}/"

class ThreeSixtyFiveScoresCollector:
    """
    Coletor robusto de dados do 365Scores, focado em buscar todos os jogos, 
    estatísticas de partidas e de jogadores para uma determinada competição.
    """
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(Config.HEADERS)
        # Configura retentativas para aumentar a robustez contra falhas de rede.
        retries = requests.adapters.Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
        self.session.mount('https://', requests.adapters.HTTPAdapter(max_retries=retries))

    def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """
        Método auxiliar para realizar requisições à API, com tratamento de erros.
        """
        url = f"{Config.BASE_URL}{endpoint}"
        merged_params = {**Config.DEFAULT_PARAMS, **(params or {})}
        
        try:
            response = self.session.get(url, params=merged_params, timeout=20)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro ao fazer requisição para {url}: {e}")
            return None
        except json.JSONDecodeError as e:
            logging.error(f"Erro ao decodificar JSON da resposta de {url}: {e}")
            return None

    def get_all_game_ids(self) -> Set[int]:
        """
        Busca todos os IDs de jogos para a competição configurada (Brasileirão).
        Itera sobre cada time da Série A para garantir que nenhum jogo seja perdido.
        """
        logging.info(f"Iniciando busca de todos os jogos para '{Config.COMPETITION_NAME}'...")
        all_game_ids: Set[int] = set()

        for team_id in Config.SERIE_A_TEAM_IDS:
            logging.info(f"Buscando jogos para o time ID: {team_id}")
            params = {"competitors": team_id}
            data = self._make_request("/games/results/", params)
            
            if data and "games" in data:
                for game in data["games"]:
                    if game.get("competitionId") == Config.COMPETITION_ID:
                        all_game_ids.add(game["id"])
            time.sleep(1) # Pausa para não sobrecarregar a API.

        logging.info(f"Total de {len(all_game_ids)} jogos únicos encontrados.")
        return all_game_ids

    def get_game_stats(self, game_id: int) -> Optional[Dict[str, Any]]:
        """
        Busca as estatísticas gerais de uma partida específica.
        """
        logging.info(f"Buscando estatísticas da partida para o jogo ID: {game_id}")
        params = {"games": game_id}
        return self._make_request("/game/stats/", params)

    def get_player_stats(self, game_id: int) -> Optional[Dict[str, Any]]:
        """
        Busca as estatísticas detalhadas dos jogadores de uma partida específica.
        """
        logging.info(f"Buscando estatísticas dos jogadores para o jogo ID: {game_id}")
        params = {"gameId": game_id}
        return self._make_request("/athletes/games/lineups", params)

    def get_full_data_for_game(self, game_id: int) -> Optional[Dict[str, Any]]:
        """
        Orquestra a coleta de todos os dados (partida e jogadores) para um único jogo.
        """
        game_stats = self.get_game_stats(game_id)
        player_stats = self.get_player_stats(game_id)

        if not game_stats or not player_stats:
            logging.warning(f"Não foi possível obter todos os dados para o jogo ID: {game_id}. Pulando.")
            return None
            
        # Extrai a informação principal do jogo para ser a raiz do nosso objeto.
        game_info = {}
        if game_stats.get("games"):
            game_info = game_stats["games"][0]

        return {
            "game_info": game_info,
            "game_statistics": game_stats.get("statistics", []),
            "player_statistics": player_stats.get("members", [])
        }

    def collect_and_save_championship_data(self, output_filename: str = "dados_campeonato.json"):
        """
        Executa o fluxo completo: busca todos os jogos, coleta os detalhes de cada um
        e salva o resultado consolidado em um arquivo JSON.
        """
        logging.info("--- INICIANDO COLETA COMPLETA DO CAMPEONATO ---")
        game_ids = self.get_all_game_ids()
        
        if not game_ids:
            logging.error("Nenhum jogo encontrado. Abortando.")
            return

        all_championship_data = []
        
        for i, game_id in enumerate(sorted(list(game_ids))):
            logging.info(f"--- Processando Jogo {i+1}/{len(game_ids)} (ID: {game_id}) ---")
            game_data = self.get_full_data_for_game(game_id)
            if game_data:
                all_championship_data.append(game_data)
            
            time.sleep(2) # Pausa maior entre a coleta de cada jogo completo.

        logging.info(f"Coleta finalizada. Total de {len(all_championship_data)} jogos processados com sucesso.")
        
        if all_championship_data:
            try:
                with open(output_filename, 'w', encoding='utf-8') as f:
                    json.dump(all_championship_data, f, ensure_ascii=False, indent=4)
                logging.info(f"Dados salvos com sucesso no arquivo: {output_filename}")
            except IOError as e:
                logging.error(f"Erro ao salvar os dados no arquivo {output_filename}: {e}")
        else:
            logging.warning("Nenhum dado foi coletado para salvar.")


if __name__ == "__main__":
    collector = ThreeSixtyFiveScoresCollector()
    collector.collect_and_save_championship_data()
