"""
Representação das rotas aéreas da LATAM - Questão 4

Modelagem:
- Grafo G = (V, E), onde:
  * Vértices: Aeródromos
  * Arestas existem em caso de rotas aéreas presentes
"""
from typing import List
import matplotlib.pyplot as plt
import networkx as nx
from main import Graph, get_vertices_num, get_edge_num
from vehicle_parts import graus

# ==================== DATASET ====================

V_AEROPORTOS = [
    'EDDF', 'LIRF', 'LIMC', 'SBPK', 'LMML', 'SBMQ', 'SAME', 'SBAR', 'SBNF', 'SBCH', 'SBJP', 'SBIZ', 'SBBE', 'SBFN', 'SBCY', 'SBSG', 'SBFZ', 'SBPL', 'SBCX', 'SBPV', 'SBBR', 'KMCO', 'SBIL', 'SBVT', 'SBGL', 'LPPT', 'SBKP', 'SBGR', 'SBCG', 'KBOS', 'SBFI', 'SBGO', 'LEMD', 'SBSL', 'SBFL', 'FAOR', 'MMMX', 'SBRP', 'SBJA', 'SBPF', 'SBBV', 'SBMA', 'SBCF', 'SCEL', 'SBTE', 'SBCA', 'KLAX', 'SPJC', 'SAZS', 'SAEZ', 'SBJE', 'SUMU', 'SBPA', 'SBMO', 'LFPG', 'LEBL', 'SBMK', 'SBEG', 'SBSP', 'KMIA', 'SDSC', 'SBSR', 'SBJU', 'SBPS', 'SBCT', 'SBPJ', 'SBUL', 'SBSN', 'KJFK', 'EGLL', 'SABE', 'SBSV', 'SBSI', 'SBRF', 'SBJV', 'SBMG', 'SBRJ', 'SBLO', 'SBRB', 'SBVC', 'VOHY'
    ]

