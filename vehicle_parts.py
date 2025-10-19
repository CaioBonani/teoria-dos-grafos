"""
Compartilhamento de Peças entre Veículos - Questão 3

Modelagem:
- Grafo bipartido G = (U ∪ W, E) onde:
  * U = conjunto de veículos (24 vértices)
  * W = conjunto de peças (22 vértices)
  * E = relações de compatibilidade carro-peça

- Grafo projetado G' = (U, E') onde:
  * Vértices: veículos
  * Aresta (u, v) existe se u e v compartilham ≥ 1 peça
  * Atributos da aresta:
    - weight: número de peças compartilhadas
    - label: vetor binário de 22 bits (quais peças)
"""

from typing import List, Tuple, Dict, Set
from collections import defaultdict
import matplotlib.pyplot as plt
import networkx as nx
from main import Graph, get_vertices_num, get_edge_num, get_adj_vertice, get_degree, list_all_degrees

# ==================== DATASET ====================

# 24 Veículos
V_CARROS = [
    "VW Golf Mk6", "Audi A3 8P", "Porsche Cayenne", "Renault Clio IV",
    "Nissan Micra K13", "VW Polo Mk5", "Audi TT Mk2", "Jeep Compass",
    "Fiat Toro", "Renault Captur", "BMW X3", "Mercedes C-Class",
    "VW Golf Mk7", "Audi A3 8V", "Audi A1 8X", "Audi Q7 4L",
    "VW Touareg 7L", "Nissan Qashqai J11", "Renault Kadjar", "Renault Clio V",
    "Nissan Micra K14", "Jeep Renegade", "BMW 3 Series (F30)", "Mercedes E-Class (W213)"
]

# 22 Peças
V_PECAS = [
    "Motor EA111 1.6", "Motor EA888 2.0T", "Transmissão DSG DQ250", "Plataforma PQ35",
    "Plataforma MQB", "Plataforma CMF-B", "Suspensão Multilink", "Motor Tigershark 2.4",
    "Transmissão Aisin 6F24", "Motor HR16DE", "Sistema ABS Bosch", "Central Multimídia MIB",
    "Turbocompressor KKK", "Plataforma PQ25", "Plataforma B (Renault-Nissan)", "Plataforma CMF-CD",
    "Plataforma Small Wide 4x4", "Plataforma PL71", "Motor VR6 3.6", "Motor N20 2.0T", "Motor M274 2.0T", "Chassi Monobloco"
]

