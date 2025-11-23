import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'coleta'))

from coleta.navegador import Navegador
from coleta.captura_xhr import CapturaXHR
from coleta.processador import ProcessadorDados
from coleta.banco import BancoDados
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def coletar_dados(url: str, segundos: int = 10):
    """Fluxo completo de coleta de dados."""
    async with Navegador() as navegador:
        await navegador.navegar_para(url)

        captura = CapturaXHR(navegador)
        await captura.configurar_interceptacao()

        await captura.capturar_por_tempo(segundos)

        # Se não capturou dados, tentar extrair do HTML
        if not captura.capturas:
            logger.info("Nenhum XHR capturado, tentando extrair do HTML...")
            html = await navegador.extrair_dados_html()
            # Salvar HTML como JSON para processamento
            import time
            captura.capturas.append({
                'url': url,
                'data': {'html': html},
                'timestamp': time.time()
            })
            await captura.salvar_capturas()

        processador = ProcessadorDados()
        dfs = processador.processar_todos()

        banco = BancoDados()
        banco.salvar_dados(dfs)

        logger.info("Coleta de dados concluída.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python coletor.py <URL> [segundos]")
        sys.exit(1)

    url = sys.argv[1]
    segundos = int(sys.argv[2]) if len(sys.argv) > 2 else 10

    asyncio.run(coletar_dados(url, segundos))