#!/usr/bin/env python3
"""
Sistema de Impressão Inteligente para Páginas Web
Converte páginas HTML em Markdown organizado e extrai dados estruturados
Substitui as "notas manuais" com IA avançada
"""

import asyncio
import json
import os
import re
import sys
from datetime import datetime
from typing import Dict, List, Optional, Any
from urllib.parse import urlparse

import requests
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import pdfplumber
from groq import Groq
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

class SmartWebPrinter:
    """Sistema de impressão inteligente de páginas web"""

    def __init__(self):
        # Usar Groq em vez de OpenAI (já configurado no projeto)
        self.groq_client = Groq(api_key=os.getenv('LLM_API_KEY'))

        # Seletores CSS comuns para anúncios e elementos indesejados
        self.ad_selectors = [
            # Google Ads
            '[id*="google_ads"]',
            '[class*="google-ads"]',
            '[id*="adsbygoogle"]',

            # Outros anúncios
            '[class*="advertisement"]',
            '[class*="ads-banner"]',
            '[class*="sponsored"]',
            '[id*="banner"]',
            '[class*="popup"]',
            '[class*="modal"]',

            # Redes sociais
            '[class*="social-share"]',
            '[class*="facebook"]',
            '[class*="twitter"]',
            '[class*="instagram"]',

            # Navegação e headers
            'nav',
            'header',
            '.header',
            '#header',

            # Footers
            'footer',
            '.footer',
            '#footer',

            # Sidebars
            'aside',
            '.sidebar',
            '#sidebar',

            # Elementos de comentários
            '[class*="comment"]',
            '[class*="disqus"]'
        ]

    async def print_webpage_to_pdf(self, url: str, output_pdf: str) -> bool:
        """Faz impressão inteligente de página web para PDF"""
        try:
            print(f"🌐 Abrindo página: {url}")

            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    viewport={'width': 1200, 'height': 800},
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                )

                page = await context.new_page()

                # Configurar para esperar pelo conteúdo
                await page.set_extra_http_headers({
                    'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8'
                })

                # Navegar para a página
                await page.goto(url, wait_until='networkidle', timeout=30000)

                # Aguardar um pouco para carregamento dinâmico
                await page.wait_for_timeout(3000)

                # Remover anúncios e elementos indesejados
                print("🧹 Removendo anúncios e elementos indesejados...")
                for selector in self.ad_selectors:
                    try:
                        elements = await page.query_selector_all(selector)
                        for element in elements:
                            try:
                                await element.evaluate('element.style.display = "none"')
                            except:
                                pass
                    except:
                        continue

                # Remover scripts e estilos inline
                await page.evaluate("""
                    // Remover scripts
                    document.querySelectorAll('script').forEach(s => s.remove());

                    // Remover estilos inline de anúncios
                    document.querySelectorAll('[style*="position: fixed"]').forEach(el => el.remove());
                    document.querySelectorAll('[style*="position: absolute"][style*="z-index"]').forEach(el => el.remove());

                    // Melhorar formatação para impressão
                    document.body.style.fontFamily = 'Arial, sans-serif';
                    document.body.style.lineHeight = '1.6';
                """)

                # Fazer print to PDF
                print("📄 Gerando PDF...")
                await page.pdf(
                    path=output_pdf,
                    format='A4',
                    print_background=True,
                    margin={'top': '1cm', 'right': '1cm', 'bottom': '1cm', 'left': '1cm'}
                )

                await browser.close()

            print(f"✅ PDF gerado: {output_pdf}")
            return True

        except Exception as e:
            print(f"❌ Erro ao gerar PDF: {e}")
            return False

    def extract_text_from_pdf(self, pdf_path: str) -> Optional[str]:
        """Extrai texto do PDF gerado"""
        try:
            print(f"📖 Extraindo texto de: {pdf_path}")
            text = ""

            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    page_text = page.extract_text()
                    if page_text:
                        text += f"## Página {page_num}\n\n"
                        text += page_text.strip() + "\n\n"

            print(f"✅ Texto extraído ({len(pdf.pages)} páginas)")
            return text

        except Exception as e:
            print(f"❌ Erro ao extrair texto: {e}")
            return None

    def clean_markdown(self, text: str) -> str:
        """Limpa e formata o texto extraído para Markdown organizado"""
        if not text:
            return ""

        # Remove linhas vazias excessivas
        lines = text.split('\n')
        cleaned_lines = []

        prev_empty = False
        for line in lines:
            line = line.strip()
            if line:  # Só adiciona linhas não vazias
                cleaned_lines.append(line)
                prev_empty = False
            elif not prev_empty:  # Adiciona no máximo uma linha vazia
                cleaned_lines.append('')
                prev_empty = True

        return '\n'.join(cleaned_lines)

    def extract_structured_data(self, markdown_content: str, url: str) -> Dict[str, Any]:
        """Usa IA para extrair dados estruturados do conteúdo Markdown"""
        try:
            print("🤖 Analisando conteúdo com IA...")

            # Detectar tipo de conteúdo baseado na URL e conteúdo
            content_type = self._detect_content_type(url, markdown_content)

            # Prompt específico baseado no tipo de conteúdo
            prompts = {
                'match_preview': """
                Analise esta pré-visualização de jogo e extraia:
                - Times envolvidos (home e away)
                - Data e horário do jogo
                - Competição/campeonato
                - Análise tática
                - Jogadores em destaque
                - Expectativas de placar
                - Probabilidades
                """,

                'player_news': """
                Analise esta notícia sobre jogador e extraia:
                - Nome completo do jogador
                - Time atual
                - Tipo de notícia (lesão, transferência, suspensão, etc.)
                - Detalhes específicos da notícia
                - Tempo de recuperação (se lesão)
                - Impacto no time
                - Valor da transferência (se aplicável)
                """,

                'match_report': """
                Analise este relatório de jogo e extraia:
                - Times envolvidos (home e away)
                - Placar final
                - Gols marcados (quem, quando, como)
                - Estatísticas do jogo (posse, chutes, corners, etc.)
                - Melhores jogadores
                - Análise pós-jogo
                - Árbitro e cartões
                """,

                'injury_report': """
                Analise este relatório de lesões e extraia:
                - Jogadores lesionados (nome completo)
                - Tipo de lesão
                - Gravidade (leve, média, grave)
                - Tempo estimado de recuperação
                - Jogos que perderão
                - Status atual (duvidoso, fora, etc.)
                """,

                'game_stats': """
                Analise estas estatísticas de jogo e extraia:
                - Times envolvidos (home e away)
                - Data do jogo
                - Todas as estatísticas disponíveis (posse, chutes, corners, faltas, etc.)
                - Estatísticas por jogador se disponíveis
                - Placar final se mencionado
                - Formato: estatística -> valor_home x valor_away
                """,

                'general_news': """
                Analise esta notícia geral de futebol e categorize:
                - Tópico principal
                - Times envolvidos
                - Jogadores mencionados
                - Impacto no campeonato
                - Informações relevantes
                """
            }

            prompt = prompts.get(content_type, prompts['general_news'])

            full_prompt = f"""
            Analise o seguinte conteúdo de uma página web sobre futebol e extraia informações estruturadas.

            URL: {url}
            Tipo detectado: {content_type}

            {prompt}

            Conteúdo:
            {markdown_content[:6000]}  # Limitar tamanho para não exceder token limit

            IMPORTANTE: Responda APENAS com um JSON válido. Para estatísticas, use o formato:
            "statistics": {{"Posse": {{"home": "55%", "away": "45%"}}, "Chutes": {{"home": "12", "away": "8"}}}}

            INSTRUÇÕES CRÍTICAS:
            - NÃO use ```json ou qualquer markdown
            - NÃO adicione texto antes ou depois do JSON
            - Se não conseguir analisar, retorne: {{"content_type": "error", "error": "Não foi possível analisar o conteúdo"}}
            - Sempre use aspas duplas, não simples

            Responda com JSON válido neste formato:

            Responda com JSON válido neste formato:
            {{
                "content_type": "{content_type}",
                "title": "título extraído",
                "teams": ["time1", "time2"],
                "players": ["jogador1", "jogador2"],
                "date": "YYYY-MM-DDTHH:MM:SS",
                "data": {{
                    "score": "placar se disponível",
                    "statistics": {{"stat_name": {{"home": "valor", "away": "valor"}}}},
                    "injuries": [{{"player": "nome", "type": "tipo", "severity": "gravidade"}}],
                    "news_details": "detalhes específicos"
                }},
                "confidence": 0.0-1.0
            }}
            """

            response = self.groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": full_prompt}],
                temperature=0.1,
                max_tokens=3000
            )

            result = response.choices[0].message.content.strip()

            # Limpar resposta da IA (remover markdown se presente)
            if result.startswith('```json'):
                result = result[7:]
            if result.endswith('```'):
                result = result[:-3]
            result = result.strip()

            # Tentar parsear JSON
            try:
                structured_data = json.loads(result)
                structured_data['source_url'] = url
                structured_data['extracted_at'] = datetime.now().isoformat()
                structured_data['raw_markdown'] = markdown_content

                print(f"✅ Dados estruturados extraídos (confiança: {structured_data.get('confidence', 0)})")

                # Adicionar informações de linkagem
                structured_data['link_info'] = self._extract_link_info(structured_data, url)

                return structured_data

            except json.JSONDecodeError as e:
                print(f"❌ Erro ao parsear JSON da IA: {e}")
                print(f"Resposta bruta: {result[:500]}...")
                return {
                    'content_type': content_type,
                    'error': 'Failed to parse AI response',
                    'raw_response': result,
                    'source_url': url,
                    'extracted_at': datetime.now().isoformat()
                }

        except Exception as e:
            print(f"❌ Erro na extração com IA: {e}")
            return {
                'content_type': 'error',
                'error': str(e),
                'source_url': url,
                'extracted_at': datetime.now().isoformat()
            }

    def _detect_content_type(self, url: str, content: str) -> str:
        """Detecta o tipo de conteúdo baseado na URL e texto"""
        url_lower = url.lower()
        content_lower = content.lower()

        # Detecção baseada em URL
        if any(keyword in url_lower for keyword in ['preview', 'previsao', 'palpite']):
            return 'match_preview'

        if any(keyword in url_lower for keyword in ['injury', 'lesao', 'machucado']):
            return 'injury_report'

        if any(keyword in url_lower for keyword in ['report', 'relatorio', 'resumo']):
            return 'match_report'

        if any(keyword in url_lower for keyword in ['stats', 'statistics', 'estatisticas']):
            return 'game_stats'

        # Detecção baseada no conteúdo
        if any(keyword in content_lower for keyword in ['lesão', 'lesionado', 'machucado', 'recuperação']):
            return 'injury_report'

        if any(keyword in content_lower for keyword in ['x', 'versus', 'vs', 'confronto']) and \
           any(keyword in content_lower for keyword in ['próximo', 'próxima', 'domingo', 'sábado']):
            return 'match_preview'

        if any(keyword in content_lower for keyword in ['gols', 'placar', 'vitória', 'derrota']) and \
           any(keyword in content_lower for keyword in ['final', 'resultado', 'marcou']):
            return 'match_report'

        # Detecção de estatísticas
        if any(keyword in content_lower for keyword in ['posse', 'chutes', 'corners', 'faltas', 'cartões']):
            return 'game_stats'

        # Detecção de notícias de jogador
        if any(keyword in content_lower for keyword in ['jogador', 'atacante', 'meio', 'defensor', 'goleiro']) and \
           any(keyword in content_lower for keyword in ['transferência', 'contrato', 'negociação']):
            return 'player_news'

        return 'general_news'

    def _extract_link_info(self, structured_data: Dict[str, Any], url: str) -> Dict[str, Any]:
        """Extrai informações para linkagem com banco de dados"""
        link_info = {
            'teams_found': [],
            'players_found': [],
            'date_found': None,
            'game_candidates': []
        }

        try:
            # Extrair times
            teams = structured_data.get('teams', [])
            if teams:
                link_info['teams_found'] = teams

            # Extrair jogadores
            players = structured_data.get('players', [])
            if players:
                link_info['players_found'] = players

            # Extrair data
            date = structured_data.get('date')
            if date:
                link_info['date_found'] = date

            # Para jogos, tentar identificar candidatos
            if structured_data.get('content_type') in ['match_report', 'game_stats', 'match_preview']:
                if len(teams) >= 2:
                    link_info['game_candidates'] = [{
                        'home_team': teams[0],
                        'away_team': teams[1],
                        'date': date,
                        'url': url
                    }]

        except Exception as e:
            print(f"Erro ao extrair link info: {e}")

        return link_info

    def check_duplicates(self, structured_data: Dict[str, Any]) -> bool:
        """Verifica se os dados já existem no banco para evitar duplicatas"""
        try:
            # Verificação básica (mais avançada será feita no flask_api.py)
            content_type = structured_data.get('content_type', '')
            teams = structured_data.get('teams', [])
            players = structured_data.get('players', [])
            date = structured_data.get('date')

            print(f"🔍 Verificação básica de duplicatas para {content_type}...")

            # Para jogos: verificar se tem times suficientes
            if content_type in ['match_preview', 'match_report', 'game_stats'] and len(teams) >= 2:
                print(f"⚠️  Jogo detectado: {teams[0]} x {teams[1]} - verificação avançada será feita na API")

            # Para lesões: verificar se tem jogadores
            if content_type == 'injury_report' and players:
                print(f"⚠️  Lesões detectadas para {len(players)} jogadores - verificação avançada será feita na API")

            # Por enquanto, retorna False (não duplicado) - verificação real na API
            return False

        except Exception as e:
            print(f"⚠️  Erro na verificação básica de duplicatas: {e}")
            return False

    async def process_web_content(self, url: str) -> Optional[Dict[str, Any]]:
        """Processo completo: URL → PDF → Markdown → Dados Estruturados"""
        try:
            print(f"🚀 Iniciando processamento inteligente de: {url}")

            # Passo 1: Detectar domínio e validar URL
            parsed_url = urlparse(url)
            if not parsed_url.scheme or not parsed_url.netloc:
                print("❌ URL inválida")
                return None

            # Passo 2: Gerar PDF da página
            temp_pdf = f"temp_smart_print_{hash(url)}.pdf"

            if not await self.print_webpage_to_pdf(url, temp_pdf):
                return None

            try:
                # Passo 3: Extrair texto do PDF
                raw_text = self.extract_text_from_pdf(temp_pdf)
                if not raw_text:
                    return None

                # Passo 4: Limpar e formatar Markdown
                clean_markdown = self.clean_markdown(raw_text)

                # Passo 5: Extrair dados estruturados com IA
                structured_data = self.extract_structured_data(clean_markdown, url)

                # Passo 6: Verificar duplicatas
                if self.check_duplicates(structured_data):
                    print("⚠️  Conteúdo duplicado detectado - pulando inserção")
                    structured_data['duplicate'] = True
                else:
                    structured_data['duplicate'] = False

                # Passo 7: Salvar Markdown para referência
                markdown_file = f"web_content_{hash(url)}.md"
                with open(markdown_file, 'w', encoding='utf-8') as f:
                    f.write(f"# Conteúdo Extraído\n\n**Fonte:** {url}\n\n---\n\n{clean_markdown}")

                structured_data['markdown_file'] = markdown_file

                print("✅ Processamento inteligente concluído!")
                return structured_data

            finally:
                # Limpar arquivo temporário
                if os.path.exists(temp_pdf):
                    os.remove(temp_pdf)
                    print(f"🧹 Arquivo temporário removido: {temp_pdf}")

        except Exception as e:
            print(f"❌ Erro no processamento inteligente: {e}")
            return None

async def main():
    """Função principal para teste"""
    if len(sys.argv) < 2:
        print("Uso: python smart_web_printer.py <URL>")
        print("Exemplo: python smart_web_printer.py https://ge.globo.com/futebol/times/flamengo/noticia/2023/11/20/flamengo-vence-palmeiras.ghtml")
        sys.exit(1)

    url = sys.argv[1]

    printer = SmartWebPrinter()
    result = await printer.process_web_content(url)

    if result:
        print("\n" + "="*50)
        print("RESULTADO ESTRUTURADO:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("❌ Falha no processamento")

if __name__ == "__main__":
    asyncio.run(main())