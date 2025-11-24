-- =====================================================
-- SCHEMA COMPLETO DE DATABASE PARA BOT DE FUTEBOL
-- Versão: 1.0
-- SGBD: SQLite
-- Autor: Sistema TradeComigo
-- =====================================================

-- Habilita foreign keys no SQLite
PRAGMA foreign_keys = ON;

-- =====================================================
-- TABELAS CORE: Entidades Básicas
-- =====================================================

-- Competições/Campeonatos
CREATE TABLE IF NOT EXISTS competicoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    api_id INTEGER UNIQUE,
    nome TEXT NOT NULL,
    nome_curto TEXT,
    pais TEXT DEFAULT 'Brasil',
    tipo TEXT, -- 'liga', 'copa', 'torneio'
    nivel INTEGER, -- 1=Série A, 2=Série B, etc
    temporada_atual TEXT,
    logo_url TEXT,
    ativa BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Times
CREATE TABLE IF NOT EXISTS times (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    api_id INTEGER UNIQUE,
    nome TEXT NOT NULL,
    nome_curto TEXT,
    sigla TEXT,
    apelido TEXT, -- "Mengão", "Verdão", etc
    fundacao_ano INTEGER,
    estadio_id INTEGER,
    cidade TEXT,
    estado TEXT,
    pais TEXT DEFAULT 'Brasil',
    logo_url TEXT,
    cores_primarias TEXT, -- JSON: ["#FF0000", "#000000"]
    ativo BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (estadio_id) REFERENCES estadios(id)
);

-- Estádios
CREATE TABLE IF NOT EXISTS estadios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    api_id INTEGER UNIQUE,
    nome TEXT NOT NULL,
    cidade TEXT,
    estado TEXT,
    capacidade INTEGER,
    superficie TEXT, -- 'grama natural', 'sintética'
    inauguracao_ano INTEGER,
    latitude REAL,
    longitude REAL,
    imagem_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Jogadores
CREATE TABLE IF NOT EXISTS jogadores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    api_id INTEGER UNIQUE,
    nome_completo TEXT NOT NULL,
    nome_exibicao TEXT,
    data_nascimento DATE,
    idade INTEGER,
    nacionalidade TEXT DEFAULT 'Brasil',
    altura_cm INTEGER,
    peso_kg INTEGER,
    pe_preferido TEXT, -- 'direito', 'esquerdo', 'ambos'
    posicao_principal TEXT, -- 'goleiro', 'zagueiro', 'lateral', 'meia', 'atacante'
    posicoes_secundarias TEXT, -- JSON array
    foto_url TEXT,
    ativo BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Árbitros
CREATE TABLE IF NOT EXISTS arbitros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    api_id INTEGER UNIQUE,
    nome_completo TEXT NOT NULL,
    data_nascimento DATE,
    nacionalidade TEXT DEFAULT 'Brasil',
    tipo TEXT, -- 'campo', 'assistente', 'var'
    categoria TEXT, -- 'fifa', 'cbf', 'estadual'
    foto_url TEXT,
    ativo BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Técnicos/Treinadores
CREATE TABLE IF NOT EXISTS tecnicos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    api_id INTEGER UNIQUE,
    nome_completo TEXT NOT NULL,
    data_nascimento DATE,
    nacionalidade TEXT DEFAULT 'Brasil',
    foto_url TEXT,
    ativo BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- TABELAS DE RELACIONAMENTO: Times e Jogadores
-- =====================================================

-- Contratos de Jogadores
CREATE TABLE IF NOT EXISTS contratos_jogadores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    jogador_id INTEGER NOT NULL,
    time_id INTEGER NOT NULL,
    data_inicio DATE NOT NULL,
    data_fim DATE,
    numero_camisa INTEGER,
    tipo_contrato TEXT, -- 'definitivo', 'empréstimo', 'temporário'
    valor_mercado REAL,
    salario_mensal REAL,
    ativo BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (jogador_id) REFERENCES jogadores(id) ON DELETE CASCADE,
    FOREIGN KEY (time_id) REFERENCES times(id) ON DELETE CASCADE
);

