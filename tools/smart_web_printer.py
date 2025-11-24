#!/usr/bin/env python3
"""
Sistema de Impressão Inteligente para Páginas Web (v2 - Otimizado)
Converte HTML em Markdown e extrai dados para revisão humana (Human-in-the-Loop).

Melhorias implementadas:
- Remoção da etapa de PDF: Conversão direta HTML -> Markdown para performance.
- Padrão Singleton para Browser: Instância única do browser.
- Preparado para HITL: Saída inclui markdown editável e status "pending_review".
- Processamento Non-blocking: Tarefas de CPU (parsing) executadas em ThreadPoolExecutor.
"""

import asyncio
import json
import logging
import os
import re
import sys
import hashlib
import time
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from functools import wraps
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor

# Dependências externas
try:
    import html2text
    from playwright.async_api import async_playwright, Browser, Playwright
    from bs4 import BeautifulSoup
    from groq import Groq
    from dotenv import load_dotenv
except ImportError as e:
    print(f"Erro de importação: {e}")
    print("Instale as dependências: pip install html2text playwright beautifulsoup4 groq python-dotenv")
    sys.exit(1)

# Carregar variáveis de ambiente
load_dotenv()

# Garantir saída UTF-8 no Windows para evitar UnicodeEncodeError ao imprimir
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass


# ==================== CONFIGURAÇÃO ====================

@dataclass
class Config:
    """Configuração centralizada do sistema"""
    # API
    groq_api_key: str = os.getenv('LLM_API_KEY', '')
    groq_model: str = os.getenv('GROQ_MODEL', 'llama-3.1-8b-instant')
    
    # Timeouts e limites
    page_timeout: int = int(os.getenv('PAGE_TIMEOUT', '30000'))
    page_load_wait: int = int(os.getenv('PAGE_LOAD_WAIT', '3000'))

    # Aumentado para suportar markdown completo
    max_content_length: int = int(os.getenv('MAX_CONTENT_LENGTH', '15000')) 
    max_tokens: int = int(os.getenv('MAX_TOKENS', '4000'))
    
    # Retry
    max_retries: int = int(os.getenv('MAX_RETRIES', '3'))
    retry_delay: float = float(os.getenv('RETRY_DELAY', '2.0'))
    
    # Cache
    enable_cache: bool = os.getenv('ENABLE_CACHE', 'true').lower() == 'true'
    cache_dir: Path = Path(os.getenv('CACHE_DIR', './cache'))
    cache_ttl_hours: int = int(os.getenv('CACHE_TTL_HOURS', '24'))
    
    # Diretórios
    output_dir: Path = Path(os.getenv('OUTPUT_DIR', './output'))
    log_dir: Path = Path(os.getenv('LOG_DIR', './logs'))
    
    # Viewport
    viewport_width: int = 1200
    viewport_height: int = 800
    
    def __post_init__(self):
        """Criar diretórios necessários"""
        for directory in [self.cache_dir, self.output_dir, self.log_dir]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def validate(self) -> Tuple[bool, List[str]]:
        """Valida a configuração"""
        errors = []
        if not self.groq_api_key:
            errors.append("GROQ_API_KEY não configurada")
        return len(errors) == 0, errors


# ==================== ENUMS ====================

class ContentType(Enum):
    """Tipos de conteúdo suportados"""
    MATCH_PREVIEW = "match_preview"
    PLAYER_NEWS = "player_news"
    MATCH_REPORT = "match_report"
    INJURY_REPORT = "injury_report"
    GAME_STATS = "game_stats"
    GENERAL_NEWS = "general_news"
    ERROR = "error"


class ProcessingStatus(Enum):
    """Status do processamento"""
    PENDING_REVIEW = "pending_review"  # Status para HITL (Human-in-the-Loop)
    COMPLETED = "completed"
    FAILED = "failed"
    CACHED = "cached"


# ==================== LOGGING ====================

class LoggerSetup:
    @staticmethod
    def setup(config: Config) -> logging.Logger:
        logger = logging.getLogger('SmartWebPrinter')
        if logger.hasHandlers():
            return logger
            
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s')
        
        log_file = config.log_dir / f'smart_printer_{datetime.now():%Y%m%d}.log'
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        
        console_handler = logging.StreamHandler(sys.stderr)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter('%(levelname)s | %(message)s'))
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        return logger


# ==================== UTILITÁRIOS ====================

