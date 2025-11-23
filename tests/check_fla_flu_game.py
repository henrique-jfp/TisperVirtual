import os
os.environ['SUPABASE_URL'] = 'https://nflmvptqgicabovfmnos.supabase.co'
os.environ['SUPABASE_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5mbG12cHRxZ2ljYWJvdmZtbm9zIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM3NzEzNTAsImV4cCI6MjA3OTM0NzM1MH0.l-RuwMrLgQgfjp8XZQ7bpEwfKODo7qKEXOhGR49xJ9c'
from supabase import create_client
import json

supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

# Buscar último jogo entre Flamengo e Fluminense
print("🔍 Procurando último jogo entre Flamengo e Fluminense...")

# Primeiro, vamos ver todos os jogos com esses times
result = supabase.table('jogos').select('api_id,start_time,status,home_team_score,away_team_score,raw_payload').execute()

flamengo_games = []
for game in result.data:
    if game.get('raw_payload'):
        payload = game['raw_payload']
        if isinstance(payload, dict):
            home_team = payload.get('homeTeam', {}).get('name', '').lower()
            away_team = payload.get('awayTeam', {}).get('name', '').lower()

            if ('flamengo' in home_team and 'fluminense' in away_team) or ('fluminense' in home_team and 'flamengo' in away_team):
                flamengo_games.append(game)

# Ordenar por data (mais recente primeiro)
flamengo_games.sort(key=lambda x: x['start_time'], reverse=True)

if flamengo_games:
    latest_game = flamengo_games[0]
    print(f"\n✅ Último jogo encontrado:")
    print(f"ID: {latest_game['api_id']}")
    print(f"Data: {latest_game['start_time'][:10]}")
    print(f"Status: {latest_game['status']}")

    if latest_game.get('raw_payload'):
        payload = latest_game['raw_payload']
        home_team = payload.get('homeTeam', {}).get('name', 'N/A')
        away_team = payload.get('awayTeam', {}).get('name', 'N/A')
        home_score = latest_game.get('home_team_score')
        away_score = latest_game.get('away_team_score')

        print(f"🏆 {home_team} {home_score} x {away_score} {away_team}")

        # Verificar se há estatísticas salvas
        game_id = latest_game['api_id']
        stats_result = supabase.table('estatisticas_jogador').select('*').eq('jogo_api_id', game_id).execute()
        print(f"📊 Estatísticas de jogadores: {len(stats_result.data)} registros")

        # Verificar eventos
        events_result = supabase.table('eventos_jogo').select('*').eq('jogo_api_id', game_id).execute()
        print(f"⚽ Eventos do jogo: {len(events_result.data)} registros")

        if events_result.data:
            print("\n📋 Últimos eventos:")
            for event in events_result.data[-5:]:  # Últimos 5 eventos
                print(f"  {event.get('minute', 'N/A')}' - {event.get('type', 'N/A')}")

    else:
        print("❌ Dados detalhados não disponíveis no raw_payload")

else:
    print("❌ Nenhum jogo entre Flamengo e Fluminense encontrado")