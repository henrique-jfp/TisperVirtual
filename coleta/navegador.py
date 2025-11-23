from playwright.async_api import async_playwright, Playwright, Browser, BrowserContext, Page
import logging
from typing import Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

class Navegador:
    """
    GHOST: Classe unificada para gerenciar o ciclo de vida do Playwright.
    - Gerenciamento de contexto assíncrono (`async with`).
    - Configurações de inicialização flexíveis (headless, user_agent).
    - Métodos de interação robustos com esperas explícitas.
    """
    def __init__(self, headless: bool = True, user_agent: str = DEFAULT_USER_AGENT):
        self.headless = headless
        self.user_agent = user_agent
        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None

    async def __aenter__(self):
        """Inicializa o navegador ao entrar no contexto."""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=self.headless)
        self.context = await self.browser.new_context(user_agent=self.user_agent)
        self.page = await self.context.new_page()
        logger.info("Navegador iniciado com sucesso.")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Fecha o navegador ao sair do contexto."""
        if self.page:
            await self.page.close()
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        logger.info("Navegador fechado.")

    async def navegar_para(self, url: str, timeout: int = 60000):
        """
        Navega para a URL especificada.
        GHOST: Usa 'domcontentloaded' para uma navegação inicial mais rápida.
        A robustez vem da espera explícita por seletores após a navegação.
        """
        if not self.page:
            raise RuntimeError("Página não está disponível. O navegador foi iniciado corretamente?")
        
        try:
            await self.page.goto(url, timeout=timeout, wait_until='domcontentloaded')
            logger.info(f"Navegado para {url}.")
        except Exception as e:
            logger.error(f"Erro ao navegar para {url}: {e}")
            raise

    async def esperar_por_seletor(self, seletor: str, timeout: int = 30000):
        """
        Espera explicitamente por um seletor na página. Essencial para SPAs.
        """
        if not self.page:
            raise RuntimeError("Página não está disponível.")
        
        try:
            await self.page.wait_for_selector(seletor, timeout=timeout)
            logger.info(f"Seletor '{seletor}' encontrado.")
        except Exception as e:
            logger.error(f"Timeout ao esperar pelo seletor '{seletor}': {e}")
            raise

    async def extrair_html(self, seletor: Optional[str] = None) -> str:
        """
        Extrai o HTML de um seletor específico ou da página inteira.
        """
        if not self.page:
            raise RuntimeError("Página não está disponível.")
        
        if seletor:
            elemento = await self.page.query_selector(seletor)
            return await elemento.inner_html() if elemento else ""
        
        return await self.page.content()
