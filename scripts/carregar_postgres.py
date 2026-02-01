"""
============================================
PROJETO BIG DATA - CS:GO MATCHMAKING
Carregar Dados no PostgreSQL
============================================

Este script carrega os CSVs normalizados no PostgreSQL.

Pré-requisitos:
1. PostgreSQL instalado e rodando
2. Criar banco de dados: CREATE DATABASE csgo_analytics;
3. pip install psycopg2-binary

Configurar as variáveis abaixo conforme seu ambiente.
"""

import pandas as pd
import psycopg2
from psycopg2 import sql
import os
from datetime import datetime

# ============================================
# CONFIGURAÇÕES DO BANCO
# ============================================
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'csgo_analytics',
    'user': 'postgres',
    'password': '159357'
}

CAMINHO_TABELAS = '../base_dados/tabelas_normalizadas/'

# ============================================
# DDL - CRIAR TABELAS
# ============================================
DDL_CRIAR_TABELAS = """
-- Limpar tabelas existentes (na ordem correta por causa das FKs)
DROP TABLE IF EXISTS evento_dano CASCADE;
DROP TABLE IF EXISTS round CASCADE;
DROP TABLE IF EXISTS partida CASCADE;
DROP TABLE IF EXISTS arma CASCADE;
DROP TABLE IF EXISTS mapa CASCADE;
DROP TABLE IF EXISTS jogador CASCADE;

-- TABELA: JOGADOR
CREATE TABLE jogador (
    jogador_id INTEGER PRIMARY KEY,
    steam_id BIGINT UNIQUE,
    rank_atual INTEGER CHECK (rank_atual BETWEEN 0 AND 18)
);

-- TABELA: MAPA
CREATE TABLE mapa (
    mapa_id INTEGER PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE
);

-- TABELA: ARMA
CREATE TABLE arma (
    arma_id INTEGER PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE,
    tipo VARCHAR(20) NOT NULL
);

-- TABELA: PARTIDA
CREATE TABLE partida (
    partida_id INTEGER PRIMARY KEY,
    arquivo_demo VARCHAR(100) NOT NULL UNIQUE,
    mapa_id INTEGER REFERENCES mapa(mapa_id),
    data_hora TIMESTAMP,
    rank_medio DECIMAL(4,1)
);

-- TABELA: ROUND
CREATE TABLE round (
    round_id INTEGER PRIMARY KEY,
    partida_id INTEGER REFERENCES partida(partida_id),
    numero INTEGER NOT NULL CHECK (numero > 0),
    tipo VARCHAR(20),
    vencedor_lado VARCHAR(20),
    ct_economia INTEGER,
    t_economia INTEGER
);

-- TABELA: EVENTO_DANO
CREATE TABLE evento_dano (
    evento_id INTEGER PRIMARY KEY,
    round_id INTEGER REFERENCES round(round_id),
    atacante_id INTEGER REFERENCES jogador(jogador_id),
    vitima_id INTEGER REFERENCES jogador(jogador_id),
    arma_id INTEGER REFERENCES arma(arma_id),
    tick INTEGER,
    segundos DECIMAL(10,4),
    dano_hp INTEGER CHECK (dano_hp >= 0),
    dano_armadura INTEGER CHECK (dano_armadura >= 0),
    hitbox VARCHAR(20),
    bomba_plantada BOOLEAN DEFAULT FALSE,
    premio INTEGER,
    atacante_x DECIMAL(15,3),
    atacante_y DECIMAL(15,3),
    vitima_x DECIMAL(15,3),
    vitima_y DECIMAL(15,3)
);

-- Índices para performance
CREATE INDEX idx_partida_mapa ON partida(mapa_id);
CREATE INDEX idx_round_partida ON round(partida_id);
CREATE INDEX idx_evento_round ON evento_dano(round_id);
CREATE INDEX idx_evento_atacante ON evento_dano(atacante_id);
CREATE INDEX idx_evento_vitima ON evento_dano(vitima_id);
CREATE INDEX idx_evento_arma ON evento_dano(arma_id);
"""

# ============================================
# FUNÇÕES
# ============================================

def conectar():
    """Conecta ao PostgreSQL."""
    print(f"🔌 Conectando ao PostgreSQL ({DB_CONFIG['host']}:{DB_CONFIG['port']})...")
    conn = psycopg2.connect(**DB_CONFIG)
    print("✅ Conectado!")
    return conn