# Arestas do Grafo Bipartido (Carro ↔ Peça)
EDGES_BIPARTIDO = [
    ("VW Golf Mk6", "Motor EA888 2.0T"), ("VW Golf Mk6", "Transmissão DSG DQ250"),
    ("VW Golf Mk6", "Plataforma PQ35"), ("VW Golf Mk6", "Sistema ABS Bosch"),
    ("VW Golf Mk6", "Central Multimídia MIB"), ("Audi A3 8P", "Motor EA111 1.6"),
    ("Audi A3 8P", "Transmissão DSG DQ250"), ("Audi A3 8P", "Plataforma PQ35"),
    ("Audi A3 8P", "Sistema ABS Bosch"), ("Audi A3 8P", "Central Multimídia MIB"),
    ("Audi TT Mk2", "Motor EA888 2.0T"), ("Audi TT Mk2", "Transmissão DSG DQ250"),
    ("Audi TT Mk2", "Turbocompressor KKK"), ("Audi TT Mk2", "Sistema ABS Bosch"),
    ("Audi TT Mk2", "Plataforma PQ35"), ("VW Polo Mk5", "Motor EA111 1.6"),
    ("VW Polo Mk5", "Plataforma PQ25"), ("VW Polo Mk5", "Sistema ABS Bosch"),
    ("Porsche Cayenne", "Suspensão Multilink"), ("Porsche Cayenne", "Sistema ABS Bosch"),
    ("Porsche Cayenne", "Turbocompressor KKK"), ("Renault Clio IV", "Plataforma B (Renault-Nissan)"),
    ("Renault Clio IV", "Motor HR16DE"), ("Renault Clio IV", "Sistema ABS Bosch"),
    ("Nissan Micra K13", "Plataforma B (Renault-Nissan)"), ("Nissan Micra K13", "Motor HR16DE"),
    ("Nissan Micra K13", "Sistema ABS Bosch"), ("Renault Captur", "Plataforma B (Renault-Nissan)"),
    ("Renault Captur", "Motor HR16DE"), ("Renault Captur", "Sistema ABS Bosch"),
    ("Jeep Compass", "Motor Tigershark 2.4"), ("Jeep Compass", "Transmissão Aisin 6F24"),
    ("Jeep Compass", "Sistema ABS Bosch"), ("Fiat Toro", "Motor Tigershark 2.4"),
    ("Fiat Toro", "Transmissão Aisin 6F24"), ("Fiat Toro", "Sistema ABS Bosch"),
    ("BMW X3", "Suspensão Multilink"), ("BMW X3", "Sistema ABS Bosch"), 
    ("BMW X3", "Turbocompressor KKK"), ("Mercedes C-Class", "Suspensão Multilink"), 
    ("Mercedes C-Class", "Sistema ABS Bosch"), ("Mercedes C-Class", "Turbocompressor KKK"),
    
    # Novos Veículos e Peças
    ("VW Golf Mk7", "Motor EA888 2.0T"), ("VW Golf Mk7", "Transmissão DSG DQ250"),
    ("VW Golf Mk7", "Plataforma MQB"), ("VW Golf Mk7", "Sistema ABS Bosch"),
    ("VW Golf Mk7", "Central Multimídia MIB"), ("Audi A3 8V", "Motor EA888 2.0T"),
    ("Audi A3 8V", "Transmissão DSG DQ250"), ("Audi A3 8V", "Plataforma MQB"),
    ("Audi A3 8V", "Sistema ABS Bosch"), ("Audi A3 8V", "Central Multimídia MIB"),
    ("Audi A1 8X", "Motor EA111 1.6"), ("Audi A1 8X", "Transmissão DSG DQ250"),
    ("Audi A1 8X", "Plataforma PQ25"), ("Audi A1 8X", "Sistema ABS Bosch"),
    ("Audi Q7 4L", "Plataforma PL71"), ("Audi Q7 4L", "Suspensão Multilink"),
    ("Audi Q7 4L", "Sistema ABS Bosch"), ("Audi Q7 4L", "Turbocompressor KKK"),
    ("Audi Q7 4L", "Motor VR6 3.6"), ("VW Touareg 7L", "Plataforma PL71"),
    ("VW Touareg 7L", "Suspensão Multilink"), ("VW Touareg 7L", "Sistema ABS Bosch"),
    ("VW Touareg 7L", "Turbocompressor KKK"), ("VW Touareg 7L", "Motor VR6 3.6"),
    ("Porsche Cayenne", "Plataforma PL71"), ("Porsche Cayenne", "Motor VR6 3.6"),
    ("Nissan Qashqai J11", "Plataforma CMF-CD"), ("Nissan Qashqai J11", "Suspensão Multilink"),
    ("Nissan Qashqai J11", "Sistema ABS Bosch"), ("Renault Kadjar", "Plataforma CMF-CD"),
    ("Renault Kadjar", "Suspensão Multilink"), ("Renault Kadjar", "Sistema ABS Bosch"),
    ("Renault Clio V", "Plataforma CMF-B"), ("Renault Clio V", "Sistema ABS Bosch"),
    ("Nissan Micra K14", "Plataforma CMF-B"), ("Nissan Micra K14", "Sistema ABS Bosch"),
    ("Jeep Renegade", "Plataforma Small Wide 4x4"), ("Jeep Renegade", "Motor Tigershark 2.4"),
    ("Jeep Renegade", "Transmissão Aisin 6F24"), ("Jeep Renegade", "Sistema ABS Bosch"),
    ("Jeep Compass", "Plataforma Small Wide 4x4"), ("Fiat Toro", "Plataforma Small Wide 4x4"),
    ("BMW 3 Series (F30)", "Suspensão Multilink"), ("BMW 3 Series (F30)", "Sistema ABS Bosch"),
    ("BMW 3 Series (F30)", "Turbocompressor KKK"), ("BMW 3 Series (F30)", "Motor N20 2.0T"),
    ("BMW X3", "Motor N20 2.0T"), ("Mercedes E-Class (W213)", "Suspensão Multilink"),
    ("Mercedes E-Class (W213)", "Sistema ABS Bosch"), ("Mercedes E-Class (W213)", "Turbocompressor KKK"),
    ("Mercedes E-Class (W213)", "Motor M274 2.0T"), ("Mercedes C-Class", "Motor M274 2.0T")
]