-- Técnicos nos Times
CREATE TABLE IF NOT EXISTS contratos_tecnicos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tecnico_id INTEGER NOT NULL,
    time_id INTEGER NOT NULL,
    data_inicio DATE NOT NULL,
    data_fim DATE,
    tipo TEXT DEFAULT 'titular', -- 'titular', 'interino', 'auxiliar'
    ativo BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tecnico_id) REFERENCES tecnicos(id) ON DELETE CASCADE,
    FOREIGN KEY (time_id) REFERENCES times(id) ON DELETE CASCADE
);

-- =====================================================
-- TABELAS DE JOGOS E PARTIDAS
-- =====================================================

-- Jogos/Partidas
CREATE TABLE IF NOT EXISTS jogos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    api_id INTEGER UNIQUE,
    competicao_id INTEGER NOT NULL,
    temporada TEXT NOT NULL,
    rodada INTEGER,
    fase TEXT, -- 'fase de grupos', 'oitavas', 'quartas', 'semi', 'final'
    
    -- Times
    time_casa_id INTEGER NOT NULL,
    time_fora_id INTEGER NOT NULL,
    
    -- Data e Local
    data_hora TIMESTAMP NOT NULL,
    estadio_id INTEGER,
    arbitro_principal_id INTEGER,
    publico_pagante INTEGER,
    publico_total INTEGER,
    
    -- Placar
    gols_casa INTEGER,
    gols_fora INTEGER,
    gols_casa_ht INTEGER, -- half-time
    gols_fora_ht INTEGER,
    
    -- Status
    status TEXT, -- 'agendado', 'ao_vivo', 'intervalo', 'finalizado', 'adiado', 'cancelado'
    minuto_atual INTEGER,
    tempo_adicional INTEGER,
    
    -- Extras
    teve_prorrogacao BOOLEAN DEFAULT 0,
    teve_penaltis BOOLEAN DEFAULT 0,
    gols_casa_penaltis INTEGER,
    gols_fora_penaltis INTEGER,
    
    -- Metadata
    tempo_jogo TEXT, -- '1T', '2T', 'Prorrogação', 'Pênaltis'
    clima TEXT, -- JSON: {"temp": 28, "condicao": "ensolarado"}
    odds_casa REAL,
    odds_empate REAL,
    odds_fora REAL,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (competicao_id) REFERENCES competicoes(id),
    FOREIGN KEY (time_casa_id) REFERENCES times(id),
    FOREIGN KEY (time_fora_id) REFERENCES times(id),
    FOREIGN KEY (estadio_id) REFERENCES estadios(id),
    FOREIGN KEY (arbitro_principal_id) REFERENCES arbitros(id)
);

-- Escalações
CREATE TABLE IF NOT EXISTS escalacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    jogo_id INTEGER NOT NULL,
    time_id INTEGER NOT NULL,
    jogador_id INTEGER NOT NULL,
    titular BOOLEAN DEFAULT 1,
    posicao TEXT,
    numero_camisa INTEGER,
    capitao BOOLEAN DEFAULT 0,
    
    -- Tempos de jogo
    minuto_entrada INTEGER DEFAULT 0,
    minuto_saida INTEGER,
    substituido BOOLEAN DEFAULT 0,
    substituiu_jogador_id INTEGER,
    
    -- Avaliação
    nota REAL, -- 0.0 a 10.0
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (jogo_id) REFERENCES jogos(id) ON DELETE CASCADE,
    FOREIGN KEY (time_id) REFERENCES times(id),
    FOREIGN KEY (jogador_id) REFERENCES jogadores(id),
    FOREIGN KEY (substituiu_jogador_id) REFERENCES jogadores(id)
);

