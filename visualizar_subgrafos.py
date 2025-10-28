"""
Visualização de Subgrafos Específicos
Gera imagens individuais para os subgrafos MQB, Small Wide e PL71
"""

import matplotlib.pyplot as plt
import networkx as nx
from main import Graph

def criar_subgrafo_pq35():
    """
    Subgrafo 1: Grupo Volkswagen-Audi (Plataforma PQ35)
    """
    vertices = ["VW Golf Mk6", "Audi A3 8P", "VW Polo Mk5", "Audi TT Mk2"]
    
    # Peças compartilhadas entre cada par
    pecas_dict = {
        ("VW Golf Mk6", "Audi A3 8P"): [
            "Transmissão DSG DQ250",
            "Plataforma PQ35",
            "Sistema ABS Bosch",
            "Central Multimídia MIB"
        ],
        ("VW Golf Mk6", "VW Polo Mk5"): [
            "Sistema ABS Bosch"
        ],
        ("VW Golf Mk6", "Audi TT Mk2"): [
            "Motor EA888 2.0T",
            "Transmissão DSG DQ250",
            "Plataforma PQ35",
            "Sistema ABS Bosch"
        ],
        ("Audi A3 8P", "VW Polo Mk5"): [
            "Motor EA111 1.6",
            "Sistema ABS Bosch"
        ],
        ("Audi A3 8P", "Audi TT Mk2"): [
            "Transmissão DSG DQ250",
            "Plataforma PQ35",
            "Sistema ABS Bosch"
        ],
        ("VW Polo Mk5", "Audi TT Mk2"): [
            "Sistema ABS Bosch"
        ]
    }
    
    edges = list(pecas_dict.keys())
    weights = {edge: len(pecas) for edge, pecas in pecas_dict.items()}
    
    return Graph(vertices, edges, weights), pecas_dict

def criar_subgrafo_mqb():
    """
    Subgrafo 2: Grupo Volkswagen-Audi (Plataforma MQB)
    """
    vertices = ["VW Golf Mk7", "Audi A3 8V"]
    
    # Peças compartilhadas
    pecas_comuns = [
        "Motor EA888 2.0T",
        "Transmissão DSG DQ250",
        "Plataforma MQB",
        "Sistema ABS Bosch",
        "Central Multimídia MIB"
    ]
    
    edges = [(vertices[0], vertices[1])]
    weights = {edges[0]: len(pecas_comuns)}
    
    return Graph(vertices, edges, weights), pecas_comuns

def criar_subgrafo_small_wide():
    """
    Subgrafo 5: Grupo Stellantis (Plataforma Small Wide 4x4)
    """
    vertices = ["Jeep Compass", "Fiat Toro", "Jeep Renegade"]
    
    # Peças compartilhadas entre cada par
    pecas_dict = {
        ("Jeep Compass", "Fiat Toro"): [
            "Motor Tigershark 2.4",
            "Transmissão Aisin 6F24",
            "Plataforma Small Wide 4x4",
            "Sistema ABS Bosch"
        ],
        ("Jeep Compass", "Jeep Renegade"): [
            "Motor Tigershark 2.4",
            "Transmissão Aisin 6F24",
            "Plataforma Small Wide 4x4",
            "Sistema ABS Bosch"
        ],
        ("Fiat Toro", "Jeep Renegade"): [
            "Motor Tigershark 2.4",
            "Transmissão Aisin 6F24",
            "Plataforma Small Wide 4x4",
            "Sistema ABS Bosch"
        ]
    }
    
    edges = list(pecas_dict.keys())
    weights = {edge: len(pecas) for edge, pecas in pecas_dict.items()}
    
    return Graph(vertices, edges, weights), pecas_dict

def criar_subgrafo_pl71():
    """
    Subgrafo 7: Plataforma PL71 (SUVs Premium VW Group)
    """
    vertices = ["Audi Q7 4L", "VW Touareg 7L", "Porsche Cayenne"]
    
    # Peças compartilhadas entre cada par
    pecas_dict = {
        ("Porsche Cayenne", "Audi Q7 4L"): [
            "Motor VR6 3.6",
            "Plataforma PL71",
            "Sistema ABS Bosch",
            "Suspensão Multilink",
            "Turbocompressor KKK"
        ],
        ("Porsche Cayenne", "VW Touareg 7L"): [
            "Motor VR6 3.6",
            "Plataforma PL71",
            "Sistema ABS Bosch",
            "Suspensão Multilink",
            "Turbocompressor KKK"
        ],
        ("Audi Q7 4L", "VW Touareg 7L"): [
            "Motor VR6 3.6",
            "Plataforma PL71",
            "Sistema ABS Bosch",
            "Suspensão Multilink",
            "Turbocompressor KKK"
        ]
    }
    
    edges = list(pecas_dict.keys())
    weights = {edge: len(pecas) for edge, pecas in pecas_dict.items()}
    
    return Graph(vertices, edges, weights), pecas_dict

