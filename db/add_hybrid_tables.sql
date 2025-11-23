-- DDL para adicionar tabelas e colunas faltantes para o módulo híbrido
-- Execute no SQL Editor do Supabase

-- =======================================================
-- Adicionar colunas para estatísticas da temporada em jogadores
-- =======================================================
ALTER TABLE public.jogadores
ADD COLUMN IF NOT EXISTS season_goals integer DEFAULT 0,
ADD COLUMN IF NOT EXISTS season_assists integer DEFAULT 0;

-- =======================================================
-- Tabela para classificação (standings)
-- =======================================================
CREATE TABLE IF NOT EXISTS public.classificacao (
    id bigserial PRIMARY KEY,
    season integer NOT NULL,
    position integer NOT NULL,
    team_name text NOT NULL,
    points integer DEFAULT 0,
    played_games integer DEFAULT 0,
    won integer DEFAULT 0,
    draw integer DEFAULT 0,
    lost integer DEFAULT 0,
    goals_for integer DEFAULT 0,
    goals_against integer DEFAULT 0,
    goal_difference integer DEFAULT 0,
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE(season, position)
);

-- Índice para consultas por temporada
CREATE INDEX IF NOT EXISTS idx_classificacao_season ON public.classificacao(season);

-- =======================================================
-- Adicionar raw_payload à tabela jogos (se não existir)
-- =======================================================
ALTER TABLE public.jogos
ADD COLUMN IF NOT EXISTS raw_payload jsonb;