-- Eventos do Jogo (Gols, Cartões, Substituições)
CREATE TABLE IF NOT EXISTS eventos_jogo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    api_id INTEGER UNIQUE,
    jogo_id INTEGER NOT NULL,
    time_id INTEGER NOT NULL,
    
    -- Tipo e Timing
    tipo TEXT NOT NULL, -- 'gol', 'cartao_amarelo', 'cartao_vermelho', 'substituicao', 'penalti_perdido', 'var'
    minuto INTEGER NOT NULL,
    minuto_adicional INTEGER DEFAULT 0,
    periodo TEXT, -- '1T', '2T', 'Prorrogação'
    
    -- Jogadores envolvidos
    jogador_principal_id INTEGER,
    jogador_secundario_id INTEGER, -- assistência ou jogador substituído
    
    -- Detalhes específicos
    detalhes TEXT, -- JSON com info extra: tipo de gol, razão do cartão, etc
    video_url TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (jogo_id) REFERENCES jogos(id) ON DELETE CASCADE,
    FOREIGN KEY (time_id) REFERENCES times(id),
    FOREIGN KEY (jogador_principal_id) REFERENCES jogadores(id),
    FOREIGN KEY (jogador_secundario_id) REFERENCES jogadores(id)
);

-- =====================================================
-- ESTATÍSTICAS: Jogos, Jogadores e Times
-- =====================================================

-- Estatísticas por Jogo (Agregadas por Time)
CREATE TABLE IF NOT EXISTS estatisticas_jogo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    jogo_id INTEGER NOT NULL,
    time_id INTEGER NOT NULL,
    
    -- Posse e Passes
    posse_bola_pct REAL,
    total_passes INTEGER,
    passes_certos INTEGER,
    passes_errados INTEGER,
    precisao_passes_pct REAL,
    
    -- Finalizações
    chutes_total INTEGER,
    chutes_no_gol INTEGER,
    chutes_fora INTEGER,
    chutes_bloqueados INTEGER,
    finalizacoes_perigosas INTEGER,
    
    -- Defesa
    defesas_goleiro INTEGER,
    tackles INTEGER,
    interceptacoes INTEGER,
    cortes INTEGER,
    
    -- Ataque
    escanteios INTEGER,
    impedimentos INTEGER,
    cruzamentos INTEGER,
    grandes_chances INTEGER,
    
    -- Disciplina
    faltas_cometidas INTEGER,
    faltas_sofridas INTEGER,
    cartoes_amarelos INTEGER,
    cartoes_vermelhos INTEGER,
    
    -- Outros
    time_posse_segundos INTEGER,
    distancia_percorrida_km REAL,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (jogo_id) REFERENCES jogos(id) ON DELETE CASCADE,
    FOREIGN KEY (time_id) REFERENCES times(id),
    UNIQUE(jogo_id, time_id)
);

-- Estatísticas por Jogador em Cada Jogo
CREATE TABLE IF NOT EXISTS estatisticas_jogador_jogo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    jogo_id INTEGER NOT NULL,
    jogador_id INTEGER NOT NULL,
    time_id INTEGER NOT NULL,
    
    -- Tempo
    minutos_jogados INTEGER DEFAULT 0,
    
    -- Ataque
    gols INTEGER DEFAULT 0,
    assistencias INTEGER DEFAULT 0,
    chutes INTEGER DEFAULT 0,
    chutes_no_gol INTEGER DEFAULT 0,
    grandes_chances_criadas INTEGER DEFAULT 0,
    grandes_chances_perdidas INTEGER DEFAULT 0,
    dribles_tentados INTEGER DEFAULT 0,
    dribles_bem_sucedidos INTEGER DEFAULT 0,
    
    -- Passe
    passes_certos INTEGER DEFAULT 0,
    passes_errados INTEGER DEFAULT 0,
    passes_chave INTEGER DEFAULT 0,
    cruzamentos INTEGER DEFAULT 0,
    
    -- Defesa
    tackles INTEGER DEFAULT 0,
    interceptacoes INTEGER DEFAULT 0,
    cortes INTEGER DEFAULT 0,
    defesas INTEGER DEFAULT 0, -- para goleiros
    
    -- Disciplina
    faltas_cometidas INTEGER DEFAULT 0,
    faltas_sofridas INTEGER DEFAULT 0,
    cartao_amarelo BOOLEAN DEFAULT 0,
    cartao_vermelho BOOLEAN DEFAULT 0,
    
    -- Avaliação
    nota REAL,
    melhor_em_campo BOOLEAN DEFAULT 0,
    
    -- Distância
    distancia_percorrida_km REAL,
    sprints INTEGER,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (jogo_id) REFERENCES jogos(id) ON DELETE CASCADE,
    FOREIGN KEY (jogador_id) REFERENCES jogadores(id),
    FOREIGN KEY (time_id) REFERENCES times(id),
    UNIQUE(jogo_id, jogador_id)
);