def criar_tabelas(conn):
    """Cria as tabelas no banco."""
    print("📦 Criando tabelas...")
    cursor = conn.cursor()
    cursor.execute(DDL_CRIAR_TABELAS)
    conn.commit()
    cursor.close()
    print("✅ Tabelas criadas!")


def carregar_csv(conn, nome_tabela, arquivo_csv, colunas):
    """Carrega um CSV na tabela usando COPY."""
    print(f"📥 Carregando {nome_tabela}...")
    
    # Ler CSV
    df = pd.read_csv(arquivo_csv)
    
    # Converter datas se existir coluna data_hora
    if 'data_hora' in colunas:
        df['data_hora'] = pd.to_datetime(df['data_hora'], format='mixed', dayfirst=False)
        df['data_hora'] = df['data_hora'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Para tabelas grandes, usar inserção em lotes
    cursor = conn.cursor()
    
    # Preparar dados
    registros = df[colunas].values.tolist()
    total = len(registros)
    
    # Inserir em lotes de 10000
    lote_size = 10000
    for i in range(0, total, lote_size):
        lote = registros[i:i+lote_size]
        
        # Criar placeholders
        placeholders = ','.join(['%s'] * len(colunas))
        colunas_str = ','.join(colunas)
        
        # Inserir lote
        args_str = ','.join(
            cursor.mogrify(f"({placeholders})", tuple(reg)).decode('utf-8')
            for reg in lote
        )
        
        cursor.execute(f"INSERT INTO {nome_tabela} ({colunas_str}) VALUES {args_str}")
        
        # Progresso
        progresso = min(i + lote_size, total)
        print(f"   {progresso:,}/{total:,} ({progresso*100//total}%)", end='\r')
    
    conn.commit()
    cursor.close()
    print(f"✅ {nome_tabela}: {total:,} registros inseridos")


def main():
    print("=" * 50)
    print("🚀 CARGA DE DADOS NO POSTGRESQL")
    print("=" * 50)
    
    # Mudar para diretório do script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    inicio = datetime.now()
    
    try:
        # Conectar
        conn = conectar()
        
        # Criar tabelas
        criar_tabelas(conn)
        
        # Carregar dados na ordem correta (respeitar FKs)
        print("\n" + "=" * 50)
        print("📥 CARREGANDO DADOS")
        print("=" * 50)
        
        # 1. Jogador
        carregar_csv(conn, 'jogador', 
                     f"{CAMINHO_TABELAS}jogador.csv",
                     ['jogador_id', 'steam_id', 'rank_atual'])
        
        # 2. Mapa
        carregar_csv(conn, 'mapa',
                     f"{CAMINHO_TABELAS}mapa.csv",
                     ['mapa_id', 'nome'])
        
        # 3. Arma
        carregar_csv(conn, 'arma',
                     f"{CAMINHO_TABELAS}arma.csv",
                     ['arma_id', 'nome', 'tipo'])
        
        # 4. Partida
        carregar_csv(conn, 'partida',
                     f"{CAMINHO_TABELAS}partida.csv",
                     ['partida_id', 'arquivo_demo', 'mapa_id', 'data_hora', 'rank_medio'])
        
        # 5. Round
        carregar_csv(conn, 'round',
                     f"{CAMINHO_TABELAS}round.csv",
                     ['round_id', 'partida_id', 'numero', 'tipo', 'vencedor_lado', 'ct_economia', 't_economia'])
        
        # 6. Evento Dano
        carregar_csv(conn, 'evento_dano',
                     f"{CAMINHO_TABELAS}evento_dano.csv",
                     ['evento_id', 'round_id', 'atacante_id', 'vitima_id', 'arma_id', 
                      'tick', 'segundos', 'dano_hp', 'dano_armadura', 'hitbox',
                      'bomba_plantada', 'premio', 'atacante_x', 'atacante_y', 'vitima_x', 'vitima_y'])
        
        # Fechar conexão
        conn.close()
        
        fim = datetime.now()
        print("\n" + "=" * 50)
        print(f"✅ CARGA CONCLUÍDA EM {fim - inicio}")
        print("=" * 50)
        
    except psycopg2.OperationalError as e:
        print(f"\n❌ Erro de conexão: {e}")
        print("\n📋 Verifique:")
        print("   1. PostgreSQL está rodando?")
        print("   2. O banco 'csgo_analytics' foi criado?")
        print("   3. Usuário e senha estão corretos?")
        print("\n💡 Para criar o banco, execute no psql ou pgAdmin:")
        print("   CREATE DATABASE csgo_analytics;")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        raise


if __name__ == "__main__":
    main()
