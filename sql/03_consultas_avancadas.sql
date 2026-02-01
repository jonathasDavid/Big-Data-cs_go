-- ============================================
-- PROJETO BIG DATA - CS:GO MATCHMAKING
-- SQL AVANÇADO - Consultas Complexas
-- ============================================

-- ============================================
-- 1. CONSULTA COM MÚLTIPLOS JOINS
-- Top 10 jogadores com mais kills por mapa
-- ============================================
SELECT 
    j.steam_id,
    m.nome AS mapa,
    COUNT(*) AS total_kills,
    SUM(e.dano_hp) AS dano_total,
    ROUND(AVG(e.dano_hp), 2) AS dano_medio_por_hit
FROM evento_dano e
INNER JOIN jogador j ON e.atacante_id = j.jogador_id
INNER JOIN round r ON e.round_id = r.round_id
INNER JOIN partida p ON r.partida_id = p.partida_id
INNER JOIN mapa m ON p.mapa_id = m.mapa_id
WHERE e.dano_hp >= 100  -- Kills (dano >= 100 = morte)
GROUP BY j.steam_id, m.nome
ORDER BY total_kills DESC
LIMIT 10;

-- ============================================
-- 2. SUBCONSULTA CORRELACIONADA
-- Jogadores com K/D ratio acima da média
-- ============================================
SELECT 
    j.steam_id,
    j.rank_atual,
    kills.total AS kills,
    deaths.total AS deaths,
    ROUND(kills.total::DECIMAL / NULLIF(deaths.total, 0), 2) AS kd_ratio
FROM jogador j
INNER JOIN (
    SELECT atacante_id, COUNT(*) AS total
    FROM evento_dano
    WHERE dano_hp >= 100
    GROUP BY atacante_id
) kills ON j.jogador_id = kills.atacante_id
INNER JOIN (
    SELECT vitima_id, COUNT(*) AS total
    FROM evento_dano
    WHERE dano_hp >= 100
    GROUP BY vitima_id
) deaths ON j.jogador_id = deaths.vitima_id
WHERE kills.total::DECIMAL / NULLIF(deaths.total, 0) > (
    SELECT AVG(k.total::DECIMAL / NULLIF(d.total, 0))
    FROM (SELECT atacante_id, COUNT(*) AS total FROM evento_dano WHERE dano_hp >= 100 GROUP BY atacante_id) k
    JOIN (SELECT vitima_id, COUNT(*) AS total FROM evento_dano WHERE dano_hp >= 100 GROUP BY vitima_id) d
    ON k.atacante_id = d.vitima_id
)
ORDER BY kd_ratio DESC
LIMIT 20;

-- ============================================
-- 3. CTE (Common Table Expression)
-- Análise de performance por arma e hitbox
-- ============================================
WITH estatisticas_arma AS (
    SELECT 
        a.nome AS arma,
        a.tipo AS tipo_arma,
        e.hitbox,
        COUNT(*) AS total_hits,
        SUM(e.dano_hp) AS dano_total,
        COUNT(CASE WHEN e.dano_hp >= 100 THEN 1 END) AS kills
    FROM evento_dano e
    INNER JOIN arma a ON e.arma_id = a.arma_id
    WHERE e.hitbox IS NOT NULL
    GROUP BY a.nome, a.tipo, e.hitbox
),
ranking_armas AS (
    SELECT 
        arma,
        tipo_arma,
        hitbox,
        total_hits,
        dano_total,
        kills,
        ROUND(kills::DECIMAL / NULLIF(total_hits, 0) * 100, 2) AS taxa_letalidade,
        ROW_NUMBER() OVER (PARTITION BY tipo_arma ORDER BY kills DESC) AS rank_por_tipo
    FROM estatisticas_arma
)
SELECT *
FROM ranking_armas
WHERE rank_por_tipo <= 3
ORDER BY tipo_arma, rank_por_tipo;