-- Estatísticas de Árbitros
CREATE TABLE IF NOT EXISTS estatisticas_arbitro (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    arbitro_id INTEGER NOT NULL,
    jogo_id INTEGER NOT NULL,
    
    -- Cartões
    cartoes_amarelos_dados INTEGER DEFAULT 0,
    cartoes_vermelhos_dados INTEGER DEFAULT 0,
    
    -- Penaltis e VAR
    penaltis_marcados INTEGER DEFAULT 0,
    revisoes_var INTEGER DEFAULT 0,
    decisoes_var_revertidas INTEGER DEFAULT 0,
    
    -- Faltas
    faltas_marcadas INTEGER DEFAULT 0,
    impedimentos_marcados INTEGER DEFAULT 0,
    
    -- Avaliação
    nota_desempenho REAL,
    controversias INTEGER DEFAULT 0, -- número de decisões polêmicas
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (arbitro_id) REFERENCES arbitros(id),
    FOREIGN KEY (jogo_id) REFERENCES jogos(id) ON DELETE CASCADE,
    UNIQUE(arbitro_id, jogo_id)
);

-- =====================================================
-- CLASSIFICAÇÃO E RANKING
-- =====================================================

-- Classificação por Competição e Temporada
CREATE TABLE IF NOT EXISTS classificacao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    competicao_id INTEGER NOT NULL,
    temporada TEXT NOT NULL,
    time_id INTEGER NOT NULL,
    
    -- Posição
    posicao INTEGER NOT NULL,
    posicao_anterior INTEGER,
    
    -- Jogos
    jogos INTEGER DEFAULT 0,
    vitorias INTEGER DEFAULT 0,
    empates INTEGER DEFAULT 0,
    derrotas INTEGER DEFAULT 0,
    
    -- Gols
    gols_pro INTEGER DEFAULT 0,
    gols_contra INTEGER DEFAULT 0,
    saldo_gols INTEGER DEFAULT 0,
    
    -- Pontos e Aproveitamento
    pontos INTEGER DEFAULT 0,
    aproveitamento_pct REAL DEFAULT 0.0,
    
    -- Sequências
    ultimos_5_jogos TEXT, -- Ex: "VEVDV"
    jogos_sem_vencer INTEGER DEFAULT 0,
    jogos_sem_perder INTEGER DEFAULT 0,
    
    -- Mandante/Visitante
    vitorias_casa INTEGER DEFAULT 0,
    vitorias_fora INTEGER DEFAULT 0,
    
    -- Metadata
    zona TEXT, -- 'libertadores', 'sulamericana', 'rebaixamento'
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (competicao_id) REFERENCES competicoes(id),
    FOREIGN KEY (time_id) REFERENCES times(id),
    UNIQUE(competicao_id, temporada, time_id)
);

-- =====================================================
-- LESÕES E SAÚDE DOS JOGADORES
-- =====================================================

-- Histórico de Lesões
CREATE TABLE IF NOT EXISTS lesoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    jogador_id INTEGER NOT NULL,
    time_id INTEGER,
    
    -- Tipo e Gravidade
    tipo_lesao TEXT NOT NULL, -- 'muscular', 'ligamentar', 'óssea', 'traumática'
    area_afetada TEXT NOT NULL, -- 'coxa', 'tornozelo', 'joelho', etc
    gravidade TEXT, -- 'leve', 'moderada', 'grave'
    
    -- Datas
    data_lesao DATE NOT NULL,
    data_prevista_retorno DATE,
    data_retorno_efetivo DATE,
    dias_afastado INTEGER,
    
    -- Contexto
    ocorreu_em_jogo BOOLEAN DEFAULT 0,
    jogo_id INTEGER,
    minuto_lesao INTEGER,
    
    -- Status
    status TEXT DEFAULT 'ativo', -- 'ativo', 'recuperacao', 'recuperado'
    
    -- Detalhes
    diagnostico_completo TEXT,
    tratamento TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (jogador_id) REFERENCES jogadores(id) ON DELETE CASCADE,
    FOREIGN KEY (time_id) REFERENCES times(id),
    FOREIGN KEY (jogo_id) REFERENCES jogos(id)
);