E_CONEXOES = [
    ('SBBR', 'SBSP'), ('SBCF', 'SBSP'), ('SBFL', 'SBSP'), ('SBSP', 'SBCT'), ('SBGR', 'SBCG'), ('SBSP', 'SBPA'), ('SBGO', 'SBGR'), ('SBRJ', 'SBSP'), ('SBSP', 'SBMG'), ('SBGR', 'SBMG'), ('SBGR', 'SBPA'), ('SBIL', 'SBGR'), ('SBBR', 'SBGR'), ('SBGR', 'SBCT'), ('SBFZ', 'SBGR'), ('SBGR', 'SBGL'), ('SBGR', 'SBSV'), ('SBBR', 'SBCY'), ('SBPL', 'SBGR'), ('SBBR', 'SBRF'), ('SBVC', 'SBGR'), ('SBGR', 'SBFI'), ('SBLO', 'SBGR'), ('SBJP', 'SBBR'), ('SBSG', 'SBBR'), ('SBBR', 'SBMA'), ('SBJE', 'SBGR'), ('SBMO', 'SBGR'), ('SBPJ', 'SBBR'), ('SBSP', 'SBSR'), ('SBBR', 'SBCF'), ('SBGR', 'SPJC'), ('SBRF', 'SCEL'), ('SBGR', 'SUMU'), ('SBGR', 'SAME'), ('SBGL', 'SBJP'), ('SBGL', 'SAEZ'), ('SBGR', 'SCEL'), ('SBCG', 'SBBR'), ('SBGL', 'SBBR'), ('SBCF', 'SBGR'), ('SBPS', 'SBBR'), ('SBGR', 'SBNF'), ('SBBR', 'SBSV'), ('SBSP', 'SBRF'), ('SBSP', 'SBFZ'), ('SBCY', 'SBGR'), ('SBGO', 'SBSP'), ('SBSV', 'SBSP'), ('SBGL', 'SBRF'), ('SBPF', 'SBGR'), ('SBSP', 'SBUL'), ('SBSP', 'SBPS'), ('SBSP', 'SBVT'), ('SBRF', 'SBGR'), ('SBFZ', 'SBTE'), ('SBSP', 'SBMO'), ('SBSP', 'SBIL'), ('SBSG', 'SBFZ'), ('SBBE', 'SBFZ'), ('SBGO', 'SBBR'), ('SBRJ', 'SBBR'), ('SBSP', 'SBCY'), ('SBGL', 'SBPA'), ('SBBR', 'SBSL'), ('SBTE', 'SBBR'), ('SBBR', 'SBFL'), ('SBGR', 'SBJP'), ('SBJV', 'SBGR'), ('SBBR', 'SBMO'), ('SBGR', 'SBSR'), ('SBGL', 'SBVT'), ('SBSV', 'SBGL'), ('SBGR', 'SBFL'), ('SBBR', 'SBPA'), ('SBSP', 'SBFI'), ('SBIZ', 'SBGR'), ('SBSP', 'SBCG'), ('SBGR', 'SBSG'), ('SBFZ', 'SBGL'), ('SBFZ', 'SBSV'), ('SBGL', 'SBSL'), ('SBGR', 'SBSL'), ('SBSV', 'SBSG'), ('SBGR', 'SBJU'), ('SBGR', 'SABE'), ('SUMU', 'SCEL'), ('SBBR', 'SBKP'), ('SBBR', 'SBAR'), ('SBBR', 'SBSI'), ('SBGR', 'SBRJ'), ('SBGR', 'SBVT'), ('SBSP', 'SBNF'), ('SAZS', 'SBGR'), ('SBBR', 'SBPV'), ('SBGR', 'SBCH'), ('SBSP', 'SBPK'), ('SBSP', 'SBCH'), ('SBBV', 'SBEG'), ('SBRF', 'SBFZ'), ('SBEG', 'SBFZ'), ('SBPV', 'SBEG'), ('SBEG', 'SBGR'), ('SBFL', 'SBPA'), ('SBGR', 'SBCA'), ('SBGR', 'SBSP'), ('SBGR', 'SDSC'), ('SBSP', 'SDSC'), ('SBBE', 'SBBR'), ('SBGL', 'SBSP'), ('SBPA', 'SDSC'), ('SBPA', 'SBCX'), ('SBFZ', 'SDSC'), ('SBGL', 'SCEL'), ('EDDF', 'SBGR'), ('SBPS', 'SBGR'), ('KMCO', 'SBGR'), ('SBGR', 'EGLL'), ('LIRF', 'SBGR'), ('SBGR', 'KMIA'), ('KMIA', 'KMCO'), ('VOHY', 'LMML'), ('LMML', 'SBFZ'), ('SBTE', 'SBGR'), ('SBBE', 'SBGR'), ('SBJP', 'SBSP'), ('SBSP', 'SBSG'), ('SBSI', 'SBGR'), ('KJFK', 'SBGR'), ('SBFZ', 'KMIA'), ('SBCF', 'SBFZ'), ('SBPJ', 'SBGR'), ('SBSL', 'SBFZ'), ('SBSV', 'SBRF'), ('SBVT', 'SBBR'), ('SBBR', 'SBRB'), ('SBGR', 'FAOR'), ('SBGR', 'SBMK'), ('LFPG', 'SBGR'), ('SBBR', 'SBEG'), ('SBGL', 'SBEG'), ('SBGR', 'LIMC'), ('LEMD', 'SBGR'), ('LIMC', 'LEMD'), ('SBGR', 'KLAX'), ('SBGL', 'SBFI'), ('SBGR', 'MMMX'), ('SBGR', 'LEBL'), ('SAEZ', 'SUMU'), ('SCEL', 'SAEZ'), ('SBFL', 'SBKP'), ('SBKP', 'SBGR'), ('SBSP', 'SBJV'), ('SBFZ', 'SCEL'), ('SBBR', 'SBFZ'), ('SCEL', 'SBBR'), ('SBGR', 'SAEZ'), ('SBCT', 'SABE'), ('SBGR', 'LPPT'), ('SBAR', 'SBGR'), ('SBEG', 'SBBE'), ('SBFZ', 'LPPT'), ('SBGR', 'KBOS'), ('SBSP', 'SBAR'), ('SBGR', 'SBMQ'), ('SBRF', 'SBJP'), ('SBGR', 'SBUL'), ('SBSP', 'SBRP'), ('SBGR', 'SBFN'), ('SBGR', 'SBCX'), ('SBBR', 'SBSN'), ('SBGR', 'SBPK'), ('SBGR', 'SBPV'), ('SBGR', 'SBJA'), ('SBJU', 'SBFZ'), ('SBBR', 'SBCT'), ('SBSP', 'SBLO'), ('SBGL', 'SBPS'), ('SBBR', 'SBBV'), ('SBFZ', 'SBGO'), ('SBBR', 'SBMQ'), ('SBGR', 'SBRB'), ('SBGO', 'SBKP'), ('SBJU', 'SBCF'), ('SBGL', 'SBCF'), ('SBGR', 'SBBV'), ('SBMQ', 'SBBE'), ('SBCT', 'SBPA'), ('SBCT', 'SBFI'), ('SBBR', 'SBIZ')
    ]

# ==================== FUNÇÕES ====================
def projetar_grafo() -> Graph:
    return Graph(V_AEROPORTOS, E_CONEXOES)

