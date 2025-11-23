import random
import re
from datetime import datetime, timedelta

class FootballTipsterAI:
    """IA de tipster para recomendações de apostas de futebol"""

    def __init__(self):
        self.risk_levels = {
            'baixo': 0.7,
            'medio': 0.5,
            'alto': 0.3
        }

    def analisar_jogo_para_aposta(self, jogo_data, estatisticas_casa, estatisticas_fora):
        """Analisa um jogo e gera recomendações de aposta"""

        casa = jogo_data.get('casa', 'Time Casa')
        fora = jogo_data.get('fora', 'Time Fora')

        # Análise baseada em estatísticas
        posse_casa = self._extrair_porcentagem(estatisticas_casa.get('Posse de Bola', '50%'))
        posse_fora = self._extrair_porcentagem(estatisticas_fora.get('Posse de Bola', '50%'))

        chutes_casa = self._extrair_numero(estatisticas_casa.get('Total de chutes', '10'))
        chutes_fora = self._extrair_numero(estatisticas_fora.get('Total de chutes', '10'))

        escanteios_casa = self._extrair_numero(estatisticas_casa.get('Escanteios', '4'))
        escanteios_fora = self._extrair_numero(estatisticas_fora.get('Escanteios', '4'))

        # Lógica de análise
        recomendacoes = []

        # Vitória do mandante
        if posse_casa > posse_fora + 10 and chutes_casa > chutes_fora:
            recomendacoes.append({
                'tipo': 'Vitória Casa',
                'time': casa,
                'odd_estimada': round(random.uniform(1.8, 2.5), 2),
                'confianca': 'Alta' if posse_casa > 60 else 'Média',
                'justificativa': f"{casa} tem superioridade em posse ({posse_casa}%) e chutes ({chutes_casa} x {chutes_fora})"
            })

        # Ambos marcam
        if escanteios_casa > 4 and escanteios_fora > 4:
            recomendacoes.append({
                'tipo': 'Ambos Marcam',
                'odd_estimada': round(random.uniform(1.6, 2.1), 2),
                'confianca': 'Média',
                'justificativa': f"Ambos os times criam oportunidades (escanteios: {escanteios_casa} x {escanteios_fora})"
            })

        # Over 2.5 gols
        total_chutes = chutes_casa + chutes_fora
        if total_chutes > 25:
            recomendacoes.append({
                'tipo': 'Over 2.5 Gols',
                'odd_estimada': round(random.uniform(1.7, 2.3), 2),
                'confianca': 'Alta' if total_chutes > 30 else 'Média',
                'justificativa': f"Jogo com muitos chutes ({total_chutes}), indica possibilidade de muitos gols"
            })

        # Empate
        if abs(posse_casa - posse_fora) < 10:
            recomendacoes.append({
                'tipo': 'Empate',
                'odd_estimada': round(random.uniform(3.0, 4.5), 2),
                'confianca': 'Baixa',
                'justificativa': f"Jogo equilibrado com posse similar ({posse_casa}% x {posse_fora}%)"
            })

        return recomendacoes

    def gerar_relatorio_tipster(self, jogos_hoje, estatisticas_times):
        """Gera relatório completo de recomendações para o dia"""

        relatorio = {
            'data_analise': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'jogos_analisados': len(jogos_hoje),
            'recomendacoes': []
        }

        for jogo in jogos_hoje:
            casa = jogo.get('casa')
            fora = jogo.get('fora')

            # Busca estatísticas dos times
            stats_casa = estatisticas_times.get(casa, {})
            stats_fora = estatisticas_times.get(fora, {})

            # Gera recomendações para este jogo
            recomendacoes_jogo = self.analisar_jogo_para_aposta(jogo, stats_casa, stats_fora)

            for rec in recomendacoes_jogo:
                rec['jogo'] = f"{casa} x {fora}"
                relatorio['recomendacoes'].append(rec)

        # Ordena por confiança
        ordem_confianca = {'Alta': 3, 'Média': 2, 'Baixa': 1}
        relatorio['recomendacoes'].sort(key=lambda x: ordem_confianca.get(x['confianca'], 0), reverse=True)

        return relatorio

    def _extrair_porcentagem(self, valor_str):
        """Extrai valor percentual de string"""
        if isinstance(valor_str, str):
            match = re.search(r'(\d+)', valor_str)
            return int(match.group(1)) if match else 50
        return valor_str if isinstance(valor_str, (int, float)) else 50

    def _extrair_numero(self, valor_str):
        """Extrai número de string"""
        if isinstance(valor_str, str):
            match = re.search(r'(\d+)', valor_str)
            return int(match.group(1)) if match else 0
        return valor_str if isinstance(valor_str, (int, float)) else 0

    def calcular_probabilidade_vitoria(self, stats_casa, stats_fora):
        """Calcula probabilidade de vitória baseada em estatísticas"""

        # Fatores considerados
        fatores = {
            'posse': 0.25,
            'chutes': 0.25,
            'escanteios': 0.15,
            'defesa': 0.15,
            'historico': 0.20
        }

        posse_casa = self._extrair_porcentagem(stats_casa.get('Posse de Bola', '50%'))
        posse_fora = self._extrair_porcentagem(stats_fora.get('Posse de Bola', '50%'))

        chutes_casa = self._extrair_numero(stats_casa.get('Total de chutes', '10'))
        chutes_fora = self._extrair_numero(stats_fora.get('Total de chutes', '10'))

        # Cálculo simplificado
        score_casa = (
            posse_casa * fatores['posse'] +
            (chutes_casa / max(chutes_casa + chutes_fora, 1)) * 100 * fatores['chutes'] +
            50  # baseline
        )

        score_fora = (
            posse_fora * fatores['posse'] +
            (chutes_fora / max(chutes_casa + chutes_fora, 1)) * 100 * fatores['chutes'] +
            50  # baseline
        )

        total = score_casa + score_fora
        prob_casa = (score_casa / total) * 100
        prob_fora = (score_fora / total) * 100
        prob_empate = 100 - prob_casa - prob_fora

        return {
            'casa': round(prob_casa, 1),
            'empate': round(prob_empate, 1),
            'fora': round(prob_fora, 1)
        }