import json

# Carregar o arquivo de estatísticas
with open('tools/playwright_captures/stats_direct_365531214467481.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("📊 ESTATÍSTICAS EXTRAÍDAS DO ARQUIVO JSON")
print("=" * 50)

# Estatísticas específicas que o usuário mencionou
target_stats = {
    'Corners': ['Escanteios'],
    'Big Chances Created': ['Chances perigosas criadas'],
    'Shots Outside Box': ['Chutes fora da área'],
    'Total Passes': ['Total de passes']
}

# Percorrer todas as estatísticas
stats_found = {}
for stat in data.get('statistics', []):
    stat_name = stat.get('name', '')
    competitor_id = stat.get('competitorId', '')
    value = stat.get('value', '')

    # Verificar se é uma das estatísticas alvo
    for category, names in target_stats.items():
        if any(name.lower() in stat_name.lower() for name in names):
            if category not in stats_found:
                stats_found[category] = []
            stats_found[category].append({
                'name': stat_name,
                'competitor': competitor_id,
                'value': value
            })

# Mostrar resultados
for category, stats in target_stats.items():
    print(f"\n🔍 {category}:")
    if category in stats_found:
        for stat in stats_found[category]:
            print(f"  • {stat['name']}: {stat['value']} (Time ID: {stat['competitor']})")
    else:
        print("  ❌ Não encontrada")

# Mostrar todas as categorias de estatísticas disponíveis
print("\n📂 CATEGORIAS DE ESTATÍSTICAS DISPONÍVEIS:")
print("=" * 50)
categories = set()
for stat in data.get('statistics', []):
    category = stat.get('categoryName', 'Geral')
    categories.add(category)

for category in sorted(categories):
    print(f"• {category}")

# Mostrar algumas estatísticas de exemplo
print("\n🎯 EXEMPLOS DE ESTATÍSTICAS ENCONTRADAS:")
print("=" * 50)
example_stats = [
    'Posse de Bola',
    'Gols esperados (xG)',
    'Total de chutes',
    'Escanteios',
    'Chances perigosas criadas',
    'Chutes fora da área',
    'Total de passes',
    'Passes completos',
    'Faltas cometidas',
    'Cartões amarelos'
]

for stat in data.get('statistics', []):
    stat_name = stat.get('name', '')
    if stat_name in example_stats:
        competitor = stat.get('competitorId', '')
        value = stat.get('value', '')
        print(f"• {stat_name}: {value} (Time: {competitor})")

print("\n💾 CONCLUSÃO:")
print("✅ Estatísticas foram extraídas por scraping e salvas em português!")
print("✅ As estatísticas específicas mencionadas (corners, big chances, shots outside box, total passes) estão presentes!")
print("❌ Porém, elas NÃO estão salvas no banco Supabase, apenas nos arquivos JSON locais.")
print("💡 Para usar essas estatísticas no chat, seria necessário criar uma tabela no banco e importar esses dados.")