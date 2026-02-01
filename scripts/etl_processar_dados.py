"""
============================================
PROJETO BIG DATA - CS:GO MATCHMAKING
Script ETL - Extração, Transformação e Carga
============================================

Este script processa o arquivo CSV original e:
1. Extrai entidades únicas (jogadores, mapas, armas)
2. Transforma dados para modelo normalizado
3. Gera arquivos CSV para cada tabela
4. (Opcional) Carrega dados no PostgreSQL

Requisitos:
    pip install pandas psycopg2-binary tqdm

Uso:
    python etl_processar_dados.py
"""

import pandas as pd
import os
from datetime import datetime
from tqdm import tqdm

# ============================================
# CONFIGURAÇÕES
# ============================================

# Caminhos dos arquivos
CAMINHO_CSV_ORIGINAL = '../base_dados/mm_master_demos.csv'
CAMINHO_SAIDA = '../base_dados/tabelas_normalizadas/'

# Criar pasta de saída se não existir
os.makedirs(CAMINHO_SAIDA, exist_ok=True)

# ============================================
# FUNÇÕES DE EXTRAÇÃO
# ============================================

def carregar_dados(caminho: str, nrows: int = None) -> pd.DataFrame:
    """Carrega o CSV original."""
    print(f"📂 Carregando dados de: {caminho}")
    
    df = pd.read_csv(caminho, nrows=nrows)
    
    print(f"✅ Carregados {len(df):,} registros com {len(df.columns)} colunas")
    return df


def extrair_jogadores(df: pd.DataFrame) -> pd.DataFrame:
    """Extrai jogadores únicos do dataset."""
    print("👤 Extraindo jogadores únicos...")
    
    # Combinar atacantes e vítimas
    atacantes = df[['att_id', 'att_rank']].rename(columns={'att_id': 'steam_id', 'att_rank': 'rank_atual'})
    vitimas = df[['vic_id', 'vic_rank']].rename(columns={'vic_id': 'steam_id', 'vic_rank': 'rank_atual'})
    
    # Concatenar e remover duplicatas (mantendo último rank conhecido)
    jogadores = pd.concat([atacantes, vitimas])
    jogadores = jogadores.drop_duplicates(subset=['steam_id'], keep='last')
    jogadores = jogadores.dropna(subset=['steam_id'])
    
    # Adicionar ID sequencial
    jogadores = jogadores.reset_index(drop=True)
    jogadores.insert(0, 'jogador_id', range(1, len(jogadores) + 1))
    
    print(f"✅ Extraídos {len(jogadores):,} jogadores únicos")
    return jogadores


def extrair_mapas(df: pd.DataFrame) -> pd.DataFrame:
    """Extrai mapas únicos do dataset."""
    print("🗺️ Extraindo mapas únicos...")
    
    mapas = df[['map']].drop_duplicates().rename(columns={'map': 'nome'})
    mapas = mapas.reset_index(drop=True)
    mapas.insert(0, 'mapa_id', range(1, len(mapas) + 1))
    
    print(f"✅ Extraídos {len(mapas)} mapas únicos")
    return mapas


def extrair_armas(df: pd.DataFrame) -> pd.DataFrame:
    """Extrai armas únicas do dataset."""
    print("🔫 Extraindo armas únicas...")
    
    armas = df[['wp', 'wp_type']].drop_duplicates().rename(columns={'wp': 'nome', 'wp_type': 'tipo'})
    armas = armas.dropna(subset=['nome'])
    armas = armas.reset_index(drop=True)
    armas.insert(0, 'arma_id', range(1, len(armas) + 1))
    
    print(f"✅ Extraídas {len(armas)} armas únicas")
    return armas


def extrair_partidas(df: pd.DataFrame, mapas: pd.DataFrame) -> pd.DataFrame:
    """Extrai partidas únicas do dataset."""
    print("🎮 Extraindo partidas únicas...")
    
    # Criar mapeamento de mapa nome -> ID
    mapa_dict = dict(zip(mapas['nome'], mapas['mapa_id']))
    
    # Extrair partidas únicas
    partidas = df[['file', 'map', 'date', 'avg_match_rank']].drop_duplicates(subset=['file'])
    partidas = partidas.rename(columns={
        'file': 'arquivo_demo',
        'date': 'data_hora',
        'avg_match_rank': 'rank_medio'
    })
    
    # Converter mapa para ID
    partidas['mapa_id'] = partidas['map'].map(mapa_dict)
    partidas = partidas.drop(columns=['map'])
    
    # Adicionar ID sequencial
    partidas = partidas.reset_index(drop=True)
    partidas.insert(0, 'partida_id', range(1, len(partidas) + 1))
    
    # Reordenar colunas
    partidas = partidas[['partida_id', 'arquivo_demo', 'mapa_id', 'data_hora', 'rank_medio']]
    
    print(f"✅ Extraídas {len(partidas):,} partidas únicas")
    return partidas


def extrair_rounds(df: pd.DataFrame, partidas: pd.DataFrame) -> pd.DataFrame:
    """Extrai rounds únicos do dataset."""
    print("🔄 Extraindo rounds únicos...")
    
    # Criar mapeamento de arquivo -> partida_id
    partida_dict = dict(zip(partidas['arquivo_demo'], partidas['partida_id']))
    
    # Extrair rounds únicos
    rounds = df[['file', 'round', 'round_type', 'winner_side', 'ct_eq_val', 't_eq_val']].drop_duplicates(
        subset=['file', 'round']
    )
    rounds = rounds.rename(columns={
        'round': 'numero',
        'round_type': 'tipo',
        'winner_side': 'vencedor_lado',
        'ct_eq_val': 'ct_economia',
        't_eq_val': 't_economia'
    })
    
    # Converter arquivo para partida_id
    rounds['partida_id'] = rounds['file'].map(partida_dict)
    rounds = rounds.drop(columns=['file'])
    
    # Adicionar ID sequencial
    rounds = rounds.reset_index(drop=True)
    rounds.insert(0, 'round_id', range(1, len(rounds) + 1))
    
    # Reordenar colunas
    rounds = rounds[['round_id', 'partida_id', 'numero', 'tipo', 'vencedor_lado', 'ct_economia', 't_economia']]
    
    print(f"✅ Extraídos {len(rounds):,} rounds únicos")
    return rounds


