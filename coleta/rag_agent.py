import os
import re
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dotenv import load_dotenv
from supabase import create_client
import requests
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

# --- Configuração de Logging ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Tentativa de usar o client local para football-data.org (híbrido)
try:
    import football_data_hybrid as fd
    FD_AVAILABLE = True
    logger.info("football_data_hybrid disponível: usando como fonte de dados alternativa")
except Exception:
    fd = None
    FD_AVAILABLE = False
    logger.info("football_data_hybrid não disponível - dependeremos apenas do Supabase/local")

# --- Carregar Variáveis de Ambiente ---
load_dotenv()

# --- Configurações ---
SUPABASE_URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
SUPABASE_KEY = os.getenv("NEXT_PUBLIC_SUPABASE_PUBLISHABLE_DEFAULT_KEY")
API_FOOTBALL_KEY = os.getenv("API_FOOTBALL_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DEFAULT_SEASON = int(os.getenv("DEFAULT_SEASON", datetime.now().year))
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("NEXT_PUBLIC_SUPABASE_SERVICE_ROLE_KEY")

# Validação de chaves
if not all([SUPABASE_URL, SUPABASE_KEY]):
    logger.error("Variáveis Supabase não configuradas!")
if not API_FOOTBALL_KEY:
    logger.warning("API_FOOTBALL_KEY não configurada - usando apenas dados locais")
if not GROQ_API_KEY:
    logger.warning("GROQ_API_KEY não configurada - IA desabilitada")

_supabase_key_used = SUPABASE_SERVICE_ROLE_KEY if SUPABASE_SERVICE_ROLE_KEY else SUPABASE_KEY
if SUPABASE_SERVICE_ROLE_KEY:
    logger.info("Usando SUPABASE_SERVICE_ROLE_KEY para operações servidor-side")
else:
    logger.info("Service role não encontrado, usando chave publishable (pode ser limitada)")

supabase = create_client(SUPABASE_URL, _supabase_key_used)

# --- Mapeamento de Times (nome -> api_id) ---
TEAMS_MAP = {
    'flamengo': 127,
    'fluminense': 129,
    'palmeiras': 128,
    'corinthians': 131,
    'são paulo': 126,
    'santos': 132,
    'grêmio': 133,
    'internacional': 134,
    'atlético-mg': 120,
    'athletico-pr': 1050,
    'cruzeiro': 1067,
    'botafogo': 130,
    'vasco': 124,
    'bahia': 759,
    'fortaleza': 1062,
    'ceará': 1059,
    'vitória': 154,
    'cuiabá': 1064,
    'bragantino': 1080,
}

# Mapa normalizado para busca por texto sem acentos
import unicodedata

def _normalize_text(s: str) -> str:
    if not s:
        return ''
    s = s.lower()
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return s

NORMALIZED_TEAMS = { _normalize_text(k): v for k, v in TEAMS_MAP.items() }

# ID do Brasileirão Série A (usado por fontes externas quando aplicável)
BRASILEIRAO_ID = 71

# Cache em memória (simples - considere Redis para produção)
_cache = {}
CACHE_TTL = 3600  # 1 hora


class APIFootballClient:
    """Cliente para integração com API-Football"""
    
    BASE_URL = "https://v3.football.api-sports.io"
    
    def __init__(self, api_key: str, season: int = None):
        self.api_key = api_key
        self.season = season or datetime.now().year
        self.headers = {
            'x-rapidapi-key': api_key,
            'x-rapidapi-host': 'v3.football.api-sports.io'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """Faz requisição à API com tratamento de erros"""
        try:
            url = f"{self.BASE_URL}/{endpoint}"
            logger.info(f"API Request: {endpoint} - Params: {params}")
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('errors'):
                logger.error(f"API Error: {data['errors']}")
                return None
            
            return data.get('response', [])
        
        except requests.exceptions.Timeout:
            logger.error(f"Timeout na requisição: {endpoint}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro na API: {e}")
            return None
    
    def get_fixtures_today(self, league_id: int = BRASILEIRAO_ID) -> List[Dict]:
        """Busca jogos de hoje (mantido apenas para compatibilidade com API-Football client)
        NOTE: não é mais usado pelo fluxo principal do bot; o bot prioriza Supabase e
        `football_data_hybrid` quando disponível.
        """
        today = datetime.now().strftime('%Y-%m-%d')
        return self._make_request('fixtures', {
            'league': league_id,
            'date': today,
            'season': self.season
        }) or []
    
    def get_fixtures_by_team(self, team_id: int, last: int = 5) -> List[Dict]:
        """Busca últimos/próximos jogos de um time"""
        return self._make_request('fixtures', {
            'team': team_id,
            'last': last,
            'season': self.season
        }) or []
    
    def get_standings(self, league_id: int = BRASILEIRAO_ID) -> List[Dict]:
        """Busca classificação do campeonato"""
        data = self._make_request('standings', {
            'league': league_id,
            'season': self.season
        })
        
        if data and len(data) > 0:
            return data[0].get('league', {}).get('standings', [[]])[0]
        return []
    
    def get_team_statistics(self, team_id: int, league_id: int = BRASILEIRAO_ID) -> Optional[Dict]:
        """Busca estatísticas de um time"""
        data = self._make_request('teams/statistics', {
            'team': team_id,
            'league': league_id,
            'season': self.season
        })
        
        return data[0] if data else None
    
    def get_odds(self, fixture_id: int) -> List[Dict]:
        """Busca odds de uma partida"""
        return self._make_request('odds', {
            'fixture': fixture_id
        }) or []


class AIAnalyzer:
    """Módulo de IA para análises inteligentes usando Groq"""
    
    def __init__(self, api_key: str):
        self.llm = ChatGroq(
            temperature=0.7,
            model_name="llama-3.3-70b-versatile",
            groq_api_key=api_key
        )
        
        self.system_prompt = """Você é um especialista em análise de futebol brasileiro e tipster profissional.
Suas respostas devem ser:
- Em português brasileiro natural e conversacional
- Baseadas em dados estatísticos fornecidos
- Objetivas mas amigáveis
- Fundamentadas em análise técnica
- Incluir probabilidades e raciocínio quando apropriado

Use emojis moderadamente para tornar as respostas mais visuais: ⚽🏆📊💡🎯"""
    
    def analyze_query(self, query: str, context: str = "") -> str:
        """Analisa query do usuário com contexto"""
        try:
            prompt = f"""Pergunta do usuário: {query}

Contexto/Dados disponíveis:
{context if context else "Nenhum dado específico fornecido"}

Forneça uma resposta útil e fundamentada."""

            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=prompt)
            ]
            
            response = self.llm.invoke(messages)
            return response.content
        
        except Exception as e:
            logger.error(f"Erro na análise de IA: {e}")
            return "Desculpe, não consegui processar sua pergunta no momento."
    
    def analyze_match(self, home_team: str, away_team: str, stats: Dict) -> str:
        """Análise profunda de confronto"""
        try:
            context = f"""Analise este confronto:
{home_team} (Casa) vs {away_team} (Visitante)

Estatísticas:
{json.dumps(stats, indent=2, ensure_ascii=False)}

Forneça:
1. Análise de desempenho recente dos times
2. Pontos fortes e fracos de cada equipe
3. Fatores decisivos (casa/fora, forma recente, confrontos diretos)
4. Palpite fundamentado com probabilidades
5. Sugestão de mercados de aposta interessantes"""

            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=context)
            ]
            
            response = self.llm.invoke(messages)
            return response.content
        
        except Exception as e:
            logger.error(f"Erro na análise de partida: {e}")
            return "Não foi possível analisar este confronto."
    
    def generate_betting_tips(self, matches: List[Dict]) -> str:
        """Gera dicas de apostas baseadas em múltiplas partidas"""
        try:
            context = f"""Analise estas partidas e sugira as melhores oportunidades de aposta:

{json.dumps(matches, indent=2, ensure_ascii=False)}

Forneça:
1. Top 3 apostas mais seguras
2. 2 apostas de valor (value bets)
3. 1 aposta ousada com alto retorno
4. Justificativa para cada sugestão"""

            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=context)
            ]
            
            response = self.llm.invoke(messages)
            return response.content
        
        except Exception as e:
            logger.error(f"Erro ao gerar dicas: {e}")
            return "Não foi possível gerar dicas de apostas."