-- ============================================
-- 4. WINDOW FUNCTIONS
-- Ranking de jogadores por rank com estatísticas acumuladas
-- ============================================
SELECT 
    j.steam_id,
    j.rank_atual,
    COUNT(CASE WHEN e.atacante_id = j.jogador_id AND e.dano_hp >= 100 THEN 1 END) AS kills,
    SUM(SUM(CASE WHEN e.atacante_id = j.jogador_id THEN e.dano_hp ELSE 0 END)) 
        OVER (PARTITION BY j.rank_atual ORDER BY j.jogador_id) AS dano_acumulado_rank,
    RANK() OVER (
        PARTITION BY j.rank_atual 
        ORDER BY COUNT(CASE WHEN e.atacante_id = j.jogador_id AND e.dano_hp >= 100 THEN 1 END) DESC
    ) AS posicao_no_rank,
    ROUND(
        AVG(COUNT(CASE WHEN e.atacante_id = j.jogador_id AND e.dano_hp >= 100 THEN 1 END)) 
        OVER (PARTITION BY j.rank_atual), 2
    ) AS media_kills_rank
FROM jogador j
LEFT JOIN evento_dano e ON j.jogador_id = e.atacante_id OR j.jogador_id = e.vitima_id
GROUP BY j.jogador_id, j.steam_id, j.rank_atual
ORDER BY j.rank_atual DESC, posicao_no_rank;

-- ============================================
-- 5. AGREGAÇÕES COMPLEXAS COM CASE
-- Taxa de vitória CT vs T por mapa
-- ============================================
SELECT 
    m.nome AS mapa,
    COUNT(DISTINCT r.round_id) AS total_rounds,
    COUNT(CASE WHEN r.vencedor_lado = 'CounterTerrorist' THEN 1 END) AS vitorias_ct,
    COUNT(CASE WHEN r.vencedor_lado = 'Terrorist' THEN 1 END) AS vitorias_t,
    ROUND(
        COUNT(CASE WHEN r.vencedor_lado = 'CounterTerrorist' THEN 1 END)::DECIMAL / 
        NULLIF(COUNT(DISTINCT r.round_id), 0) * 100, 2
    ) AS taxa_vitoria_ct,
    ROUND(
        COUNT(CASE WHEN r.vencedor_lado = 'Terrorist' THEN 1 END)::DECIMAL / 
        NULLIF(COUNT(DISTINCT r.round_id), 0) * 100, 2
    ) AS taxa_vitoria_t
FROM mapa m
INNER JOIN partida p ON m.mapa_id = p.mapa_id
INNER JOIN round r ON p.partida_id = r.partida_id
GROUP BY m.nome
ORDER BY total_rounds DESC;

-- ============================================
-- 6. ANÁLISE DE ECONOMIA POR TIPO DE ROUND
-- ============================================
SELECT 
    r.tipo AS tipo_round,
    COUNT(DISTINCT r.round_id) AS total_rounds,
    ROUND(AVG(r.ct_economia), 0) AS media_economia_ct,
    ROUND(AVG(r.t_economia), 0) AS media_economia_t,
    ROUND(
        COUNT(CASE WHEN r.vencedor_lado = 'CounterTerrorist' THEN 1 END)::DECIMAL / 
        COUNT(*) * 100, 2
    ) AS taxa_vitoria_ct,
    ROUND(AVG(e.dano_hp), 2) AS dano_medio_por_evento
FROM round r
LEFT JOIN evento_dano e ON r.round_id = e.round_id
WHERE r.tipo IS NOT NULL
GROUP BY r.tipo
ORDER BY total_rounds DESC;

-- ============================================
-- 7. HEADSHOT PERCENTAGE POR ARMA
-- ============================================
SELECT 
    a.nome AS arma,
    a.tipo AS tipo,
    COUNT(*) AS total_hits,
    COUNT(CASE WHEN e.hitbox = 'Head' THEN 1 END) AS headshots,
    ROUND(
        COUNT(CASE WHEN e.hitbox = 'Head' THEN 1 END)::DECIMAL / 
        NULLIF(COUNT(*), 0) * 100, 2
    ) AS headshot_percentage