def extrair_eventos(df: pd.DataFrame, rounds: pd.DataFrame, jogadores: pd.DataFrame, armas: pd.DataFrame) -> pd.DataFrame:
    """Extrai eventos de dano com FKs corretas."""
    print("💥 Processando eventos de dano...")
    
    # Criar dicionários de mapeamento
    jogador_dict = dict(zip(jogadores['steam_id'], jogadores['jogador_id']))
    arma_dict = dict(zip(armas['nome'], armas['arma_id']))
    
    # Criar chave composta para rounds
    rounds['chave'] = rounds['partida_id'].astype(str) + '_' + rounds['numero'].astype(str)
    
    # Criar mapeamento de partida (precisa do arquivo_demo)
    # Primeiro, recriar o mapeamento arquivo -> partida_id
    partidas = pd.read_csv(f"{CAMINHO_SAIDA}partida.csv")
    partida_dict = dict(zip(partidas['arquivo_demo'], partidas['partida_id']))
    
    # Adicionar partida_id ao df
    df['partida_id_temp'] = df['file'].map(partida_dict)
    df['chave_round'] = df['partida_id_temp'].astype(str) + '_' + df['round'].astype(str)
    
    round_dict = dict(zip(rounds['chave'], rounds['round_id']))
    
    # Processar eventos
    eventos = df.copy()
    eventos['round_id'] = eventos['chave_round'].map(round_dict)
    eventos['atacante_id'] = eventos['att_id'].map(jogador_dict)
    eventos['vitima_id'] = eventos['vic_id'].map(jogador_dict)
    eventos['arma_id'] = eventos['wp'].map(arma_dict)
    
    # Selecionar e renomear colunas
    eventos = eventos[[
        'round_id', 'atacante_id', 'vitima_id', 'arma_id',
        'tick', 'seconds', 'hp_dmg', 'arm_dmg', 'hitbox',
        'is_bomb_planted', 'award', 'att_pos_x', 'att_pos_y', 'vic_pos_x', 'vic_pos_y'
    ]].rename(columns={
        'seconds': 'segundos',
        'hp_dmg': 'dano_hp',
        'arm_dmg': 'dano_armadura',
        'is_bomb_planted': 'bomba_plantada',
        'award': 'premio',
        'att_pos_x': 'atacante_x',
        'att_pos_y': 'atacante_y',
        'vic_pos_x': 'vitima_x',
        'vic_pos_y': 'vitima_y'
    })
    
    # Adicionar ID sequencial
    eventos = eventos.reset_index(drop=True)
    eventos.insert(0, 'evento_id', range(1, len(eventos) + 1))
    
    print(f"✅ Processados {len(eventos):,} eventos")
    return eventos


# ============================================
# FUNÇÃO PRINCIPAL
# ============================================

def main():
    """Executa o pipeline ETL completo."""
    print("=" * 50)
    print("🚀 INICIANDO ETL - CS:GO MATCHMAKING DATA")
    print("=" * 50)
    
    inicio = datetime.now()
    
    # 1. Carregar dados originais
    # Use nrows=10000 para teste, None para todos os dados
    df = carregar_dados(CAMINHO_CSV_ORIGINAL, nrows=None)
    
    # 2. Extrair entidades
    print("\n" + "=" * 50)
    print("📦 EXTRAÇÃO DE ENTIDADES")
    print("=" * 50)
    
    jogadores = extrair_jogadores(df)
    mapas = extrair_mapas(df)
    armas = extrair_armas(df)
    partidas = extrair_partidas(df, mapas)
    rounds = extrair_rounds(df, partidas)
    
    # Salvar tabelas intermediárias para uso na extração de eventos
    jogadores.to_csv(f"{CAMINHO_SAIDA}jogador.csv", index=False)
    mapas.to_csv(f"{CAMINHO_SAIDA}mapa.csv", index=False)
    armas.to_csv(f"{CAMINHO_SAIDA}arma.csv", index=False)
    partidas.to_csv(f"{CAMINHO_SAIDA}partida.csv", index=False)
    rounds.to_csv(f"{CAMINHO_SAIDA}round.csv", index=False)
    
    # Extrair eventos (depende das outras tabelas)
    eventos = extrair_eventos(df, rounds, jogadores, armas)
    eventos.to_csv(f"{CAMINHO_SAIDA}evento_dano.csv", index=False)
    
    # 3. Resumo
    print("\n" + "=" * 50)
    print("📊 RESUMO DA EXTRAÇÃO")
    print("=" * 50)
    print(f"  • Jogadores:    {len(jogadores):>10,}")
    print(f"  • Mapas:        {len(mapas):>10,}")
    print(f"  • Armas:        {len(armas):>10,}")
    print(f"  • Partidas:     {len(partidas):>10,}")
    print(f"  • Rounds:       {len(rounds):>10,}")
    print(f"  • Eventos:      {len(eventos):>10,}")
    
    fim = datetime.now()
    print(f"\n⏱️ Tempo total: {fim - inicio}")
    print(f"📁 Arquivos salvos em: {CAMINHO_SAIDA}")
    print("✅ ETL CONCLUÍDO COM SUCESSO!")


if __name__ == "__main__":
    main()