-- =====================================================
-- NOTÍCIAS E CONTEÚDO
-- =====================================================

-- Notícias
CREATE TABLE IF NOT EXISTS noticias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Conteúdo
    titulo TEXT NOT NULL,
    subtitulo TEXT,
    conteudo TEXT,
    resumo TEXT,
    
    -- Categorização
    categoria TEXT, -- 'transferência', 'lesão', 'resultado', 'bastidores', 'entrevista'
    tags TEXT, -- JSON array: ["mercado", "série-a"]
    
    -- Entidades relacionadas
    times_relacionados TEXT, -- JSON array de IDs
    jogadores_relacionados TEXT, -- JSON array de IDs
    competicao_id INTEGER,
    jogo_id INTEGER,
    
    -- Fonte
    fonte TEXT,
    autor TEXT,
    url_original TEXT UNIQUE,
    imagem_destaque_url TEXT,
    
    -- Datas
    data_publicacao TIMESTAMP,
    data_atualizacao TIMESTAMP,
    
    -- Metadata
    visualizacoes INTEGER DEFAULT 0,
    relevancia_score REAL, -- 0.0 a 1.0
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (competicao_id) REFERENCES competicoes(id),
    FOREIGN KEY (jogo_id) REFERENCES jogos(id)
);

-- =====================================================
-- TRANSFERÊNCIAS E MERCADO
-- =====================================================

-- Transferências
CREATE TABLE IF NOT EXISTS transferencias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    jogador_id INTEGER NOT NULL,
    
    -- Times
    time_origem_id INTEGER,
    time_destino_id INTEGER NOT NULL,
    
    -- Tipo
    tipo TEXT NOT NULL, -- 'compra', 'empréstimo', 'livre', 'troca'
    
    -- Valores
    valor_transferencia REAL,
    moeda TEXT DEFAULT 'BRL',
    salario_anual REAL,
    
    -- Datas
    data_anuncio DATE NOT NULL,
    data_oficializacao DATE,
    duracao_contrato_anos INTEGER,
    
    -- Status
    status TEXT DEFAULT 'concluída', -- 'rumor', 'negociando', 'concluída', 'cancelada'
    
    -- Extras
    tem_opcao_compra BOOLEAN DEFAULT 0,
    valor_opcao_compra REAL,
    percentual_direitos REAL, -- % dos direitos econômicos
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (jogador_id) REFERENCES jogadores(id) ON DELETE CASCADE,
    FOREIGN KEY (time_origem_id) REFERENCES times(id),
    FOREIGN KEY (time_destino_id) REFERENCES times(id)
);

-- =====================================================
-- ANÁLISES E PREDIÇÕES (Para o Bot)
-- =====================================================

-- Análises de Jogos (Pré-jogo)
CREATE TABLE IF NOT EXISTS analises_jogos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    jogo_id INTEGER NOT NULL,
    
    -- Predições
    probabilidade_vitoria_casa REAL,
    probabilidade_empate REAL,
    probabilidade_vitoria_fora REAL,
    
    -- Over/Under
    probabilidade_over_25 REAL,
    probabilidade_btts REAL, -- both teams to score
    
    -- Contexto
    forma_casa TEXT, -- últimos 5: "VEVDV"
    forma_fora TEXT,
    confrontos_diretos_resumo TEXT, -- JSON
    
    -- Fatores
    importancia_jogo TEXT, -- 'decisivo', 'normal', 'protocolar'
    motivacao_casa INTEGER, -- 1-10
    motivacao_fora INTEGER,
    
    -- Metadata
    confianca_predicao REAL, -- 0.0 a 1.0
    modelo_usado TEXT, -- 'xgboost', 'random_forest', 'neural_net'
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (jogo_id) REFERENCES jogos(id) ON DELETE CASCADE,
    UNIQUE(jogo_id)
);

