-- ============================================
-- PROJETO BIG DATA - CS:GO MATCHMAKING
-- DDL - Criação das Tabelas
-- ============================================

-- Criar banco de dados (executar separadamente)
-- CREATE DATABASE csgo_analytics;

-- ============================================
-- TABELA: JOGADOR
-- ============================================
CREATE TABLE IF NOT EXISTS jogador (
    jogador_id SERIAL PRIMARY KEY,
    steam_id BIGINT NOT NULL UNIQUE,
    rank_atual INTEGER CHECK (rank_atual BETWEEN 1 AND 18)
);

COMMENT ON TABLE jogador IS 'Jogadores únicos identificados por Steam ID';
COMMENT ON COLUMN jogador.steam_id IS 'Steam ID único do jogador';
COMMENT ON COLUMN jogador.rank_atual IS 'Último rank conhecido (1=Silver I, 18=Global Elite)';

-- ============================================
-- TABELA: MAPA
-- ============================================
CREATE TABLE IF NOT EXISTS mapa (
    mapa_id SERIAL PRIMARY KEY,
    nome VARCHAR(20) NOT NULL UNIQUE
);

COMMENT ON TABLE mapa IS 'Mapas disponíveis no jogo';
COMMENT ON COLUMN mapa.nome IS 'Nome do mapa (ex: de_dust2, de_mirage)';

-- ============================================
-- TABELA: ARMA
-- ============================================
CREATE TABLE IF NOT EXISTS arma (
    arma_id SERIAL PRIMARY KEY,
    nome VARCHAR(25) NOT NULL UNIQUE,
    tipo VARCHAR(15) NOT NULL
);

COMMENT ON TABLE arma IS 'Armas disponíveis no jogo';
COMMENT ON COLUMN arma.nome IS 'Nome da arma (ex: AK-47, M4A4)';
COMMENT ON COLUMN arma.tipo IS 'Categoria da arma (Rifle, Pistol, SMG, etc.)';

-- ============================================
-- TABELA: PARTIDA
-- ============================================
CREATE TABLE IF NOT EXISTS partida (
    partida_id SERIAL PRIMARY KEY,
    arquivo_demo VARCHAR(60) NOT NULL UNIQUE,
    mapa_id INTEGER NOT NULL REFERENCES mapa(mapa_id),
    data_hora TIMESTAMP NOT NULL,
    rank_medio DECIMAL(4,1)
);

COMMENT ON TABLE partida IS 'Partidas únicas (arquivos demo)';
COMMENT ON COLUMN partida.arquivo_demo IS 'Nome do arquivo demo da partida';
COMMENT ON COLUMN partida.rank_medio IS 'Rank médio dos jogadores na partida';

-- Índice para busca por data
CREATE INDEX idx_partida_data ON partida(data_hora);
CREATE INDEX idx_partida_mapa ON partida(mapa_id);

-- ============================================
-- TABELA: ROUND
-- ============================================
CREATE TABLE IF NOT EXISTS round (
    round_id SERIAL PRIMARY KEY,
    partida_id INTEGER NOT NULL REFERENCES partida(partida_id),
    numero INTEGER NOT NULL CHECK (numero > 0),
    tipo VARCHAR(20),
    vencedor_lado VARCHAR(20),
    ct_economia INTEGER,
    t_economia INTEGER,
    UNIQUE(partida_id, numero)
);

COMMENT ON TABLE round IS 'Rounds jogados em cada partida';
COMMENT ON COLUMN round.numero IS 'Número do round (1-30+)';
COMMENT ON COLUMN round.tipo IS 'Tipo do round (PISTOL_ROUND, ECO, etc.)';
COMMENT ON COLUMN round.vencedor_lado IS 'Lado vencedor (CounterTerrorist/Terrorist)';

-- Índice para busca por partida
CREATE INDEX idx_round_partida ON round(partida_id);

-- ============================================
-- TABELA: EVENTO_DANO
-- ============================================
CREATE TABLE IF NOT EXISTS evento_dano (
    evento_id SERIAL PRIMARY KEY,
    round_id INTEGER NOT NULL REFERENCES round(round_id),
    atacante_id INTEGER REFERENCES jogador(jogador_id),
    vitima_id INTEGER REFERENCES jogador(jogador_id),
    arma_id INTEGER REFERENCES arma(arma_id),
    tick INTEGER,
    segundos DECIMAL(10,4),
    dano_hp INTEGER CHECK (dano_hp >= 0),
    dano_armadura INTEGER CHECK (dano_armadura >= 0),
    hitbox VARCHAR(15),
    bomba_plantada BOOLEAN DEFAULT FALSE,
    premio INTEGER,
    atacante_x DECIMAL(15,3),
    atacante_y DECIMAL(15,3),
    vitima_x DECIMAL(15,3),
    vitima_y DECIMAL(15,3)
);

COMMENT ON TABLE evento_dano IS 'Eventos de dano registrados nas partidas';
COMMENT ON COLUMN evento_dano.tick IS 'Tick do servidor no momento do evento';
COMMENT ON COLUMN evento_dano.hitbox IS 'Parte do corpo atingida';
COMMENT ON COLUMN evento_dano.premio IS 'Prêmio em dinheiro pelo dano/kill';

-- Índices para consultas frequentes
CREATE INDEX idx_evento_round ON evento_dano(round_id);
CREATE INDEX idx_evento_atacante ON evento_dano(atacante_id);
CREATE INDEX idx_evento_vitima ON evento_dano(vitima_id);
CREATE INDEX idx_evento_arma ON evento_dano(arma_id);
CREATE INDEX idx_evento_hitbox ON evento_dano(hitbox);

-- ============================================
-- VIEWS AUXILIARES
-- ============================================

-- View: Estatísticas por jogador
CREATE OR REPLACE VIEW vw_estatisticas_jogador AS
SELECT 
    j.jogador_id,
    j.steam_id,
    j.rank_atual,
    COUNT(CASE WHEN e.atacante_id = j.jogador_id AND e.dano_hp >= 100 THEN 1 END) as kills,
    COUNT(CASE WHEN e.vitima_id = j.jogador_id AND e.dano_hp >= 100 THEN 1 END) as deaths,
    SUM(CASE WHEN e.atacante_id = j.jogador_id THEN e.dano_hp ELSE 0 END) as dano_total
FROM jogador j
LEFT JOIN evento_dano e ON j.jogador_id = e.atacante_id OR j.jogador_id = e.vitima_id
GROUP BY j.jogador_id, j.steam_id, j.rank_atual;

-- View: Estatísticas por mapa
CREATE OR REPLACE VIEW vw_estatisticas_mapa AS
SELECT 
    m.mapa_id,
    m.nome as mapa,
    COUNT(DISTINCT p.partida_id) as total_partidas,
    COUNT(DISTINCT r.round_id) as total_rounds,
    COUNT(e.evento_id) as total_eventos
FROM mapa m
LEFT JOIN partida p ON m.mapa_id = p.mapa_id
LEFT JOIN round r ON p.partida_id = r.partida_id
LEFT JOIN evento_dano e ON r.round_id = e.round_id
GROUP BY m.mapa_id, m.nome;

-- ============================================
-- FIM DO SCRIPT DDL
-- ============================================
