from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime
from typing import Dict, Any, Optional
from football_nlp_processor import FootballQueryProcessor
from football_tipster_ai import FootballTipsterAI
import asyncio
import sys
import os

# Adicionar o diretório tools ao path para importar smart_web_printer
sys.path.append(os.path.join(os.path.dirname(__file__), 'tools'))

try:
    from smart_web_printer import SmartWebPrinter
    smart_printer = SmartWebPrinter()
except ImportError as e:
    print(f"⚠️  SmartWebPrinter não disponível: {e}")
    smart_printer = None

app = Flask(__name__)
CORS(app)

# Inicializar processadores
nlp_processor = FootballQueryProcessor()
tipster_ai = FootballTipsterAI()

# Config Supabase
SUPABASE_URL = "https://nflmvptqgicabovfmnos.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5mbG12cHRxZ2ljYWJvdmZtbm9zIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM3NzEzNTAsImV4cCI6MjA3OTM0NzM1MH0.l-RuwMrLgQgfjp8XZQ7bpEwfKODo7qKEXOhGR49xJ9c"

def get_supabase_client():
    from supabase import create_client
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def consultar_classificacao():
    """Busca classificação atual do Brasileirão - prioriza Supabase, usa API-Football como fallback"""
    try:
        # Primeiro tentar Supabase (dados locais mais atuais)
        supabase = get_supabase_client()
        result = supabase.table('classificacao').select('*').order('position').execute()

        if result.data and len(result.data) > 0:
            print(f"✅ Classificação obtida do Supabase: {len(result.data)} times")
            return result.data

        # Fallback para API-Football (dados históricos)
        print("⚠️ Nenhum dado no Supabase, tentando API-Football...")
        import requests
        import os

        api_key = os.environ.get("API_FOOTBALL_KEY") or os.environ.get("RAPIDAPI_KEY") or os.environ.get("X_APISPORTS_KEY")
        if not api_key:
            print("❌ Nenhuma chave de API-Football encontrada")
            return []

        url = "https://v3.football.api-sports.io/standings"
        headers = {"x-apisports-key": api_key}
        params = {"league": 71, "season": 2023}

        response = requests.get(url, headers=headers, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            standings = data.get('response', [])

            if standings and len(standings) > 0:
                league_standings = standings[0].get('league', {}).get('standings', [])

                classificacao_formatada = []
                for pos, team_data in enumerate(league_standings[0] if league_standings else [], 1):
                    team_info = team_data.get('team', {})
                    stats = team_data.get('all', {})

                    classificacao_formatada.append({
                        'position': pos,
                        'nome': team_info.get('name', 'N/A'),
                        'pontos': team_data.get('points', 0),
                        'jogos': stats.get('played', 0),
                        'vitorias': stats.get('win', 0),
                        'empates': stats.get('draw', 0),
                        'derrotas': stats.get('lose', 0),
                        'gols_pro': stats.get('goals', {}).get('for', 0),
                        'gols_contra': stats.get('goals', {}).get('against', 0),
                        'saldo_gols': team_data.get('goalsDiff', 0)
                    })

                print(f"✅ Classificação obtida via API-Football: {len(classificacao_formatada)} times")
                return classificacao_formatada

        print(f"❌ Erro na API-Football: {response.status_code}")
        return []

    except Exception as e:
        print(f"❌ Erro ao consultar classificação: {e}")
        return []

def buscar_jogos_fla_flu():
    try:
        supabase = get_supabase_client()
        
        # IDs dos times Fla x Flu (API IDs)
        flamengo_api_id = 1215
        fluminense_api_id = 1216
        
        # Buscar jogos onde um time é Flamengo e outro é Fluminense
        result1 = supabase.table('jogos').select('*').eq('home_team_api_id', flamengo_api_id).eq('away_team_api_id', fluminense_api_id).order('start_time', desc=True).execute()
        result2 = supabase.table('jogos').select('*').eq('home_team_api_id', fluminense_api_id).eq('away_team_api_id', flamengo_api_id).order('start_time', desc=True).execute()
        
        # Combinar e ordenar resultados
        jogos = result1.data + result2.data
        jogos.sort(key=lambda x: x.get('start_time', ''), reverse=True)
        
        return jogos
    except Exception as e:
        print(f"Erro ao buscar jogos Fla x Flu: {e}")
        return []

def consultar_estatisticas_jogo(jogo_api_id=None):
    try:
        supabase = get_supabase_client()
        
        if jogo_api_id:
            # Buscar estatísticas de um jogo específico
            result = supabase.table('estatisticas_jogo').select('*').eq('jogo_api_id', jogo_api_id).execute()
        else:
            # Buscar estatísticas do último jogo disponível
            result = supabase.table('estatisticas_jogo').select('*').order('created_at', desc=True).limit(50).execute()
        
        if not result.data:
            return {}
        
        # Organizar estatísticas por jogo
        stats_por_jogo = {}
        for stat in result.data:
            jogo_id = stat.get('jogo_api_id')
            if jogo_id not in stats_por_jogo:
                stats_por_jogo[jogo_id] = {
                    'estatisticas': {},
                    'home_team': 'Casa',
                    'away_team': 'Visitante'
                }
            
            stat_name = stat.get('stat_name', '')
            home_value = stat.get('home_value', '0')
            away_value = stat.get('away_value', '0')
            
            stats_por_jogo[jogo_id]['estatisticas'][stat_name] = {
                'home': home_value,
                'away': away_value
            }
        
        return stats_por_jogo
    except Exception as e:
        print(f"Erro ao consultar estatísticas: {e}")
        return {}

def consultar_jogos_futuros(dias_ahead=7):
    """Busca jogos futuros nos próximos dias - prioriza Supabase, usa API-Football como fallback"""
    try:
        from datetime import datetime, timedelta

        # Primeiro tentar Supabase (dados locais mais atuais)
        supabase = get_supabase_client()
        hoje = datetime.now()
        data_fim = hoje + timedelta(days=dias_ahead)

        # Buscar jogos futuros no Supabase
        result = supabase.table('jogos').select('*').gte('start_time', hoje.isoformat()).lte('start_time', data_fim.isoformat()).order('start_time').execute()

        if result.data and len(result.data) > 0:
            jogos_formatados = []
            for jogo in result.data:
                jogos_formatados.append({
                    'data': jogo.get('start_time', 'N/A')[:10] if jogo.get('start_time') else 'N/A',
                    'hora': jogo.get('start_time', 'N/A')[11:16] if jogo.get('start_time') else 'N/A',
                    'casa': 'Time Casa',  # TODO: mapear nomes dos times
                    'fora': 'Time Fora',
                    'estadio': 'Estádio',
                    'api_id': jogo.get('api_id'),
                    'status': jogo.get('status', 'NS'),
                    'round': 'Rodada N/A'  # TODO: adicionar rodada
                })

            print(f"✅ Jogos futuros obtidos do Supabase: {len(jogos_formatados)} jogos")
            return jogos_formatados

        # Fallback para API-Football
        print("⚠️ Nenhum jogo futuro no Supabase, tentando API-Football...")
        import requests
        import os

        api_key = os.environ.get("API_FOOTBALL_KEY") or os.environ.get("RAPIDAPI_KEY") or os.environ.get("X_APISPORTS_KEY")
        if not api_key:
            print("❌ Nenhuma chave de API-Football encontrada")
            return []

        # Usar API-Football para fixtures
        url = "https://v3.football.api-sports.io/fixtures"
        headers = {"x-apisports-key": api_key}
        params = {
            "league": 71,  # ID do Brasileirão Série A
            "season": 2023,  # Temporada 2023 (disponível no plano gratuito)
            "from": hoje.strftime('%Y-%m-%d'),
            "to": data_fim.strftime('%Y-%m-%d'),
            "status": "NS"  # Not Started - apenas jogos não iniciados
        }

        response = requests.get(url, headers=headers, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            fixtures = data.get('response', [])

            jogos_formatados = []
            for fixture in fixtures:
                fixture_info = fixture.get('fixture', {})
                teams = fixture.get('teams', {})

                jogos_formatados.append({
                    'data': fixture_info.get('date', 'N/A')[:10] if fixture_info.get('date') else 'N/A',
                    'hora': fixture_info.get('date', 'N/A')[11:16] if fixture_info.get('date') else 'N/A',
                    'casa': teams.get('home', {}).get('name', 'Time Casa'),
                    'fora': teams.get('away', {}).get('name', 'Time Fora'),
                    'estadio': fixture.get('fixture', {}).get('venue', {}).get('name', 'Estádio'),
                    'api_id': fixture_info.get('id'),
                    'status': fixture_info.get('status', {}).get('short', 'NS'),
                    'round': fixture.get('league', {}).get('round', 'N/A')
                })

            print(f"✅ Jogos futuros obtidos via API-Football: {len(jogos_formatados)} jogos nos próximos {dias_ahead} dias")
            return jogos_formatados

        print(f"❌ Erro na API-Football: {response.status_code}")
        return []

    except Exception as e:
        print(f"❌ Erro ao buscar jogos futuros: {e}")
        return []

def consultar_jogos_time(team_name):
    """Busca próximos jogos de um time específico"""
    try:
        supabase = get_supabase_client()
        # TODO: implementar mapeamento de nomes para API IDs
        # Por enquanto retorna jogos recentes
        result = supabase.table('jogos').select('*').order('start_time', desc=True).limit(5).execute()

        jogos_formatados = []
        for jogo in result.data:
            jogos_formatados.append({
                'data': jogo.get('start_time', 'N/A')[:10] if jogo.get('start_time') else 'N/A',
                'hora': jogo.get('start_time', 'N/A')[11:16] if jogo.get('start_time') else 'N/A',
                'adversario': 'Adversário',
                'mandante': True,  # TODO: determinar se é mandante
                'api_id': jogo.get('api_id')
            })

        return jogos_formatados
    except Exception as e:
        print(f"Erro ao buscar jogos do time {team_name}: {e}")
        return []

def consultar_estatisticas_time(team_name):
    """Busca estatísticas recentes de um time"""
    try:
        # TODO: implementar busca real por time
        # Por enquanto retorna estatísticas genéricas
        return {
            'Posse de Bola': '55%',
            'Total de chutes': '12',
            'Escanteios': '6',
            'Faltas cometidas': '15'
        }
    except Exception as e:
        return {}

def consultar_estatisticas_jogador(player_name):
    """Busca estatísticas de um jogador"""
    try:
        # TODO: implementar busca real por jogador
        return {
            'Gols': 5,
            'Assistências': 3,
            'Chutes': 25,
            'Passes certos': '85%'
        }
    except Exception as e:
        return {}

def consultar_historico_confronto(team1, team2):
    """Busca histórico de confrontos entre dois times"""
    try:
        # TODO: implementar busca real de confrontos
        return {
            'vitorias_team1': 12,
            'vitorias_team2': 8,
            'empates': 5
        }
    except Exception as e:
        return {}

async def processar_conteudo_web(url: str) -> Dict[str, Any]:
    """Processa conteúdo web usando impressão inteligente"""
    if not smart_printer:
        return {
            'error': 'Sistema de impressão inteligente não disponível',
            'details': 'Verifique se todas as dependências estão instaladas'
        }

    try:
        # Processar conteúdo
        resultado = await smart_printer.process_web_content(url)

        if resultado:
            # Verificar duplicatas e inserir no banco se não for duplicado
            if not resultado.get('duplicate', False):
                # TODO: Implementar inserção no banco baseada no tipo de conteúdo
                print(f"📥 Inserindo dados no banco: {resultado.get('content_type')}")

                # Simulação de inserção baseada no tipo
                content_type = resultado.get('content_type', '')

                if content_type == 'injury_report':
                    # Inserir relatório de lesões
                    insert_result = await inserir_relatorio_lesoes(resultado)
                    resultado['insert_result'] = insert_result
                elif content_type in ['match_preview', 'match_report']:
                    # Inserir dados de jogo
                    insert_result = await inserir_dados_jogo(resultado)
                    resultado['insert_result'] = insert_result
                elif content_type == 'player_news':
                    # Inserir notícias de jogador
                    insert_result = await inserir_noticia_jogador(resultado)
                    resultado['insert_result'] = insert_result
                elif content_type == 'game_stats':
                    # Inserir estatísticas de jogo
                    insert_result = await inserir_dados_jogo(resultado)
                    resultado['insert_result'] = insert_result
                else:
                    print(f"⚠️  Tipo de conteúdo não suportado para inserção: {content_type}")

            return resultado
        else:
            return {'error': 'Falha no processamento do conteúdo'}

    except Exception as e:
        return {'error': f'Erro no processamento: {str(e)}'}

async def inserir_relatorio_lesoes(data: Dict[str, Any]):
    """Insere relatório de lesões no banco"""
    try:
        supabase = get_supabase_client()

        # Verificar duplicatas
        is_duplicate, existing_id = verificar_duplicata_lesao(data)
        if is_duplicate:
            print(f"⚠️  Lesão já existe (ID: {existing_id}) - pulando inserção")
            return {'status': 'duplicate', 'id': existing_id}

        # Inserir lesões
        lesoes_inseridas = []
        for jogador_data in data.get('players', []):
            lesao_data = {
                'jogador_nome': jogador_data.get('name'),
                'tipo_lesao': jogador_data.get('injury_type'),
                'gravidade': jogador_data.get('severity'),
                'tempo_recuperacao': jogador_data.get('recovery_time'),
                'data_lesao': data.get('date'),
                'fonte': data.get('source_url'),
                'created_at': datetime.now().isoformat()
            }

            result = supabase.table('lesoes').insert(lesao_data).execute()
            if result.data:
                lesoes_inseridas.append(result.data[0])

        print(f"🏥 Inseridas {len(lesoes_inseridas)} lesões")
        return {'status': 'inserted', 'count': len(lesoes_inseridas)}

    except Exception as e:
        print(f"Erro ao inserir lesões: {e}")
        return {'status': 'error', 'error': str(e)}

async def inserir_dados_jogo(data: Dict[str, Any]):
    """Insere dados de jogo no banco (com verificação de duplicata)"""
    try:
        supabase = get_supabase_client()

        # Tentar encontrar jogo existente
        jogo_existente = encontrar_jogo_por_dados(data)

        if jogo_existente:
            jogo_id = jogo_existente['id']
            print(f"🎯 Jogo encontrado: {jogo_id} - atualizando estatísticas")

            # Verificar se já tem estatísticas
            stats_existentes = supabase.table('estatisticas_jogo').select('*').eq('jogo_api_id', jogo_id).execute()
            if stats_existentes.data:
                print(f"⚠️  Jogo {jogo_id} já tem estatísticas - pulando")
                return {'status': 'duplicate', 'jogo_id': jogo_id}

            # Inserir estatísticas
            return await inserir_estatisticas_jogo(jogo_id, data)
        else:
            print("⚠️  Jogo não encontrado no banco - criando novo jogo")

            # Criar novo jogo
            novo_jogo = await criar_jogo_de_dados_extraidos(data)
            if novo_jogo:
                return await inserir_estatisticas_jogo(novo_jogo['id'], data)

        return {'status': 'error', 'message': 'Não foi possível processar dados do jogo'}

    except Exception as e:
        print(f"Erro ao inserir dados de jogo: {e}")
        return {'status': 'error', 'error': str(e)}

async def inserir_estatisticas_jogo(jogo_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
    """Insere estatísticas específicas de um jogo"""
    try:
        supabase = get_supabase_client()

        stats_inseridas = 0
        estatisticas = data.get('data', {}).get('statistics', {})

        for stat_name, stat_data in estatisticas.items():
            stat_record = {
                'jogo_api_id': jogo_id,
                'stat_name': stat_name,
                'home_value': stat_data.get('home', '0'),
                'away_value': stat_data.get('away', '0'),
                'created_at': datetime.now().isoformat()
            }

            result = supabase.table('estatisticas_jogo').insert(stat_record).execute()
            if result.data:
                stats_inseridas += 1

        print(f"📊 Inseridas {stats_inseridas} estatísticas para jogo {jogo_id}")
        return {'status': 'inserted', 'jogo_id': jogo_id, 'stats_count': stats_inseridas}

    except Exception as e:
        print(f"Erro ao inserir estatísticas: {e}")
        return {'status': 'error', 'error': str(e)}

async def inserir_noticia_jogador(data: Dict[str, Any]):
    """Insere notícia de jogador no banco"""
    try:
        supabase = get_supabase_client()

        # Verificar duplicatas
        is_duplicate, existing_id = verificar_duplicata_noticia_jogador(data)
        if is_duplicate:
            print(f"⚠️  Notícia já existe (ID: {existing_id}) - pulando inserção")
            return {'status': 'duplicate', 'id': existing_id}

        # Inserir notícia
        noticia_data = {
            'jogador_nome': data.get('player_name'),
            'titulo': data.get('title'),
            'conteudo': data.get('content'),
            'tipo_noticia': data.get('news_type'),
            'time_atual': data.get('current_team'),
            'fonte': data.get('source_url'),
            'data_publicacao': data.get('date'),
            'created_at': datetime.now().isoformat()
        }

        result = supabase.table('noticias_jogadores').insert(noticia_data).execute()

        if result.data:
            print(f"👤 Notícia de jogador inserida: {result.data[0]['id']}")
            return {'status': 'inserted', 'id': result.data[0]['id']}

    except Exception as e:
        print(f"Erro ao inserir notícia: {e}")
        return {'status': 'error', 'error': str(e)}

def verificar_duplicata_lesao(data: Dict[str, Any]) -> tuple[bool, Optional[int]]:
    """Verifica se lesão já existe"""
    try:
        supabase = get_supabase_client()

        for jogador in data.get('players', []):
            result = supabase.table('lesoes').select('id').eq('jogador_nome', jogador.get('name')).eq('data_lesao', data.get('date')).execute()
            if result.data:
                return True, result.data[0]['id']

        return False, None
    except Exception as e:
        print(f"Erro na verificação de duplicata lesão: {e}")
        return False, None

def verificar_duplicata_noticia_jogador(data: Dict[str, Any]) -> tuple[bool, Optional[int]]:
    """Verifica se notícia de jogador já existe"""
    try:
        supabase = get_supabase_client()

        result = supabase.table('noticias_jogadores').select('id').eq('jogador_nome', data.get('player_name')).eq('titulo', data.get('title')).execute()
        if result.data:
            return True, result.data[0]['id']

        return False, None
    except Exception as e:
        print(f"Erro na verificação de duplicata notícia: {e}")
        return False, None

def encontrar_jogo_por_dados(data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Encontra jogo existente baseado nos dados extraídos"""
    try:
        supabase = get_supabase_client()

        teams = data.get('teams', [])
        if len(teams) < 2:
            return None

        # Tentar encontrar por nomes dos times
        # Primeiro, buscar times por nome aproximado
        home_team_result = supabase.table('times').select('api_id').ilike('name', f'%{teams[0]}%').execute()
        away_team_result = supabase.table('times').select('api_id').ilike('name', f'%{teams[1]}%').execute()

        if not home_team_result.data or not away_team_result.data:
            return None

        home_api_id = home_team_result.data[0]['api_id']
        away_api_id = away_team_result.data[0]['api_id']

        # Buscar jogo por times
        jogo_result = supabase.table('jogos').select('*').eq('home_team_api_id', home_api_id).eq('away_team_api_id', away_api_id).execute()

        if jogo_result.data:
            # Se encontrou múltiplos, pegar o mais recente
            jogos_ordenados = sorted(jogo_result.data, key=lambda x: x.get('start_time', ''), reverse=True)
            return jogos_ordenados[0]

        return None

    except Exception as e:
        print(f"Erro ao buscar jogo: {e}")
        return None

async def criar_jogo_de_dados_extraidos(data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Cria novo jogo baseado em dados extraídos"""
    try:
        supabase = get_supabase_client()

        teams = data.get('teams', [])
        if len(teams) < 2:
            return None

        # Buscar IDs dos times
        home_team_result = supabase.table('times').select('api_id').ilike('name', f'%{teams[0]}%').execute()
        away_team_result = supabase.table('times').select('api_id').ilike('name', f'%{teams[1]}%').execute()

        if not home_team_result.data or not away_team_result.data:
            print(f"Times não encontrados: {teams}")
            return None

        # Criar jogo básico
        jogo_data = {
            'home_team_api_id': home_team_result.data[0]['api_id'],
            'away_team_api_id': away_team_result.data[0]['api_id'],
            'start_time': data.get('date', datetime.now().isoformat()),
            'status': 'FT',  # Finished
            'created_at': datetime.now().isoformat()
        }

        result = supabase.table('jogos').insert(jogo_data).execute()
        if result.data:
            print(f"⚽ Novo jogo criado: {result.data[0]['id']}")
            return result.data[0]

        return None

    except Exception as e:
        print(f"Erro ao criar jogo: {e}")
        return None

def calcular_odds_jogo(team1, team2):
    """Calcula odds estimadas para um jogo"""
    try:
        # Tenta buscar odds reais primeiro
        odds_reais = nlp_processor.buscar_odds_jogo(team1, team2)
        if odds_reais:
            return odds_reais

        # Fallback para cálculo baseado em estatísticas
        # Buscar estatísticas dos times
        stats1 = consultar_estatisticas_time(team1)
        stats2 = consultar_estatisticas_time(team2)

        # Usar Tipster AI para calcular probabilidades
        probs = tipster_ai.calcular_probabilidade_vitoria(stats1, stats2)

        # Converter probabilidades em odds (simplificado)
        odds = {
            'casa': round(100 / probs['casa'], 2) if probs['casa'] > 0 else 1.01,
            'empate': round(100 / probs['empate'], 2) if probs['empate'] > 0 else 1.01,
            'fora': round(100 / probs['fora'], 2) if probs['fora'] > 0 else 1.01,
            'fonte': 'Cálculo baseado em estatísticas',
            'atualizado_em': datetime.now().strftime('%H:%M')
        }

        return odds
    except Exception as e:
        return {'casa': 2.0, 'empate': 3.5, 'fora': 3.0, 'fonte': 'Padrão', 'atualizado_em': datetime.now().strftime('%H:%M')}

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        prompt = data.get('message', data.get('prompt', ''))

        # Classificar a query usando NLP
        classification = nlp_processor.classify_query(prompt)

        # Buscar dados relevantes baseado no tipo de query
        response_data = None

        if classification['type'] == 'jogos_hoje':
            # Buscar jogos de hoje
            response_data = {'jogos': consultar_jogos_hoje()}
        elif classification['type'] == 'jogos_time':
            team = classification['entities'].get('team')
            response_data = {'jogos': consultar_jogos_time(team)}
        elif classification['type'] == 'classificacao':
            response_data = {'classificacao': consultar_classificacao()}
        elif classification['type'] == 'estatisticas_time':
            team = classification['entities'].get('team')
            response_data = {'estatisticas': consultar_estatisticas_time(team)}
        elif classification['type'] == 'jogos_semana':
            # Buscar jogos futuros
            jogos_futuros = consultar_jogos_futuros(7)
            # Gerar recomendações usando Tipster AI (simplificado)
            response_data = {'jogos': jogos_futuros}
        elif classification['type'] == 'estatisticas_jogador':
            player = classification['entities'].get('player')
            response_data = {'estatisticas': consultar_estatisticas_jogador(player)}
        elif classification['type'] == 'historico_confronto':
            team1 = classification['entities'].get('team1')
            team2 = classification['entities'].get('team2')
            response_data = {'historico': consultar_historico_confronto(team1, team2)}
        elif classification['type'] == 'odds_jogo':
            # Para odds específicas de um jogo
            team1 = classification['entities'].get('team1')
            team2 = classification['entities'].get('team2')
            response_data = {'odds': calcular_odds_jogo(team1, team2)}

        # Gerar resposta natural
        resposta = nlp_processor.generate_response(classification, response_data)

        return jsonify({'reply': resposta})

    except Exception as e:
        return jsonify({'reply': f'❌ Erro no processamento: {str(e)}'})

@app.route('/api/smart-print', methods=['POST'])
def smart_print_endpoint():
    """Endpoint para processar conteúdo web com impressão inteligente"""
    try:
        data = request.get_json()
        url = data.get('url')

        if not url:
            return jsonify({
                'error': 'URL não fornecida',
                'usage': 'POST /api/smart-print com {"url": "https://..."}'
            }), 400

        # Processar conteúdo de forma assíncrona
        resultado = asyncio.run(processar_conteudo_web(url))

        if 'error' in resultado:
            return jsonify(resultado), 500

        return jsonify({
            'success': True,
            'data': resultado,
            'message': 'Conteúdo processado com sucesso'
        })

    except Exception as e:
        return jsonify({
            'error': f'Erro interno: {str(e)}'
        }), 500

@app.route('/')
def root():
    return {'message': 'TradeComigo API - Online', 'status': 'OK'}

if __name__ == '__main__':
    print("Iniciando TradeComigo API (Flask)...")
    app.run(host='127.0.0.1', port=5000, debug=False)