def visualizar_subgrafo(g: Graph, titulo: str, pecas_info, arquivo: str, cor='#2ca02c'):
    """
    Visualiza um subgrafo específico
    """
    # Criar grafo NetworkX
    Gnx = nx.Graph()
    Gnx.add_nodes_from(g.vertices)
    
    for edge in g.edges:
        u, v = edge
        weight = g.weights.get(edge, 1)
        Gnx.add_edge(u, v, weight=weight)
    
    # Configurar figura
    plt.figure(figsize=(12, 10))
    
    # Layout circular para melhor visualização
    if len(g.vertices) == 2:
        pos = nx.spring_layout(Gnx, k=3, iterations=50)
    else:
        pos = nx.circular_layout(Gnx)
    
    # Desenhar nós
    nx.draw_networkx_nodes(Gnx, pos, node_color=cor, node_size=3000, alpha=0.9)
    nx.draw_networkx_labels(Gnx, pos, font_size=10, font_weight='bold')
    
    # Desenhar arestas com espessura proporcional ao peso
    edges = Gnx.edges()
    weights = [Gnx[u][v]['weight'] for u, v in edges]
    nx.draw_networkx_edges(Gnx, pos, width=[w*1.5 for w in weights], alpha=0.6, edge_color=cor)
    
    # Adicionar labels nas arestas com o número de peças
    edge_labels = {edge: f"{Gnx[edge[0]][edge[1]]['weight']} peças" for edge in edges}
    nx.draw_networkx_edge_labels(Gnx, pos, edge_labels, font_size=9)
    
    plt.title(titulo, fontsize=14, fontweight='bold', pad=20)
    plt.axis('off')
    
    # Adicionar informações sobre as peças
    info_text = "Peças Compartilhadas:\n\n"
    
    if isinstance(pecas_info, list):
        # Para subgrafo com 2 vértices (MQB)
        info_text += "\n".join([f"• {peca}" for peca in pecas_info])
    else:
        # Para subgrafos com múltiplos pares (Small Wide, PL71)
        for i, (edge, pecas) in enumerate(pecas_info.items()):
            u, v = edge
            info_text += f"\n{u} ↔ {v}:\n"
            info_text += "\n".join([f"  • {peca}" for peca in pecas])
            if i < len(pecas_info) - 1:
                info_text += "\n"
    
    # Adicionar caixa de texto
    plt.text(0.02, 0.98, info_text, transform=plt.gcf().transFigure, 
             fontsize=9, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig(arquivo, dpi=300, bbox_inches='tight')
    print(f"Imagem salva: {arquivo}")
    plt.close()

def main():
    """
    Gera as quatro visualizações de subgrafos
    """
    print("="*80)
    print("GERAÇÃO DE VISUALIZAÇÕES DE SUBGRAFOS")
    print("="*80)
    
    # Subgrafo PQ35
    print("\n1. Gerando subgrafo PQ35 (Volkswagen-Audi)...")
    g_pq35, pecas_pq35 = criar_subgrafo_pq35()
    visualizar_subgrafo(
        g_pq35,
        "Subgrafo PQ35: Volkswagen-Audi (Plataforma Histórica)",
        pecas_pq35,
        "subgrafo_pq35.png",
        cor='#1f77b4'
    )
    
    # Subgrafo MQB
    print("\n2. Gerando subgrafo MQB (Volkswagen-Audi)...")
    g_mqb, pecas_mqb = criar_subgrafo_mqb()
    visualizar_subgrafo(
        g_mqb,
        "Subgrafo MQB: Volkswagen-Audi (Plataforma Modular)",
        pecas_mqb,
        "subgrafo_mqb.png",
        cor='#2ca02c'
    )
    
    # Subgrafo Small Wide
    print("\n3. Gerando subgrafo Small Wide (Stellantis)...")
    g_small, pecas_small = criar_subgrafo_small_wide()
    visualizar_subgrafo(
        g_small,
        "Subgrafo Small Wide 4x4: Stellantis (Jeep + Fiat)",
        pecas_small,
        "subgrafo_small_wide.png",
        cor='#d62728'
    )
    
    # Subgrafo PL71
    print("\n4. Gerando subgrafo PL71 (SUVs Premium VW Group)...")
    g_pl71, pecas_pl71 = criar_subgrafo_pl71()
    visualizar_subgrafo(
        g_pl71,
        "Subgrafo PL71: SUVs Premium VW Group",
        pecas_pl71,
        "subgrafo_pl71.png",
        cor='#9467bd'
    )
    
    print("\n" + "="*80)
    print("VISUALIZAÇÕES GERADAS COM SUCESSO")
    print("="*80)
    print("Arquivos criados:")
    print("  - subgrafo_pq35.png")
    print("  - subgrafo_mqb.png")
    print("  - subgrafo_small_wide.png")
    print("  - subgrafo_pl71.png")
    print("="*80)

if __name__ == "__main__":
    main()
