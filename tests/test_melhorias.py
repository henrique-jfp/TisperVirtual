#!/usr/bin/env python3
"""
Teste completo das melhorias do SmartWebPrinter
"""

import asyncio
import json
from flask_api import processar_conteudo_web

async def test_melhorias():
    """Testa todas as melhorias implementadas"""

    print("🧪 TESTANDO MELHORIAS DO SMARTWEBPRINTER")
    print("=" * 60)

    # URLs de teste para diferentes tipos de conteúdo
    test_urls = [
        {
            'url': 'https://www.flashscore.com/match/abc123/#/match-summary',
            'expected_type': 'game_stats',
            'description': 'Página de estatísticas do Flashscore'
        },
        {
            'url': 'https://ge.globo.com/futebol/times/flamengo/noticia/2024/01/20/lesoes-flamengo.ghtml',
            'expected_type': 'injury_report',
            'description': 'Relatório de lesões'
        },
        {
            'url': 'https://ge.globo.com/futebol/times/flamengo/noticia/2024/01/20/flamengo-x-palmeiras.ghtml',
            'expected_type': 'match_report',
            'description': 'Relatório de jogo'
        }
    ]

    for i, test_case in enumerate(test_urls, 1):
        print(f"\n{i}. Testando: {test_case['description']}")
        print(f"   URL: {test_case['url']}")
        print(f"   Tipo esperado: {test_case['expected_type']}")

        try:
            # Processar conteúdo
            resultado = await processar_conteudo_web(test_case['url'])

            if 'error' in resultado:
                print(f"   ❌ Erro: {resultado['error']}")
                continue

            # Verificar tipo detectado
            content_type = resultado.get('content_type', 'unknown')
            print(f"   ✅ Tipo detectado: {content_type}")

            # Verificar dados estruturados
            if 'data' in resultado:
                data = resultado['data']
                teams = data.get('teams', [])
                players = data.get('players', [])
                confidence = data.get('confidence', 0)

                print(f"   📊 Times encontrados: {len(teams)} - {teams[:2]}")
                print(f"   👥 Jogadores encontrados: {len(players)} - {players[:3]}")
                print(f"   🎯 Confiança: {confidence}")

                # Verificar link_info
                link_info = data.get('link_info', {})
                if link_info:
                    print(f"   🔗 Info de linkagem: {link_info.get('teams_found', [])}")

                # Verificar resultado de inserção
                insert_result = resultado.get('insert_result')
                if insert_result:
                    status = insert_result.get('status')
                    if status == 'inserted':
                        print(f"   💾 Dados inseridos com sucesso")
                    elif status == 'duplicate':
                        print(f"   ⚠️  Dados duplicados - não inseridos")
                    else:
                        print(f"   ❌ Erro na inserção: {insert_result}")

            print(f"   📄 Markdown salvo: {resultado.get('markdown_file', 'N/A')}")

        except Exception as e:
            print(f"   ❌ Erro inesperado: {e}")

    print("\n" + "=" * 60)
    print("🏁 TESTE DAS MELHORIAS CONCLUÍDO")

    # Teste adicional: verificar funções de linkagem
    print("\n🔗 TESTANDO FUNÇÕES DE LINKAGEM")
    print("-" * 40)

    # Simular dados de jogo
    jogo_teste = {
        'content_type': 'game_stats',
        'teams': ['Flamengo', 'Palmeiras'],
        'date': '2024-01-20T16:00:00',
        'data': {
            'statistics': {
                'Posse': {'home': '55%', 'away': '45%'},
                'Chutes': {'home': '12', 'away': '8'}
            }
        }
    }

    print("Dados de teste:")
    print(json.dumps(jogo_teste, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(test_melhorias())