def entrada_conjuntos(g_projetado: Graph):
    """
    Entrar com os conjuntos que compõem a definição de um grafo
    """
    
    print("\nMODELAGEM DO PROBLEMA:")
    print(f"  Grafo projetado G = (V, E) com {len(V_AEROPORTOS)} aeródromos")
    print(f"  V = conjunto de aeródromos")
    print(f"  E = arestas entre aeródromos que possuem rotas aéreas entre si")
    
    print("\nPROCESSO DE CONSTRUÇÃO:")
    print("\n1. Dataset de entrada:")
    print(f"   - {len(V_AEROPORTOS)} aeródromos")
    print(f"   - {len(E_CONEXOES)} rotas aéreas")
    
    print("\n2. Grafo:")
    print("   G = Graph(V_AEROPORTOS, E_CONEXOES)")
    
    print(f"\nRESULTADO:")
    print(f"   n = |V| = {get_vertices_num(g=g_projetado)} vértices")
    print(f"   m = |E'| = {get_edge_num(g=g_projetado)} arestas")

def subgrafos(g_projetado: Graph):
    """
    Montar subconjuntos do problema e verificar se eles são subgrafos
    """

    # Subgrafo 1
    print("\n" + "-"*80)
    print("Subgrafo 1: CGH, MAO, BSB, POA")
    subgrafo1 = ['SBSP', 'SBEG', 'SBBR', 'SBPA']
    analisar_subgrafo(g_projetado, subgrafo1)

    # Subgrafo 2
    print("\n" + "-"*80)
    print("Subgrafo 2: MDZ(Argentina), BEL, FRA(Alemanha), XAP, BPM(Índia)")
    subgrafo2 = ['SAME', 'SBBE', 'EDDF', 'SBCH', 'VOHY']
    analisar_subgrafo(g_projetado, subgrafo2)

    # Subgrafo 3
    print("\n" + "-"*80)
    print("Subgrafo 3: JJG, MLA(Malta), MOC, QSC")
    subgrafo3 = ['SBJA', 'LMML', 'SBMK', 'SDSC']
    analisar_subgrafo(g_projetado, subgrafo3)

    print("\n" + "-"*80)
    print("Subgrafo 4: GRU, CDG(França), Boston(Estados Unidos), AEP(Argentina)")
    subgrafo4 = ['SBGR', 'LFPG', 'KBOS', 'SABE']
    analisar_subgrafo(g_projetado, subgrafo4)

def analisar_subgrafo(g_projetado: Graph, vertices_subgrafo: List[str]):
    """
    Analisar se um conjunto de vértices forma um subgrafo.
    """
    # Verificar se todos os vértices existem no grafo
    vertices_validos = [v for v in vertices_subgrafo if v in g_projetado.vertices]
    
    if len(vertices_validos) != len(vertices_subgrafo):
        print(f"AVISO: Alguns vértices não existem no grafo")
        print(f"Válidos: {len(vertices_validos)}/{len(vertices_subgrafo)}")
        return
    
    # Extrair arestas do subgrafo
    arestas_subgrafo = []
    for edge in g_projetado.edges:
        u, v = edge
        if u in vertices_subgrafo and v in vertices_subgrafo:
            arestas_subgrafo.append(edge)
    
    n_sub = len(vertices_subgrafo)
    m_sub = len(arestas_subgrafo)
    
    print(f"Vértices: {{ {', '.join(vertices_subgrafo)} }}")
    print(f"|V_sub| = {n_sub}, |E_sub| = {m_sub}")



# ==================== VISUALIZAÇÃO ====================
def visualizar_grafo(g_projetado: Graph, salvar_como='airroute_graph.png'):
    print(f"\nGerando visualização: {salvar_como}")
    
    # Criar grafo NetworkX
    Gnx = nx.Graph()
    Gnx.add_nodes_from(g_projetado.vertices)
    
    for edge in g_projetado.edges:
        u, v = edge
        weight = g_projetado.weights.get(edge, 1)
        Gnx.add_edge(u, v)
    
    node_colors = ['#bcbd22']

    plt.figure(figsize=(20, 16))
    pos = nx.spring_layout(Gnx, k=2, iterations=50, seed=42)
    
    # Desenhar
    nx.draw_networkx_nodes(Gnx, pos, node_color=node_colors, node_size=800, alpha=0.9)
    nx.draw_networkx_labels(Gnx, pos, font_size=8, font_weight='bold')

    # Modificar aresstas
    nx.draw_networkx_edges(Gnx, pos, width=1, alpha=0.3)

    
    plt.title("Grafo Projetado: Rotas aéreas da LATAM", fontsize=16, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(salvar_como, dpi=300, bbox_inches='tight')
    print(f"Visualização salva com sucesso: {salvar_como}")
    plt.close()

def main():
    g_projetado = projetar_grafo()
    entrada_conjuntos(g_projetado)
    graus(g_projetado)
    subgrafos(g_projetado)
    visualizar_grafo(g_projetado)

if __name__ == '__main__':
    main()