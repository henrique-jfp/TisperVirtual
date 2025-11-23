import re
import psycopg2
from urllib.parse import urlparse

RAG_AGENT_PATH = r"c:\TradeComigo\coleta\rag_agent.py"

def extract_database_url(path):
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('DATABASE_URL') and ('"' in line or "'" in line):
                parts = line.split('"')
                if len(parts) >= 3:
                    return parts[1]
                parts = line.split("'")
                if len(parts) >= 3:
                    return parts[1]
    return None

DB_URL = extract_database_url(RAG_AGENT_PATH)
if not DB_URL:
    raise SystemExit('Não foi possível extrair DATABASE_URL de coleta/rag_agent.py')

print('Usando DATABASE_URL:', DB_URL)

def connect(db_url):
    # psycopg2 accepts the URL directly
    return psycopg2.connect(db_url)

TABLES = ['jogadores', 'estatisticas_jogador', 'eventos_jogo', 'jogos', 'jogos_processados', 'raw_game_data']

with connect(DB_URL) as conn:
    with conn.cursor() as cur:
        for t in TABLES:
            print(f"\n=== TABELA: {t} ===")
            try:
                cur.execute("SELECT COUNT(*) FROM %s" % t)
                cnt = cur.fetchone()[0]
                print(f"COUNT = {cnt}")
            except Exception as e:
                print(f"Erro ao contar {t}: {e}")

            try:
                # listar colunas
                cur.execute("SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name=%s ORDER BY ordinal_position", (t,))
                cols = cur.fetchall()
                if not cols:
                    print('  (nenhuma coluna encontrada)')
                else:
                    for c in cols:
                        print(f"  - {c[0]} : {c[1]} nullable={c[2]}")
            except Exception as e:
                print(f"Erro ao listar colunas de {t}: {e}")

        # também verificar se há regras RLS que bloqueiam inserts (requer superuser; apenas listar policies se possível)
        try:
            cur.execute("SELECT polname, polcmd, polpermissive, polroles FROM pg_policies WHERE schemaname='public' AND tablename IN %s", (tuple(TABLES),))
            policies = cur.fetchall()
            print('\nPolicies encontradas:')
            if not policies:
                print('  (nenhuma policy encontrada)')
            else:
                for p in policies:
                    print('  ', p)
        except Exception as e:
            print('Falha ao listar policies (pode não ter permissão):', e)

print('\nInspeção completa.')
