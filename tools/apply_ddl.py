import sys
import traceback
from pathlib import Path

# Carrega DATABASE_URL de rag_agent.py
import re

rag_path = Path('c:/TradeComigo/coleta/rag_agent.py')
if not rag_path.exists():
    print('ERRO: coleta/rag_agent.py não encontrado')
    sys.exit(2)

content = rag_path.read_text(encoding='utf8')
match = re.search(r"DATABASE_URL\s*=\s*['\"](?P<url>[^'\"]+)['\"]", content)
DATABASE_URL = match.group('url') if match else None
if not DATABASE_URL:
    print('ERRO: DATABASE_URL não encontrada em coleta/rag_agent.py')
    sys.exit(2)

sql_path = Path('c:/TradeComigo/db/create_tables.sql')
if not sql_path.exists():
    print('ERRO: Arquivo SQL não encontrado em', sql_path)
    sys.exit(2)

sql_text = sql_path.read_text(encoding='utf8')

print('Usando DATABASE_URL:', DATABASE_URL)

try:
    import psycopg2
    from psycopg2 import sql
except Exception as e:
    print('ERRO: psycopg2 não disponível:', e)
    sys.exit(3)

# Conecta e executa o SQL
try:
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = False
    cur = conn.cursor()
    print('Conectado. Executando SQL...')
    cur.execute(sql_text)
    conn.commit()
    print('DDL aplicado com sucesso.')
    cur.close()
    conn.close()
except Exception as e:
    print('ERRO durante execução do DDL:')
    traceback.print_exc()
    try:
        conn.rollback()
    except Exception:
        pass
    sys.exit(4)
