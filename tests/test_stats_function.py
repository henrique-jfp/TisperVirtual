# Testar a função diretamente
import sys
sys.path.append('.')
from flask_api import consultar_estatisticas_jogo

stats = consultar_estatisticas_jogo()
if stats:
    print('📊 Estatísticas encontradas!')
    for categoria, estatisticas in list(stats.items())[:3]:  # Mostrar 3 categorias
        print(f'\n🔹 {categoria}:')
        for stat in estatisticas[:3]:  # 3 stats por categoria
            print(f'  • {stat["nome"]}: {stat["valor"]} (Time {stat["time"]})')
else:
    print('❌ Nenhuma estatística encontrada')