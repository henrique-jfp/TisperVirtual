import os
os.environ['SUPABASE_URL'] = 'https://nflmvptqgicabovfmnos.supabase.co'
os.environ['SUPABASE_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5mbG12cHRxZ2ljYWJvdmZtbm9zIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM3NzEzNTAsImV4cCI6MjA3OTM0NzM1MH0.l-RuwMrLgQgfjp8XZQ7bpEwfKODo7qKEXOhGR49xJ9c'
from supabase import create_client
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])
result = supabase.table('jogos').select('api_id,start_time,status').eq('status', 'FINISHED').order('start_time', desc=True).limit(10).execute()
for game in result.data:
    print(f'ID: {game["api_id"]}, Data: {game["start_time"][:10]}, Status: {game["status"]}')