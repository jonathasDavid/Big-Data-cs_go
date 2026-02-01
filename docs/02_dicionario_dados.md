# Seção 3 - Dicionário de Dados

## 3.1 Dados Originais (CSV)

### Tabela: mm_master_demos.csv

| # | Atributo | Domínio/Tipo | Tamanho | Descrição |
|---|----------|--------------|---------|-----------|
| 1 | file | VARCHAR | 50 | Nome do arquivo demo da partida |
| 2 | map | VARCHAR | 20 | Nome do mapa jogado (ex: de_dust2) |
| 3 | date | TIMESTAMP | - | Data e hora da partida |
| 4 | round | INTEGER | - | Número do round (1-30+) |
| 5 | tick | INTEGER | - | Tick do servidor no momento do evento |
| 6 | seconds | DECIMAL | 10,4 | Segundos decorridos no round |
| 7 | att_team | VARCHAR | 10 | Nome do time do atacante |
| 8 | vic_team | VARCHAR | 10 | Nome do time da vítima |
| 9 | att_side | VARCHAR | 20 | Lado do atacante (CounterTerrorist/Terrorist) |
| 10 | vic_side | VARCHAR | 20 | Lado da vítima (CounterTerrorist/Terrorist) |
| 11 | hp_dmg | INTEGER | - | Dano causado em HP (pontos de vida) |
| 12 | arm_dmg | INTEGER | - | Dano causado na armadura |
| 13 | is_bomb_planted | BOOLEAN | - | Indica se a bomba estava plantada |
| 14 | bomb_site | CHAR | 1 | Local da bomba (A, B ou vazio) |
| 15 | hitbox | VARCHAR | 15 | Parte do corpo atingida |
| 16 | wp | VARCHAR | 20 | Nome da arma utilizada |
| 17 | wp_type | VARCHAR | 15 | Categoria da arma |
| 18 | award | INTEGER | - | Prêmio em dinheiro pelo dano/kill |
| 19 | winner_team | VARCHAR | 10 | Time vencedor do round |
| 20 | winner_side | VARCHAR | 20 | Lado vencedor do round |
| 21 | att_id | BIGINT | - | Steam ID do atacante |
| 22 | att_rank | INTEGER | - | Rank competitivo do atacante (1-18) |
| 23 | vic_id | BIGINT | - | Steam ID da vítima |
| 24 | vic_rank | INTEGER | - | Rank competitivo da vítima (1-18) |
| 25 | att_pos_x | DECIMAL | 15,3 | Posição X do atacante no mapa |
| 26 | att_pos_y | DECIMAL | 15,3 | Posição Y do atacante no mapa |
| 27 | vic_pos_x | DECIMAL | 15,3 | Posição X da vítima no mapa |
| 28 | vic_pos_y | DECIMAL | 15,3 | Posição Y da vítima no mapa |
| 29 | round_type | VARCHAR | 20 | Tipo do round (PISTOL_ROUND, ECO, etc.) |
| 30 | ct_eq_val | INTEGER | - | Valor total do equipamento dos CTs |
| 31 | t_eq_val | INTEGER | - | Valor total do equipamento dos Ts |
| 32 | avg_match_rank | DECIMAL | 4,1 | Rank médio da partida |

---

## 3.2 Dicionário das Entidades Normalizadas

### Tabela: JOGADOR

| Atributo | Domínio | Tamanho | PK/FK | Descrição |
|----------|---------|---------|-------|-----------|
| jogador_id | SERIAL | - | PK | Identificador único do jogador |
| steam_id | BIGINT | - | UNIQUE | Steam ID do jogador |
| rank_atual | INTEGER | - | - | Último rank conhecido (1-18) |

### Tabela: MAPA

| Atributo | Domínio | Tamanho | PK/FK | Descrição |
|----------|---------|---------|-------|-----------|
| mapa_id | SERIAL | - | PK | Identificador único do mapa |
| nome | VARCHAR | 20 | UNIQUE | Nome do mapa (ex: de_dust2) |

### Tabela: ARMA

| Atributo | Domínio | Tamanho | PK/FK | Descrição |
|----------|---------|---------|-------|-----------|
| arma_id | SERIAL | - | PK | Identificador único da arma |
| nome | VARCHAR | 20 | UNIQUE | Nome da arma (ex: AK-47, M4A4) |
| tipo | VARCHAR | 15 | - | Categoria (Rifle, Pistol, SMG, etc.) |

