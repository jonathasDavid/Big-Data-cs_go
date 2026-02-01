# Seção 1 - Introdução

## 1.1 Origem dos Dados

A base de dados utilizada neste projeto foi obtida através da plataforma **Kaggle**, um dos maiores repositórios de datasets públicos para ciência de dados e machine learning.

**Informações da Base:**
| Item | Descrição |
|------|-----------|
| Nome | CS:GO Matchmaking Master Demos |
| Arquivo | `mm_master_demos.csv` |
| Tamanho | ~955.468 registros |
| Formato | CSV (Comma-Separated Values) |
| Fonte | Kaggle |

## 1.2 Tipo de Informação Tratada

A base contém dados de **eventos de dano** ocorridos em partidas de **Counter-Strike: Global Offensive (CS:GO)** no modo **Matchmaking** (partidas competitivas ranqueadas).

### Contexto do Jogo

CS:GO é um jogo de tiro em primeira pessoa (FPS) onde duas equipes de 5 jogadores competem:
- **Counter-Terrorists (CT):** Defendem bombsites e resgatam reféns
- **Terrorists (T):** Plantam a bomba ou eliminam os CTs

### Dados Capturados

Cada registro representa um **evento de dano**, contendo:

1. **Informações da Partida:**
   - Identificador do arquivo demo
   - Mapa jogado (de_dust2, de_mirage, etc.)
   - Data e hora da partida
   - Rank médio dos jogadores

2. **Informações do Round:**
   - Número do round
   - Tipo do round (pistol, eco, force buy, etc.)
   - Vencedor do round
   - Status da bomba
   - Economia das equipes

3. **Informações do Evento:**
   - Jogador atacante (Steam ID, rank, time, posição)
   - Jogador vítima (Steam ID, rank, time, posição)
   - Arma utilizada
   - Parte do corpo atingida (hitbox)
   - Dano causado (HP e armadura)
   - Prêmio recebido

## 1.3 Relevância dos Dados

Estes dados permitem análises como:
- Performance de jogadores por rank
- Efetividade de armas por mapa
- Padrões de economia e compra
- Taxa de vitória CT vs T por mapa
- Heatmaps de posicionamento
- Análise de headshots por arma

---

# Seção 2 - Obtenção dos Dados

## 2.1 Download da Base

Os dados foram obtidos através do Kaggle seguindo os passos:

1. Acesso ao site: https://www.kaggle.com/
2. Busca pelo dataset "CS:GO Matchmaking Demos"
3. Download do arquivo CSV (~XXX MB)
4. Armazenamento local na pasta `base_dados/`

## 2.2 Análise Exploratória

Antes da inserção no SGBD, foi realizada análise exploratória usando Python:

```python
import pandas as pd

# Carregar amostra dos dados
df = pd.read_csv('base_dados/mm_master_demos.csv', nrows=1000)

# Verificar estrutura
print(df.shape)        # (linhas, colunas)
print(df.columns)      # Lista de colunas
print(df.dtypes)       # Tipos de dados
print(df.describe())   # Estatísticas básicas
```

## 2.3 Processo de ETL

O processo de inserção dos dados no SGBD seguiu as etapas:

### Etapa 1 - Extração
- Leitura do arquivo CSV com Pandas
- Tratamento de valores nulos
- Conversão de tipos de dados

### Etapa 2 - Transformação
- Extração de entidades únicas (jogadores, mapas, armas)
- Criação de chaves primárias sintéticas
- Normalização dos dados em múltiplas tabelas

### Etapa 3 - Carga (Load)
- Criação das tabelas no PostgreSQL (DDL)
- Inserção dos dados normalizados
- Criação de índices para otimização

## 2.4 SGBD Utilizado

| Item | Descrição |
|------|-----------|
| SGBD | PostgreSQL 15 |
| Interface | pgAdmin 4 / DBeaver |
| Conexão Python | psycopg2 |

---

*[Completar com detalhes específicos após execução do ETL]*