# ==================== FUNÇÕES ====================
def criar_grafo_bipartido() -> Graph:
    """
    Cria o grafo bipartido G = (V_CARROS ∪ V_PECAS, E)
    onde E são as relações carro-peça.
    """
    vertices = V_CARROS + V_PECAS
    return Graph(vertices, EDGES_BIPARTIDO)

def projetar_grafo_veiculos() -> Graph:
    """
    Cria o grafo projetado G' = (V_CARROS, E')
    onde existe aresta (u, v) se os veículos u e v compartilham ≥1 peça.
    
    Atributos da aresta:
    - weight: número de peças compartilhadas
    - label: string binária de 22 bits indicando quais peças
    - pecas_compartilhadas: lista dos nomes das peças
    """
    # Mapear cada carro às suas peças
    carro_pecas: Dict[str, Set[str]] = {carro: set() for carro in V_CARROS}
    
    for carro, peca in EDGES_BIPARTIDO:
        if carro in V_CARROS and peca in V_PECAS:
            carro_pecas[carro].add(peca)
    
    # Construir arestas do grafo projetado
    edges_projetado = []
    weights = {}
    labels = {}
    pecas_compartilhadas_dict = {}
    
    for i, carro1 in enumerate(V_CARROS):
        for carro2 in V_CARROS[i+1:]:  # Evita duplicatas e loops
            pecas_comuns = carro_pecas[carro1] & carro_pecas[carro2]
            
            if pecas_comuns:  # Existe aresta se compartilham ≥1 peça
                edges_projetado.append((carro1, carro2))
                
                # Calcular peso
                weights[(carro1, carro2)] = len(pecas_comuns)
                
                # Calcular label binário (22 bits)
                label_bits = []
                for peca in V_PECAS:
                    label_bits.append('1' if peca in pecas_comuns else '0')
                labels[(carro1, carro2)] = ''.join(label_bits)
                
                # Armazenar lista de peças compartilhadas
                pecas_compartilhadas_dict[(carro1, carro2)] = sorted(list(pecas_comuns))
    
    # Criar grafo com atributos
    g = Graph(V_CARROS, edges_projetado, weights)
    g.labels = labels
    g.pecas_compartilhadas = pecas_compartilhadas_dict
    
    return g

# ==================== ANÁLISE DO PROBLEMA ====================
def entrada_conjuntos(g_projetado: Graph):
    """
    Entrar com os conjuntos que compõem a definição de um grafo
    """
    
    print("\nMODELAGEM DO PROBLEMA:")
    print(f"  Grafo projetado G' = (V, E') com {len(V_CARROS)} veículos")
    print(f"  V = conjunto de veículos")
    print(f"  E' = arestas entre veículos que compartilham peças")
    
    print("\nPROCESSO DE CONSTRUÇÃO:")
    print("\n1. Dataset de entrada:")
    print(f"   - {len(V_CARROS)} veículos")
    print(f"   - {len(V_PECAS)} peças automotivas")
    print(f"   - {len(EDGES_BIPARTIDO)} relações carro-peça")
    
    print("\n2. Grafo bipartido:")
    print("   G_bipartido = Graph(V_CARROS + V_PECAS, EDGES_BIPARTIDO)")
    
    print("\n3. Projeção para grafo veículo-veículo:")
    print("   a) Para cada carro, mapear suas peças: carro_pecas[c] = set(peças)")
    print("   b) Para cada par (u, v) de veículos:")
    print("      - Calcular: pecas_comuns = carro_pecas[u] ∩ carro_pecas[v]")
    print("      - Se |pecas_comuns| ≥ 1: adicionar aresta (u, v)")
    print("      - Calcular atributos:")
    print("        * weight = |pecas_comuns|")
    print("        * label = vetor binário 22 bits")
    print("        * pecas_compartilhadas = lista das peças comuns")
    
    print("\n4. Criação do grafo projetado:")
    print("   G_projetado = Graph(V_CARROS, edges_projetado, weights)")
    print("   - Atributos adicionais: labels, pecas_compartilhadas")
    
    print("\n5. Lógica de conversão:")
    print("   (u, v) ∈ E' ⟺ ∃ p ∈ V_PECAS: (u,p) ∈ E ∧ (v,p) ∈ E")
    
    print(f"\nRESULTADO:")
    print(f"   n = |V| = {get_vertices_num(g=g_projetado)} vértices")
    print(f"   m = |E'| = {get_edge_num(g=g_projetado)} arestas")

