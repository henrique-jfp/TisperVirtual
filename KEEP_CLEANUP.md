# Manutenção: O que manter e o que remover

Data: 2025-11-24

Objetivo: fornecer uma lista prática e priorizada de arquivos/áreas do repositório para manter, consolidar ou remover, sempre preservando a versão mais completa e funcional do sistema que roda no servidor local (SQLite + collectors).

**Princípio guia**: manter a implementação que seja mais completa, testada e adequada para execução no servidor caseiro (Termux + SQLite). Remover duplicatas, utilitários obsoletos e integrações com clientes de nuvem do código backend (front-end pode ser tratado separadamente).

- **Contexto do servidor:** execução em Termux (m21s), banco local SQLite (`db/tradecomigo.sqlite3`), processos gerenciados por `pm2`/systemd. Backup do arquivo DB e controles de permissão são necessários.

**Manter (Alta prioridade)**
- **`schema.sql`**: schema completo direcionado a SQLite. Motivo: representa a modelagem principal do bot; usada pelo script de inicialização do DB.
- **`tools/init_sqlite_db.py`**: script que cria/atualiza o SQLite a partir do `schema.sql`. Motivo: bootstrap idempotente do ambiente no servidor.
- **`coleta/` (pasta)**: especialmente `banco_dados.py`, `api_coleta_365scores.py`, `processador.py`, `processador` e `run_coleta.py`. Motivo: reagente principal do scraping/ETL que popula o DB local.
- **`run_coleta.py`**: orquestrador de coleta. Motivo: processo principal que você roda no Termux.
- **`tools/smart_web_printer.py`** e utilitários de extração (PDF/html): Motivo: responsáveis por conversão HTML→Markdown e preparação de payloads para ingestão — mantê-los se você usa a pipeline HITL.
- **`coleta/bot_queries.py`**: adaptado para SQLite — mantém consultas frequentes para integração do bot.
- **`requirements.txt`** (limpo): manter e garantir que não contenha dependências supérfluas (removemos `supabase`). Motivo: referência para instalação no servidor.
- **`tools/*` essenciais**: `find_and_capture.py`, `reprocess_with_local_json.py`, `run_3_games.py` — ferramentas que facilitam reprocessamento e debugging local.
- **`servidor.md`**: documentação do servidor (m21s). Motivo: orientação operacional para deploy e backups.

**Consolidar (Média prioridade)**
- **`tools/inspect_stats_params.py`, `tools/probe_stats_endpoints.py`, `tools/find_player_paths.py`, tools/analyze_stats_structure.py`**: grande sobreposição (inspeção/probing). Recomendação: consolidar em `tools/stats_inspector.py` com subcomandos (`probe`, `analyze`, `find_paths`, `capture`). Motivo: reduz duplicação e facilita manutenção.
- **Extratores de conteúdo**: mover lógica de `tools/extract_pdf_to_md.py` e partes de `data_collector.py` para um módulo único `extractors.py` (ou `coleta/extractors.py`). Motivo: evitar duplicidade de código de parsing/normalização.
- **`tools/db_checks.py`, `tools/check_supabase_counts.py`, `tools/cleanup_jogadores_bad.py`**: consolidar verificações e scripts de manutenção do DB local em `tools/db_maintenance.py` com subcomandos (`counts`, `cleanup`, `integrity`). Motivo: centralização da manutenção do banco.

**Remover / Arquivos a arquivar (Baixa prioridade / opcional)**
-- **Integrações de cliente de nuvem (remover do backend)**: arquivos que importam clientes externos para DB (ex.: `supabase`) e dependências relacionadas. Substituir por acesso local (SQLite) ou por APIs internas. Especificamente:
  - `coleta/supabase_fallback.py` (se existir) — já substituído pela solução SQLite.
  - Qualquer script em `tools/` que dependa exclusivamente de clientes de nuvem e não tenha contraparte local.
  - Observação: não remova código frontend que dependa de serviços externos sem validação visual — podem existir endpoints no Next.js que precisem ser adaptados para usar APIs locais.
- **Arquivos duplicados de testes manuais / debug**: se você tiver múltiplos scripts com mesma finalidade (ex.: vários `debug_*`, `check_*` que fazem a mesma query), arquivar ou consolidar. Exemplos: `tests/check_games.py`, `tools/db_checks.py` (consolide).
- **Scripts temporários e experimentos**: `tools/test_requests_user.py`, `tert_host_resolution.py`, `test_host_resolution.py` — mover para `archive/` ou remover se já há implementação estável em `coleta/banco_dados.py`.

**Por que essas escolhas?**
- Minimizar duplicidade reduz dívidas técnicas e o risco de divergência entre utilitários.
- Manter a versão mais completa e testada (coleta + processador + schema) garante que o bot funcione de forma autônoma no servidor.
- Consolidar ferramentas facilita suporte e debugging remoto (menos arquivos para gerenciar via SSH/Termux).

**Passo a passo recomendado para aplicar a limpeza (seguro/idempotente)**
1. Criar branch: `git checkout -b maintenance/sqlite-cleanup`
2. Mover arquivos que serão arquivados para `archive/` (mantém histórico):
   - `mkdir archive && git mv tools/test_requests_user.py archive/` etc.
3. Consolidar scripts: criar `tools/stats_inspector.py` e migrar funcionalidades de outros scripts para subcomandos.
4. Testar localmente: executar `python tools/init_sqlite_db.py` e `python run_coleta.py` em ambiente virtual.
5. Commit + push: `git add -A && git commit -m "chore: consolidate tools & migrate to sqlite-centric workflow" && git push origin maintenance/sqlite-cleanup`
6. Revisar no servidor: `ssh m21s && cd TisperVirtual && git pull origin maintenance/sqlite-cleanup && pip install -r requirements.txt && python tools/init_sqlite_db.py && pm2 restart tradecoletor`

**Check-list rápido (resumido)**
- Manter: `schema.sql`, `tools/init_sqlite_db.py`, `coleta/*` (core), `run_coleta.py`, `tools/smart_web_printer.py`, `servidor.md`.
- Consolidar: `tools/inspect_stats_*` → `tools/stats_inspector.py`; extratores → `coleta/extractors.py`.
- Arquivar/remover: scripts experimentais, clientes Supabase obsoletos, duplicatas de debug.

Se quiser, eu
- implemento a consolidação inicial (criar `tools/stats_inspector.py` importando as funções existentes),
- ou aplico a mudança ao `coleta/banco_dados.py` para garantir fallback de `RETURNING` → `lastrowid` se necessário.

Escolha qual ação prefere que eu execute agora (Consolidar, Arquivar, Implementar fallback `RETURNING`), e eu começo a aplicar as mudanças e commito um branch com o trabalho.