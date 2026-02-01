"""
============================================
PROJETO BIG DATA - CS:GO MATCHMAKING
Testar Consultas SQL e Gerar Gráficos
============================================

Este script executa consultas SQL avançadas e gera
gráficos para o relatório final.
"""

import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import os

# Configuração do banco
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'csgo_analytics',
    'user': 'postgres',
    'password': '159357'
}

# Pasta para salvar gráficos
PASTA_GRAFICOS = '../modelos/graficos/'
os.makedirs(PASTA_GRAFICOS, exist_ok=True)

def conectar():
    return psycopg2.connect(**DB_CONFIG)

def executar_consulta(conn, sql, descricao):
    """Executa uma consulta e retorna DataFrame."""
    print(f"\n{'='*50}")
    print(f"📊 {descricao}")
    print('='*50)
    df = pd.read_sql(sql, conn)
    print(df.to_string())
    return df

def main():
    print("="*60)
    print("🔍 EXECUTANDO CONSULTAS SQL AVANÇADAS")
    print("="*60)
    
    conn = conectar()
    print("✅ Conectado ao PostgreSQL!")
    
    # ========================================
    # CONSULTA 1: Contagem de registros por tabela
    # ========================================
    sql_contagem = """
    SELECT 'jogador' as tabela, COUNT(*) as registros FROM jogador
    UNION ALL
    SELECT 'mapa', COUNT(*) FROM mapa
    UNION ALL
    SELECT 'arma', COUNT(*) FROM arma
    UNION ALL
    SELECT 'partida', COUNT(*) FROM partida
    UNION ALL
    SELECT 'round', COUNT(*) FROM round
    UNION ALL
    SELECT 'evento_dano', COUNT(*) FROM evento_dano
    ORDER BY registros DESC;
    """
    df_contagem = executar_consulta(conn, sql_contagem, "Contagem de Registros por Tabela")
    
    # Gráfico de barras
    plt.figure(figsize=(10, 6))
    plt.barh(df_contagem['tabela'], df_contagem['registros'], color='steelblue')
    plt.xlabel('Número de Registros')
    plt.title('Quantidade de Registros por Tabela')
    plt.xscale('log')
    for i, v in enumerate(df_contagem['registros']):
        plt.text(v, i, f' {v:,}', va='center')
    plt.tight_layout()
    plt.savefig(f'{PASTA_GRAFICOS}01_registros_por_tabela.png', dpi=150)
    plt.close()
    print(f"📈 Gráfico salvo: 01_registros_por_tabela.png")
    
    # ========================================
    # CONSULTA 2: Top 10 Mapas Mais Jogados
    # ========================================
    sql_mapas = """
    SELECT m.nome as mapa, COUNT(DISTINCT p.partida_id) as partidas
    FROM mapa m
    INNER JOIN partida p ON m.mapa_id = p.mapa_id
    GROUP BY m.nome
    ORDER BY partidas DESC
    LIMIT 10;
    """
    df_mapas = executar_consulta(conn, sql_mapas, "Top 10 Mapas Mais Jogados")
    
    plt.figure(figsize=(10, 6))
    plt.bar(df_mapas['mapa'], df_mapas['partidas'], color='darkgreen')
    plt.xlabel('Mapa')
    plt.ylabel('Número de Partidas')
    plt.title('Top 10 Mapas Mais Jogados')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(f'{PASTA_GRAFICOS}02_mapas_mais_jogados.png', dpi=150)
    plt.close()
    print(f"📈 Gráfico salvo: 02_mapas_mais_jogados.png")
    
    # ========================================
    # CONSULTA 3: Taxa de Vitória CT vs T
    # ========================================
    sql_ct_t = """
    SELECT 
        m.nome as mapa,
        COUNT(CASE WHEN r.vencedor_lado = 'CounterTerrorist' THEN 1 END) as vitorias_ct,
        COUNT(CASE WHEN r.vencedor_lado = 'Terrorist' THEN 1 END) as vitorias_t,
        COUNT(*) as total_rounds
    FROM round r
    INNER JOIN partida p ON r.partida_id = p.partida_id
    INNER JOIN mapa m ON p.mapa_id = m.mapa_id
    WHERE m.mapa_id <= 21
    GROUP BY m.nome
    HAVING COUNT(*) > 100
    ORDER BY total_rounds DESC
    LIMIT 10;
    """
    df_ct_t = executar_consulta(conn, sql_ct_t, "Taxa de Vitória CT vs T por Mapa")
    
    # Gráfico de barras agrupadas
    x = range(len(df_ct_t))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(12, 6))
    bars1 = ax.bar([i - width/2 for i in x], df_ct_t['vitorias_ct'], width, label='CT', color='#5b89a6')
    bars2 = ax.bar([i + width/2 for i in x], df_ct_t['vitorias_t'], width, label='Terrorist', color='#c9a227')
    
    ax.set_xlabel('Mapa')
    ax.set_ylabel('Vitórias')
    ax.set_title('Vitórias CT vs Terrorist por Mapa')
    ax.set_xticks(x)
    ax.set_xticklabels(df_ct_t['mapa'], rotation=45, ha='right')
    ax.legend()
    plt.tight_layout()
    plt.savefig(f'{PASTA_GRAFICOS}03_ct_vs_t.png', dpi=150)
    plt.close()
    print(f"📈 Gráfico salvo: 03_ct_vs_t.png")
    
    # ========================================
    # CONSULTA 4: Top 10 Armas Mais Usadas
    # ========================================
    sql_armas = """
    SELECT a.nome as arma, a.tipo, COUNT(*) as usos,
           SUM(e.dano_hp) as dano_total
    FROM evento_dano e
    INNER JOIN arma a ON e.arma_id = a.arma_id
    WHERE a.arma_id <= 42
    GROUP BY a.nome, a.tipo
    ORDER BY usos DESC
    LIMIT 10;
    """
    df_armas = executar_consulta(conn, sql_armas, "Top 10 Armas Mais Usadas")
    
    plt.figure(figsize=(10, 6))
    colors = plt.cm.Reds([0.3 + i*0.07 for i in range(len(df_armas))])
    plt.barh(df_armas['arma'], df_armas['usos'], color=colors)
    plt.xlabel('Número de Usos')
    plt.title('Top 10 Armas Mais Usadas')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(f'{PASTA_GRAFICOS}04_armas_mais_usadas.png', dpi=150)
    plt.close()
    print(f"📈 Gráfico salvo: 04_armas_mais_usadas.png")
    
    # ========================================
    # CONSULTA 5: Distribuição de Dano por Hitbox
    # ========================================
    sql_hitbox = """
    SELECT hitbox, 
           COUNT(*) as hits,
           ROUND(AVG(dano_hp), 2) as dano_medio,
           SUM(dano_hp) as dano_total
    FROM evento_dano
    WHERE hitbox IS NOT NULL AND hitbox != ''
    GROUP BY hitbox
    ORDER BY hits DESC;
    """
    df_hitbox = executar_consulta(conn, sql_hitbox, "Distribuição de Hits por Hitbox")
    
    plt.figure(figsize=(10, 6))
    colors_hitbox = ['#ff6b6b' if h == 'Head' else '#4ecdc4' for h in df_hitbox['hitbox']]
    plt.pie(df_hitbox['hits'], labels=df_hitbox['hitbox'], autopct='%1.1f%%', colors=plt.cm.Set3.colors)
    plt.title('Distribuição de Hits por Parte do Corpo')
    plt.tight_layout()
    plt.savefig(f'{PASTA_GRAFICOS}05_hits_por_hitbox.png', dpi=150)
    plt.close()
    print(f"📈 Gráfico salvo: 05_hits_por_hitbox.png")
    
    # ========================================
    # CONSULTA 6: Distribuição de Ranks
    # ========================================
    sql_ranks = """
    SELECT rank_atual as rank, COUNT(*) as jogadores
    FROM jogador
    WHERE rank_atual > 0 AND rank_atual <= 18
    GROUP BY rank_atual
    ORDER BY rank_atual;
    """
    df_ranks = executar_consulta(conn, sql_ranks, "Distribuição de Jogadores por Rank")
    
    rank_names = {
        1: 'Silver I', 2: 'Silver II', 3: 'Silver III', 4: 'Silver IV',
        5: 'Silver Elite', 6: 'Silver Elite M', 7: 'Gold Nova I', 8: 'Gold Nova II',
        9: 'Gold Nova III', 10: 'Gold Nova M', 11: 'MG I', 12: 'MG II',
        13: 'MG Elite', 14: 'DMG', 15: 'LE', 16: 'LEM', 17: 'Supreme', 18: 'Global'
    }
    df_ranks['rank_nome'] = df_ranks['rank'].map(rank_names)
    
    plt.figure(figsize=(12, 6))
    colors_rank = plt.cm.RdYlGn([i/18 for i in df_ranks['rank']])
    plt.bar(df_ranks['rank_nome'], df_ranks['jogadores'], color=colors_rank)
    plt.xlabel('Rank')
    plt.ylabel('Número de Jogadores')
    plt.title('Distribuição de Jogadores por Rank')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(f'{PASTA_GRAFICOS}06_distribuicao_ranks.png', dpi=150)
    plt.close()
    print(f"📈 Gráfico salvo: 06_distribuicao_ranks.png")
    
    # ========================================
    # CONSULTA 7: Headshot Percentage por Arma
    # ========================================
    sql_hs = """
    SELECT a.nome as arma,
           COUNT(*) as total_hits,
           COUNT(CASE WHEN e.hitbox = 'Head' THEN 1 END) as headshots,
           ROUND(COUNT(CASE WHEN e.hitbox = 'Head' THEN 1 END)::DECIMAL / COUNT(*) * 100, 2) as hs_percent
    FROM evento_dano e
    INNER JOIN arma a ON e.arma_id = a.arma_id
    WHERE a.arma_id <= 42
    GROUP BY a.nome
    HAVING COUNT(*) > 1000
    ORDER BY hs_percent DESC
    LIMIT 10;
    """
    df_hs = executar_consulta(conn, sql_hs, "Top 10 Armas por Headshot %")
    
    plt.figure(figsize=(10, 6))
    plt.barh(df_hs['arma'], df_hs['hs_percent'], color='crimson')
    plt.xlabel('Headshot %')
    plt.title('Top 10 Armas por Taxa de Headshot')
    plt.gca().invert_yaxis()
    for i, v in enumerate(df_hs['hs_percent']):
        plt.text(v + 0.5, i, f'{v}%', va='center')
    plt.tight_layout()
    plt.savefig(f'{PASTA_GRAFICOS}07_headshot_por_arma.png', dpi=150)
    plt.close()
    print(f"📈 Gráfico salvo: 07_headshot_por_arma.png")
    
    # ========================================
    # CONSULTA 8: Top Jogadores por Kills
    # ========================================
    sql_top_players = """
    SELECT j.steam_id, j.rank_atual,
           COUNT(*) as kills
    FROM evento_dano e
    INNER JOIN jogador j ON e.atacante_id = j.jogador_id
    WHERE e.dano_hp >= 100
    GROUP BY j.steam_id, j.rank_atual
    ORDER BY kills DESC
    LIMIT 15;
    """
    df_players = executar_consulta(conn, sql_top_players, "Top 15 Jogadores por Kills")
    
    # ========================================
    # RESUMO FINAL
    # ========================================
    print("\n" + "="*60)
    print("✅ CONSULTAS EXECUTADAS COM SUCESSO!")
    print("="*60)
    print(f"\n📁 Gráficos salvos em: {os.path.abspath(PASTA_GRAFICOS)}")
    print("\n📊 Gráficos gerados:")
    print("   1. Registros por tabela")
    print("   2. Mapas mais jogados")
    print("   3. CT vs Terrorist")
    print("   4. Armas mais usadas")
    print("   5. Hits por hitbox")
    print("   6. Distribuição de ranks")
    print("   7. Headshot % por arma")
    
    conn.close()

if __name__ == "__main__":
    main()