def graus(g_projetado: Graph):
    """
    Encontrar os vértices de maior e menor grau (não-ponderado).
    """
    
    graus = list_all_degrees(g=g_projetado)
    
    # Encontrar máximo e mínimo
    grau_max = max(graus.values())
    grau_min = min(graus.values())
    
    vertices_max = [v for v, g in graus.items() if g == grau_max]
    vertices_min = [v for v, g in graus.items() if g == grau_min]

    print(f"\nGRAU MÁXIMO: {grau_max}")
    print(f" Vértices com Grau Máximo ({len(vertices_max)}):")
    for v in vertices_max:
        print(f"- {v}: grau = {grau_max}")
    
    print(f"\nGRAU MÍNIMO: {grau_min}")
    print(f" Vértices com grau mínimo ({len(vertices_min)}):")
    for v in vertices_min:
        print(f"- {v}: grau = {grau_min}")

    mostra_classificacao_ponderada(g_projetado, top_n=5)

def graus_ponderados(g: Graph) -> Dict[str, int]:
    """
    Retorna o grau ponderado para cada veículo:
    soma dos pesos de todas as arestas incidentes.
    """
    wdeg = defaultdict(int)
    for (u, v) in g.edges:
        w = g.weights.get((u, v))
        if w is None:  # If weights are keyed by unordered pairs, try the flipped tuple
            w = g.weights.get((v, u), 1)
        wdeg[u] += w
        wdeg[v] += w
    return dict(wdeg)

def mostra_classificacao_ponderada(g: Graph, top_n: int = 5) -> None:
    """
    Imprime veículos Top-N e Bottom-N por grau ponderado.
    """
    wdeg = graus_ponderados(g)
    ordered = sorted(wdeg.items(), key=lambda x: (-x[1], x[0]))

    print("\nGRAU PONDERADO (soma dos pesos das arestas incidentes)")
    print(" Top {}:".format(top_n))
    for car, val in ordered[:top_n]:
        print(f" - {car}: {val}")

    print("\n Bottom {}:".format(top_n))
    for car, val in sorted(wdeg.items(), key=lambda x: (x[1], x[0]))[:top_n]:
        print(f" - {car}: {val}")
           
