import os
os.environ['SUPABASE_URL'] = 'https://nflmvptqgicabovfmnos.supabase.co'
os.environ['SUPABASE_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5mbG12cHRxZ2ljYWJvdmZtbm9zIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM3NzEzNTAsImV4cCI6MjA3OTM0NzM1MH0.l-RuwMrLgQgfjp8XZQ7bpEwfKODo7qKEXOhGR49xJ9c'
from supabase import create_client
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

game_id = 4380287
stats_result = supabase.table('estatisticas_jogador').select('player_api_id,stat_name,value').eq('jogo_api_id', game_id).execute()
print(f"Estatísticas de jogadores para jogo {game_id}: {len(stats_result.data)} registros")
for stat in stats_result.data[:20]:  # Mostra primeiras 20
    print(f'  Jogador {stat["player_api_id"]}: {stat["stat_name"]} = {stat["value"]}')

# Ver também jogadores
players_result = supabase.table('jogadores').select('api_id,name').limit(10).execute()
print(f"\nTotal de jogadores no banco: {len(players_result.data)}")
for player in players_result.data[:5]:
    print(f'  {player["api_id"]}: {player["name"]}')