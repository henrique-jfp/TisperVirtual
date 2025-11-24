# Histórico: Conexões Supabase (arquivo mantido para referência)

Este documento continha passos para diagnosticar problemas com uma instância Supabase.
O projeto foi migrado para um modo SQLite-local por padrão para execução em servidores domésticos (Termux). Mantemos este arquivo apenas como referência histórica; a solução atual recomenda:

- Usar o script `tools/init_sqlite_db.py` para criar/atualizar o banco local `db/tradecomigo.sqlite3`.
- Rodar `python run_coleta.py` para popular os dados localmente.

Se você ainda precisar operar com uma instância Supabase externa, favor considerar migrar os dados do SQLite para um Postgres remoto e adaptar `coleta/banco_dados.py` para apontar para a URL remota.