def subgrafos(g_projetado: Graph):
    """
    Considerar subconjuntos do problema e verificar se eles são subgrafos
    """
    
    print("\nEstratégia de identificação:")
    print("  - Agrupar veículos por grupo automotivo/aliança")
    print("  - Verificar se formam subgrafos induzidos")
    print("  - Analisar densidade e conectividade")
    
    # Subgrafo 1: Grupo VW-Audi (Plataforma PQ35)
    print("\n" + "-"*80)
    print("SUBGRAFO 1: Grupo Volkswagen-Audi (Plataforma PQ35)")
    print("-"*80)
    vertices_vw_audi_pq35 = ["VW Golf Mk6", "Audi A3 8P", "VW Polo Mk5", "Audi TT Mk2"]
    analisar_subgrafo(g_projetado, vertices_vw_audi_pq35, 
                     "Compartilham plataforma PQ35, motores EA e transmissões DSG")
    
    # Subgrafo 2: Grupo VW-Audi (Plataforma MQB)
    print("\n" + "-"*80)
    print("SUBGRAFO 2: Grupo Volkswagen-Audi (Plataforma MQB)")
    print("-"*80)
    vertices_vw_audi_mqb = ["VW Golf Mk7", "Audi A3 8V"]
    analisar_subgrafo(g_projetado, vertices_vw_audi_mqb,
                     "Compartilham plataforma MQB (modular), motor EA888 e DSG")
    
    # Subgrafo 3: Aliança Renault-Nissan (Plataforma B)
    print("\n" + "-"*80)
    print("SUBGRAFO 3: Aliança Renault-Nissan (Plataforma B)")
    print("-"*80)
    vertices_rn_b = ["Renault Clio IV", "Nissan Micra K13", "Renault Captur"]
    analisar_subgrafo(g_projetado, vertices_rn_b,
                     "Aliança Renault-Nissan: Plataforma B e Motor HR16DE")
    
    # Subgrafo 4: Aliança Renault-Nissan (Plataforma CMF)
    print("\n" + "-"*80)
    print("SUBGRAFO 4: Aliança Renault-Nissan (Plataformas CMF)")
    print("-"*80)
    vertices_rn_cmf = ["Renault Clio V", "Nissan Micra K14", "Nissan Qashqai J11", "Renault Kadjar"]
    analisar_subgrafo(g_projetado, vertices_rn_cmf,
                     "Plataformas CMF-B e CMF-CD (Common Module Family)")
    
    # Subgrafo 5: Grupo Stellantis
    print("\n" + "-"*80)
    print("SUBGRAFO 5: Grupo Stellantis (Jeep + Fiat)")
    print("-"*80)
    vertices_stellantis = ["Jeep Compass", "Fiat Toro", "Jeep Renegade"]
    analisar_subgrafo(g_projetado, vertices_stellantis,
                     "Motor Tigershark 2.4 e Plataforma Small Wide 4x4")
    
    # Subgrafo 6: Marcas Premium Alemãs
    print("\n" + "-"*80)
    print("SUBGRAFO 6: Marcas Premium Alemãs")
    print("-"*80)
    vertices_premium = ["BMW X3", "BMW 3 Series (F30)", "Mercedes C-Class", "Mercedes E-Class (W213)"]
    analisar_subgrafo(g_projetado, vertices_premium,
                     "Suspensão Multilink e Turbocompressor KKK")
    
    # Subgrafo 7: Plataforma PL71 (SUVs Premium)
    print("\n" + "-"*80)
    print("SUBGRAFO 7: Plataforma PL71 (SUVs Premium VW Group)")
    print("-"*80)
    vertices_pl71 = ["Audi Q7 4L", "VW Touareg 7L", "Porsche Cayenne"]
    analisar_subgrafo(g_projetado, vertices_pl71,
                     "Plataforma PL71 compartilhada, Motor VR6 3.6")

def analisar_subgrafo(g: Graph, vertices_subgrafo: List[str], justificativa: str):
    """
    Analisar se um conjunto de vértices forma um subgrafo e suas propriedades.
    """
    # Verificar se todos os vértices existem no grafo
    vertices_validos = [v for v in vertices_subgrafo if v in g.vertices]
    
    if len(vertices_validos) != len(vertices_subgrafo):
        print(f"AVISO: Alguns vértices não existem no grafo")
        print(f"Válidos: {len(vertices_validos)}/{len(vertices_subgrafo)}")
        return
    
    # Extrair arestas do subgrafo
    arestas_subgrafo = []
    for edge in g.edges:
        u, v = edge
        if u in vertices_subgrafo and v in vertices_subgrafo:
            arestas_subgrafo.append(edge)
    
    n_sub = len(vertices_subgrafo)
    m_sub = len(arestas_subgrafo)
    
    print(f"Vértices: {{ {', '.join(vertices_subgrafo)} }}")
    print(f"|V_sub| = {n_sub}, |E_sub| = {m_sub}")
    
    print(f"Justificativa: {justificativa}")
    
    # Listar peças compartilhadas (se disponível)
    if hasattr(g, 'pecas_compartilhadas') and arestas_subgrafo:
        print(f"\nExemplo de peças compartilhadas:")
        for i, edge in enumerate(arestas_subgrafo[:3]):  # Mostrar até 3 arestas
            pecas = g.pecas_compartilhadas.get(edge, [])
            u, v = edge
            print(f"  {u} ↔ {v}:")
            print(f"    {', '.join(pecas[:3])}" + ("..." if len(pecas) > 3 else ""))

