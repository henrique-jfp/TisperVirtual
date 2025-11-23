import os
os.environ['SUPABASE_URL'] = 'https://nflmvptqgicabovfmnos.supabase.co'
os.environ['SUPABASE_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5mbG12cHRxZ2ljYWJvdmZtbm9zIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM3NzEzNTAsImV4cCI6MjA3OTM0NzM1MH0.l-RuwMrLgQgfjp8XZQ7bpEwfKODo7qKEXOhGR49xJ9c'
from supabase import create_client
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

# Ver jogos já processados
result = supabase.table('jogos_processados').select('jogo_api_id,status,details').eq('status', 'PROCESSED').limit(5).execute()
print("Jogos já processados com estatísticas:")
for item in result.data:
    print(f'ID: {item["jogo_api_id"]}, Status: {item["status"]}, Detalhes: {item["details"]}')

# Ver se há estatísticas de jogadores para esses jogos
if result.data:
    game_id = result.data[0]["jogo_api_id"]
    stats_result = supabase.table('estatisticas_jogador').select('player_api_id,stat_name,value').eq('jogo_api_id', game_id).limit(10).execute()
    print(f"\nEstatísticas de jogadores para jogo {game_id}:")
    for stat in stats_result.data:
        print(f'  Jogador {stat["player_api_id"]}: {stat["stat_name"]} = {stat["value"]}')