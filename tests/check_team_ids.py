from supabase import create_client

SUPABASE_URL = "https://nflmvptqgicabovfmnos.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5mbG12cHRxZ2ljYWJvdmZtbm9zIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM3NzEzNTAsImV4cCI6MjA3OTM0NzM1MH0.l-RuwMrLgQgfjp8XZQ7bpEwfKODo7qKEXOhGR49xJ9c"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# IDs dos times Fla x Flu
flamengo_result = supabase.table('times').select('id, api_id, name').ilike('name', '%Flamengo%').execute()
fluminense_result = supabase.table('times').select('id, api_id, name').ilike('name', '%Fluminense%').execute()

print('Flamengo:')
if flamengo_result.data:
    print(f'  ID interno: {flamengo_result.data[0]["id"]}')
    print(f'  API ID: {flamengo_result.data[0]["api_id"]}')
    print(f'  Nome: {flamengo_result.data[0]["name"]}')

print('Fluminense:')
if fluminense_result.data:
    print(f'  ID interno: {fluminense_result.data[0]["id"]}')
    print(f'  API ID: {fluminense_result.data[0]["api_id"]}')
    print(f'  Nome: {fluminense_result.data[0]["name"]}')

# Verificar se há jogos com esses API IDs
fla_api_id = flamengo_result.data[0]['api_id'] if flamengo_result.data else None
flu_api_id = fluminense_result.data[0]['api_id'] if fluminense_result.data else None

if fla_api_id and flu_api_id:
    print(f'\nProcurando jogos com API IDs: {fla_api_id} vs {flu_api_id}')
    result1 = supabase.table('jogos').select('*').eq('home_team_api_id', fla_api_id).eq('away_team_api_id', flu_api_id).execute()
    result2 = supabase.table('jogos').select('*').eq('home_team_api_id', flu_api_id).eq('away_team_api_id', fla_api_id).execute()
    
    jogos = result1.data + result2.data
    print(f'Jogos encontrados: {len(jogos)}')
    
    for jogo in jogos:
        data = jogo.get('start_time', 'N/A')[:10] if jogo.get('start_time') else 'N/A'
        home_score = jogo.get('home_team_score', '?')
        away_score = jogo.get('away_team_score', '?')
        print(f'{data}: {fla_api_id if jogo["home_team_api_id"] == fla_api_id else flu_api_id} {home_score}x{away_score} {flu_api_id if jogo["away_team_api_id"] == flu_api_id else fla_api_id}')