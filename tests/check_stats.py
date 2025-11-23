from supabase import create_client
import json

SUPABASE_URL = "https://nflmvptqgicabovfmnos.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5mbG12cHRxZ2ljYWJvdmZtbm9zIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM3NzEzNTAsImV4cCI6MjA3OTM0NzM1MH0.l-RuwMrLgQgfjp8XZQ7bpEwfKODo7qKEXOhGR49xJ9c"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Verificar se há dados no raw_payload dos jogos
result = supabase.table('jogos').select('id, api_id, raw_payload').limit(3).execute()

print('Verificando raw_payload dos jogos...')
for jogo in result.data:
    print(f'\nJogo ID: {jogo["id"]} (API: {jogo["api_id"]})')
    if jogo.get('raw_payload'):
        try:
            payload = json.loads(jogo['raw_payload']) if isinstance(jogo['raw_payload'], str) else jogo['raw_payload']
            print('Raw payload encontrado!')

            # Procurar por estatísticas no payload
            if isinstance(payload, dict):
                # Verificar se há seções de estatísticas
                stats_keys = [k for k in payload.keys() if 'stat' in k.lower() or 'corner' in k.lower() or 'shot' in k.lower() or 'pass' in k.lower()]
                if stats_keys:
                    print(f'Possíveis chaves de stats: {stats_keys}')

                # Mostrar estrutura geral
                print('Estrutura do payload:')
                for key in list(payload.keys())[:10]:  # Primeiras 10 chaves
                    value = payload[key]
                    if isinstance(value, (list, dict)):
                        print(f'  {key}: {type(value)} (tamanho: {len(value) if hasattr(value, "__len__") else "N/A"})')
                    else:
                        print(f'  {key}: {value}')

                # Procurar especificamente por corners, shots, passes
                search_terms = ['corner', 'shot', 'pass', 'big chance', 'total pass']
                found_stats = {}
                def search_in_dict(d, path=''):
                    for k, v in d.items():
                        current_path = f'{path}.{k}' if path else k
                        if any(term in k.lower() for term in search_terms):
                            found_stats[current_path] = v
                        if isinstance(v, dict):
                            search_in_dict(v, current_path)
                        elif isinstance(v, list) and v and isinstance(v[0], dict):
                            for i, item in enumerate(v[:3]):  # Verificar primeiros 3 itens
                                search_in_dict(item, f'{current_path}[{i}]')

                search_in_dict(payload)
                if found_stats:
                    print('\n📊 Estatísticas encontradas:')
                    for stat_path, value in found_stats.items():
                        print(f'  {stat_path}: {value}')
                else:
                    print('\n❌ Nenhuma estatística específica encontrada neste jogo')
            else:
                print(f'Payload não é um dict: {type(payload)}')
        except Exception as e:
            print(f'Erro ao processar payload: {e}')
    else:
        print('Sem raw_payload')