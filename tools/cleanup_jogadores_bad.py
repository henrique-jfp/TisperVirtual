import os
import sys
import json
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, REPO_ROOT)

# importa o client supabase já configurado no coletor
from coleta.api_coleta_365scores import supabase

BAD_API_IDS = [10,76,3,4,24,8,9,19,2,5,6,79,13,146,21,147,78,52,148,149,53,15,46,80,81,14,41,77,23,51,40,66,150,56,55,37,54,60,84,73,12,1,144]

def main():
    timestamp = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    backup_path = os.path.join(REPO_ROOT, f'tools/jogadores_bad_backup_{timestamp}.json')

    print(f"Buscando registros com api_id IN {BAD_API_IDS}...")
    try:
        # consultar os registros existentes
        res = supabase.table('jogadores').select('*').in_('api_id', BAD_API_IDS).execute()
    except Exception as e:
        print(f"Erro ao consultar 'jogadores': {e}")
        return

    rows = getattr(res, 'data', None) or []
    print(f"Encontrados {len(rows)} registros para backup.")

    # Salvar backup local em JSON
    try:
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump({'backup_at': timestamp, 'rows': rows}, f, ensure_ascii=False, indent=2)
        print(f"Backup salvo em: {backup_path}")
    except Exception as e:
        print(f"Falha ao salvar backup local: {e}")
        return

    if not rows:
        print("Nenhum registro a deletar.")
        return

    # Deletar os registros do Supabase
    try:
        del_res = supabase.table('jogadores').delete().in_('api_id', BAD_API_IDS).execute()
        print(f"Delete executado. Resultado: {getattr(del_res, 'data', None)}")
    except Exception as e:
        print(f"Erro ao deletar registros: {e}")
        print("Se a API do client não suportar .in_(), podemos iterar por .match() em cada id.")
        # fallback iterativo
        try:
            cnt = 0
            for aid in BAD_API_IDS:
                try:
                    r = supabase.table('jogadores').delete().match({'api_id': aid}).execute()
                    if getattr(r, 'data', None):
                        cnt += len(r.data)
                except Exception:
                    pass
            print(f"Fallback iterativo deletou ~{cnt} registros (estimado).")
        except Exception as e2:
            print(f"Falha no fallback de deleção: {e2}")

if __name__ == '__main__':
    main()
