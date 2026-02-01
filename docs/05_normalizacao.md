# Seção 6 - Normalização

## 6.1 Análise da Base Original (Não Normalizada)

A tabela original `mm_master_demos` apresenta os seguintes problemas de normalização:

### Problemas Identificados

| Problema | Descrição | Exemplo |
|----------|-----------|---------|
| **Redundância de Mapa** | Nome do mapa repetido em cada linha | "de_dust2" aparece milhares de vezes |
| **Redundância de Arma** | Nome e tipo da arma repetidos | "USP", "Pistol" repetidos |
| **Redundância de Partida** | Dados da partida em cada evento | arquivo_demo, date, rank_medio |
| **Redundância de Round** | Dados do round em cada evento | round_type, ct_eq_val, t_eq_val |
| **Dependência Transitiva** | wp_type depende de wp, não da PK | AK-47 → Rifle |

---

## 6.2 Primeira Forma Normal (1FN)

### Requisitos da 1FN:
1. ✅ Todos os atributos contêm valores atômicos
2. ✅ Não há grupos repetitivos
3. ✅ Existe uma chave primária

### Análise:

A tabela original **já está em 1FN** porque:
- Cada célula contém um único valor (atômico)
- Não há arrays ou listas em nenhum campo
- Cada linha pode ser identificada pela combinação de campos

### Verificação:

| Atributo | Atômico? | Observação |
|----------|----------|------------|
| file | ✅ Sim | Valor único |
| map | ✅ Sim | Valor único |
| date | ✅ Sim | Timestamp único |
| hitbox | ✅ Sim | Uma parte do corpo |
| wp | ✅ Sim | Uma arma |
| ... | ✅ Sim | Todos atômicos |

**Conclusão: Tabela original em 1FN** ✅

---

## 6.3 Segunda Forma Normal (2FN)

### Requisitos da 2FN:
1. ✅ Estar em 1FN
2. ✅ Não ter dependências parciais (atributos dependem da PK inteira)

### Análise:

Se considerarmos a PK composta como `(file, round, tick, att_id, vic_id)`:

| Atributo | Depende de toda PK? | Problema |
|----------|---------------------|----------|
| map | ❌ Depende só de `file` | Dependência parcial |
| date | ❌ Depende só de `file` | Dependência parcial |
| round_type | ❌ Depende de `file` + `round` | Dependência parcial |
| wp_type | ❌ Depende só de `wp` | Dependência parcial |
| avg_match_rank | ❌ Depende só de `file` | Dependência parcial |

### Solução - Decomposição:

Para atingir 2FN, separamos em tabelas:

```
PARTIDA (partida_id, arquivo_demo, mapa_id, data_hora, rank_medio)
         ──────────
         Atributos que dependem apenas da partida

ROUND (round_id, partida_id, numero, tipo, vencedor_lado, ct_economia, t_economia)
       ────────
       Atributos que dependem da partida + round

ARMA (arma_id, nome, tipo)
      ───────
      Atributos que dependem apenas da arma

EVENTO_DANO (evento_id, round_id, atacante_id, vitima_id, arma_id, ...)
             ─────────
             Atributos que dependem do evento específico
```

**Conclusão: Modelo proposto em 2FN** ✅

---

## 6.4 Terceira Forma Normal (3FN)

### Requisitos da 3FN:
1. ✅ Estar em 2FN
2. ✅ Não ter dependências transitivas

### Análise de Dependências Transitivas:

| Dependência | Tipo | Problema |
|-------------|------|----------|
| `evento_id → arma_id → tipo` | Transitiva | tipo depende de arma, não do evento |
| `evento_id → atacante_id → rank` | Transitiva | rank depende do jogador |

### Solução:

As tabelas propostas já eliminam as dependências transitivas:

```
ARMA (arma_id, nome, tipo)
      ───────
      tipo depende diretamente de arma_id (PK)

JOGADOR (jogador_id, steam_id, rank_atual)
         ──────────
         rank depende diretamente de jogador_id (PK)
```

### Verificação Final das Tabelas:

#### JOGADOR
```
jogador_id → steam_id, rank_atual
```
- Sem dependências transitivas ✅

#### MAPA
```
mapa_id → nome
```
- Sem dependências transitivas ✅

#### ARMA
```
arma_id → nome, tipo
```
- `tipo` depende funcionalmente de `arma_id` (cada arma tem um tipo fixo) ✅

#### PARTIDA
```
partida_id → arquivo_demo, mapa_id, data_hora, rank_medio
```
- Sem dependências transitivas ✅

#### ROUND
```
round_id → partida_id, numero, tipo, vencedor_lado, ct_economia, t_economia
```
- Sem dependências transitivas ✅

#### EVENTO_DANO
```
evento_id → round_id, atacante_id, vitima_id, arma_id, tick, segundos, 
            dano_hp, dano_armadura, hitbox, bomba_plantada, premio,
            atacante_x, atacante_y, vitima_x, vitima_y
```
- Todos os atributos dependem diretamente de evento_id ✅

**Conclusão: Modelo proposto em 3FN** ✅

---

## 6.5 Resumo da Normalização

### Antes (Tabela Original)
```
mm_master_demos (33 colunas, 955.468 linhas)
├── Redundância de mapa: ~950k repetições
├── Redundância de partida: ~15k partidas × 63 linhas média
├── Redundância de arma: ~35 armas × milhares de repetições
└── Dependências transitivas: wp → wp_type
```

### Depois (Modelo Normalizado)
```
JOGADOR (~50.000 linhas)
MAPA (~10 linhas)
ARMA (~35 linhas)
PARTIDA (~15.000 linhas)
ROUND (~300.000 linhas)
EVENTO_DANO (955.468 linhas)
```

### Benefícios Obtidos

| Benefício | Descrição |
|-----------|-----------|
| **Menos Redundância** | Dados não repetidos desnecessariamente |
| **Integridade** | FKs garantem consistência |
| **Manutenção** | Atualizar mapa/arma em um só lugar |
| **Performance** | Índices em IDs numéricos |
| **Flexibilidade** | Fácil adicionar atributos às entidades |

---

## 6.6 Dependências Funcionais

### Diagrama de Dependências

```
JOGADOR:
  jogador_id → {steam_id, rank_atual}
  steam_id → {jogador_id}  (candidata)

MAPA:
  mapa_id → {nome}
  nome → {mapa_id}  (candidata)

ARMA:
  arma_id → {nome, tipo}
  nome → {arma_id, tipo}  (candidata)

PARTIDA:
  partida_id → {arquivo_demo, mapa_id, data_hora, rank_medio}
  arquivo_demo → {partida_id}  (candidata)

ROUND:
  round_id → {partida_id, numero, tipo, vencedor_lado, ct_economia, t_economia}
  (partida_id, numero) → {round_id}  (candidata)

EVENTO_DANO:
  evento_id → {round_id, atacante_id, vitima_id, arma_id, tick, segundos,
               dano_hp, dano_armadura, hitbox, bomba_plantada, premio,
               atacante_x, atacante_y, vitima_x, vitima_y}
```
