from coleta.api_coleta_365scores import supabase

resp = supabase.table('jogos').select('api_id, competition').limit(10).execute()
for r in resp.data:
    print(f'{r["api_id"]}: {r["competition"]}')