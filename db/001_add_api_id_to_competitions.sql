ALTER TABLE public.competitions ADD COLUMN api_id BIGINT UNIQUE;
COMMENT ON COLUMN public.competitions.api_id IS 'ID da competição na API de origem (ex: 365scores)';