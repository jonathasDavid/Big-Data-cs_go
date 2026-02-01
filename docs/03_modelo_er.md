# Seção 4 - Modelo Entidade-Relacionamento (MER)

## 4.1 Entidades Identificadas

### Lista de Entidades

| # | Entidade | Descrição | Quantidade Estimada |
|---|----------|-----------|---------------------|
| 1 | **JOGADOR** | Jogadores únicos identificados por Steam ID | ~50.000+ |
| 2 | **MAPA** | Mapas disponíveis no jogo | ~10 |
| 3 | **ARMA** | Armas disponíveis no jogo | ~35 |
| 4 | **PARTIDA** | Partidas únicas (arquivos demo) | ~15.000+ |
| 5 | **ROUND** | Rounds jogados em cada partida | ~300.000+ |
| 6 | **EVENTO_DANO** | Eventos de dano registrados | 955.468 |

---

## 4.2 Atributos por Entidade

### JOGADOR
```
JOGADOR
├── jogador_id (PK)
├── steam_id (UNIQUE)
└── rank_atual
```

### MAPA
```
MAPA
├── mapa_id (PK)
└── nome (UNIQUE)
```

### ARMA
```
ARMA
├── arma_id (PK)
├── nome (UNIQUE)
└── tipo
```

### PARTIDA
```
PARTIDA
├── partida_id (PK)
├── arquivo_demo (UNIQUE)
├── mapa_id (FK)
├── data_hora
└── rank_medio
```

### ROUND
```
ROUND
├── round_id (PK)
├── partida_id (FK)
├── numero
├── tipo
├── vencedor_lado
├── ct_economia
└── t_economia
```

### EVENTO_DANO
```
EVENTO_DANO
├── evento_id (PK)
├── round_id (FK)
├── atacante_id (FK)
├── vitima_id (FK)
├── arma_id (FK)
├── tick
├── segundos
├── dano_hp
├── dano_armadura
├── hitbox
├── bomba_plantada
├── premio
├── atacante_x
├── atacante_y
├── vitima_x
└── vitima_y
```

---

## 4.3 Relacionamentos

### Diagrama de Relacionamentos

```
                         ┌─────────────┐
                         │    MAPA     │
                         │─────────────│
                         │ mapa_id (PK)│
                         │ nome        │
                         └──────┬──────┘
                                │
                                │ 1
                                │
                                ▼ N
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   JOGADOR   │         │   PARTIDA   │         │    ARMA     │
│─────────────│         │─────────────│         │─────────────│
│jogador_id PK│         │partida_id PK│         │ arma_id (PK)│
│ steam_id    │         │arquivo_demo │         │ nome        │
│ rank_atual  │         │ mapa_id (FK)│         │ tipo        │
└──────┬──────┘         │ data_hora   │         └──────┬──────┘
       │                │ rank_medio  │                │
       │                └──────┬──────┘                │
       │                       │                       │
       │                       │ 1                     │
       │                       │                       │
       │                       ▼ N                     │
       │                ┌─────────────┐                │
       │                │    ROUND    │                │
       │                │─────────────│                │
       │                │round_id (PK)│                │
       │                │partida_id FK│                │
       │                │ numero      │                │
       │                │ tipo        │                │
       │                │vencedor_lado│                │
       │                │ ct_economia │                │
       │                │ t_economia  │                │
       │                └──────┬──────┘                │
       │                       │                       │
       │                       │ 1                     │
       │                       │                       │
       │                       ▼ N                     │
       │                ┌─────────────┐                │
       │       N        │ EVENTO_DANO │        N       │
       └───────────────►│─────────────│◄───────────────┘
        (atacante)      │evento_id PK │    (arma)
        (vitima)        │round_id  FK │
                        │atacante_id  │
                        │vitima_id    │
                        │arma_id   FK │
                        │ tick        │
                        │ segundos    │
                        │ dano_hp     │
                        │ dano_armad. │
                        │ hitbox      │
                        │ bomba_plant.│
                        │ premio      │
                        │ atacante_x  │
                        │ atacante_y  │
                        │ vitima_x    │
                        │ vitima_y    │
                        └─────────────┘
```

---

## 4.4 Descrição dos Relacionamentos

| Relacionamento | Entidades | Cardinalidade | Descrição |
|----------------|-----------|---------------|-----------|
| PARTIDA-MAPA | PARTIDA ↔ MAPA | N:1 | Uma partida ocorre em um mapa; um mapa pode ter várias partidas |
| PARTIDA-ROUND | PARTIDA ↔ ROUND | 1:N | Uma partida tem vários rounds; um round pertence a uma partida |
| ROUND-EVENTO | ROUND ↔ EVENTO_DANO | 1:N | Um round tem vários eventos; um evento pertence a um round |
| EVENTO-ATACANTE | EVENTO_DANO ↔ JOGADOR | N:1 | Um evento tem um atacante; um jogador pode ser atacante em vários eventos |
| EVENTO-VITIMA | EVENTO_DANO ↔ JOGADOR | N:1 | Um evento tem uma vítima; um jogador pode ser vítima em vários eventos |
| EVENTO-ARMA | EVENTO_DANO ↔ ARMA | N:1 | Um evento usa uma arma; uma arma pode ser usada em vários eventos |

---

## 4.5 Diagrama ER (Notação Chen)

*[Inserir diagrama criado no brModelo ou draw.io]*

### Instruções para criar no brModelo:

1. Criar entidades: JOGADOR, MAPA, ARMA, PARTIDA, ROUND, EVENTO_DANO
2. Adicionar atributos conforme seção 4.2
3. Criar relacionamentos conforme seção 4.4
4. Definir cardinalidades
5. Exportar como imagem PNG

### Instruções para criar no draw.io:

1. Acessar https://draw.io
2. Usar shapes de ER (Entity Relationship)
3. Retângulos para entidades
4. Losangos para relacionamentos
5. Elipses para atributos
6. Exportar para `modelos/diagrama_mer.png`
