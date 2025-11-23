import os
import sys
import json
from datetime import datetime, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, REPO_ROOT)

from coleta.api_coleta_365scores import supabase


def main():
    # Consulta as últimas 30 linhas da tabela jogadores ordenadas por created_at desc
    try:
        res = supabase.table('jogadores').select('*').order('created_at', desc=True).limit(30).execute()
    except Exception as e:
        print(f"Erro ao consultar jogadores: {e}")
        return

    rows = getattr(res, 'data', None) or []
    print(json.dumps(rows, ensure_ascii=False, indent=2, default=str))

if __name__ == '__main__':
    main()