FROM evento_dano e
INNER JOIN arma a ON e.arma_id = a.arma_id
GROUP BY a.nome, a.tipo
HAVING COUNT(*) > 100  -- Mínimo de hits para relevância estatística
ORDER BY headshot_percentage DESC;

-- ============================================
-- 8. ANÁLISE TEMPORAL - PARTIDAS POR MÊS
-- ============================================
SELECT 
    DATE_TRUNC('month', p.data_hora) AS mes,
    COUNT(DISTINCT p.partida_id) AS total_partidas,
    COUNT(DISTINCT r.round_id) AS total_rounds,
    ROUND(AVG(p.rank_medio), 2) AS rank_medio,
    COUNT(e.evento_id) AS total_eventos
FROM partida p
INNER JOIN round r ON p.partida_id = r.partida_id
LEFT JOIN evento_dano e ON r.round_id = e.round_id
GROUP BY DATE_TRUNC('month', p.data_hora)
ORDER BY mes;

-- ============================================
-- 9. TOP ARMAS MAIS LETAIS (KILLS POR HIT)
-- ============================================
WITH arma_stats AS (
    SELECT 
        a.arma_id,
        a.nome,
        a.tipo,
        COUNT(*) AS total_hits,
        COUNT(CASE WHEN e.dano_hp >= 100 THEN 1 END) AS kills,
        SUM(e.dano_hp) AS dano_total
    FROM evento_dano e
    INNER JOIN arma a ON e.arma_id = a.arma_id
    GROUP BY a.arma_id, a.nome, a.tipo
)
SELECT 
    nome AS arma,
    tipo,
    total_hits,
    kills,
    dano_total,
    ROUND(kills::DECIMAL / NULLIF(total_hits, 0) * 100, 2) AS taxa_letalidade,
    ROUND(dano_total::DECIMAL / NULLIF(total_hits, 0), 2) AS dano_medio
FROM arma_stats
WHERE total_hits > 50
ORDER BY taxa_letalidade DESC
LIMIT 15;

-- ============================================
-- 10. DISTRIBUIÇÃO DE RANKS NAS PARTIDAS
-- ============================================
SELECT 
    CASE 
        WHEN j.rank_atual BETWEEN 1 AND 6 THEN 'Silver'
        WHEN j.rank_atual BETWEEN 7 AND 10 THEN 'Gold Nova'
        WHEN j.rank_atual BETWEEN 11 AND 14 THEN 'Master Guardian'
        WHEN j.rank_atual BETWEEN 15 AND 16 THEN 'Eagle'
        WHEN j.rank_atual BETWEEN 17 AND 18 THEN 'Supreme/Global'
        ELSE 'Desconhecido'
    END AS categoria_rank,
    COUNT(DISTINCT j.jogador_id) AS total_jogadores,
    ROUND(AVG(kills.total), 2) AS media_kills,
    ROUND(AVG(deaths.total), 2) AS media_deaths
FROM jogador j
LEFT JOIN (
    SELECT atacante_id, COUNT(*) AS total
    FROM evento_dano WHERE dano_hp >= 100
    GROUP BY atacante_id
) kills ON j.jogador_id = kills.atacante_id
LEFT JOIN (
    SELECT vitima_id, COUNT(*) AS total
    FROM evento_dano WHERE dano_hp >= 100
    GROUP BY vitima_id
) deaths ON j.jogador_id = deaths.vitima_id
GROUP BY categoria_rank
ORDER BY 
    CASE categoria_rank
        WHEN 'Silver' THEN 1
        WHEN 'Gold Nova' THEN 2
        WHEN 'Master Guardian' THEN 3
        WHEN 'Eagle' THEN 4
        WHEN 'Supreme/Global' THEN 5
        ELSE 6
    END;

-- ============================================
-- FIM DAS CONSULTAS AVANÇADAS
-- ============================================