-- Dicas de Apostas (Geradas pelo Bot)
CREATE TABLE IF NOT EXISTS dicas_apostas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    jogo_id INTEGER NOT NULL,
    
    -- Tipo de aposta
    mercado TEXT NOT NULL, -- 'resultado', 'over_under', 'btts', 'handicap'
    aposta_sugerida TEXT NOT NULL, -- '1', 'X', '2', 'Over 2.5', etc
    
    -- Odds
    odd_sugerida REAL,
    odd_encontrada REAL,
    bookmaker TEXT,
    
    -- Confiança
    confianca TEXT, -- 'baixa', 'média', 'alta'
    stake_sugerido TEXT, -- '1u', '2u', '3u'
    
    -- Justificativa
    justificativa TEXT,
    fatores_chave TEXT, -- JSON array
    
    -- Resultado
    resultado_aposta TEXT, -- 'green', 'red', 'push', 'pendente'
    roi REAL,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (jogo_id) REFERENCES jogos(id) ON DELETE CASCADE
);

-- =====================================================
-- CACHE E RAW DATA
-- =====================================================

-- Cache de API (Para evitar requests duplicados)
CREATE TABLE IF NOT EXISTS cache_api (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    endpoint TEXT NOT NULL,
    params TEXT, -- JSON de parâmetros
    response_data TEXT, -- JSON da resposta
    cache_key TEXT UNIQUE NOT NULL, -- hash de endpoint+params
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Raw Data (Backup dos JSONs originais)
CREATE TABLE IF NOT EXISTS raw_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_type TEXT NOT NULL, -- 'jogo', 'jogador', 'time'
    entity_id INTEGER NOT NULL,
    api_source TEXT, -- '365scores', 'api-football'
    raw_json TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- ÍNDICES PARA PERFORMANCE
-- =====================================================

-- Índices em jogos
CREATE INDEX IF NOT EXISTS idx_jogos_data ON jogos(data_hora);
CREATE INDEX IF NOT EXISTS idx_jogos_competicao ON jogos(competicao_id, temporada);
CREATE INDEX IF NOT EXISTS idx_jogos_times ON jogos(time_casa_id, time_fora_id);
CREATE INDEX IF NOT EXISTS idx_jogos_status ON jogos(status);

-- Índices em eventos
CREATE INDEX IF NOT EXISTS idx_eventos_jogo ON eventos_jogo(jogo_id);
CREATE INDEX IF NOT EXISTS idx_eventos_tipo ON eventos_jogo(tipo);
CREATE INDEX IF NOT EXISTS idx_eventos_jogador ON eventos_jogo(jogador_principal_id);

-- Índices em estatísticas
CREATE INDEX IF NOT EXISTS idx_stats_jogo ON estatisticas_jogo(jogo_id);
CREATE INDEX IF NOT EXISTS idx_stats_jogador_jogo ON estatisticas_jogador_jogo(jogo_id, jogador_id);

-- Índices em escalações
CREATE INDEX IF NOT EXISTS idx_escalacoes_jogo ON escalacoes(jogo_id);
CREATE INDEX IF NOT EXISTS idx_escalacoes_jogador ON escalacoes(jogador_id);

-- Índices em classificação
CREATE INDEX IF NOT EXISTS idx_classificacao_comp ON classificacao(competicao_id, temporada);
CREATE INDEX IF NOT EXISTS idx_classificacao_posicao ON classificacao(posicao);

-- Índices em lesões
CREATE INDEX IF NOT EXISTS idx_lesoes_jogador ON lesoes(jogador_id);
CREATE INDEX IF NOT EXISTS idx_lesoes_status ON lesoes(status);

-- Índices em notícias
CREATE INDEX IF NOT EXISTS idx_noticias_data ON noticias(data_publicacao);
CREATE INDEX IF NOT EXISTS idx_noticias_categoria ON noticias(categoria);

-- Índices em cache
CREATE INDEX IF NOT EXISTS idx_cache_key ON cache_api(cache_key);
CREATE INDEX IF NOT EXISTS idx_cache_expires ON cache_api(expires_at);

-- =====================================================
-- TRIGGERS PARA ATUALIZAÇÃO AUTOMÁTICA
-- =====================================================

-- Trigger para atualizar updated_at
CREATE TRIGGER IF NOT EXISTS update_times_timestamp 
AFTER UPDATE ON times
FOR EACH ROW
BEGIN
    UPDATE times SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS update_jogadores_timestamp 
AFTER UPDATE ON jogadores
FOR EACH ROW
BEGIN
    UPDATE jogadores SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS update_jogos_timestamp 
AFTER UPDATE ON jogos
FOR EACH ROW
BEGIN
    UPDATE jogos SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- Trigger para calcular saldo de gols automaticamente
CREATE TRIGGER IF NOT EXISTS update_classificacao_saldo 
AFTER UPDATE OF gols_pro, gols_contra ON classificacao
FOR EACH ROW
BEGIN
    UPDATE classificacao 
    SET saldo_gols = NEW.gols_pro - NEW.gols_contra 
    WHERE id = NEW.id;
END;

-- =====================================================
-- VIEWS ÚTEIS
-- =====================================================

-- View: Próximos Jogos
CREATE VIEW IF NOT EXISTS v_proximos_jogos AS
SELECT 
    j.id,
    j.api_id,
    c.nome AS competicao,
    j.rodada,
    tc.nome AS time_casa,
    tf.nome AS time_fora,
    j.data_hora,
    e.nome AS estadio,
    j.status,
    j.odds_casa,
    j.odds_empate,
    j.odds_fora
FROM jogos j
JOIN competicoes c ON j.competicao_id = c.id
JOIN times tc ON j.time_casa_id = tc.id
JOIN times tf ON j.time_fora_id = tf.id
LEFT JOIN estadios e ON j.estadio_id = e.id
WHERE j.status IN ('agendado', 'ao_vivo')
ORDER BY j.data_hora ASC;

-- View: Artilharia
CREATE VIEW IF NOT EXISTS v_artilharia AS
SELECT 
    jog.id AS jogador_id,
    jog.nome_completo,
    t.nome AS time,
    COUNT(e.id) AS total_gols,
    c.nome AS competicao,
    j.temporada
FROM eventos_jogo e
JOIN jogadores jog ON e.jogador_principal_id = jog.id
JOIN jogos j ON e.jogo_id = j.id
JOIN competicoes c ON j.competicao_id = c.id
JOIN times t ON e.time_id = t.id
WHERE e.tipo = 'gol'
GROUP BY jog.id, j.competicao_id, j.temporada
ORDER BY total_gols DESC;

-- View: Jogadores Lesionados
CREATE VIEW IF NOT EXISTS v_jogadores_lesionados AS
SELECT 
    j.nome_completo AS jogador,
    t.nome AS time,
    l.tipo_lesao,
    l.gravidade,
    l.data_lesao,
    l.data_prevista_retorno,
    julianday(l.data_prevista_retorno) - julianday('now') AS dias_para_retorno,
    l.status
FROM lesoes l
JOIN jogadores j ON l.jogador_id = j.id
LEFT JOIN times t ON l.time_id = t.id
WHERE l.status IN ('ativo', 'recuperacao')
ORDER BY l.gravidade DESC, l.data_lesao DESC;

-- View: Forma Recente dos Times (últimos 5 jogos)
CREATE VIEW IF NOT EXISTS v_forma_times AS
SELECT 
    t.id AS time_id,
    t.nome AS time,
    GROUP_CONCAT(
        CASE 
            WHEN (j.time_casa_id = t.id AND j.gols_casa > j.gols_fora) OR 
                 (j.time_fora_id = t.id AND j.gols_fora > j.gols_casa) THEN 'V'
            WHEN j.gols_casa = j.gols_fora THEN 'E'
            ELSE 'D'
        END
    ) AS ultimos_5
FROM times t
JOIN jogos j ON (t.id = j.time_casa_id OR t.id = j.time_fora_id)
WHERE j.status = 'finalizado'
GROUP BY t.id
HAVING COUNT(*) <= 5
ORDER BY j.data_hora DESC;

-- =====================================================
-- FIM DO SCHEMA
-- =====================================================

-- Versão do Schema
CREATE TABLE IF NOT EXISTS schema_version (
    version TEXT PRIMARY KEY,
applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
INSERT OR IGNORE INTO schema_version (version) VALUES ('1.0.0SSS');