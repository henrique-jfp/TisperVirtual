-- DDL para Postgres (Supabase) - Modelo completo para coleta do Brasileirão
-- Execute no SQL Editor do Supabase ou com psql; inclui IF NOT EXISTS para segurança.
-- DDL para Postgres (Supabase) - Modelo preciso e cirúrgico para coleta do Brasileirão
-- Execute no SQL Editor do Supabase ou com psql; inclui IF NOT EXISTS para segurança.

-- =======================================================
-- 1) competitions (campeonatos)
-- =======================================================
CREATE TABLE IF NOT EXISTS public.competitions (
    id bigint PRIMARY KEY,
    name text NOT NULL,
    country_id bigint,
    season_num integer,
    metadata jsonb,
    created_at timestamptz NOT NULL DEFAULT now()
);

-- =======================================================
-- 2) teams (times)
-- =======================================================
CREATE TABLE IF NOT EXISTS public.times (
    api_id bigint PRIMARY KEY,
    name text NOT NULL,
    short_name text,
    country_id bigint,
    venue jsonb,
    metadata jsonb,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX IF NOT EXISTS ux_times_name ON public.times(lower(name));

-- =======================================================
-- 3) players (jogadores)
-- =======================================================
CREATE TABLE IF NOT EXISTS public.jogadores (
    api_id bigint PRIMARY KEY,
    name text NOT NULL,
    common_name text,
    position text,
    birthdate date,
    nationality text,
    height_cm integer,
    weight_kg integer,
    current_team_api_id bigint REFERENCES public.times(api_id) ON DELETE SET NULL,
    profile jsonb,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_jogadores_team ON public.jogadores(current_team_api_id);

-- =======================================================
-- 4) jogos (partidas)
-- =======================================================
CREATE TABLE IF NOT EXISTS public.jogos (
    api_id bigint PRIMARY KEY,
    competition_id bigint REFERENCES public.competitions(id) ON DELETE SET NULL,
    season_num integer,
    stage_num integer,
    start_time timestamptz,
    status text,
    home_team_api_id bigint REFERENCES public.times(api_id) ON DELETE SET NULL,
    away_team_api_id bigint REFERENCES public.times(api_id) ON DELETE SET NULL,
    home_team_score smallint,
    away_team_score smallint,
    raw_payload jsonb,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_jogos_start_time ON public.jogos(start_time);
CREATE INDEX IF NOT EXISTS idx_jogos_competition ON public.jogos(competition_id);

-- =======================================================
-- 5) estatisticas_time (estatísticas por time por jogo)
-- =======================================================
CREATE TABLE IF NOT EXISTS public.estatisticas_time (
    id bigserial PRIMARY KEY,
    jogo_api_id bigint NOT NULL REFERENCES public.jogos(api_id) ON DELETE CASCADE,
    team_api_id bigint NOT NULL REFERENCES public.times(api_id) ON DELETE CASCADE,
    type text NOT NULL,
    value text,
    metadata jsonb,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_estatisticas_time_jogo ON public.estatisticas_time(jogo_api_id);

-- =======================================================
-- 6) estatisticas_jogador (estatísticas normalizadas por jogador)
-- =======================================================
CREATE TABLE IF NOT EXISTS public.estatisticas_jogador (
    jogo_api_id bigint NOT NULL REFERENCES public.jogos(api_id) ON DELETE CASCADE,
    player_api_id bigint NOT NULL REFERENCES public.jogadores(api_id) ON DELETE CASCADE,
    team_api_id bigint REFERENCES public.times(api_id) ON DELETE SET NULL,
    stat_name text NOT NULL,
    value text,
    metadata jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (jogo_api_id, player_api_id, stat_name)
);

CREATE INDEX IF NOT EXISTS idx_est_jogador_player ON public.estatisticas_jogador(player_api_id);
CREATE INDEX IF NOT EXISTS idx_est_jogador_jogo ON public.estatisticas_jogador(jogo_api_id);