### Tabela: PARTIDA

| Atributo | Domínio | Tamanho | PK/FK | Descrição |
|----------|---------|---------|-------|-----------|
| partida_id | SERIAL | - | PK | Identificador único da partida |
| arquivo_demo | VARCHAR | 50 | UNIQUE | Nome do arquivo demo |
| mapa_id | INTEGER | - | FK → MAPA | Mapa jogado |
| data_hora | TIMESTAMP | - | - | Data e hora da partida |
| rank_medio | DECIMAL | 4,1 | - | Rank médio dos jogadores |

### Tabela: ROUND

| Atributo | Domínio | Tamanho | PK/FK | Descrição |
|----------|---------|---------|-------|-----------|
| round_id | SERIAL | - | PK | Identificador único do round |
| partida_id | INTEGER | - | FK → PARTIDA | Partida do round |
| numero | INTEGER | - | - | Número do round (1-30+) |
| tipo | VARCHAR | 20 | - | Tipo (PISTOL_ROUND, ECO, etc.) |
| vencedor_lado | VARCHAR | 20 | - | Lado vencedor (CT/T) |
| ct_economia | INTEGER | - | - | Valor equipamento CTs |
| t_economia | INTEGER | - | - | Valor equipamento Ts |

### Tabela: EVENTO_DANO

| Atributo | Domínio | Tamanho | PK/FK | Descrição |
|----------|---------|---------|-------|-----------|
| evento_id | SERIAL | - | PK | Identificador único do evento |
| round_id | INTEGER | - | FK → ROUND | Round do evento |
| atacante_id | INTEGER | - | FK → JOGADOR | Jogador atacante |
| vitima_id | INTEGER | - | FK → JOGADOR | Jogador vítima |
| arma_id | INTEGER | - | FK → ARMA | Arma utilizada |
| tick | INTEGER | - | - | Tick do servidor |
| segundos | DECIMAL | 10,4 | - | Segundos no round |
| dano_hp | INTEGER | - | - | Dano em HP |
| dano_armadura | INTEGER | - | - | Dano na armadura |
| hitbox | VARCHAR | 15 | - | Parte do corpo |
| bomba_plantada | BOOLEAN | - | - | Se bomba estava plantada |
| premio | INTEGER | - | - | Prêmio recebido |
| atacante_x | DECIMAL | 15,3 | - | Posição X atacante |
| atacante_y | DECIMAL | 15,3 | - | Posição Y atacante |
| vitima_x | DECIMAL | 15,3 | - | Posição X vítima |
| vitima_y | DECIMAL | 15,3 | - | Posição Y vítima |

---

## 3.3 Domínios Específicos

### Ranks CS:GO (1-18)

| Valor | Rank |
|-------|------|
| 1 | Silver I |
| 2 | Silver II |
| 3 | Silver III |
| 4 | Silver IV |
| 5 | Silver Elite |
| 6 | Silver Elite Master |
| 7 | Gold Nova I |
| 8 | Gold Nova II |
| 9 | Gold Nova III |
| 10 | Gold Nova Master |
| 11 | Master Guardian I |
| 12 | Master Guardian II |
| 13 | Master Guardian Elite |
| 14 | Distinguished Master Guardian |
| 15 | Legendary Eagle |
| 16 | Legendary Eagle Master |
| 17 | Supreme Master First Class |
| 18 | Global Elite |

### Hitboxes

| Valor | Descrição |
|-------|-----------|
| Head | Cabeça |
| Chest | Peito |
| Stomach | Estômago |
| LeftArm | Braço esquerdo |
| RightArm | Braço direito |
| LeftLeg | Perna esquerda |
| RightLeg | Perna direita |

### Tipos de Round

| Valor | Descrição |
|-------|-----------|
| PISTOL_ROUND | Round inicial (só pistolas) |
| ECO | Round econômico |
| SEMI_ECO | Semi-eco (compra parcial) |
| SEMI_BUY | Compra parcial |
| FULL_BUY | Compra completa |
| FORCE_BUY | Compra forçada |

### Tipos de Arma

| Valor | Descrição |
|-------|-----------|
| Pistol | Pistolas |
| Rifle | Rifles |
| SMG | Submetralhadoras |
| Shotgun | Escopetas |
| Sniper | Snipers |
| Machine Gun | Metralhadoras |
| Knife | Faca |
| Grenade | Granadas |