class FootballTipsterBot:
    """Bot inteligente de análise de futebol com RAG"""
    
    def __init__(self, supabase_client, api_football_key: str = None, groq_key: str = None):
        self.supabase = supabase_client
        self.today = datetime.now().date()
        
        # Inicializar clientes externos
        # Não usar API-Football: priorizar Supabase e football-data local (football_data_hybrid)
        self.fd_client = fd if FD_AVAILABLE else None
        self.ai_analyzer = AIAnalyzer(groq_key) if groq_key else None

        # Checar conexão com Supabase (select simples)
        try:
            # consulta genérica para validar conexão sem depender de colunas específicas
            resp = self.supabase.table('jogos').select('*').limit(1).execute()
            resp_data = getattr(resp, 'data', resp)
            logger.info(f"Supabase connected - test query response: {resp_data}")
        except Exception as e:
            logger.error(f"Falha ao conectar no Supabase: {e}")

        logger.info("Bot inicializado com sucesso")
    
    def _get_cache(self, key: str) -> Optional[Any]:
        """Busca dados do cache"""
        if key in _cache:
            data, timestamp = _cache[key]
            if (datetime.now().timestamp() - timestamp) < CACHE_TTL:
                logger.info(f"Cache hit: {key}")
                return data
            else:
                del _cache[key]
        return None
    
    def _set_cache(self, key: str, data: Any):
        """Salva dados no cache"""
        _cache[key] = (data, datetime.now().timestamp())
    
    def _extract_team_info(self, query: str) -> Tuple[Optional[str], Optional[int]]:
        """Extrai nome e ID do time da query"""
        query_norm = _normalize_text(query)
        # primeiro tentar mapear por nome normalizado conhecido
        for name_norm, team_id in NORMALIZED_TEAMS.items():
            if name_norm in query_norm:
                # retornar nome original do map para apresentação
                # encontra chave original
                for orig, tid in TEAMS_MAP.items():
                    if tid == team_id:
                        return orig, team_id
        # fallback: tentar buscar por nome no banco (home/away)
        try:
            # procurar por substring em home_team_name ou away_team_name
            resp = self.supabase.table('jogos').select('home_team_name,away_team_name,home_team_api_id,away_team_api_id').ilike('home_team_name', f'%{query}%').limit(1).execute()
            if getattr(resp, 'data', None):
                row = resp.data[0]
                # preferir api id se existir
                return row.get('home_team_name'), row.get('home_team_api_id')
        except Exception:
            pass

        try:
            resp = self.supabase.table('jogos').select('home_team_name,away_team_name,home_team_api_id,away_team_api_id').ilike('away_team_name', f'%{query}%').limit(1).execute()
            if getattr(resp, 'data', None):
                row = resp.data[0]
                return row.get('away_team_name'), row.get('away_team_api_id')
        except Exception:
            pass

        return None, None
    
    def _format_fixture(self, fixture: Dict) -> str:
        """Formata dados de partida da API-Football"""
        try:
            home = fixture['teams']['home']['name']
            away = fixture['teams']['away']['name']
            date = fixture['fixture']['date']
            status = fixture['fixture']['status']['long']
            
            result = f"\n⚽ {home} vs {away}"
            result += f"\n📅 {date}"
            result += f"\n📊 Status: {status}"
            
            if fixture['goals']['home'] is not None:
                result += f"\n🎯 Placar: {fixture['goals']['home']} x {fixture['goals']['away']}"
            
            return result
        except KeyError as e:
            logger.error(f"Erro ao formatar fixture: {e}")
            return "\n❌ Erro ao formatar jogo"

    def _format_fd_match(self, match: Dict) -> str:
        """Formata partida no formato football-data.org (football_data_hybrid)"""
        try:
            home = match.get('homeTeam', {}).get('name') or match.get('homeTeam', {}).get('shortName')
            away = match.get('awayTeam', {}).get('name') or match.get('awayTeam', {}).get('shortName')
            date = match.get('utcDate') or match.get('fixture', {}).get('date')
            status = match.get('status', 'N/A')

            result = f"\n⚽ {home} vs {away}"
            result += f"\n📅 {date}"
            result += f"\n📊 Status: {status}"

            score = match.get('score', {})
            full = score.get('fullTime', {})
            if full:
                if full.get('home') is not None:
                    result += f"\n🎯 Placar: {full.get('home')} x {full.get('away')}"

            return result
        except Exception as e:
            logger.error(f"Erro ao formatar match football-data: {e}")
            return "\n❌ Erro ao formatar jogo"

    def _get_next_matches_from_supabase(self, team_id: int, limit: int = 5) -> List[Dict]:
        try:
            today_str = datetime.now().strftime('%Y-%m-%d')
            resp = self.supabase.table('jogos').select('*').or_(f'home_team_api_id.eq.{team_id},away_team_api_id.eq.{team_id}').gte('start_time', today_str).order('start_time', count='planned').limit(limit).execute()
            return getattr(resp, 'data', []) or []
        except Exception as e:
            logger.debug(f"Erro ao buscar próximos jogos no Supabase: {e}")
            return []

    def _get_last_match_from_supabase(self, team_id: int) -> Optional[Dict]:
        try:
            resp = self.supabase.table('jogos').select('*').or_(f'home_team_api_id.eq.{team_id},away_team_api_id.eq.{team_id}').lte('start_time', datetime.now().isoformat()).order('start_time', desc=True).limit(1).execute()
            rows = getattr(resp, 'data', []) or []
            return rows[0] if rows else None
        except Exception as e:
            logger.debug(f"Erro ao buscar último jogo no Supabase: {e}")
            return None
    
    def _save_fixture_to_db(self, fixture: Dict):
        """Salva jogo no Supabase"""
        try:
            data = {
                'api_fixture_id': fixture['fixture']['id'],
                'home_team_name': fixture['teams']['home']['name'],
                'away_team_name': fixture['teams']['away']['name'],
                'home_team_api_id': fixture['teams']['home']['id'],
                'away_team_api_id': fixture['teams']['away']['id'],
                'start_time': fixture['fixture']['date'],
                'status': fixture['fixture']['status']['long'],
                'home_score': fixture['goals']['home'],
                'away_score': fixture['goals']['away']
            }
            
            resp = self.supabase.table('jogos').upsert(data, on_conflict='api_fixture_id').execute()
            resp_data = getattr(resp, 'data', resp)
            resp_error = getattr(resp, 'error', None)
            logger.info(f"Supabase upsert response: {resp_data} | error: {resp_error}")
            if resp_error:
                logger.error(f"Erro ao salvar jogo no Supabase: {resp_error}")
            else:
                logger.info(f"Jogo salvo: {data['home_team_name']} vs {data['away_team_name']}")
        
        except Exception as e:
            logger.error(f"Erro ao salvar jogo no DB: {e}")
    
    # ========== JOGOS E CALENDÁRIO ==========
    
    def get_games_today(self) -> str:
        """Busca jogos de hoje (API-Football prioritário)"""
        try:
            cache_key = f"games_today_{self.today}"
            cached = self._get_cache(cache_key)
            if cached:
                return cached
            # Priorizar Supabase local
            today_str = self.today.strftime('%Y-%m-%d')
            response = self.supabase.table('jogos').select('*').gte('start_time', today_str).lt('start_time', f'{today_str} 23:59:59').execute()
            if getattr(response, 'data', None):
                result = f"⚽ JOGOS DE HOJE ({self.today}) - Dados locais:\n"
                for game in response.data[:50]:
                    result += f"\n🏟️ {game.get('home_team_name') or game.get('home_team_score', '??')} vs {game.get('away_team_name') or game.get('away_team_score','??')}"
                    result += f"\n📅 {game.get('start_time')}"
                self._set_cache(cache_key, result)
                return result

            # Se não tiver no Supabase, tentar football-data (local/importado)
            if self.fd_client:
                matches = fd.get_all_match_scores(status="SCHEDULED")
                # Filtrar só os de hoje
                today_matches = [m for m in matches if m.get('utcDate', '').startswith(today_str)]
                if today_matches:
                    # salvar via helper do hybrid
                    try:
                        fd.save_matches_to_db(today_matches, source='football_data', dry_run=False)
                    except Exception as e:
                        logger.warning(f"Falha ao salvar matches via football_data_hybrid: {e}")

                    result = f"⚽ JOGOS DE HOJE ({self.today}) - Fonte football-data:\n"
                    for m in today_matches[:10]:
                        result += self._format_fd_match(m) + "\n"
                    self._set_cache(cache_key, result)
                    return result

            # Fallback final: banco local (mesmo que vazio)
            today_str = self.today.strftime('%Y-%m-%d')
            response = self.supabase.table('jogos').select('*').gte('start_time', today_str).lt('start_time', f'{today_str} 23:59:59').execute()
            if not getattr(response, 'data', None):
                return f"❌ Nenhum jogo encontrado para hoje ({self.today})"
            result = f"⚽ JOGOS DE HOJE ({self.today}) - Dados locais:\n"
            for game in response.data[:10]:
                result += f"\n🏟️ {game.get('home_team_name')} vs {game.get('away_team_name')}"
                result += f"\n📅 {game.get('start_time')}"
            return result
        
        except Exception as e:
            logger.error(f"Erro ao buscar jogos de hoje: {e}")
            return f"❌ Erro ao buscar jogos: {str(e)}"
    
    def get_team_next_match(self, team_name: str, team_id: int) -> str:
        """Próximo jogo de um time"""
        try:
            cache_key = f"next_match_{team_id}"
            cached = self._get_cache(cache_key)
            if cached:
                return cached
            # Priorizar Supabase
            today_str = self.today.strftime('%Y-%m-%d')
            response = self.supabase.table('jogos').select('*').or_(f'home_team_api_id.eq.{team_id},away_team_api_id.eq.{team_id}').gte('start_time', today_str).order('start_time', count='planned').limit(1).execute()

            if getattr(response, 'data', None) and len(response.data) > 0:
                game = response.data[0]
                result = f"📅 PRÓXIMO JOGO - {team_name.upper()}:\n🏟️ {game.get('home_team_name')} vs {game.get('away_team_name')}\n📅 {game.get('start_time')}"
                self._set_cache(cache_key, result)
                return result

            # Tentar football-data como fallback
            if self.fd_client:
                future = fd.search_future_games()
                # Buscar primeiro jogo envolvendo o time
                for m in future:
                    home = m.get('homeTeam', {}).get('name', '').lower()
                    away = m.get('awayTeam', {}).get('name', '').lower()
                    if team_name in home or team_name in away:
                        try:
                            fd.save_matches_to_db([m], source='football_data', dry_run=False)
                        except Exception:
                            logger.debug('Falha ao salvar match via fd hybrid')
                        result = f"📅 PRÓXIMO JOGO - {team_name.upper()}:"
                        result += self._format_fd_match(m)
                        if self.ai_analyzer:
                            context = f"Próximo jogo: {m.get('homeTeam',{}).get('name')} vs {m.get('awayTeam',{}).get('name')}"
                            analysis = self.ai_analyzer.analyze_query("Analise brevemente este confronto", context)
                            result += f"\n\n💡 ANÁLISE:\n{analysis}"
                        self._set_cache(cache_key, result)
                        return result

            # Fallback final: banco local (vazio)
            today_str = self.today.strftime('%Y-%m-%d')
            response = self.supabase.table('jogos').select('*').or_(f'home_team_api_id.eq.{team_id},away_team_api_id.eq.{team_id}').gte('start_time', today_str).order('start_time').limit(1).execute()
            if not getattr(response, 'data', None):
                return f"❌ Nenhum próximo jogo encontrado para {team_name}"
            game = response.data[0]
            return f"📅 PRÓXIMO JOGO - {team_name.upper()}:\n🏟️ {game['home_team_name']} vs {game['away_team_name']}\n📅 {game['start_time']}"
        
        except Exception as e:
            logger.error(f"Erro ao buscar próximo jogo: {e}")
            return f"❌ Erro: {str(e)}"
    
    # ========== CLASSIFICAÇÃO ==========
    
    def get_standings(self) -> str:
        """Busca classificação do Brasileirão"""
        try:
            cache_key = "standings_brasileirao"
            cached = self._get_cache(cache_key)
            if cached:
                return cached

            # Priorizar dados locais no Supabase
            try:
                resp = self.supabase.table('classificacao').select('*').order('position').execute()
                if getattr(resp, 'data', None):
                    rows = resp.data
                    result = f"🏆 CLASSIFICAÇÃO - BRASILEIRÃO SÉRIE A {datetime.now().year}\n\n"
                    result += f"{'Pos':<4} {'Time':<20} {'Pts':<5} {'J':<4} {'V-E-D':<10} {'SG':<5}\n"
                    result += "=" * 60 + "\n"
                    for team in rows[:20]:
                        pos = team.get('position')
                        name = team.get('team_name','')[:18]
                        pts = team.get('points')
                        played = team.get('played_games')
                        wins = team.get('won')
                        draws = team.get('draw')
                        losses = team.get('lost')
                        gd = team.get('goal_difference', 0)
                        emoji = "🥇" if pos == 1 else "🥈" if pos == 2 else "🥉" if pos == 3 else "🔻" if pos > 16 else "  "
                        result += f"{emoji}{pos:<3} {name:<20} {pts:<5} {played:<4} {wins}-{draws}-{losses:<5} {gd:+3}\n"
                    result += "\n🔝 Libertadores: 1-6 | 🔻 Rebaixamento: 17-20"
                    self._set_cache(cache_key, result)
                    return result
            except Exception:
                logger.debug('Erro ao ler tabela `classificacao` do Supabase')

            # Fallback: usar football-data.org via module hybrid
            if self.fd_client:
                standings = fd.get_standings()
                if not standings:
                    return "❌ Não foi possível buscar a classificação"
                result = f"🏆 CLASSIFICAÇÃO - BRASILEIRÃO SÉRIE A {datetime.now().year}\n\n"
                result += f"{'Pos':<4} {'Time':<20} {'Pts':<5} {'J':<4} {'V-E-D':<10} {'SG':<5}\n"
                result += "=" * 60 + "\n"
                for idx, team in enumerate(standings, start=1):
                    pos = team.get('position', idx)
                    name = team.get('team', {}).get('name','')[:18]
                    pts = team.get('points')
                    played = team.get('playedGames')
                    wins = team.get('won')
                    draws = team.get('draw')
                    losses = team.get('lost')
                    gd = team.get('goalDifference', 0)
                    emoji = "🥇" if pos == 1 else "🥈" if pos == 2 else "🥉" if pos == 3 else "🔻" if pos > 16 else "  "
                    result += f"{emoji}{pos:<3} {name:<20} {pts:<5} {played:<4} {wins}-{draws}-{losses:<5} {gd:+3}\n"
                result += "\n🔝 Libertadores: 1-6 | 🔻 Rebaixamento: 17-20"
                self._set_cache(cache_key, result)
                return result

            return "❌ Classificação não disponível (sem dados locais nem football-data)"
        
        except Exception as e:
            logger.error(f"Erro ao buscar classificação: {e}")
            return f"❌ Erro: {str(e)}"
    
    # ========== ESTATÍSTICAS ==========
    
    def get_team_stats(self, team_name: str, team_id: int) -> str:
        """Estatísticas completas de um time"""
        try:
            cache_key = f"stats_{team_id}"
            cached = self._get_cache(cache_key)
            if cached:
                return cached
            # Tentar coletar estatísticas a partir do Supabase (tabela 'jogos')
            try:
                # pegar últimos 50 jogos envolvendo o time
                resp = self.supabase.table('jogos').select('*').or_(f'home_team_api_id.eq.{team_id},away_team_api_id.eq.{team_id}').order('start_time', desc=True).limit(50).execute()
                rows = getattr(resp, 'data', []) or []
                if rows:
                    played = 0
                    wins = 0
                    draws = 0
                    losses = 0
                    goals_for = 0
                    goals_against = 0
                    form_list = []
                    for r in rows:
                        # obter placar com chaves possíveis
                        home_score = r.get('home_score') if r.get('home_score') is not None else r.get('home_team_score')
                        away_score = r.get('away_score') if r.get('away_score') is not None else r.get('away_team_score')
                        if home_score is None or away_score is None:
                            continue
                        played += 1
                        is_home = (r.get('home_team_api_id') == team_id) or (r.get('home_team_name','').lower() == team_name)
                        gf = home_score if is_home else away_score
                        ga = away_score if is_home else home_score
                        goals_for += gf or 0
                        goals_against += ga or 0
                        if gf > ga:
                            wins += 1
                            form_list.append('V')
                        elif gf == ga:
                            draws += 1
                            form_list.append('E')
                        else:
                            losses += 1
                            form_list.append('D')

                    result = f"📊 ESTATÍSTICAS - {team_name.upper()}\n\n"
                    result += f"🎯 Jogos (últimos {played} considerados): {played}\n"
                    result += f"✅ Vitórias: {wins}\n"
                    result += f"🤝 Empates: {draws}\n"
                    result += f"❌ Derrotas: {losses}\n\n"
                    result += f"⚽ Gols marcados: {goals_for}\n"
                    result += f"🥅 Gols sofridos: {goals_against}\n\n"
                    result += f"📈 Forma recente: {''.join(form_list[:10]) or 'N/A'}\n"

                    if self.ai_analyzer:
                        analysis = self.ai_analyzer.analyze_query(
                            f"Analise o desempenho do {team_name}",
                            json.dumps({'played': played, 'wins': wins, 'draws': draws, 'losses': losses, 'gf': goals_for, 'ga': goals_against}, ensure_ascii=False)
                        )
                        result += f"\n💡 ANÁLISE:\n{analysis}"

                    self._set_cache(cache_key, result)
                    return result
            except Exception:
                logger.debug('Erro ao calcular estatísticas a partir do Supabase')

            # Fallback: tentar obter via football-data (se disponível), agregando localmente
            if self.fd_client:
                matches = fd.get_all_match_scores(status='FINISHED')
                team_matches = [m for m in matches if (m.get('homeTeam', {}).get('name','').lower() == team_name or m.get('awayTeam', {}).get('name','').lower() == team_name)]
                if team_matches:
                    played = len(team_matches)
                    wins = draws = losses = goals_for = goals_against = 0
                    form_list = []
                    for m in team_matches[:50]:
                        home = m.get('homeTeam', {}).get('name','').lower()
                        away = m.get('awayTeam', {}).get('name','').lower()
                        home_score = m.get('score', {}).get('fullTime', {}).get('home')
                        away_score = m.get('score', {}).get('fullTime', {}).get('away')
                        if home_score is None or away_score is None:
                            continue
                        is_home = (team_name == home)
                        gf = home_score if is_home else away_score
                        ga = away_score if is_home else home_score
                        goals_for += gf or 0
                        goals_against += ga or 0
                        if gf > ga:
                            wins += 1
                            form_list.append('V')
                        elif gf == ga:
                            draws += 1
                            form_list.append('E')
                        else:
                            losses += 1
                            form_list.append('D')

                    result = f"📊 ESTATÍSTICAS - {team_name.upper()}\n\n"
                    result += f"🎯 Jogos: {played}\n✅ Vitórias: {wins}\n🤝 Empates: {draws}\n❌ Derrotas: {losses}\n\n"
                    result += f"⚽ Gols marcados: {goals_for}\n🥅 Gols sofridos: {goals_against}\n\n"
                    result += f"📈 Forma recente: {''.join(form_list[:10]) or 'N/A'}\n"
                    if self.ai_analyzer:
                        analysis = self.ai_analyzer.analyze_query(f"Analise o desempenho do {team_name}", json.dumps({'played': played, 'wins': wins, 'draws': draws, 'losses': losses}, ensure_ascii=False))
                        result += f"\n💡 ANÁLISE:\n{analysis}"
                    self._set_cache(cache_key, result)
                    return result

            return f"❌ Estatísticas não disponíveis para {team_name}"
        
        except Exception as e:
            logger.error(f"Erro ao buscar estatísticas: {e}")
            return f"❌ Erro: {str(e)}"
    
    # ========== ODDS E ANÁLISE ==========
    
    def get_match_odds(self, home_team: str, away_team: str) -> str:
        """Busca odds reais ou simula com análise"""
        try:
            result = f"🎲 ODDS - {home_team.upper()} vs {away_team.upper()}\n\n"
            
            # Simular odds (em produção, integrar com Odds API)
            result += f"🏠 Vitória {home_team}: 2.10 (47.6%)\n"
            result += f"🤝 Empate: 3.20 (31.2%)\n"
            result += f"✈️ Vitória {away_team}: 3.50 (28.6%)\n\n"
            result += f"💡 Over 2.5 gols: 1.90\n"
            result += f"💡 Ambas marcam: 1.75\n\n"
            
            # Análise com IA
            if self.ai_analyzer:
                context = f"Confronto: {home_team} vs {away_team}"
                analysis = self.ai_analyzer.analyze_query(
                    "Analise este confronto e sugira apostas de valor",
                    context
                )
                result += f"🎯 ANÁLISE DETALHADA:\n{analysis}"
            
            return result
        
        except Exception as e:
            logger.error(f"Erro ao buscar odds: {e}")
            return f"❌ Erro: {str(e)}"
    
    # ========== ANÁLISE INTELIGENTE ==========
    
    def analyze_query(self, query: str) -> str:
        """Análise inteligente de queries com IA"""
        q_norm = _normalize_text(query)
        logger.info(f"analyze_query called. raw='{query}' | normalized='{q_norm}'")
        try:
            # diagnóstico: tentar extrair time imediatamente para logs
            try:
                extracted_name, extracted_id = self._extract_team_info(query)
            except Exception:
                extracted_name, extracted_id = (None, None)
            logger.info(f"Extracted team from query: name={extracted_name} id={extracted_id}")
            # Padrões reconhecidos (usando texto normalizado)
            if any(p in q_norm for p in ['jogos hoje', 'partidas hoje', 'jogos de hoje']):
                return self.get_games_today()

            if 'classificacao' in q_norm or 'tabela' in q_norm or 'classificacao' in q_norm:
                return self.get_standings()

            # Próximos jogos (plural) e próximo jogo
            if any(p in q_norm for p in ['proximo jogo', 'proximos jogos', 'proximo jogos', 'proximos jogo', 'proximo']):
                team_name, team_id = self._extract_team_info(query)
                if team_name and team_id:
                    # buscar próximos 5 jogos
                    matches = self._get_next_matches_from_supabase(team_id, limit=5)
                    if matches:
                        res = f"📅 PRÓXIMOS JOGOS - {team_name.upper()}:\n"
                        for m in matches:
                            # formato dependendo da origem
                            if m.get('home_team_name'):
                                res += f"\n🏟️ {m.get('home_team_name')} vs {m.get('away_team_name')}\n📅 {m.get('start_time')}\n"
                            else:
                                res += self._format_fd_match(m) + "\n"
                        return res
                    # fallback to football-data
                    if self.fd_client:
                        future = fd.search_future_games()
                        team_norm = _normalize_text(team_name)
                        team_matches = [m for m in future if team_norm in _normalize_text(m.get('homeTeam', {}).get('name','')) or team_norm in _normalize_text(m.get('awayTeam', {}).get('name',''))]
                        if team_matches:
                            res = f"📅 PRÓXIMOS JOGOS - {team_name.upper()}:\n"
                            for m in team_matches[:5]:
                                res += self._format_fd_match(m) + "\n"
                            return res

                    return f"❌ Nenhum próximo jogo encontrado para {team_name}"

            # Último jogo / estatísticas do último jogo
            if any(p in q_norm for p in ['ultimo jogo', 'último jogo', 'estatisticas do ultimo jogo', 'estatisticas ultimo jogo', 'estatistica ultimo']):
                team_name, team_id = self._extract_team_info(query)
                if team_name and team_id:
                    last = self._get_last_match_from_supabase(team_id)
                    if last:
                        # formatar
                        info = f"📊 ÚLTIMO JOGO - {team_name.upper()}:\n"
                        if last.get('home_team_name'):
                            info += f"🏟️ {last.get('home_team_name')} {last.get('home_team_score')} x {last.get('away_team_score')} {last.get('away_team_name')}\n"
                            info += f"📅 {last.get('start_time')} | Status: {last.get('status')}\n"
                        else:
                            info += self._format_fd_match(last) + "\n"
                        return info
                    # fallback football-data
                    if self.fd_client:
                        finished = fd.get_all_match_scores(status='FINISHED')
                        team_norm = _normalize_text(team_name)
                        team_matches = [m for m in finished if team_norm in _normalize_text(m.get('homeTeam', {}).get('name','')) or team_norm in _normalize_text(m.get('awayTeam', {}).get('name',''))]
                        if team_matches:
                            m = sorted(team_matches, key=lambda x: x.get('utcDate',''), reverse=True)[0]
                            return self._format_fd_match(m)
                    return f"❌ Nenhum último jogo encontrado para {team_name}"

            # Estatísticas gerais
            if 'estatistica' in q_norm or 'desempenho' in q_norm or 'estatisticas' in q_norm:
                team_name, team_id = self._extract_team_info(query)
                if team_name and team_id:
                    return self.get_team_stats(team_name, team_id)
                return "❌ Especifique um time. Ex: 'estatísticas do Palmeiras'"

            # Odds/apostas
            if 'odds' in q_norm or 'aposta' in q_norm:
                # Extrair times da query (usando normalized keys)
                teams = [orig for orig in TEAMS_MAP.keys() if _normalize_text(orig) in q_norm]
                if len(teams) >= 2:
                    return self.get_match_odds(teams[0], teams[1])
                return "❌ Mencione dois times. Ex: 'odds Flamengo vs Palmeiras'"

            # Query não reconhecida - usar IA
            if self.ai_analyzer:
                logger.info(f"Query não reconhecida, usando IA: {query}")
                context = "Dados disponíveis limitados. Fornecendo análise geral."
                return self.ai_analyzer.analyze_query(query, context)

            return self._get_help_message()

        except Exception as e:
            logger.error(f"Erro ao analisar query: {e}")
            return f"❌ Erro ao processar sua pergunta: {str(e)}"
    
    def _get_help_message(self) -> str:
        """Mensagem de ajuda"""
        return """
🤖 BOT TIPSTER DE FUTEBOL - Comandos Disponíveis:

📅 JOGOS:
• "Quais jogos hoje?"
• "Próximo jogo do Flamengo"
• "Jogos de amanhã"

📊 ESTATÍSTICAS:
• "Estatísticas do Palmeiras"
• "Classificação do Brasileirão"
• "Tabela da Série A"

🎲 ODDS E ANÁLISE:
• "Odds Flamengo vs Corinthians"
• "Análise do jogo de hoje"
• "Quem vai ganhar?"

💡 PERGUNTAS LIVRES:
Faça qualquer pergunta sobre futebol! A IA responderá.
Exemplos: "Quem tem mais chances de ser campeão?"
         "O Fluminense vai cair?"
"""

    def sync_daily_data(self):
        """Sincroniza dados diários da API"""
        try:
            logger.info("Iniciando sincronização diária...")
            # Priorizar football-data hybrid para sincronização (se disponível)
            if self.fd_client:
                try:
                    matches = fd.get_all_match_scores(status='FINISHED')
                    if matches:
                        fd.save_matches_to_db(matches, source='football_data', dry_run=False)
                    # atualizar futuros agendados
                    future_games = fd.search_future_games()
                    if future_games:
                        fd.save_matches_to_db(future_games, source='football_data', dry_run=False)
                    # standings
                    standings = fd.get_standings()
                    if standings:
                        fd.save_standings_to_db(standings, season=DEFAULT_SEASON, dry_run=False)
                    logger.info(f"Sincronização concluída: {len(matches) if matches else 0} jogos salvos (football-data)")
                    return
                except Exception as e:
                    logger.error(f"Erro usando football-data hybrid: {e}")

            logger.warning("Nenhuma fonte externa configurada para sincronização (football-data indisponível)")
        
        except Exception as e:
            logger.error(f"Erro na sincronização: {e}")


