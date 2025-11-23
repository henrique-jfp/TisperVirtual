import re
import random
from datetime import datetime, timedelta

class FootballQueryProcessor:
    """Processador de linguagem natural para consultas de futebol brasileiro"""

    def __init__(self):
        # Data atual para contexto
        self.data_atual = datetime.now()

        # Padrões para identificar tipos de perguntas
        self.patterns = {
            'data_hoje': [
                r'que.*dia.*hoje',
                r'qual.*dia.*hoje',
                r'que.*dia.*é.*hoje',
                r'qual.*dia.*é.*hoje',
                r'dia.*hoje',
                r'data.*hoje',
                r'que.*data.*hoje',
                r'qual.*data.*hoje'
            ],
            'data_ontem': [
                r'que.*dia.*foi.*ontem',
                r'qual.*dia.*foi.*ontem',
                r'quando.*foi.*ontem',
                r'ontem.*foi.*que.*dia',
                r'dia.*ontem',
                r'data.*ontem'
            ],
            'data_amanha': [
                r'que.*dia.*será.*amanhã',
                r'qual.*dia.*será.*amanhã',
                r'quando.*será.*amanhã',
                r'amanhã.*será.*que.*dia',
                r'dia.*amanhã',
                r'data.*amanhã'
            ],
            'jogos_hoje': [
                r'jogos.*hoje',
                r'partidas.*hoje',
                r'quais.*jogos.*hoje',
                r'quais.*partidas.*hoje'
            ],
            'jogos_semana': [
                r'jogos.*semana',
                r'partidas.*semana',
                r'próximos.*jogos',
                r'jogos.*próximos',
                r'jogos.*futuros',
                r'partidas.*futuras',
                r'próximas.*partidas',
                r'quais.*próximos.*jogos',
                r'quais.*jogos.*futuros',
                r'quais.*os.*proximos.*jogos',
                r'quais.*os.*jogos.*futuros',
                r'quais.*próximas.*partidas',
                r'conte.*sobre.*jogo',
                r'fale.*sobre.*jogo'
            ],
            'estatisticas_jogador': [  # Mais específico primeiro
                r'como.*está.*jogando',
                r'estatísticas.*jogando',
                r'performance.*jogando'
            ],
            'jogos_time': [
                r'jogos.*(?:do|da|do)\s+([A-Za-zÀ-ÿ\s]+?)(?:\s|$|x|\?|jogando|nas)',
                r'partidas.*(?:do|da|do)\s+([A-Za-zÀ-ÿ\s]+?)(?:\s|$|x|\?|jogando|nas)',
                r'próximos.*jogos.*(?:do|da|do)\s+([A-Za-zÀ-ÿ\s]+?)(?:\s|$|x|\?|jogando|nas)',
                r'qual.*próximo.*jogo.*(?:do|da|do)\s+([A-Za-zÀ-ÿ\s]+?)(?:\s|$|\?)',
                r'qual.*próximos.*jogos.*(?:do|da|do)\s+([A-Za-zÀ-ÿ\s]+?)(?:\s|$|\?)',
                r'qual.*o.*próximo.*jogo.*(?:do|da|do)\s+([A-Za-zÀ-ÿ\s]+?)(?:\s|$|\?)',
                r'qual.*o.*próximos.*jogos.*(?:do|da|do)\s+([A-Za-zÀ-ÿ\s]+?)(?:\s|$|\?)',
                r'qual.*proximo.*jogo.*(?:do|da|do)\s+([A-Za-zÀ-ÿ\s]+?)(?:\s|$|\?)',
                r'qual.*proximos.*jogos.*(?:do|da|do)\s+([A-Za-zÀ-ÿ\s]+?)(?:\s|$|\?)',
                r'qual.*o.*proximo.*jogo.*(?:do|da|do)\s+([A-Za-zÀ-ÿ\s]+?)(?:\s|$|\?)',
                r'qual.*o.*proximos.*jogos.*(?:do|da|do)\s+([A-Za-zÀ-ÿ\s]+?)(?:\s|$|\?)',
                r'quando.*(?:joga|joga).*o.*([A-Za-zÀ-ÿ\s]+?)(?:\s|$|\?)',
                r'próximo.*jogo.*(?:do|da|do)\s+([A-Za-zÀ-ÿ\s]+?)(?:\s|$|\?)',
                r'proximo.*jogo.*(?:do|da|do)\s+([A-Za-zÀ-ÿ\s]+?)(?:\s|$|\?)'
            ],
            'classificacao': [
                r'classificação',
                r'tabela',
                r'posição.*times',
                r'ranking'
            ],
            'estatisticas_time': [
                r'estatísticas\s+do\s+([A-Za-zÀ-ÿ\s]+?)(?:\s|$)',
                r'stats\s+do\s+([A-Za-zÀ-ÿ\s]+?)(?:\s|$)',
                r'como\s+está\s+o\s+([A-Za-zÀ-ÿ\s]+?)(?:\s|$|nas)'
            ],
            'odds_jogo': [
                r'odd.*vitória.*([A-Za-zÀ-ÿ\s]+?)\s+contra\s+([A-Za-zÀ-ÿ\s]+?)(?:\s|$)',
                r'odd.*empate.*([A-Za-zÀ-ÿ\s]+?)\s+x\s+([A-Za-zÀ-ÿ\s]+?)(?:\s|$)',
                r'probabilidade.*([A-Za-zÀ-ÿ\s]+?)\s+x\s+([A-Za-zÀ-ÿ\s]+?)(?:\s|$|\?)'
            ],
            'melhor_aposta': [
                r'melhor.*aposta',
                r'aposta.*segura',
                r'recomendação.*aposta',
                r'palpite.*hoje',
                r'recomenda.*apostar',
                r'o.*que.*recomenda.*apostar'
            ],
            'historico_confronto': [
                r'histórico.*([A-Za-zÀ-ÿ\s]+).*x.*([A-Za-zÀ-ÿ\s]+)',
                r'confronto.*([A-Za-zÀ-ÿ\s]+).*x.*([A-Za-zÀ-ÿ\s]+)',
                r'retrospecto.*([A-Za-zÀ-ÿ\s]+).*x.*([A-Za-zÀ-ÿ\s]+)'
            ]
        }

        # Mapeamento de nomes de times para normalização
        self.team_mapping = {
            'fla': 'Flamengo',
            'flu': 'Fluminense',
            'mengo': 'Flamengo',
            'tricolor': 'Fluminense',
            'vasco': 'Vasco',
            'botafogo': 'Botafogo',
            'fluminense': 'Fluminense',
            'flamengo': 'Flamengo',
            'palmeiras': 'Palmeiras',
            'corinthians': 'Corinthians',
            'são paulo': 'São Paulo',
            'santos': 'Santos',
            'internacional': 'Internacional',
            'grêmio': 'Grêmio',
            'atlético-mg': 'Atlético-MG',
            'cruzeiro': 'Cruzeiro',
            'bahia': 'Bahia',
            'vitória': 'Vitória',
            'sport': 'Sport',
            'ceará': 'Ceará',
            'fortaleza': 'Fortaleza',
            'goiás': 'Goiás',
            'atlético-go': 'Atlético-GO',
            'coritiba': 'Coritiba',
            'juventude': 'Juventude',
            'américa-mg': 'América-MG',
            'cuiabá': 'Cuiabá',
            'bragantino': 'Bragantino',
            'athletico-pr': 'Athletico-PR'
        }

    def normalize_team_name(self, team_name):
        """Normaliza o nome do time"""
        if not team_name:
            return team_name

        team_lower = team_name.lower().strip()

        # Mapeamento direto
        for key, value in self.team_mapping.items():
            if key in team_lower or team_lower in key:
                return value

        # Tentar encontrar correspondência parcial
        for key, value in self.team_mapping.items():
            if key in team_lower:
                return value

        # Se não encontrou, retornar o original capitalizado
        return team_name.strip().title()

    def get_data_atual_formatada(self):
        """Retorna a data atual formatada em português"""
        meses = {
            1: 'janeiro', 2: 'fevereiro', 3: 'março', 4: 'abril',
            5: 'maio', 6: 'junho', 7: 'julho', 8: 'agosto',
            9: 'setembro', 10: 'outubro', 11: 'novembro', 12: 'dezembro'
        }
        dia = self.data_atual.day
        mes = meses[self.data_atual.month]
        ano = self.data_atual.year
        return f"{dia} de {mes} de {ano}"

    def get_data_ontem_formatada(self):
        """Retorna a data de ontem formatada em português"""
        ontem = self.data_atual - timedelta(days=1)
        meses = {
            1: 'janeiro', 2: 'fevereiro', 3: 'março', 4: 'abril',
            5: 'maio', 6: 'junho', 7: 'julho', 8: 'agosto',
            9: 'setembro', 10: 'outubro', 11: 'novembro', 12: 'dezembro'
        }
        dia = ontem.day
        mes = meses[ontem.month]
        ano = ontem.year
        return f"{dia} de {mes} de {ano}"

    def get_dia_semana_ontem(self):
        """Retorna o dia da semana de ontem"""
        ontem = self.data_atual - timedelta(days=1)
        dias = ['segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira',
                'sexta-feira', 'sábado', 'domingo']
        return dias[ontem.weekday()]

    def get_dia_semana_amanha(self):
        """Retorna o dia da semana de amanhã"""
        amanha = self.data_atual + timedelta(days=1)
        dias = ['segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira',
                'sexta-feira', 'sábado', 'domingo']
        return dias[amanha.weekday()]

    def get_data_amanha_formatada(self):
        """Retorna a data de amanhã formatada em português"""
        amanha = self.data_atual + timedelta(days=1)
        meses = {
            1: 'janeiro', 2: 'fevereiro', 3: 'março', 4: 'abril',
            5: 'maio', 6: 'junho', 7: 'julho', 8: 'agosto',
            9: 'setembro', 10: 'outubro', 11: 'novembro', 12: 'dezembro'
        }
        dia = amanha.day
        mes = meses[amanha.month]
        ano = amanha.year
        return f"{dia} de {mes} de {ano}"

    def get_dia_semana(self):
        """Retorna o dia da semana atual"""
        dias = ['segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira',
                'sexta-feira', 'sábado', 'domingo']
        return dias[self.data_atual.weekday()]

    def buscar_odds_jogo(self, time1, time2):
        """Busca odds reais para um jogo (integração com APIs de odds)"""
        try:
            # TODO: Implementar integração com APIs reais como:
            # - Odds API (odds-api.com)
            # - BetExplorer API
            # - Football Data API com odds
            # - The Odds API

            # Por enquanto, simula busca de odds realistas
            return self._simular_odds_reais(time1, time2)
        except Exception as e:
            print(f"Erro ao buscar odds: {e}")
            return None

    def _simular_odds_reais(self, time1, time2):
        """Simula odds realistas baseadas em estatísticas dos times"""
        # Times considerados "grandes" no Brasil
        grandes_times = ['Flamengo', 'Palmeiras', 'São Paulo', 'Corinthians',
                        'Santos', 'Grêmio', 'Internacional', 'Cruzeiro']

        # Ajusta odds baseado na força relativa dos times
        time1_grande = any(t.lower() in time1.lower() for t in grandes_times)
        time2_grande = any(t.lower() in time2.lower() for t in grandes_times)

        if time1_grande and not time2_grande:
            # Time grande em casa vs time menor
            return {
                'casa': round(random.uniform(1.40, 1.80), 2),
                'empate': round(random.uniform(4.00, 5.50), 2),
                'fora': round(random.uniform(6.00, 9.00), 2),
                'fonte': 'Estimativa baseada em força dos times',
                'atualizado_em': self.data_atual.strftime('%H:%M')
            }
        elif time2_grande and not time1_grande:
            # Time menor em casa vs time grande
            return {
                'casa': round(random.uniform(3.50, 5.00), 2),
                'empate': round(random.uniform(3.50, 4.50), 2),
                'fora': round(random.uniform(1.60, 2.10), 2),
                'fonte': 'Estimativa baseada em força dos times',
                'atualizado_em': self.data_atual.strftime('%H:%M')
            }
        else:
            # Jogo equilibrado
            return {
                'casa': round(random.uniform(2.20, 2.80), 2),
                'empate': round(random.uniform(3.00, 3.80), 2),
                'fora': round(random.uniform(2.80, 3.50), 2),
                'fonte': 'Estimativa baseada em força dos times',
                'atualizado_em': self.data_atual.strftime('%H:%M')
            }

    def atualizar_data_atual(self):
        """Atualiza a data atual (útil para testes ou mudanças de dia)"""
        self.data_atual = datetime.now()

    def classify_query(self, query):
        """Classifica o tipo de pergunta e extrai entidades"""
        query_lower = query.lower().strip()

        # Verifica cada padrão
        for query_type, patterns in self.patterns.items():
            for pattern in patterns:
                match = re.search(pattern, query_lower)
                if match:
                    entities = {}

                    if query_type == 'estatisticas_jogador':
                        # Extrair jogador - mais específico para evitar conflito
                        jogador_match = re.search(r'está\s+o\s+([A-Za-zÀ-ÿ]+)\s+jogando', query_lower)
                        if jogador_match:
                            entities['player'] = jogador_match.group(1).strip()
                    elif query_type == 'jogos_time':
                        # Extrair time da pergunta sobre jogos - usar grupos do match principal
                        if match.groups():
                            team_name = match.group(1).strip()
                            entities['team'] = self.normalize_team_name(team_name)
                    elif query_type == 'estatisticas_time':
                        # Extrair time da pergunta sobre estatísticas
                        time_match = re.search(r'está\s+o\s+([A-Za-zÀ-ÿ\s]+)', query_lower)
                        if time_match:
                            entities['team'] = self.normalize_team_name(time_match.group(1).strip())
                    elif query_type == 'historico_confronto':
                        # Extrair times do confronto
                        confronto_match = re.search(r'([A-Za-zÀ-ÿ\s]+)\s+x\s+([A-Za-zÀ-ÿ\s]+)', query_lower)
                        if confronto_match:
                            entities['team1'] = self.normalize_team_name(confronto_match.group(1).strip())
                            entities['team2'] = self.normalize_team_name(confronto_match.group(2).strip())
                    elif query_type == 'odds_jogo':
                        # Extrair times das odds
                        odds_match = re.search(r'([A-Za-zÀ-ÿ\s]+)\s+contra\s+([A-Za-zÀ-ÿ\s]+)', query_lower)
                        if odds_match:
                            entities['team1'] = self.normalize_team_name(odds_match.group(1).strip())
                            entities['team2'] = self.normalize_team_name(odds_match.group(2).strip())

                    return {
                        'type': query_type,
                        'entities': entities,
                        'confidence': 0.8,  # Simplificado
                        'original_query': query
                    }

        return {
            'type': 'unknown',
            'entities': {},
            'confidence': 0.0,
            'original_query': query
        }

    def generate_response(self, classification, data=None):
        """Gera resposta natural baseada na classificação e dados"""
        query_type = classification['type']
        entities = classification['entities']

        # Adiciona contexto de data em todas as respostas
        data_contexto = f"📅 Hoje é {self.get_dia_semana()}, {self.get_data_atual_formatada()}."

        if query_type == 'data_hoje':
            return self._resposta_data_hoje()
        elif query_type == 'data_ontem':
            return self._resposta_data_ontem()
        elif query_type == 'data_amanha':
            return self._resposta_data_amanha()
        elif query_type == 'jogos_hoje':
            resposta = self._resposta_jogos_hoje(data)
            return f"{data_contexto}\n\n{resposta}"
        elif query_type == 'jogos_time':
            return self._resposta_jogos_time(entities.get('team'), data)
        elif query_type == 'classificacao':
            resposta = self._resposta_classificacao(data)
            return f"{data_contexto}\n\n{resposta}"
        elif query_type == 'estatisticas_time':
            return self._resposta_estatisticas_time(entities.get('team'), data)
        elif query_type == 'jogos_semana':
            resposta = self._resposta_jogos_semana(data)
            return f"{data_contexto}\n\n{resposta}"
            resposta = self._resposta_melhor_aposta(data)
            return f"{data_contexto}\n\n{resposta}"
        elif query_type == 'estatisticas_jogador':
            return self._resposta_estatisticas_jogador(entities.get('player'), data)
        elif query_type == 'historico_confronto':
            return self._resposta_historico_confronto(entities.get('team1'), entities.get('team2'), data)
        elif query_type == 'odds_jogo':
            return self._resposta_odds_jogo(entities.get('team1'), entities.get('team2'))
        else:
            resposta = self._resposta_generica(classification['original_query'])
            return f"{data_contexto}\n\n{resposta}"

    def _resposta_jogos_semana(self, data):
        """Resposta para próximos jogos/jogos da semana"""
        if not data or not data.get('jogos'):
            return "📅 Não encontrei jogos programados para os próximos dias."

        jogos = data['jogos']
        if not jogos:
            return "📅 Nenhum jogo da Série A está marcado para os próximos dias."

        resposta = f"⚽ Próximos jogos da Série A ({len(jogos)} partidas):\n\n"

        # Agrupar por data
        jogos_por_data = {}
        for jogo in jogos:
            data_jogo = jogo.get('data', 'N/A')
            if data_jogo not in jogos_por_data:
                jogos_por_data[data_jogo] = []
            jogos_por_data[data_jogo].append(jogo)

        # Mostrar até 15 jogos organizados por data
        jogos_mostrados = 0
        for data_jogo in sorted(jogos_por_data.keys()):
            if jogos_mostrados >= 15:
                break

            resposta += f"📆 {data_jogo}:\n"

            for jogo in jogos_por_data[data_jogo]:
                if jogos_mostrados >= 15:
                    break

                hora = jogo.get('hora', 'N/A')
                casa = jogo.get('casa', 'N/A')
                fora = jogo.get('fora', 'N/A')
                estadio = jogo.get('estadio', '')
                rodada = jogo.get('round', '')

                resposta += f"  🕐 {hora}: {casa} x {fora}"
                if estadio:
                    resposta += f" - {estadio}"
                if rodada:
                    resposta += f" ({rodada})"
                resposta += "\n"

                jogos_mostrados += 1

        return resposta + "\n💡 Para ver jogos de um time específico, pergunte 'jogos do [nome do time]'!"

    def _resposta_jogos_time(self, team, data):
        """Resposta para jogos de um time específico"""
        if not team:
            return "🤔 Qual time você quer saber sobre os jogos?"

        if not data or not data.get('jogos'):
            return f"📅 Não encontrei jogos recentes do {team}."

        jogos = data['jogos']
        resposta = f"📅 Próximos jogos do {team}:\n\n"

        for jogo in jogos[:5]:
            data_jogo = jogo.get('data', 'N/A')
            hora = jogo.get('hora', 'N/A')
            adversario = jogo.get('adversario', 'N/A')
            casa_fora = "Casa" if jogo.get('mandante') else "Fora"
            resposta += f"📆 {data_jogo} {hora}: {team} x {adversario} ({casa_fora})\n"

        return resposta

    def _resposta_classificacao(self, data):
        """Resposta para classificação/tabela"""
        if not data or not data.get('classificacao'):
            return "📊 Não foi possível carregar a classificação no momento."

        classificacao = data['classificacao']
        resposta = "🏆 Classificação do Brasileirão Série A:\n\n"

        for i, time in enumerate(classificacao[:10], 1):
            nome = time.get('nome', 'N/A')
            pontos = time.get('pontos', 0)
            resposta += f"{i}º {nome} - {pontos} pts\n"

        return resposta + "\n💡 Os 4 primeiros garantem Libertadores, os 6 últimos caem para Série B!"

    def _resposta_estatisticas_time(self, team, data):
        """Resposta para estatísticas de um time"""
        if not team:
            return "🤔 De qual time você quer ver as estatísticas?"

        if not data or not data.get('estatisticas'):
            return f"📊 Não encontrei estatísticas recentes do {team}."

        stats = data['estatisticas']
        resposta = f"📊 Estatísticas recentes do {team}:\n\n"

        # Estatísticas principais
        principais = ['Posse de Bola', 'Total de chutes', 'Escanteios', 'Faltas cometidas']
        for stat in principais:
            if stat in stats:
                valor = stats[stat]
                resposta += f"• {stat}: {valor}\n"

        return resposta + f"\n💡 O {team} está jogando {'bem' if stats.get('Posse de Bola', '0%') > '50%' else 'regular'} ultimamente!"

    def _resposta_melhor_aposta(self, data):
        """Resposta para melhor aposta do dia"""
        if not data or not data.get('recomendacoes'):
            return "🎯 Baseado na análise estatística, hoje recomendo ficar de olho no jogo Palmeiras x Corinthians. O Verdão está em boa fase e joga em casa!"

        recomendacoes = data['recomendacoes']
        resposta = "🎯 Minhas recomendações de apostas para hoje:\n\n"

        for rec in recomendacoes[:3]:
            jogo = rec.get('jogo', 'N/A')
            tipo = rec.get('tipo', 'Vitória')
            odd = rec.get('odd', 'N/A')
            confianca = rec.get('confianca', 'Média')
            resposta += f"• {jogo}: {tipo} ({odd}) - Confiança: {confianca}\n"

        return resposta + "\n⚠️ Lembre-se: apostas são arriscadas, aposte apenas o que pode perder!"

    def _resposta_estatisticas_jogador(self, player, data):
        """Resposta para estatísticas de jogador"""
        if not player:
            return "🤔 De qual jogador você quer ver as estatísticas?"

        if not data or not data.get('estatisticas'):
            return f"⚽ Não encontrei estatísticas recentes de {player}."

        stats = data['estatisticas']
        resposta = f"⚽ Estatísticas de {player}:\n\n"

        for stat, valor in stats.items():
            resposta += f"• {stat}: {valor}\n"

        return resposta + f"\n💡 {player} está {'em boa fase' if stats.get('Gols', 0) > 0 else 'precisando de mais minutos'}!"

    def _resposta_odds_jogo(self, team1, team2):
        """Resposta para odds de um jogo específico"""
        if not team1 or not team2:
            return "🤔 Preciso saber os dois times para consultar as odds."

        odds = self.buscar_odds_jogo(team1, team2)

        if not odds:
            return f"📊 Não foi possível obter as odds para {team1} x {team2} no momento."

        resposta = f"💰 Odds para {team1} x {team2}:\n\n"
        resposta += f"🏆 Vitória {team1}: {odds['casa']}\n"
        resposta += f"🤝 Empate: {odds['empate']}\n"
        resposta += f"⚽ Vitória {team2}: {odds['fora']}\n\n"
        resposta += f"📊 Fonte: {odds['fonte']}\n"
        resposta += f"🕐 Atualizado às {odds['atualizado_em']}\n\n"
        resposta += "⚠️ Odds sujeitas a mudança. Verifique com sua casa de apostas!"

        return resposta

    def _resposta_data_hoje(self):
        """Resposta para pergunta sobre o dia de hoje"""
        dia_semana = self.get_dia_semana()
        data_formatada = self.get_data_atual_formatada()
        return f"📅 Hoje é {dia_semana}, {data_formatada}.\n\nSe você quiser saber sobre jogos de hoje, classificação ou outras informações do Brasileirão, é só perguntar! ⚽"

    def _resposta_data_ontem(self):
        """Resposta para pergunta sobre ontem"""
        dia_semana_ontem = self.get_dia_semana_ontem()
        data_ontem = self.get_data_ontem_formatada()
        return f"📅 Ontem foi {dia_semana_ontem}, {data_ontem}.\n\nPosso te ajudar com informações sobre jogos, estatísticas ou classificação do Brasileirão! 🏆"

    def _resposta_data_amanha(self):
        """Resposta para pergunta sobre amanhã"""
        dia_semana_amanha = self.get_dia_semana_amanha()
        data_amanha = self.get_data_amanha_formatada()
        return f"📅 Amanhã será {dia_semana_amanha}, {data_amanha}.\n\nQuer saber quais jogos acontecem amanhã ou outras informações do futebol brasileiro? ⚽"

    def _resposta_generica(self, query):
        """Resposta genérica para queries não reconhecidas"""
        return f"🤔 Entendi que você perguntou sobre: \"{query}\"\n\nInfelizmente ainda não tenho essa informação específica. Tente perguntar sobre:\n• Jogos de hoje\n• Classificação\n• Estatísticas de times\n• Melhores apostas\n• Histórico de confrontos\n\nOu digite 'ajuda' para ver todos os comandos disponíveis!"