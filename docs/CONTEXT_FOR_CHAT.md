# Contexto do Coletor 365scores (para colar em novo chat)

Use este arquivo como contexto rápido ao abrir um novo chat/assistente no VSCode. Contém a arquitetura, o estado atual, comandos úteis e próximos passos.

**Resumo objetivo**
- Coletor para 365scores focado no Brasileirão Série A.
- Duas fases: (1) descoberta de jogos (`run_collect_games`) e (2) coleta profunda de detalhes por jogo (`run_collect_details` / `fetch_and_save_game_details`).
- Persistência em Supabase/PostgREST; captura de payloads brutos em `raw_game_data`.

**Arquivos principais**
- `coleta/api_coleta_365scores.py` — coletor principal (fetch, parsing, normalização, upserts).
- `tools/reprocess_with_local_json.py` — reprocessa um `gameId` usando JSON local (útil quando rede falha).
- `tools/playwright_find_games_and_capture.py` — script Playwright para capturar XHRs e salvar JSONs.
- `tools/playwright_captures/` — diretório com captures (ex.: `stats_direct_365531214467481.json`).
- `tools/cleanup_jogadores_bad.py` — backup + deleção de registros errados da tabela `jogadores`.
- `tools/query_jogadores_recent.py` — lista últimas linhas de `jogadores`.

**Tabelas DB importantes (Supabase/Postgres)**
- `jogos` — lista de jogos descobertos
- `times` — times/competidores
- `jogadores` — atletas
- `estatisticas_time` — estatísticas agregadas por time
- `estatisticas_jogador` — estatísticas por jogador (normalizadas)
- `escalacoes` — lineups
- `eventos_jogo` — eventos do jogo
- `raw_game_data` — payloads brutos (debug)
- `jogos_processados` — status de processamento (PROCESSED, NO_EVENTS, etc.)

**Fluxo de coleta (atual)**
1. `run_collect_games()` varre os times da Série A e salva jogos em `jogos`.
2. `run_collect_details()` processa jogos não marcados como processados:
   - tenta `/web/game/?gameId=...` (payload rico);
   - tenta `/web/game/stats/?games=...` com variantes de params (`includePlayers`, `includePlayerStats`, etc.);
   - tenta endpoints alternativos (`/web/game/lineups`, `/web/game/playersStats`, `/web/game/players`);
   - usa Playwright fallback (`fetch_game_via_playwright`) para capturar XHRs se necessário.
3. Parse/normalização:
   - extrai `teams`, `players`, `team_stats`, `player_stats`, `lineups` e `events` (incl. `chartEvents.events`);
   - normaliza formatos variados (dict/list, valores string/num);
4. Persistência:
   - salva JSON bruto em `raw_game_data`;
   - usa `safe_upsert()` com deduplicação e fallback por linha (`.match()`);
   - filtra eventos sem `api_id` antes de inserir;
   - grava status em `jogos_processados`.

**Heurísticas e proteções implementadas**
- `has_player_data(stats_obj)` — busca recursiva por estruturas com players.
- `_find_lists` endurecido e validação "player-like": só considera listas candidatas se os itens tiverem chaves indicativas (`athleteId`, `playerId`, `jerseyNumber`, `position`, `shortName`).
- `safe_upsert()`:
  - deduplica linhas quando `on_conflict` é informado;
  - usa `.match()` no fallback por linha para compatibilidade com o cliente Supabase;
- `table_has_column()` para omitir campos não suportados pelo PostgREST (ex.: `detail`).
- Normalização de eventos aceita `id` ou `key` e converte string-num para int.

**Estado atual (o que foi feito nesta sessão)**
- Implementado fallback Playwright e captura de JSONs (em `tools/playwright_captures`).
- Corrigido `safe_upsert` (dedupe + `.match()`).
- Endurecida heurística de detecção de jogadores para reduzir inserções incorretas.
- Realizados reprocessamentos locais usando `tools/playwright_captures/stats_direct_365531214467481.json`.
- Feito cleanup de registros incorretos em `jogadores` (backup + delete) — operação manual realizada pelo usuário.
- Último reprocessamento após cleanup inseriu apenas um registro indesejado: `api_id=144` (Athletic Bilbao) — recomendado endurecer validação adicional.

**Problema atual**
- O coletor às vezes confunde listas de definições de estatísticas (ou competidores) com jogadores, inserindo `id`+`name` incorretos em `jogadores`.
- Já foram aplicadas heurísticas, mas há casos-limite (ex.: competidor com só `id`+`name`).

**Recomendações imediatas (curto prazo)**
1. Exigir explicitamente `athleteId`/`playerId` ou ao menos `jerseyNumber`/`shortName`/`positionName` para inserir em `jogadores`.
2. Criar um modo `--dry-run` que apenas parseie e mostre o que seria inserido (sem gravar) para validar antes do upsert.
3. Adicionar testes unitários com fixtures dos JSONs capturados (evita regressões ao ajustar heurísticas).

**Comandos úteis (PowerShell)**
- Ativar venv:
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
- Reprocessar jogo com JSON local:
  ```powershell
  .\.venv\Scripts\python.exe .\tools\reprocess_with_local_json.py --game 4467481 --json tools/playwright_captures/stats_direct_365531214467481.json
  ```
- Consultar últimas linhas da tabela `jogadores`:
  ```powershell
  .\.venv\Scripts\python.exe .\tools\query_jogadores_recent.py
  ```
- Backup + delete (script criado):
  ```powershell
  .\.venv\Scripts\python.exe .\tools\cleanup_jogadores_bad.py
  ```
- Capturar via Playwright (exemplo):
  ```powershell
  .\.venv\Scripts\python.exe .\tools\playwright_find_games_and_capture.py --game 4467481
  ```

**O que colar no novo chat (bloco curto e pronto)**
```
Repo: c:\TradeComigo
Entry: coleta/api_coleta_365scores.py
Scripts: tools/reprocess_with_local_json.py, tools/playwright_find_games_and_capture.py, tools/cleanup_jogadores_bad.py
Captures: tools/playwright_captures/stats_direct_365531214467481.json
DB: Supabase (SUPABASE_URL/KEY set em coleta/api_coleta_365scores.py)
Estado atual: fallback Playwright implementado; safe_upsert atualizado (dedupe + match); heurística players hardened.
Último teste: reprocess gameId=4467481 com JSON local; após cleanup o único registro novo em `jogadores` foi api_id=144 (Athletic Bilbao).
Problema atual: evitar que métricas/competidores (id+name) sejam inseridos em `jogadores`.
Comandos úteis:
  .\\.venv\\Scripts\\python.exe .\\tools\\reprocess_with_local_json.py --game 4467481
  .\\.venv\\Scripts\\python.exe .\\tools\\query_jogadores_recent.py
```

**Próximos passos sugeridos (médio prazo)**
- Implementar `--dry-run` e testes automatizados com fixtures.
- Padronizar mapeamento de `team_api_id` e IDs de eventos.
- Monitorar taxa de jogos com `NO_EVENTS` e agregar métricas (reprocessamento automático com parâmetros diferentes).

---
Gerado automaticamente para facilitar iniciar um novo chat com contexto mínimo e reproduzível.
