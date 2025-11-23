import os
os.environ['SUPABASE_URL'] = 'https://nflmvptqgicabovfmnos.supabase.co'
os.environ['SUPABASE_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5mbG12cHRxZ2ljYWJvdmZtbm9zIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM3NzEzNTAsImV4cCI6MjA3OTM0NzM1MH0.l-RuwMrLgQgfjp8XZQ7bpEwfKODo7qKEXOhGR49xJ9c'
from supabase import create_client
import json

supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

print("🔍 Procurando jogos clássicos (Flamengo x Fluminense)...")

# Buscar todos os jogos e verificar raw_payload
all_games = supabase.table('jogos').select('api_id,start_time,status,raw_payload').execute()

classic_games = []
for game in all_games.data:
    if game.get('raw_payload') and isinstance(game['raw_payload'], dict):
        payload = game['raw_payload']
        home_team = payload.get('homeTeam', {}).get('name', '').lower()
        away_team = payload.get('awayTeam', {}).get('name', '').lower()

        # Verificar várias possibilidades de nomes
        teams_text = f"{home_team} vs {away_team}"

        # Flamengo: flamengo, mengo, fla
        # Fluminense: fluminense, flu, xente, tricolor
        has_flamengo = any(term in teams_text for term in ['flamengo', 'mengo', 'fla'])
        has_fluminense = any(term in teams_text for term in ['fluminense', 'flu', 'xente', 'tricolor'])

        if has_flamengo and has_fluminense:
            classic_games.append(game)

if classic_games:
    # Ordenar por data (mais recente primeiro)
    classic_games.sort(key=lambda x: x['start_time'], reverse=True)

    print(f"\n✅ Encontrados {len(classic_games)} jogos clássicos!")
    print("\n📅 Lista de jogos Fla x Flu:")

    for i, game in enumerate(classic_games[:10]):  # Mostrar os 10 mais recentes
        payload = game['raw_payload']
        home_team = payload.get('homeTeam', {}).get('name', 'N/A')
        away_team = payload.get('awayTeam', {}).get('name', 'N/A')
        home_score = game.get('home_team_score')
        away_score = game.get('away_team_score')

        print(f"{i+1}. {game['start_time'][:10]}: {home_team} {home_score}-{away_score} {away_team}")

    # Mostrar detalhes do mais recente
    latest_game = classic_games[0]
    print(f"\n🎯 DETALHES DO ÚLTIMO JOGO:")
    print(f"ID: {latest_game['api_id']}")
    print(f"Data: {latest_game['start_time'][:10]}")
    print(f"Status: {latest_game['status']}")

    payload = latest_game['raw_payload']
    home_team = payload.get('homeTeam', {}).get('name', 'N/A')
    away_team = payload.get('awayTeam', {}).get('name', 'N/A')
    home_score = latest_game.get('home_team_score')
    away_score = latest_game.get('away_team_score')

    print(f"🏆 {home_team} {home_score} x {away_score} {away_team}")

    # Verificar estatísticas
    game_id = latest_game['api_id']
    stats_result = supabase.table('estatisticas_jogador').select('*').eq('jogo_api_id', game_id).execute()
    print(f"📊 Estatísticas de jogadores: {len(stats_result.data)} registros")

    events_result = supabase.table('eventos_jogo').select('*').eq('jogo_api_id', game_id).execute()
    print(f"⚽ Eventos do jogo: {len(events_result.data)} registros")

else:
    print("❌ Nenhum jogo clássico encontrado")
    print("\n💡 Verificando alguns jogos aleatórios para entender a estrutura...")

    # Mostrar alguns jogos para debug
    sample_games = all_games.data[:3]
    for game in sample_games:
        if game.get('raw_payload') and isinstance(game['raw_payload'], dict):
            payload = game['raw_payload']
            home_team = payload.get('homeTeam', {}).get('name', 'N/A')
            away_team = payload.get('awayTeam', {}).get('name', 'N/A')
            print(f"Exemplo - ID {game['api_id']}: {home_team} vs {away_team}")