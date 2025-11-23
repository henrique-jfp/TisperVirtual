from supabase import create_client

SUPABASE_URL = "https://nflmvptqgicabovfmnos.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5mbG12cHRxZ2ljYWJvdmZtbm9zIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM3NzEzNTAsImV4cCI6MjA3OTM0NzM1MH0.l-RuwMrLgQgfjp8XZQ7bpEwfKODo7qKEXOhGR49xJ9c"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Verificar total de jogos
result = supabase.table('jogos').select('id, home_team_api_id, away_team_api_id, start_time').order('start_time', desc=True).limit(10).execute()
print(f'Total de jogos na tabela: {len(result.data)}')
print('Últimos 10 jogos:')
for jogo in result.data:
    data = jogo.get('start_time', 'N/A')[:10] if jogo.get('start_time') else 'N/A'
    home_id = jogo.get('home_team_api_id', '?')
    away_id = jogo.get('away_team_api_id', '?')
    print(f'{data}: Time {home_id} vs Time {away_id}')