# Seção 5 - Esquema Relacional e Decisões de Mapeamento

## 5.1 Mapeamento MER → Modelo Relacional

### Regras de Mapeamento Aplicadas

| Regra | Descrição | Aplicação |
|-------|-----------|-----------|
| **R1** | Cada entidade vira uma tabela | Todas as 6 entidades |
| **R2** | Atributos simples viram colunas | Todos os atributos |
| **R3** | Chave primária identificada | jogador_id, mapa_id, etc. |
| **R4** | Relacionamento 1:N → FK no lado N | partida.mapa_id, round.partida_id, etc. |
| **R5** | Relacionamento N:M → Tabela associativa | Não aplicável neste modelo |

---

## 5.2 Esquema Relacional

### Notação

```
TABELA (atributo1, atributo2, ..., atributoN)
        ─────────
        Chave Primária sublinhada
        #FK indica Chave Estrangeira
```

### Esquema

```
JOGADOR (jogador_id, steam_id, rank_atual)
         ──────────

MAPA (mapa_id, nome)
      ───────

ARMA (arma_id, nome, tipo)
      ───────

PARTIDA (partida_id, arquivo_demo, #mapa_id, data_hora, rank_medio)
         ──────────

ROUND (round_id, #partida_id, numero, tipo, vencedor_lado, ct_economia, t_economia)
       ────────

EVENTO_DANO (evento_id, #round_id, #atacante_id, #vitima_id, #arma_id, tick, 
             ─────────
             segundos, dano_hp, dano_armadura, hitbox, bomba_plantada, premio,
             atacante_x, atacante_y, vitima_x, vitima_y)
```

---

## 5.3 Decisões de Mapeamento

### Decisão 1: Separação de JOGADOR
**Problema:** Os dados originais têm `att_id` e `vic_id` como colunas separadas.

**Decisão:** Criar uma única tabela JOGADOR com todos os Steam IDs únicos.

**Justificativa:** 
- Evita redundância de dados
- Permite consultar estatísticas por jogador
- Facilita joins para análise

### Decisão 2: Tabela MAPA separada
**Problema:** O mapa aparece como string em cada linha.

**Decisão:** Extrair mapas únicos para tabela separada com FK.

**Justificativa:**
- Normalização (evita repetição do nome do mapa)
- Permite adicionar atributos ao mapa no futuro (ex: tamanho, ano de lançamento)
- Melhora performance com ID numérico

### Decisão 3: Tabela ARMA separada
**Problema:** Arma e tipo de arma aparecem como strings.

**Decisão:** Criar tabela ARMA com nome e tipo.

**Justificativa:**
- Evita redundância de wp_type
- Permite adicionar atributos (preço, dano base, etc.)
- Facilita consultas por tipo de arma

### Decisão 4: Separação de ROUND
**Problema:** Informações do round repetidas em cada evento.

**Decisão:** Criar tabela ROUND com dados únicos por round.

**Justificativa:**
- Dados como `round_type`, `ct_eq_val`, `t_eq_val`, `winner_side` são por round
- Evita redundância massiva
- Melhora integridade dos dados

### Decisão 5: Chaves Primárias Sintéticas
**Problema:** Usar Steam ID como PK seria BIGINT (8 bytes).

**Decisão:** Usar SERIAL (INTEGER auto-incremento) como PK.

**Justificativa:**
- Menor uso de armazenamento em FKs
- Melhor performance em JOINs
- Steam ID mantido como UNIQUE para referência

### Decisão 6: Posições como atributos de EVENTO
**Problema:** Posições X,Y de atacante e vítima.

**Decisão:** Manter como atributos de EVENTO_DANO.

**Justificativa:**
- Posição muda a cada evento
- Não faz sentido criar tabela separada
- Permite análise de heatmaps

---

## 5.4 Diagrama do Esquema Relacional

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│     JOGADOR     │       │      MAPA       │       │      ARMA       │
├─────────────────┤       ├─────────────────┤       ├─────────────────┤
│ PK jogador_id   │       │ PK mapa_id      │       │ PK arma_id      │
│    steam_id     │       │    nome         │       │    nome         │
│    rank_atual   │       └────────┬────────┘       │    tipo         │
└────────┬────────┘                │                └────────┬────────┘
         │                         │ 1                       │
         │                         │                         │
         │                         ▼ N                       │
         │                ┌─────────────────┐                │
         │                │     PARTIDA     │                │
         │                ├─────────────────┤                │
         │                │ PK partida_id   │                │
         │                │    arquivo_demo │                │
         │                │ FK mapa_id ─────┼────────────────┘
         │                │    data_hora    │
         │                │    rank_medio   │
         │                └────────┬────────┘
         │                         │ 1
         │                         │
         │                         ▼ N
         │                ┌─────────────────┐
         │                │      ROUND      │
         │                ├─────────────────┤
         │                │ PK round_id     │
         │                │ FK partida_id   │
         │                │    numero       │
         │                │    tipo         │
         │                │    vencedor_lado│
         │                │    ct_economia  │
         │                │    t_economia   │
         │                └────────┬────────┘
         │                         │ 1
         │                         │
         │                         ▼ N
         │                ┌─────────────────┐
         │   N            │   EVENTO_DANO   │            N
         └───────────────►├─────────────────┤◄───────────────┐
          (atacante_id)   │ PK evento_id    │    (arma_id)   │
          (vitima_id)     │ FK round_id     │                │
                          │ FK atacante_id  │                │
                          │ FK vitima_id    │                │
                          │ FK arma_id ─────┼────────────────┘
                          │    tick         │
                          │    segundos     │
                          │    dano_hp      │
                          │    dano_armadura│
                          │    hitbox       │
                          │    bomba_plantada│
                          │    premio       │
                          │    atacante_x   │
                          │    atacante_y   │
                          │    vitima_x     │
                          │    vitima_y     │
                          └─────────────────┘
```

---

## 5.5 Constraints de Integridade

### Chaves Primárias
- `JOGADOR.jogador_id` - SERIAL
- `MAPA.mapa_id` - SERIAL
- `ARMA.arma_id` - SERIAL
- `PARTIDA.partida_id` - SERIAL
- `ROUND.round_id` - SERIAL
- `EVENTO_DANO.evento_id` - SERIAL

### Chaves Estrangeiras
- `PARTIDA.mapa_id` → `MAPA.mapa_id`
- `ROUND.partida_id` → `PARTIDA.partida_id`
- `EVENTO_DANO.round_id` → `ROUND.round_id`
- `EVENTO_DANO.atacante_id` → `JOGADOR.jogador_id`
- `EVENTO_DANO.vitima_id` → `JOGADOR.jogador_id`
- `EVENTO_DANO.arma_id` → `ARMA.arma_id`

### Unique Constraints
- `JOGADOR.steam_id` - UNIQUE
- `MAPA.nome` - UNIQUE
- `ARMA.nome` - UNIQUE
- `PARTIDA.arquivo_demo` - UNIQUE

### Check Constraints
- `JOGADOR.rank_atual` BETWEEN 1 AND 18
- `ROUND.numero` > 0
- `EVENTO_DANO.dano_hp` >= 0
- `EVENTO_DANO.dano_armadura` >= 0