-- =======================================================
-- 7) escalacoes (lineups)
-- =======================================================
CREATE TABLE IF NOT EXISTS public.escalacoes (
    id bigserial PRIMARY KEY,
    jogo_api_id bigint NOT NULL REFERENCES public.jogos(api_id) ON DELETE CASCADE,
    player_api_id bigint REFERENCES public.jogadores(api_id) ON DELETE SET NULL,
    team_api_id bigint REFERENCES public.times(api_id) ON DELETE SET NULL,
    is_starter boolean DEFAULT false,
    position text,
    shirt_number integer,
    metadata jsonb,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_escalacoes_jogo ON public.escalacoes(jogo_api_id);

-- =======================================================
-- 8) eventos_jogo (gols, cartões, substituições, etc.)
-- =======================================================
CREATE TABLE IF NOT EXISTS public.eventos_jogo (
    api_id bigint PRIMARY KEY,
    jogo_api_id bigint NOT NULL REFERENCES public.jogos(api_id) ON DELETE CASCADE,
    type text NOT NULL,
    minute smallint,
    player_api_id bigint REFERENCES public.jogadores(api_id) ON DELETE SET NULL,
    team_api_id bigint REFERENCES public.times(api_id) ON DELETE SET NULL,
    detail jsonb,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_eventos_jogo_jogo ON public.eventos_jogo(jogo_api_id);
CREATE INDEX IF NOT EXISTS idx_eventos_jogo_player ON public.eventos_jogo(player_api_id);

-- =======================================================
-- 9) raw_game_data (JSON bruto salvo para recuperação)
-- =======================================================
CREATE TABLE IF NOT EXISTS public.raw_game_data (
    jogo_api_id bigint PRIMARY KEY REFERENCES public.jogos(api_id) ON DELETE CASCADE,
    details_json jsonb,
    stats_json jsonb,
    fetched_at timestamptz NOT NULL DEFAULT now()
);

-- =======================================================
-- 10) jogos_processados (controle de processamento / resumability)
-- =======================================================
CREATE TABLE IF NOT EXISTS public.jogos_processados (
    jogo_api_id bigint PRIMARY KEY REFERENCES public.jogos(api_id) ON DELETE CASCADE,
    status text NOT NULL,
    details text,
    processed_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_jogos_processados_status ON public.jogos_processados(status);

-- =======================================================
-- 11) atletas_detalhes (cache do endpoint /web/athletes)
-- =======================================================
CREATE TABLE IF NOT EXISTS public.atletas_detalhes (
    athlete_api_id bigint PRIMARY KEY,
    details_json jsonb,
    fetched_at timestamptz NOT NULL DEFAULT now()
);

-- =======================================================
-- 12) bookmakers e odds_snapshot (opcional, para odds/historico)
-- =======================================================
CREATE TABLE IF NOT EXISTS public.bookmakers (
    id bigint PRIMARY KEY,
    name text,
    metadata jsonb
);

CREATE TABLE IF NOT EXISTS public.odds_snapshot (
    id bigserial PRIMARY KEY,
    jogo_api_id bigint REFERENCES public.jogos(api_id) ON DELETE CASCADE,
    bookmaker_id bigint REFERENCES public.bookmakers(id) ON DELETE SET NULL,
    market jsonb,
    fetched_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_odds_jogo ON public.odds_snapshot(jogo_api_id);

-- =======================================================
-- 13) times_snapshot (opcional)
-- =======================================================
CREATE TABLE IF NOT EXISTS public.times_snapshot (
    id bigserial PRIMARY KEY,
    api_id bigint,
    snapshot jsonb,
    captured_at timestamptz NOT NULL DEFAULT now()
);

-- =======================================================
-- 14) jobs_log (logs leves de execução)
-- =======================================================
CREATE TABLE IF NOT EXISTS public.jobs_log (
    id bigserial PRIMARY KEY,
    job_name text NOT NULL,
    payload jsonb,
    status text,
    message text,
    created_at timestamptz NOT NULL DEFAULT now()
);

-- =======================================================
-- Permissões sugeridas (ajuste conforme política do projeto)
-- =======================================================
-- GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO anon;

-- =======================================================
-- Observações / recomendações
-- 1) Após aplicar estas tabelas, verifique roles e políticas de Row Level Security no Supabase.
-- 2) Se quiser que eu aplique o DDL agora, confirme explicitamente (eu usarei a chave presente no repo).
-- 3) Podemos aplicar etapas incrementais (DDL mínimo primeiro) para reduzir risco; diga se prefere incremental.

