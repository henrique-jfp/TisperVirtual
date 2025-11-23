import json
import os
import asyncio
import time
from typing import List, Dict, Any
from navegador import Navegador
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import asyncio
import json
import os
import time
from typing import List, Dict, Any, Optional, Callable, Awaitable
import logging
from .navegador import Navegador

logger = logging.getLogger(__name__)

class CapturaXHR:
    """
    GHOST: Classe redesenhada para uma captura de XHR precisa e orientada a ações.
    - Filtros de URL para capturar apenas dados relevantes.
    - Captura durante a execução de uma ação específica (ex: clique, rolagem).
    - Armazenamento em memória com salvamento explícito.
    """
    def __init__(self, navegador: Navegador, pasta_saida: str = "dados_raw"):
        if not navegador or not navegador.page:
            raise ValueError("Uma instância de Navegador com uma página ativa é necessária.")
        self.navegador = navegador
        self.page = navegador.page
        self.pasta_saida = pasta_saida
        self.capturas: List[Dict[str, Any]] = []
        os.makedirs(self.pasta_saida, exist_ok=True)

    def _handle_response(self, response, url_filtros: Optional[List[str]]):
        """Callback para processar respostas de rede."""
        try:
            url = response.url
            # Se filtros forem definidos, a URL deve conter pelo menos um deles.
            if url_filtros and not any(filtro in url for filtro in url_filtros):
                return

            resource_type = response.request.resource_type
            if resource_type in ['xhr', 'fetch']:
                content_type = response.headers.get('content-type', '')
                if 'application/json' in content_type:
                    # O corpo da resposta é obtido de forma síncrona dentro do handler,
                    # mas a conversão para JSON é assíncrona.
                    # Agendamos a corrotina para não bloquear o handler.
                    asyncio.create_task(self._processar_e_armazenar_json(response))

        except Exception as e:
            logger.warning(f"Erro no handler de resposta para {response.url}: {e}")

    async def _processar_e_armazenar_json(self, response):
        """Processa o corpo da resposta JSON e armazena os dados."""
        try:
            data = await response.json()
            captura = {
                'url': response.url,
                'data': data,
                'timestamp': time.time()
            }
            self.capturas.append(captura)
            logger.info(f"Capturado JSON de: {response.url}")
        except json.JSONDecodeError:
            logger.warning(f"Não foi possível decodificar JSON de: {response.url}")
        except Exception as e:
            logger.error(f"Erro ao processar JSON de {response.url}: {e}")

    async def capturar_durante_acao(self, acao: Callable[[], Awaitable[Any]], url_filtros: Optional[List[str]] = None):
        """
        Inicia a interceptação, executa uma ação e para a interceptação.
        GHOST: Esta é a abordagem robusta. A captura ocorre apenas quando o site
        é estimulado a carregar dados.
        
        Exemplo de ação:
        acao = lambda: self.page.click("#botao-carregar-mais")
        """
        handler = lambda response: self._handle_response(response, url_filtros)
        
        self.page.on('response', handler)
        logger.info(f"Interceptação de XHR iniciada. Filtros: {url_filtros or 'Nenhum'}")
        
        try:
            await acao()
            # Pequena espera para garantir que as últimas requisições sejam processadas
            await self.page.wait_for_timeout(3000)
        finally:
            self.page.remove_listener('response', handler)
            logger.info("Interceptação de XHR finalizada.")

    def obter_capturas(self) -> List[Dict[str, Any]]:
        """Retorna os dados capturados e limpa a lista interna."""
        dados = list(self.capturas)
        self.capturas.clear()
        return dados

    def salvar_capturas(self, capturas: List[Dict[str, Any]], nome_base: str = "captura"):
        """Salva uma lista de capturas em arquivos JSON."""
        if not capturas:
            logger.info("Nenhuma captura para salvar.")
            return
            
        for i, captura in enumerate(capturas):
            timestamp = int(captura.get('timestamp', time.time()))
            filename = f"{nome_base}_{timestamp}_{i}.json"
            filepath = os.path.join(self.pasta_saida, filename)
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(captura, f, ensure_ascii=False, indent=2)
                logger.info(f"Captura salva: {filepath}")
            except Exception as e:
                logger.error(f"Erro ao salvar captura em {filepath}: {e}")