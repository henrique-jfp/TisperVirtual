from supabase import create_client
import json

SUPABASE_URL = "https://nflmvptqgicabovfmnos.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5mbG12cHRxZ2ljYWJvdmZtbm9zIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM3NzEzNTAsImV4cCI6MjA3OTM0NzM1MH0.l-RuwMrLgQgfjp8XZQ7bpEwfKODo7qKEXOhGR49xJ9c"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Buscar IDs dos times Flamengo e Fluminense
flamengo_result = supabase.table('times').select('id, name').ilike('name', '%Flamengo%').execute()
fluminense_result = supabase.table('times').select('id, name').ilike('name', '%Fluminense%').execute()

flamengo_id = flamengo_result.data[0]['id'] if flamengo_result.data else None
fluminense_id = fluminense_result.data[0]['id'] if fluminense_result.data else None

print(f'Flamengo ID: {flamengo_id}')
print(f'Fluminense ID: {fluminense_id}')

if flamengo_id and fluminense_id:
    # Buscar jogos Fla x Flu
    result1 = supabase.table('jogos').select('*').eq('home_team_api_id', flamengo_id).eq('away_team_api_id', fluminense_id).order('start_time', desc=True).limit(5).execute()
    result2 = supabase.table('jogos').select('*').eq('home_team_api_id', fluminense_id).eq('away_team_api_id', flamengo_id).order('start_time', desc=True).limit(5).execute()

    # Combinar resultados
    todos_jogos = result1.data + result2.data
    # Ordenar por data decrescente
    todos_jogos.sort(key=lambda x: x.get('start_time', ''), reverse=True)
    jogos = todos_jogos[:5]  # Pegar os 5 mais recentes

    print('\nJogos Fla x Flu encontrados:')
    for jogo in jogos:
        data = jogo.get('start_time', 'N/A')[:10] if jogo.get('start_time') else 'N/A'
        home_score = jogo.get('home_team_score', '?')
        away_score = jogo.get('away_team_score', '?')
        print(f'{data}: Time {jogo.get("home_team_api_id", "?")} {home_score}x{away_score} Time {jogo.get("away_team_api_id", "?")}')

    print(f'\nTotal de jogos encontrados: {len(jogos)}')
else:
    print('Times não encontrados')