class CacheManager:
    def __init__(self, cache_dir: Path, ttl_hours: int = 24):
        self.cache_dir = cache_dir
        self.ttl_hours = ttl_hours
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_key(self, url: str) -> str:
        return hashlib.sha256(url.encode()).hexdigest()

    def _get_cache_path(self, cache_key: str) -> Path:
        return self.cache_dir / f"{cache_key}.json"

    def get(self, url: str) -> Optional[Dict[str, Any]]:
        cache_path = self._get_cache_path(self._get_cache_key(url))
        if not cache_path.exists():
            return None
        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                cached_data = json.load(f)
            
            cached_time = datetime.fromisoformat(cached_data.get('cached_at', '2000-01-01'))
            if (datetime.now() - cached_time).total_seconds() / 3600 > self.ttl_hours:
                cache_path.unlink()
                return None
                
            return cached_data.get('data')
        except Exception:
            return None

    def set(self, url: str, data: Dict[str, Any]):
        cache_path = self._get_cache_path(self._get_cache_key(url))
        try:
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump({
                    'url': url,
                    'cached_at': datetime.now().isoformat(),
                    'data': data
                }, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

def retry_with_backoff(max_retries: int = 3, initial_delay: float = 1.0):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            delay = initial_delay
            last_exception = None
            for _ in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    await asyncio.sleep(delay)
                    delay *= 2
            raise last_exception
        return wrapper
    return decorator


# ==================== CLASSE PRINCIPAL ====================

class SmartWebPrinter:
    """
    Sistema de impressão inteligente de páginas web.
    Gerencia ciclo de vida do browser (Singleton) e processamento paralelo.
    """
    
    AD_SELECTORS = [
        '[id*="google_ads"]', '[class*="google-ads"]', '[id*="adsbygoogle"]',
        '[class*="advertisement"]', '[class*="ads-banner"]', '[class*="sponsored"]',
        '[id*="banner"]', '[class*="popup"]', '[class*="modal"]',
        '[class*="social-share"]', '[class*="comment"]', 'script', 'style', 'iframe'
    ]

    CONTENT_PROMPTS = {
        ContentType.MATCH_PREVIEW: "Analise esta pré-visualização de jogo e extraia:\n- Times envolvidos (home e away)\n- Data e horário (ISO 8601)\n- Competição\n- Análise tática\n- Jogadores em destaque\n- Probabilidades",
        ContentType.PLAYER_NEWS: "Analise esta notícia sobre jogador e extraia:\n- Nome do jogador\n- Time atual\n- Tipo de notícia (lesão, transferência, etc.)\n- Detalhes específicos\n- Impacto no time",
        ContentType.MATCH_REPORT: "Analise este relatório de jogo e extraia:\n- Times (home e away)\n- Placar final\n- Gols (jogador, minuto)\n- Estatísticas principais\n- Destaques\n- Data (ISO 8601)",
        ContentType.INJURY_REPORT: "Analise este relatório de lesões e extraia:\n- Jogadores lesionados\n- Tipo de lesão\n- Gravidade\n- Tempo de recuperação\n- Status atual",
        ContentType.GAME_STATS: "Analise estas estatísticas de jogo e extraia:\n- Times (home e away)\n- Data (ISO 8601)\n- Placar final\n- Estatísticas detalhadas (Posse, Chutes, Corners, etc.) em formato {'stat': {'home': 'valor', 'away': 'valor'}}",
        ContentType.GENERAL_NEWS: "Analise esta notícia geral de futebol e extraia:\n- Tópico principal\n- Times e jogadores mencionados\n- Competição\n- Informações relevantes"
    }

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        is_valid, errors = self.config.validate()
        if not is_valid:
            raise ValueError(f"Configuração inválida: {', '.join(errors)}")
        
        self.logger = LoggerSetup.setup(self.config)
        self.groq_client = Groq(api_key=self.config.groq_api_key)
        self.cache = CacheManager(self.config.cache_dir, self.config.cache_ttl_hours)
        
        # Singleton Resources
        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None
        
        # Executor para tarefas CPU-bound (HTML parsing/conversion)
        self.executor = ThreadPoolExecutor(max_workers=min(4, os.cpu_count() or 1))
        self.logger.info("SmartWebPrinter inicializado")

    async def __aenter__(self):
        """Inicializa o browser (padrão Singleton)"""
        if self.browser is None:
            self.logger.info("Iniciando instância Singleton do browser...")
            self.playwright = await async_playwright().__aenter__()
            self.browser = await self.playwright.chromium.launch(headless=True)
            self.logger.info("Browser iniciado com sucesso.")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Fecha o browser e desliga o executor"""
        if self.browser:
            self.logger.info("Fechando instância do browser...")
            try:
                await self.browser.close()
            except Exception as e:
                self.logger.warning(f"Erro ao fechar browser: {e}")
            finally:
                self.browser = None

        if self.playwright:
            # Playwright não expõe __aexit__ no objeto Playwright; usar stop()
            try:
                await self.playwright.stop()
            except Exception as e:
                self.logger.warning(f"Erro ao parar playwright: {e}")
            finally:
                self.playwright = None

        try:
            self.executor.shutdown(wait=True)
        except Exception:
            pass

        self.logger.info("Recursos liberados.")

    def _convert_html_to_markdown(self, html_content: str) -> str:
        """
        [CPU-BOUND] Limpa o HTML com BeautifulSoup e converte para Markdown.
        Tenta extrair o conteúdo principal de '#detail' e os elementos de estatística.
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extrair campeonato do meta tag, uma fonte mais confiável
            championship_text = ""
            championship_meta = soup.select_one('meta[property="og:description"]')
            if championship_meta and championship_meta.get('content'):
                # Formato: "PAÍS: CAMPEONATO - Rodada X"
                content = championship_meta['content']
                parts = content.split(':')
                if len(parts) > 1:
                    # Pega a parte do campeonato, remove " - Rodada X" se existir
                    championship_part = parts[1].split(' - ')[0].strip()
                    championship_text = championship_part

            main_content = soup.select_one('#detail')
            
            if main_content:
                # Seletores para as informações essenciais do jogo
                date_element = main_content.select_one('.duelParticipant__startTime')
                teams_elements = main_content.select('.participant__participantName')
                score_element = main_content.select_one('.detailScore__wrapper')
                stats_elements = main_content.select('div[data-testid^="wcl-statistics-"]')

                if stats_elements:
                    clean_soup = BeautifulSoup('<div></div>', 'html.parser')
                    container = clean_soup.div

                    # Adiciona os elementos na ordem correta
                    if championship_text:
                        championship_tag = soup.new_tag('p')
                        championship_tag.string = championship_text
                        container.append(championship_tag)
                    if date_element:
                        container.append(date_element)
                    for team in teams_elements:
                        container.append(team)
                    if score_element:
                        container.append(score_element)
                    for el in stats_elements:
                        container.append(el)
                    
                    main_content = container
                else:
                    self.logger.warning("Nenhum elemento de estatística com 'data-testid' encontrado em '#detail'.")

            if not main_content:
                self.logger.warning("Container '#detail' não encontrado, usando 'body' como fallback.")
                main_content = soup.body
                if not main_content:
                    self.logger.error("Tag 'body' não encontrada no HTML.")
                    return ""

            for selector in self.AD_SELECTORS:
                for element in main_content.select(selector):
                    element.decompose()

            h = html2text.HTML2Text()
            h.ignore_links = True
            h.ignore_images = True
            h.body_width = 0
            
            markdown = h.handle(str(main_content))

            lines = [line.strip() for line in markdown.split('\n')]
            clean_markdown = '\n'.join(line for line in lines if line and 'publicidade' not in line.lower())
            
            return clean_markdown
        except Exception as e:
            self.logger.error(f"Erro na conversão HTML->Markdown: {e}")
            return ""

    @retry_with_backoff(max_retries=3, initial_delay=2.0)
    async def _get_page_html(self, url: str) -> str:
        """Busca o conteúdo HTML de uma página com retry usando o browser singleton."""
        if not self.browser:
            raise RuntimeError("Browser não inicializado. Use 'async with SmartWebPrinter()'.")

        context = await self.browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': self.config.viewport_width, 'height': self.config.viewport_height}
        )
        
        page = await context.new_page()
        try:
            self.logger.debug(f"Navegando para: {url}")
            await page.goto(url, wait_until='domcontentloaded', timeout=self.config.page_timeout)
            
            # Pequena espera para hidratação de frameworks JS (React/Next/Vue)
            await page.wait_for_timeout(self.config.page_load_wait)
            
            html_content = await page.content()
            return html_content
        except Exception as e:
            self.logger.error(f"Erro ao carregar página {url}: {e}")
            raise e
        finally:
            await context.close()

    def _detect_content_type(self, url: str, content: str) -> ContentType:
        url_lower = url.lower()
        content_lower = content.lower()[:2000]
        
        keywords = {
            ContentType.MATCH_PREVIEW: {'url': ['preview', 'previsao'], 'content': ['próximo jogo', 'prévia', 'provável escalação']},
            ContentType.INJURY_REPORT: {'url': ['injury', 'lesao'], 'content': ['lesionado', 'departamento médico', 'desfalque']},
            ContentType.MATCH_REPORT: {'url': ['report', 'resumo', 'pos-jogo'], 'content': ['placar final', 'gols', 'melhores momentos']},
            ContentType.GAME_STATS: {'url': ['stats', 'estatisticas'], 'content': ['posse de bola', 'chutes a gol', 'escanteios']},
            ContentType.PLAYER_NEWS: {'url': ['transfer', 'contratacao', 'mercado'], 'content': ['transferência', 'contrato', 'assinou']}
        }
        
        for c_type, kw in keywords.items():
            if any(w in url_lower for w in kw['url']) or any(w in content_lower for w in kw['content']):
                return c_type
        return ContentType.GENERAL_NEWS

    def _extract_link_info(self, structured_data: Dict[str, Any], url: str) -> Dict[str, Any]:
        """Gera metadados auxiliares para links"""
        link_info = {
            'teams_found': structured_data.get('teams', []),
            'players_found': structured_data.get('players', []),
            'date_found': structured_data.get('date'),
            'game_candidates': []
        }
        
        if structured_data.get('content_type') in ['match_report', 'game_stats', 'match_preview'] and len(link_info['teams_found']) >= 2:
            link_info['game_candidates'].append({
                'home_team': link_info['teams_found'][0],
                'away_team': link_info['teams_found'][1],
                'date': link_info['date_found'],
                'url': url
            })
        return link_info

    async def extract_structured_data(self, markdown_content: str, url: str) -> Dict[str, Any]:
        """Extrai dados estruturados usando IA via Groq."""
        try:
            self.logger.info("Analisando conteúdo Markdown com IA...")
            content_type = self._detect_content_type(url, markdown_content)
            
            # Truncar conteúdo para não estourar contexto do LLM
            content_excerpt = markdown_content[:self.config.max_content_length]
            
            specific_prompt = self.CONTENT_PROMPTS.get(content_type, self.CONTENT_PROMPTS[ContentType.GENERAL_NEWS])

            full_prompt = f"""Analise o conteúdo Markdown a seguir e extraia informações estruturadas.
URL: {url}
Tipo Detectado: {content_type.value}
{specific_prompt}

Conteúdo (Markdown):
{content_excerpt}

INSTRUÇÕES CRÍTICAS: 
1. Responda APENAS com JSON válido.
2. Não use blocos de código markdown (```json).
3. Use formato ISO 8601 para datas.
4. Se houver dúvida, marque 'confidence' baixo.

Formato de resposta esperado:
{{
    "content_type": "{content_type.value}", 
    "title": "Título Sugerido", 
    "teams": ["Time A", "Time B"], 
    "players": ["Jogador 1"],
    "date": "YYYY-MM-DDTHH:MM:SS", 
    "competition": "Nome da Competição", 
    "data": {{ "campo_especifico": "valor" }}, 
    "confidence": 0.85
}}"""

            response = await asyncio.to_thread(
                self.groq_client.chat.completions.create,
                model=self.config.groq_model,
                messages=[{"role": "user", "content": full_prompt}],
                temperature=0.1,
                max_tokens=self.config.max_tokens
            )
            
            result = response.choices[0].message.content.strip()
            # Limpeza de segurança para JSON
            result = re.sub(r'^```(?:json)?\s*|\s*```$', '', result).strip()

            if not result:
                self.logger.warning('LLM retornou resposta vazia.')
                return self._create_error_result(url, 'LLM returned empty response')

            try:
                structured_data = json.loads(result)
            except Exception as e:
                # Logar o output cru para depuração
                try:
                    self.logger.error(f"Falha ao parsear JSON retornado pelo LLM. Raw output: {result!r}")
                except Exception:
                    self.logger.error('Falha ao logar saída bruta do LLM')
                return self._create_error_result(url, f'Invalid JSON from LLM: {str(e)}')
            structured_data.update({
                'source_url': url,
                'extracted_at': datetime.now().isoformat(),
                'link_info': self._extract_link_info(structured_data, url)
            })
            
            self.logger.info(f"Dados extraídos (confiança: {structured_data.get('confidence', 0):.2f})")
            return structured_data

        except Exception as e:
            self.logger.error(f"Erro na extração com IA: {e}", exc_info=True)
            return self._create_error_result(url, str(e))

    def _create_error_result(self, url: str, error: str) -> Dict[str, Any]:
        return {
            'content_type': ContentType.ERROR.value,
            'status': ProcessingStatus.FAILED.value,
            'error': error,
            'source_url': url,
            'extracted_at': datetime.now().isoformat()
        }

    async def process_web_content(self, url: str, force: bool = False) -> Optional[Dict[str, Any]]:
        """
        Processo completo: URL -> HTML -> Markdown -> Dados Estruturados.
        Retorna objeto pronto para revisão humana (HITL).
        """
        try:
            self.logger.info(f"Iniciando processamento: {url}")
            if not urlparse(url).scheme:
                return self._create_error_result(url, "URL inválida")

            # 1. Verificar Cache
            if self.config.enable_cache and not force:
                if cached := self.cache.get(url):
                    self.logger.info("Resultado recuperado do cache")
                    return cached

            # 2. Obter HTML (I/O Bound)
            raw_html = await self._get_page_html(url)
            if not raw_html:
                return self._create_error_result(url, "Falha ao obter HTML")

            # Salvar HTML para depuração
            debug_html_path = self.config.output_dir / 'debug_page.html'
            try:
                with open(debug_html_path, 'w', encoding='utf-8') as f:
                    f.write(raw_html)
                self.logger.info(f"HTML bruto salvo para depuração em: {debug_html_path}")
            except Exception as e:
                self.logger.error(f"Falha ao salvar HTML de depuração: {e}")

            # 3. Converter para Markdown (CPU Bound - ThreadPool)
            loop = asyncio.get_running_loop()
            editable_markdown = await loop.run_in_executor(
                self.executor, 
                self._convert_html_to_markdown, 
                raw_html
            )
            
            if not editable_markdown:
                self.logger.warning("Markdown gerado está vazio.")

            self.logger.info(f"Markdown gerado com {len(editable_markdown)} caracteres.")

            # 4. Extrair Dados com IA (I/O Bound)
            structured_data = await self.extract_structured_data(editable_markdown, url)

            # 5. Preparar para HITL (Human-in-the-Loop)
            # Adicionamos o markdown cru para edição no frontend e definimos status
            structured_data['status'] = ProcessingStatus.PENDING_REVIEW.value
            structured_data['editable_markdown'] = editable_markdown
            
            # Salvar no cache
            if self.config.enable_cache:
                self.cache.set(url, structured_data)

            self.logger.info("✅ Processamento concluído, pronto para revisão.")
            return structured_data

        except Exception as e:
            self.logger.error(f"Erro no processamento: {e}", exc_info=True)
            return self._create_error_result(url, str(e))


