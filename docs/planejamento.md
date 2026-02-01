# 📋 Planejamento do Projeto - Passo a Passo

## 🎯 Visão Geral

Este documento descreve o passo a passo completo para execução do projeto de Big Data com a base de CS:GO Matchmaking.

---

## 📊 Fases do Projeto

### ✅ FASE 0 - Preparação Inicial
| # | Tarefa | Status | Observações |
|---|--------|--------|-------------|
| 0.1 | Escolher base de dados | ✅ Concluído | mm_master_demos.csv (Kaggle) |
| 0.2 | Analisar estrutura dos dados | ✅ Concluído | 33 colunas, 955k linhas |
| 0.3 | Criar estrutura de pastas | ✅ Concluído | Estrutura organizada |
| 0.4 | Documentar planejamento | ✅ Concluído | Este documento |

---

### ✅ FASE 1 - Documentação Inicial (Seções 1-3)

| # | Tarefa | Status | Arquivo |
|---|--------|--------|---------|
| 1.1 | Escrever Introdução | ✅ Concluído | `docs/01_introducao.md` |
| 1.2 | Descrever processo de obtenção | ✅ Concluído | `docs/01_introducao.md` |
| 1.3 | Criar Dicionário de Dados | ✅ Concluído | `docs/02_dicionario_dados.md` |

**Entregáveis:**
- Seção 1: Introdução (origem e tipo de dados)
- Seção 2: Obtenção (como obteve e inseriu no SGBD)
- Seção 3: Dicionário de Dados (atributo, domínio, tamanho, descrição)

---

### ✅ FASE 2 - Modelagem Conceitual (Seção 4)

| # | Tarefa | Status | Arquivo |
|---|--------|--------|---------|
| 2.1 | Identificar entidades | ✅ Concluído | `docs/03_modelo_er.md` |
| 2.2 | Definir atributos por entidade | ✅ Concluído | `docs/03_modelo_er.md` |
| 2.3 | Estabelecer relacionamentos | ✅ Concluído | `docs/03_modelo_er.md` |
| 2.4 | Definir cardinalidades | ✅ Concluído | `docs/03_modelo_er.md` |
| 2.5 | Desenhar diagrama MER | ⬜ Pendente | `modelos/diagrama_mer.png` |

**Entidades Propostas:**
1. JOGADOR
2. PARTIDA  
3. MAPA
4. ROUND
5. EVENTO_DANO
6. ARMA

**Ferramentas:** brModelo, draw.io, Lucidchart

---

### ✅ FASE 3 - Mapeamento MER → Relacional (Seção 5)

| # | Tarefa | Status | Arquivo |
|---|--------|--------|---------|
| 3.1 | Mapear entidades para tabelas | ✅ Concluído | `docs/04_esquema_relacional.md` |
| 3.2 | Definir chaves primárias | ✅ Concluído | `docs/04_esquema_relacional.md` |
| 3.3 | Definir chaves estrangeiras | ✅ Concluído | `docs/04_esquema_relacional.md` |
| 3.4 | Documentar decisões de mapeamento | ✅ Concluído | `docs/04_esquema_relacional.md` |
| 3.5 | Criar diagrama relacional | ⬜ Pendente | `modelos/diagrama_relacional.png` |

---

### ✅ FASE 4 - Normalização (Seção 6)

| # | Tarefa | Status | Arquivo |
|---|--------|--------|---------|
| 4.1 | Verificar 1ª Forma Normal (1FN) | ✅ Concluído | `docs/05_normalizacao.md` |
| 4.2 | Verificar 2ª Forma Normal (2FN) | ✅ Concluído | `docs/05_normalizacao.md` |
| 4.3 | Verificar 3ª Forma Normal (3FN) | ✅ Concluído | `docs/05_normalizacao.md` |
| 4.4 | Documentar dependências funcionais | ✅ Concluído | `docs/05_normalizacao.md` |
| 4.5 | Ajustar tabelas se necessário | ✅ Concluído | `docs/05_normalizacao.md` |

---

### ✅ FASE 5 - Implementação Física

| # | Tarefa | Status | Arquivo |
|---|--------|--------|---------|
| 5.1 | Instalar PostgreSQL | ✅ Concluído | - |
| 5.2 | Criar banco de dados | ✅ Concluído | `csgo_analytics` |
| 5.3 | Criar tabelas (DDL) | ✅ Concluído | `sql/01_ddl_criar_tabelas.sql` |
| 5.4 | Criar script ETL Python | ✅ Concluído | `scripts/etl_processar_dados.py` |
| 5.5 | Processar CSV e separar em tabelas | ✅ Concluído | `scripts/etl_processar_dados.py` |
| 5.6 | Gerar dados sintéticos | ✅ Concluído | `scripts/gerar_dados_sinteticos.py` |
| 5.7 | Carregar dados no PostgreSQL | ✅ Concluído | `scripts/carregar_postgres.py` |
| 5.8 | Criar índices | ✅ Concluído | `sql/01_ddl_criar_tabelas.sql` |

