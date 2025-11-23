import os
os.environ['SUPABASE_URL'] = 'https://nflmvptqgicabovfmnos.supabase.co'
os.environ['SUPABASE_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5mbG12cHRxZ2ljYWJvdmZtbm9zIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM3NzEzNTAsImV4cCI6MjA3OTM0NzM1MH0.l-RuwMrLgQgfjp8XZQ7bpEwfKODo7qKEXOhGR49xJ9c'
from supabase import create_client
import json

supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

# Verificar alguns jogos recentes para ver como os times estão salvos
print("🔍 Verificando estrutura dos dados de jogos recentes...")

result = supabase.table('jogos').select('api_id,start_time,status,raw_payload').eq('status', 'FINISHED').order('start_time', desc=True).limit(5).execute()

for game in result.data:
    print(f"\n--- Jogo ID: {game['api_id']} ---")
    print(f"Data: {game['start_time'][:10]}, Status: {game['status']}")

    if game.get('raw_payload') and isinstance(game['raw_payload'], dict):
        payload = game['raw_payload']
        home_team = payload.get('homeTeam', {}).get('name', 'N/A')
        away_team = payload.get('awayTeam', {}).get('name', 'N/A')
        print(f"Times: {home_team} vs {away_team}")

        # Verificar se algum desses times contém "fla" ou "flu"
        home_lower = home_team.lower()
        away_lower = away_team.lower()

        if ('fla' in home_lower or 'fla' in away_lower or
            'flu' in home_lower or 'flu' in away_lower or
            'mengo' in home_lower or 'mengo' in away_lower):
            print("🎯 POSSÍVEL JOGO FLA x FLU!")
    else:
        print("Sem raw_payload detalhado")

print("\n🔍 Agora procurando especificamente por jogos com 'fla' ou 'flu'...")

# Busca mais ampla
all_games = supabase.table('jogos').select('api_id,start_time,status,raw_payload').execute()

fla_flu_games = []
for game in all_games.data:
    if game.get('raw_payload') and isinstance(game['raw_payload'], dict):
        payload = game['raw_payload']
        home_team = payload.get('homeTeam', {}).get('name', '')
        away_team = payload.get('awayTeam', {}).get('name', '')

        home_lower = home_team.lower()
        away_lower = away_team.lower()

        # Verificar várias possibilidades
        has_fla = ('fla' in home_lower or 'fla' in away_lower or 'mengo' in home_lower or 'mengo' in away_lower)
        has_flu = ('flu' in home_lower or 'flu' in away_lower or 'xente' in home_lower or 'xente' in away_lower)

        if has_fla and has_flu:
            fla_flu_games.append(game)

if fla_flu_games:
    # Ordenar por data
    fla_flu_games.sort(key=lambda x: x['start_time'], reverse=True)
    latest_game = fla_flu_games[0]

    print(f"\n✅ Último jogo Fla x Flu encontrado:")
    print(f"ID: {latest_game['api_id']}")
    print(f"Data: {latest_game['start_time'][:10]}")

    payload = latest_game['raw_payload']
    home_team = payload.get('homeTeam', {}).get('name', 'N/A')
    away_team = payload.get('awayTeam', {}).get('name', 'N/A')
    home_score = latest_game.get('home_team_score')
    away_score = latest_game.get('away_team_score')

    print(f"🏆 {home_team} {home_score} x {away_score} {away_team}")
else:
    print("❌ Ainda nenhum jogo Fla x Flu encontrado")