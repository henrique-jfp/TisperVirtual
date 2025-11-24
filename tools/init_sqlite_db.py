#!/usr/bin/env python3
"""
Inicializa um banco SQLite a partir do arquivo `schema.sql` na raiz do projeto.

Uso:
    python tools/init_sqlite_db.py --db-path db/tradecomigo.sqlite3

O script cria o diretório pai do arquivo de banco, lê `schema.sql` e executa
o script SQL usando sqlite3.executescript.
"""
from __future__ import annotations
import argparse
import sqlite3
from pathlib import Path
import sys


def init_sqlite_db(schema_file: Path, db_path: Path) -> None:
    """Cria (ou abre) um banco SQLite e aplica o schema SQL.

    Args:
        schema_file: caminho para o arquivo `schema.sql`.
        db_path: caminho para o arquivo .sqlite3 a ser criado/atualizado.
    """
    if not schema_file.exists():
        raise FileNotFoundError(f"schema.sql não encontrado em: {schema_file}")

    db_parent = db_path.parent
    db_parent.mkdir(parents=True, exist_ok=True)

    schema_sql = schema_file.read_text(encoding="utf-8")

    # Conecta e executa todo o script (executa múltiplos comandos)
    conn = sqlite3.connect(str(db_path))
    try:
        conn.executescript(schema_sql)
        conn.commit()
    finally:
        conn.close()


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Inicializa SQLite a partir de schema.sql")
    p.add_argument("--schema", type=Path, default=Path("schema.sql"), help="Caminho para schema.sql (padrão: ./schema.sql)")
    p.add_argument("--db-path", type=Path, default=Path("db/tradecomigo.sqlite3"), help="Caminho do arquivo SQLite a ser criado (padrão: db/tradecomigo.sqlite3)")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    try:
        print(f"Usando schema: {args.schema.resolve()}")
        print(f"Criando/atualizando DB SQLite em: {args.db_path.resolve()}")
        init_sqlite_db(args.schema, args.db_path)
        print("Banco SQLite inicializado com sucesso.")
        return 0
    except Exception as e:
        print(f"Erro: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