---

### ✅ FASE 6 - SQL Avançado (Seção 7)

| # | Tarefa | Status | Arquivo |
|---|--------|--------|---------|
| 6.1 | Consulta com múltiplos JOINs | ✅ Concluído | `sql/03_consultas_avancadas.sql` |
| 6.2 | Subconsultas correlacionadas | ✅ Concluído | `sql/03_consultas_avancadas.sql` |
| 6.3 | CTEs (Common Table Expressions) | ✅ Concluído | `sql/03_consultas_avancadas.sql` |
| 6.4 | Window Functions | ✅ Concluído | `sql/03_consultas_avancadas.sql` |
| 6.5 | Agregações complexas | ✅ Concluído | `sql/03_consultas_avancadas.sql` |
| 6.6 | Views | ✅ Concluído | `sql/03_consultas_avancadas.sql` |

**Consultas executadas com sucesso:**
1. Top 10 jogadores com mais kills ✅
2. Mapas mais jogados ✅
3. Taxa de vitória CT vs T por mapa ✅
4. Armas mais usadas ✅
5. Distribuição de hits por hitbox ✅
6. Distribuição de ranks ✅
7. Headshot % por arma ✅

---

### ✅ FASE 7 - Visualização (Seção 8)

| # | Tarefa | Status | Ferramenta |
|---|--------|--------|------------|
| 7.1 | Gerar gráficos | ✅ Concluído | Python/Matplotlib |
| 7.2 | Registros por tabela | ✅ Concluído | `modelos/graficos/01_registros_por_tabela.png` |
| 7.3 | Mapas mais jogados | ✅ Concluído | `modelos/graficos/02_mapas_mais_jogados.png` |
| 7.4 | CT vs Terrorist | ✅ Concluído | `modelos/graficos/03_ct_vs_t.png` |
| 7.5 | Armas mais usadas | ✅ Concluído | `modelos/graficos/04_armas_mais_usadas.png` |
| 7.6 | Hits por hitbox | ✅ Concluído | `modelos/graficos/05_hits_por_hitbox.png` |
| 7.7 | Distribuição de ranks | ✅ Concluído | `modelos/graficos/06_distribuicao_ranks.png` |
| 7.8 | Headshot por arma | ✅ Concluído | `modelos/graficos/07_headshot_por_arma.png` |

---

### 📄 FASE 8 - Documentação Final

| # | Tarefa | Status | Arquivo |
|---|--------|--------|---------|
| 8.1 | Compilar relatório final | ⬜ Pendente | `relatorio/relatorio_final.md` |
| 8.2 | Adicionar capa e formatação | ⬜ Pendente | `relatorio/relatorio_final.md` |
| 8.3 | Revisar documento | ⬜ Pendente | - |
| 8.4 | Exportar para PDF | ⬜ Pendente | - |

---

### 🎤 FASE 9 - Apresentação

| # | Tarefa | Status | Observações |
|---|--------|--------|-------------|
| 9.1 | Criar slides | ⬜ Pendente | PowerPoint/Google Slides |
| 9.2 | Ensaiar apresentação | ⬜ Pendente | Máx. 10 minutos |
| 9.3 | Preparar demo ao vivo | ⬜ Pendente | Opcional |

---

## 📅 Cronograma Sugerido

| Semana | Fases | Entregas |
|--------|-------|----------|
| 1 | Fase 0, 1 | Documentação inicial |
| 2 | Fase 2, 3 | Modelos conceitual e lógico |
| 3 | Fase 4, 5 | Normalização e implementação |
| 4 | Fase 6, 7 | SQL e visualizações |
| 5 | Fase 8, 9 | Relatório e apresentação |

---

## 🛠️ Ferramentas Necessárias

| Ferramenta | Uso | Status |
|------------|-----|--------|
| PostgreSQL 15+ | SGBD | ⬜ Instalar |
| Python 3.10+ | ETL | ⬜ Verificar |
| Pandas | Processamento CSV | ⬜ Instalar |
| psycopg2 | Conexão Python-PostgreSQL | ⬜ Instalar |
| brModelo / draw.io | Diagramas ER | ⬜ Escolher |
| Apache Superset | Visualização | ⬜ Instalar (Docker) |
| VS Code | Editor | ✅ OK |

---

## 📝 Notas Importantes

1. **Dados sintéticos:** Se alguma tabela ficar com menos de 10.000 linhas, usar ChatGPT para gerar dados sintéticos
2. **Backup:** Fazer backup dos scripts e dados regularmente
3. **Versionamento:** Considerar usar Git para versionar o projeto
4. **Apresentação:** Máximo 10 minutos - ser objetivo e focar nos pontos principais
