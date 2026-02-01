# 🎮 Projeto Big Data - CS:GO Matchmaking Analytics

## 📋 Informações do Projeto

| Item | Descrição |
|------|-----------|
| **Disciplina** | Banco de Dados I |
| **Tipo** | Projeto de Engenharia Reversa - Big Data |
| **Base de Dados** | CS:GO Matchmaking Master Demos |
| **Origem** | Kaggle |
| **Total de Registros** | 955.468 linhas |

---

## 📁 Estrutura do Projeto

```
bigdata/
├── README.md                    # Este arquivo
├── descricao.txt               # Descrição original do trabalho
├── base_dados/                 # Dados originais
│   ├── mm_master_demos.csv     # Base completa (955k linhas)
│   └── dezlinhas.csv           # Amostra (10 linhas)
├── docs/                       # Documentação do projeto
│   ├── 01_introducao.md        # Seção 1 - Introdução
│   ├── 02_dicionario_dados.md  # Seção 3 - Dicionário de dados
│   ├── 03_modelo_er.md         # Seção 4 - Modelo ER
│   ├── 04_esquema_relacional.md# Seção 5 - Esquema Relacional
│   ├── 05_normalizacao.md      # Seção 6 - Normalização
│   └── planejamento.md         # Passo a passo do projeto
├── scripts/                    # Scripts de ETL
│   └── etl_processar_dados.py  # Script Python para processar CSV
├── sql/                        # Scripts SQL
│   ├── 01_ddl_criar_tabelas.sql
│   ├── 02_dml_inserir_dados.sql
│   └── 03_consultas_avancadas.sql
├── modelos/                    # Diagramas e modelos
│   └── (diagramas ER)
└── relatorio/                  # Relatório final
    └── relatorio_final.md
```

---

## 🎯 Objetivo

Realizar engenharia reversa em uma base de dados pública de partidas de CS:GO, construindo:
- Modelo Conceitual (MER)
- Modelo Lógico (Esquema Relacional)
- Modelo Físico (DDL SQL)
- Consultas SQL avançadas
- Visualizações gráficas

---

## 🔧 Tecnologias Utilizadas

- **SGBD:** PostgreSQL
- **ETL:** Python + Pandas
- **Visualização:** Apache Superset
- **Modelagem:** brModelo / draw.io

---

## 👥 Equipe

| Nome | RA |
|------|-----|
| [Seu Nome] | [Seu RA] |

---

## 📅 Cronograma

Ver arquivo: `docs/planejamento.md`