# ==================== CLI ====================

class CLI:
    async def run(self, args: List[str]):
        if len(args) < 2:
            self.print_usage()
            return

        try:
            # Context Manager garante que o browser abra uma vez e feche ao final
            async with SmartWebPrinter(Config()) as printer:
                command = args[1]

                if command == 'process':
                    await self.cmd_process(printer, args[2:])
                else:
                    printer.logger.error(f"Comando desconhecido: {command}")
                    self.print_usage()
                    
        except Exception as e:
            sys.stderr.write(f"ERROR: Erro fatal na execução: {e}\n")

    async def cmd_process(self, printer: SmartWebPrinter, args: List[str]):
        if not args:
            sys.stderr.write("ERROR: URL não fornecida\n")
            return
            
        url = args[0]
        force = '--force' in args

        printer.logger.info(f"Processando: {url}")
        result = await printer.process_web_content(url, force=force)

        if result:
            # Saída JSON pura para integração com outros sistemas
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(json.dumps({"error": "Falha desconhecida"}, ensure_ascii=False))

    def print_usage(self):
        print("\nUSO: python smart_web_printer.py process <URL> [--force]\n")


# ==================== MAIN ====================

async def main():
    cli = CLI()
    await cli.run(sys.argv)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.stderr.write("\n\nInterrupted by user\n")
    except Exception as e:
        sys.stderr.write(f"\nERROR: Erro não tratado: {e}\n")