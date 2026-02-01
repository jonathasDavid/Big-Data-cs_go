"""
============================================
PROJETO BIG DATA - CS:GO MATCHMAKING
Gerar Diagrama ER usando Matplotlib
============================================
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import os

# Pasta para salvar
PASTA_MODELOS = '../modelos/'
os.makedirs(PASTA_MODELOS, exist_ok=True)

def criar_diagrama_er():
    """Cria diagrama ER usando Matplotlib."""
    
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 12)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Cores
    cor_entidade = '#4A90D9'
    cor_texto = 'white'
    cor_pk = '#FFD700'
    cor_fk = '#90EE90'
    
    def desenhar_entidade(x, y, nome, atributos, width=2.8, height=None):
        """Desenha uma entidade (retângulo com atributos)."""
        if height is None:
            height = 0.4 + len(atributos) * 0.35
        
        # Caixa principal
        rect = FancyBboxPatch((x - width/2, y - height/2), width, height,
                              boxstyle="round,pad=0.05,rounding_size=0.1",
                              facecolor=cor_entidade, edgecolor='#2C5F8A', linewidth=2)
        ax.add_patch(rect)
        
        # Nome da entidade
        ax.text(x, y + height/2 - 0.25, nome, ha='center', va='center',
                fontsize=11, fontweight='bold', color=cor_texto)
        
        # Linha separadora
        ax.plot([x - width/2 + 0.1, x + width/2 - 0.1], 
                [y + height/2 - 0.45, y + height/2 - 0.45], 
                color='white', linewidth=1)
        
        # Atributos
        for i, (attr, tipo) in enumerate(atributos):
            y_attr = y + height/2 - 0.65 - i * 0.35
            
            # Cor do marcador baseado no tipo
            if tipo == 'PK':
                marker_color = cor_pk
                prefix = '[PK] '
            elif tipo == 'FK':
                marker_color = cor_fk
                prefix = '[FK] '
            else:
                marker_color = 'white'
                prefix = '     '
            
            ax.text(x - width/2 + 0.15, y_attr, prefix + attr, 
                    ha='left', va='center', fontsize=9, color=cor_texto)
    
    def desenhar_relacionamento(x1, y1, x2, y2, label1, label2):
        """Desenha linha de relacionamento entre entidades."""
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='-', color='#333', lw=1.5))
        
        # Labels de cardinalidade
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        
        # Posicionar labels perto das entidades
        ax.text(x1 + (x2-x1)*0.15, y1 + (y2-y1)*0.15, label1, 
                fontsize=10, fontweight='bold', color='#333')
        ax.text(x2 - (x2-x1)*0.15, y2 - (y2-y1)*0.15, label2, 
                fontsize=10, fontweight='bold', color='#333')
    
    # ========================================
    # DESENHAR ENTIDADES
    # ========================================
    
    # MAPA (topo esquerda)
    desenhar_entidade(3, 10, 'MAPA', [
        ('mapa_id', 'PK'),
        ('nome', '')
    ])
    
    # JOGADOR (topo direita)
    desenhar_entidade(13, 10, 'JOGADOR', [
        ('jogador_id', 'PK'),
        ('steam_id', ''),
        ('rank_atual', '')
    ])
    
    # ARMA (direita meio)
    desenhar_entidade(13, 6, 'ARMA', [
        ('arma_id', 'PK'),
        ('nome', ''),
        ('tipo', '')
    ])
    
    # PARTIDA (esquerda meio)
    desenhar_entidade(3, 6.5, 'PARTIDA', [
        ('partida_id', 'PK'),
        ('arquivo_demo', ''),
        ('mapa_id', 'FK'),
        ('data_hora', ''),
        ('rank_medio', '')
    ])
    
    # ROUND (centro)
    desenhar_entidade(7, 4, 'ROUND', [
        ('round_id', 'PK'),
        ('partida_id', 'FK'),
        ('numero', ''),
        ('tipo', ''),
        ('vencedor_lado', ''),
        ('ct_economia', ''),
        ('t_economia', '')
    ])
    
    # EVENTO_DANO (baixo centro)
    desenhar_entidade(10, 1.5, 'EVENTO_DANO', [
        ('evento_id', 'PK'),
        ('round_id', 'FK'),
        ('atacante_id', 'FK'),
        ('vitima_id', 'FK'),
        ('arma_id', 'FK'),
        ('tick', ''),
        ('dano_hp', ''),
        ('hitbox', ''),
        ('...', '')
    ], width=3)
    
    # ========================================
    # DESENHAR RELACIONAMENTOS
    # ========================================
    
    # MAPA -> PARTIDA (1:N)
    desenhar_relacionamento(3, 9.2, 3, 8.3, '1', 'N')
    
    # PARTIDA -> ROUND (1:N)
    desenhar_relacionamento(4.4, 5.5, 5.6, 4.5, '1', 'N')
    
    # ROUND -> EVENTO_DANO (1:N)
    desenhar_relacionamento(8.4, 3, 8.6, 2.5, '1', 'N')
    
    # JOGADOR -> EVENTO_DANO (1:N) - atacante
    desenhar_relacionamento(13, 9, 11.2, 3.2, '1', 'N')
    
    # ARMA -> EVENTO_DANO (1:N)
    desenhar_relacionamento(13, 4.8, 11.2, 2.5, '1', 'N')
    
    # ========================================
    # LEGENDA
    # ========================================
    
    # Caixa de legenda
    legend_x, legend_y = 0.5, 1.5
    ax.add_patch(FancyBboxPatch((legend_x, legend_y), 2.5, 1.5,
                                boxstyle="round,pad=0.05",
                                facecolor='white', edgecolor='gray', linewidth=1))
    ax.text(legend_x + 1.25, legend_y + 1.3, 'Legenda', ha='center', 
            fontsize=10, fontweight='bold')
    ax.text(legend_x + 0.1, legend_y + 0.9, '[PK] Chave Primaria', fontsize=9)
    ax.text(legend_x + 0.1, legend_y + 0.5, '[FK] Chave Estrangeira', fontsize=9)
    ax.text(legend_x + 0.1, legend_y + 0.1, '1:N = Um para Muitos', fontsize=9)
    
    # Título
    ax.text(8, 11.5, 'Modelo Entidade-Relacionamento\nCS:GO Matchmaking Analytics', 
            ha='center', va='center', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'{PASTA_MODELOS}diagrama_er.png', dpi=200, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    
    print(f"✅ Diagrama ER salvo em: {PASTA_MODELOS}diagrama_er.png")


def criar_diagrama_relacional():
    """Cria diagrama do esquema relacional."""
    
    fig, ax = plt.subplots(1, 1, figsize=(18, 10))
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Cores
    cor_tabela = '#2C3E50'
    cor_header = '#3498DB'
    cor_pk = '#F1C40F'
    cor_fk = '#2ECC71'
    
    def desenhar_tabela(x, y, nome, colunas, width=3):
        """Desenha uma tabela do esquema relacional."""
        height = 0.5 + len(colunas) * 0.35
        
        # Cabeçalho
        header = FancyBboxPatch((x, y), width, 0.45,
                               boxstyle="round,pad=0.02,rounding_size=0.05",
                               facecolor=cor_header, edgecolor='#2980B9', linewidth=2)
        ax.add_patch(header)
        ax.text(x + width/2, y + 0.22, nome, ha='center', va='center',
                fontsize=11, fontweight='bold', color='white')
        
        # Corpo
        body = FancyBboxPatch((x, y - height + 0.45), width, height - 0.45,
                             boxstyle="round,pad=0.02,rounding_size=0.05",
                             facecolor='white', edgecolor='#BDC3C7', linewidth=1)
        ax.add_patch(body)
        
        # Colunas
        for i, (col, tipo, constraint) in enumerate(colunas):
            y_col = y - 0.1 - i * 0.35
            
            # Ícone baseado no constraint
            if constraint == 'PK':
                icon = '[PK]'
                col_color = '#C0392B'
            elif constraint == 'FK':
                icon = '[FK]'
                col_color = '#27AE60'
            else:
                icon = '    '
                col_color = '#333'
            
            ax.text(x + 0.1, y_col, f"{icon} {col}", 
                    ha='left', va='center', fontsize=9, color=col_color)
            ax.text(x + width - 0.1, y_col, tipo, 
                    ha='right', va='center', fontsize=8, color='#777')
        
        return height
    
    # ========================================
    # DESENHAR TABELAS
    # ========================================
    
    # Linha 1
    desenhar_tabela(0.5, 9, 'JOGADOR', [
        ('jogador_id', 'SERIAL', 'PK'),
        ('steam_id', 'BIGINT', ''),
        ('rank_atual', 'INTEGER', '')
    ])
    
    desenhar_tabela(4.5, 9, 'MAPA', [
        ('mapa_id', 'SERIAL', 'PK'),
        ('nome', 'VARCHAR(50)', '')
    ])
    
    desenhar_tabela(8.5, 9, 'ARMA', [
        ('arma_id', 'SERIAL', 'PK'),
        ('nome', 'VARCHAR(50)', ''),
        ('tipo', 'VARCHAR(20)', '')
    ])
    
    # Linha 2
    desenhar_tabela(2.5, 5.5, 'PARTIDA', [
        ('partida_id', 'SERIAL', 'PK'),
        ('arquivo_demo', 'VARCHAR(100)', ''),
        ('mapa_id', 'INTEGER', 'FK'),
        ('data_hora', 'TIMESTAMP', ''),
        ('rank_medio', 'DECIMAL', '')
    ])
    
    desenhar_tabela(7, 5.5, 'ROUND', [
        ('round_id', 'SERIAL', 'PK'),
        ('partida_id', 'INTEGER', 'FK'),
        ('numero', 'INTEGER', ''),
        ('tipo', 'VARCHAR(20)', ''),
        ('vencedor_lado', 'VARCHAR(20)', ''),
        ('ct_economia', 'INTEGER', ''),
        ('t_economia', 'INTEGER', '')
    ])
    
    # Linha 3
    desenhar_tabela(4, 1.5, 'EVENTO_DANO', [
        ('evento_id', 'SERIAL', 'PK'),
        ('round_id', 'INTEGER', 'FK'),
        ('atacante_id', 'INTEGER', 'FK'),
        ('vitima_id', 'INTEGER', 'FK'),
        ('arma_id', 'INTEGER', 'FK'),
        ('tick', 'INTEGER', ''),
        ('dano_hp', 'INTEGER', ''),
        ('hitbox', 'VARCHAR(20)', ''),
        ('bomba_plantada', 'BOOLEAN', ''),
        ('...', '...', '')
    ], width=3.5)
    
    # ========================================
    # DESENHAR CONEXÕES (FKs)
    # ========================================
    
    # Estilo das setas
    arrow_style = dict(arrowstyle='->', color='#E74C3C', lw=1.5, 
                       connectionstyle='arc3,rad=0.1')
    
    # MAPA -> PARTIDA
    ax.annotate('', xy=(4, 5.3), xytext=(5.5, 8.2),
                arrowprops=arrow_style)
    
    # PARTIDA -> ROUND
    ax.annotate('', xy=(7, 4.8), xytext=(5.5, 4.8),
                arrowprops=arrow_style)
    
    # ROUND -> EVENTO_DANO
    ax.annotate('', xy=(5.5, 2.5), xytext=(7.5, 2.8),
                arrowprops=arrow_style)
    
    # JOGADOR -> EVENTO_DANO (atacante)
    ax.annotate('', xy=(5.2, 2.2), xytext=(2, 8),
                arrowprops=dict(arrowstyle='->', color='#E74C3C', lw=1.5,
                               connectionstyle='arc3,rad=-0.2'))
    
    # ARMA -> EVENTO_DANO
    ax.annotate('', xy=(7.2, 1.8), xytext=(9.5, 7.5),
                arrowprops=dict(arrowstyle='->', color='#E74C3C', lw=1.5,
                               connectionstyle='arc3,rad=0.2'))
    
    # Título
    ax.text(9, 9.7, 'Esquema Relacional - CS:GO Matchmaking Analytics', 
            ha='center', va='center', fontsize=14, fontweight='bold')
    
    # Legenda
    ax.text(13, 5, 'Legenda:', fontsize=10, fontweight='bold')
    ax.text(13, 4.5, '[PK] Chave Primaria', fontsize=9)
    ax.text(13, 4.1, '[FK] Chave Estrangeira', fontsize=9)
    ax.text(13, 3.7, '-> Referencia FK', fontsize=9, color='#E74C3C')
    
    plt.tight_layout()
    plt.savefig(f'{PASTA_MODELOS}diagrama_relacional.png', dpi=200, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    
    print(f"✅ Diagrama Relacional salvo em: {PASTA_MODELOS}diagrama_relacional.png")


def main():
    print("=" * 50)
    print("📊 GERANDO DIAGRAMAS")
    print("=" * 50)
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    criar_diagrama_er()
    criar_diagrama_relacional()
    
    print("\n✅ Diagramas gerados com sucesso!")


if __name__ == "__main__":
    main()
