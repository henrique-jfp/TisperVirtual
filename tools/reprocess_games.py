import re
import os
import sys
import time
import argparse
from typing import List


def extract_database_url_from_rag(path: str) -> str:
    """Extrai DATABASE_URL do arquivo rag_agent.py via regex."""
    import io
    with open(path, 'r', encoding='utf-8') as f:
        txt = f.read()
    m = re.search(r"DATABASE_URL\s*=\s*[\"'](.+?)[\"']", txt)
    if not m:
        raise RuntimeError("DATABASE_URL não encontrada em rag_agent.py")
    return m.group(1)


def get_recent_game_ids(database_url: str, limit: int = 10) -> List[int]:
    try:
        import psycopg2
        import psycopg2.extras
    except Exception as e:
        print("[ERRO] psycopg2 não disponível no ambiente. Instale com: pip install psycopg2-binary")
        raise

    conn = psycopg2.connect(database_url)
    try:
        cur = conn.cursor()
        cur.execute("SELECT api_id FROM public.jogos ORDER BY start_time DESC NULLS LAST LIMIT %s", (limit,))
        rows = cur.fetchall()
        return [int(r[0]) for r in rows]
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(description="Reprocessar coleta profunda para N jogos.")
    parser.add_argument("--ids", help="Lista separada por vírgula de game IDs para reprocessar (ex: 123,456,789)")
    parser.add_argument("--limit", type=int, default=10, help="Número de jogos recentes a buscar no DB quando --ids não for fornecido")
    args = parser.parse_args()

    base = os.path.join(os.path.dirname(__file__), '..', 'coleta', 'rag_agent.py')
    rag_path = os.path.abspath(base)
    if not os.path.exists(rag_path):
        print(f"[ERRO] Não encontrei o arquivo rag_agent.py em: {rag_path}")
        sys.exit(1)

    try:
        database_url = extract_database_url_from_rag(rag_path)
    except Exception as e:
        print(f"[ERRO] Falha ao extrair DATABASE_URL: {e}")
        sys.exit(1)

    print(f"Usando DATABASE_URL extraída de {rag_path}")


    # Se o usuário passou --ids, usa essa lista em vez de consultar o DB
    if args.ids:
        try:
            game_ids = [int(x.strip()) for x in args.ids.split(',') if x.strip()]
        except Exception as e:
            print(f"[ERRO] Formato inválido em --ids: {e}")
            sys.exit(1)
    else:
        try:
            game_ids = get_recent_game_ids(database_url, limit=args.limit)
        except Exception as e:
            print(f"[ERRO] Falha ao consultar jogos: {e}")
            sys.exit(1)

    if not game_ids:
        print("Nenhum jogo encontrado na tabela 'jogos'. Execute a coleta ampla primeiro.")
        sys.exit(0)

    print(f"Serão reprocessados {len(game_ids)} jogos (IDs): {game_ids}")

    # Importar o coletor local pelo caminho (evita necessidade de pacote instalado)
    try:
        import importlib.util
        from pathlib import Path
        spec = importlib.util.spec_from_file_location("api_coleta_365scores", str(Path(__file__).resolve().parents[1] / 'coleta' / 'api_coleta_365scores.py'))
        collector = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(collector)
    except Exception as e:
        print(f"[ERRO] Falha ao importar o coletor pelo caminho: {e}")
        sys.exit(1)

    failures = []
    for i, gid in enumerate(game_ids, start=1):
        print(f"\n[{i}/{len(game_ids)}] Reprocessando jogo ID={gid}...")
        try:
            collector.fetch_and_save_game_details(gid)
            time.sleep(1)
        except Exception as e:
            print(f"[ERRO] Falha ao reprocessar jogo {gid}: {e}")
            failures.append((gid, str(e)))

    print("\n--- Resumo da reprocessagem ---")
    print(f"Total tentados: {len(game_ids)}")
    print(f"Falhas: {len(failures)}")
    if failures:
        for gid, msg in failures:
            print(f" - {gid}: {msg}")


if __name__ == '__main__':
    main()