# ========== INTERFACE DE COMPATIBILIDADE ==========

_bot_instance = None

def get_bot_instance():
    """Retorna instância singleton do bot"""
    global _bot_instance
    if _bot_instance is None:
        _bot_instance = FootballTipsterBot(
            supabase,
            API_FOOTBALL_KEY,
            GROQ_API_KEY
        )
    return _bot_instance

def ask_bot(query: str) -> str:
    """
    Interface de compatibilidade para imports existentes.
    
    Args:
        query: Pergunta do usuário
        
    Returns:
        Resposta do bot
    """
    try:
        bot = get_bot_instance()
        return bot.analyze_query(query)
    except Exception as e:
        logger.error(f"Erro no ask_bot: {e}")
        return f"❌ Erro ao processar pergunta: {str(e)}"

def main():
    """Função principal"""
    bot = get_bot_instance()
    
    print("=" * 70)
    print("⚽ BOT TIPSTER DE FUTEBOL BRASILEIRO - VERSÃO INTELIGENTE")
    print("=" * 70)
    print(f"📅 Data: {bot.today}")
    print(f"🤖 IA: {'✅ Ativa' if bot.ai_analyzer else '❌ Desabilitada'}")
    print(f"🌐 Football-Data: {'✅ Disponível' if bot.fd_client else '❌ Indisponível'} | Supabase: {'✅ Conectado' if bot.supabase else '❌ Offline'}")
    print("=" * 70)
    print("\n💬 Digite suas perguntas ou 'sair' para encerrar")
    print("💡 Digite 'ajuda' para ver comandos\n")
    
    while True:
        try:
            user_input = input("🗣️  Você: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['sair', 'exit', 'quit']:
                print("\n👋 Até logo! Boas apostas! 🍀")
                break
            
            if user_input.lower() in ['ajuda', 'help']:
                print(bot._get_help_message())
                continue
            
            # Processar query
            print("\n🤔 Analisando...\n")
            response = bot.analyze_query(user_input)
            print(f"🤖 Bot:\n{response}\n")
            print("-" * 70)
        
        except KeyboardInterrupt:
            print("\n\n👋 Encerrando...")
            break
        except Exception as e:
            logger.error(f"Erro no loop principal: {e}")
            print(f"\n❌ Erro: {str(e)}\n")

if __name__ == '__main__':
    main()