# ==================== VISUALIZAÇÃO ====================
def visualizar_grafo_projetado(g_projetado: Graph, salvar_como='projected_vehicle_graph.png'):
    """
    Visualizar o grafo projetado com cores por grupo automotivo.
    """
    print(f"\nGerando visualização: {salvar_como}")
    
    # Criar grafo NetworkX
    Gnx = nx.Graph()
    Gnx.add_nodes_from(g_projetado.vertices)
    
    for edge in g_projetado.edges:
        u, v = edge
        weight = g_projetado.weights.get(edge, 1)
        Gnx.add_edge(u, v, weight=weight)
    
    # Definir cores por grupo
    grupos = {
        'VW-Audi PQ': ['VW Golf Mk6', 'Audi A3 8P', 'VW Polo Mk5', 'Audi TT Mk2', 'Audi A1 8X'],
        'VW-Audi MQB': ['VW Golf Mk7', 'Audi A3 8V'],
        'VW-Audi PL71': ['Audi Q7 4L', 'VW Touareg 7L'],
        'Porsche': ['Porsche Cayenne'],
        'Renault-Nissan B': ['Renault Clio IV', 'Nissan Micra K13', 'Renault Captur'],
        'Renault-Nissan CMF': ['Renault Clio V', 'Nissan Micra K14', 'Nissan Qashqai J11', 'Renault Kadjar'],
        'Stellantis': ['Jeep Compass', 'Fiat Toro', 'Jeep Renegade'],
        'BMW': ['BMW X3', 'BMW 3 Series (F30)'],
        'Mercedes': ['Mercedes C-Class', 'Mercedes E-Class (W213)']
    }
    
    cores_grupo = {
        'VW-Audi PQ': '#1f77b4', 'VW-Audi MQB': '#2ca02c', 'VW-Audi PL71': '#9467bd',
        'Porsche': '#8c564b', 'Renault-Nissan B': '#e377c2', 'Renault-Nissan CMF': '#f7b6d2',
        'Stellantis': '#d62728', 'BMW': '#ff7f0e', 'Mercedes': '#7f7f7f'
    }
    
    node_colors = []
    for node in Gnx.nodes():
        for grupo, veiculos in grupos.items():
            if node in veiculos:
                node_colors.append(cores_grupo[grupo])
                break
        else:
            node_colors.append('#bcbd22')  # Cor padrão
    
    # Layout
    plt.figure(figsize=(20, 16))
    pos = nx.spring_layout(Gnx, k=2, iterations=50, seed=42)
    
    # Desenhar
    nx.draw_networkx_nodes(Gnx, pos, node_color=node_colors, node_size=800, alpha=0.9)
    nx.draw_networkx_labels(Gnx, pos, font_size=8, font_weight='bold')
    
    # Arestas com espessura proporcional ao peso
    edges = Gnx.edges()
    weights = [Gnx[u][v]['weight'] for u, v in edges]
    nx.draw_networkx_edges(Gnx, pos, width=[w*0.5 for w in weights], alpha=0.3)
    
    plt.title("Grafo Projetado: Veículos que Compartilham Peças", fontsize=16, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(salvar_como, dpi=300, bbox_inches='tight')
    print(f"Visualização salva com sucesso: {salvar_como}")
    plt.close()

# ==================== MAIN ====================
def main():
    print("\n" + "="*80)
    print("Compartilhamento de Peças entre Veículos - Questão 3")
    print("="*80)

    # Criar grafo bipartido
    print("\nCriando grafo bipartido carro-peça...")
    g_bipartido = criar_grafo_bipartido()
    print(f"Grafo bipartido criado: {get_vertices_num(g=g_bipartido)} nós, {get_edge_num(g=g_bipartido)} arestas")
    
    # Projetar para grafo veículo-veículo
    print("\nProjetando grafo veículo-veículo...")
    g_projetado = projetar_grafo_veiculos()
    print(f"Grafo projetado criado: {len(V_CARROS)} veículos, {get_edge_num(g=g_projetado)} conexões")
    
    # Executar análises da Questão 3
    print("\n" + "="*80)
    print("QUESTÃO 3 - ITEM 1: ENTRADA DOS CONJUNTOS V e E")
    print("="*80)
    entrada_conjuntos(g_projetado)
    
    print("\n" + "="*80)
    print("QUESTÃO 3 - ITEM 2: VÉRTICES DE MAIOR E MENOR GRAU")
    print("="*80)
    graus(g_projetado)
    
    subgrafos(g_projetado)
    
    # Visualização
    print("\n" + "="*80)
    print("VISUALIZAÇÃO DO GRAFO")
    print("="*80)
    visualizar_grafo_projetado(g_projetado)

if __name__ == "__main__":
    main()
