from flask_api import consultar_estatisticas_jogo

print("🧪 TESTANDO CONSULTA DE ESTATÍSTICAS DO SUPABASE")
print("=" * 60)

# Testar consulta geral
print("\n1. Consultando estatísticas gerais...")
stats = consultar_estatisticas_jogo()
if stats:
    print(f"✅ Encontrados {len(stats)} jogos com estatísticas")
    for jogo_id, jogo_data in list(stats.items())[:2]:  # Mostrar 2 jogos
        print(f"\n🏟️ Jogo {jogo_id}:")
        estatisticas = jogo_data['estatisticas']
        print(f"   Total de estatísticas: {len(estatisticas)}")

        # Verificar estatísticas específicas
        estatisticas_alvo = ['Corners', 'Big Chances Created', 'Shots Outside Box', 'Total Passes']
        for stat_name in estatisticas_alvo:
            if stat_name in estatisticas:
                home_val = estatisticas[stat_name]['home']
                away_val = estatisticas[stat_name]['away']
                print(f"   ✅ {stat_name}: Casa {home_val} x Visitante {away_val}")
            else:
                print(f"   ❌ {stat_name}: Não encontrado")
else:
    print("❌ Nenhuma estatística encontrada")

# Testar consulta específica
print("\n2. Testando consulta de jogo específico...")
jogo_teste = 4380263  # Primeiro jogo dos dados
stats_especifico = consultar_estatisticas_jogo(jogo_teste)
if stats_especifico and jogo_teste in stats_especifico:
    print(f"✅ Estatísticas do jogo {jogo_teste} encontradas")
    jogo_data = stats_especifico[jogo_teste]
    estatisticas = jogo_data['estatisticas']
    print(f"   Estatísticas encontradas: {len(estatisticas)}")

    # Mostrar algumas estatísticas
    for stat_name in ['Corners', 'Big Chances Created', 'Shots Outside Box', 'Total Passes', 'Possession']:
        if stat_name in estatisticas:
            home_val = estatisticas[stat_name]['home']
            away_val = estatisticas[stat_name]['away']
            print(f"   • {stat_name}: {home_val} x {away_val}")
else:
    print(f"❌ Estatísticas do jogo {jogo_teste} não encontradas")

print("\n" + "=" * 60)
print("🏁 TESTE CONCLUÍDO")