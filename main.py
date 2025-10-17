# grafo_repr.py
# Implementações das conversões pedidas no Exercício 1 (sem bibliotecas, exceto networkx para visualizar)
from typing import List, Tuple, Dict, Any
import matplotlib.pyplot as plt
import networkx as nx

class Graph:
    """
    Representa um grafo simples não-direcionado, possivelmente com pesos nas arestas.
    vertices: lista de rótulos (qualquer hashable)
    edges: lista de tuplas (u, v) com u, v em vertices
    weights: dicionário opcional que mapeia arestas (u, v) para seus pesos
    Observações: armazena arestas como (u, v) com u and v nos rótulos originais.
    """
    def __init__(self, vertices: List[Any], edges: List[Tuple[Any, Any]], weights: Dict[Tuple[Any, Any], float] = None):
        self.vertices = list(vertices)
        # normalizar arestas: ordenar par (menor, maior) para grafos não-direcionados
        normalized = []
        self.weights = {}
        for (u, v) in edges:
            if u == v:
                normalized.append((u, v))  # loop permitido
                if weights and (u, v) in weights:
                    self.weights[(u, v)] = weights[(u, v)]
            else:
                # manter ordem consistente para evitar duplicatas (u,v) e (v,u)
                if u is None or v is None:
                    raise ValueError("Aresta com vértice None")
                if (u, v) not in normalized and (v, u) not in normalized:
                    normalized.append((u, v))
                    # adicionar peso se fornecido
                    if weights:
                        w = weights.get((u, v)) or weights.get((v, u))
                        if w is not None:
                            self.weights[(u, v)] = w
        self.edges = normalized

    def __repr__(self):
        return f"Graph(vertices={self.vertices}, edges={self.edges})"


# 1) Dado um grafo, gere sua matriz de adjacência
def graph_to_adj_matrix(g: Graph) -> List[List[int]]:
    """
    Retorna uma matriz NxN (lista de listas) com 1 quando há aresta entre i e j, 0 caso contrário.
    As linhas/colunas seguem a ordem de g.vertices.
    """
    n = len(g.vertices)
    idx = {v: i for i, v in enumerate(g.vertices)}
    M = [[0 for _ in range(n)] for __ in range(n)]
    for (u, v) in g.edges:
        i, j = idx[u], idx[v]
        M[i][j] = 1
        M[j][i] = 1  # não-direcionado
    return M

# 2) Dada a matriz de adjacência, gere o grafo correspondente
def adj_matrix_to_graph(M: List[List[int]], vertices: List[Any] = None) -> Graph:
    """
    Recebe matriz quadrada M (lista de listas). Se vertices for None, usa rótulos 0..n-1.
    Constrói arestas (i, j) para cada entrada M[i][j] != 0 com i <= j (evita duplicatas).
    """
    n = len(M)
    if vertices is None:
        vertices = list(range(n))
    if len(vertices) != n:
        raise ValueError("Tamanho da lista de vértices não bate com M")
    edges = []
    for i in range(n):
        for j in range(i, n):  # i<=j para evitar duplicação em matriz simétrica
            val = M[i][j]
            if val:
                edges.append((vertices[i], vertices[j]))
    return Graph(vertices, edges)

# 3) Dado um grafo, gere sua matriz de incidência
def graph_to_incidence_matrix(g: Graph) -> List[List[int]]:
    """
    Retorna matriz de incidência com dimensão V x E (linhas = vértices, colunas = arestas).
    Para aresta (u,v): coloca 1 em linha u e 1 em linha v. Para loop (u,u) coloca 2 (incidência dupla).
    """
    v_list = g.vertices
    idx = {v: i for i, v in enumerate(v_list)}
    m = len(v_list)
    e = len(g.edges)
    I = [[0 for _ in range(e)] for __ in range(m)]
    for col, (u, v) in enumerate(g.edges):
        if u == v:
            I[idx[u]][col] = 2  # loop: conta como duas incidências
        else:
            I[idx[u]][col] = 1
            I[idx[v]][col] = 1
    return I

# 4) Dada uma matriz de incidência, gere o grafo correspondente
def incidence_matrix_to_graph(I: List[List[int]], vertices: List[Any] = None) -> Graph:
    """
    Recebe matriz de incidência I (linhas = vértices, colunas = arestas).
    Cada coluna deve ter exatamente dois '1's (arestas normais) ou um '2' (loop).
    vertices opcional: rótulos das linhas; se None, usa 0..m-1.
    """
    m = len(I)
    if m == 0:
        return Graph([], [])
    ncols = len(I[0])
    if vertices is None:
        vertices = list(range(m))
    if len(vertices) != m:
        raise ValueError("Tamanho dos vértices não coincide com número de linhas em I")

    edges = []
    for col in range(ncols):
        incident = []
        for row in range(m):
            val = I[row][col]
            if val != 0:
                # considerar 2 como loop em única vértice
                incident.append((row, val))
        if len(incident) == 1:
            row, val = incident[0]
            if val == 2:
                v = vertices[row]
                edges.append((v, v))  # loop
            else:
                raise ValueError(f"Coluna {col}: único valor de incidência diferente de 0 mas não é 2.")
        elif len(incident) == 2:
            # ambas devem ser 1 normalmente
            r1, v1 = incident[0]
            r2, v2 = incident[1]
            # aceitar se v1 or v2 ==1 (ou até >=1)
            edges.append((vertices[r1], vertices[r2]))
        else:
            raise ValueError(f"Coluna {col}: número de vértices incidentes = {len(incident)} (não é 1 nem 2).")
    return Graph(vertices, edges)

# 5) Dado um grafo, gere sua lista (lista de adjacência)
def graph_to_adj_list(g: Graph) -> Dict[Any, List[Any]]:
    """
    Retorna dicionário: vértice -> lista de vizinhos.
    """
    adj = {v: [] for v in g.vertices}
    for (u, v) in g.edges:
        if u == v:
            adj[u].append(v)  # loop aparece uma vez (poderíamos adicionar duas vezes se quisermos)
        else:
            adj[u].append(v)
            adj[v].append(u)
    return adj

# 6) Dado uma lista (adjacency list), gere o grafo correspondente
def adj_list_to_graph(adj: Dict[Any, List[Any]]) -> Graph:
    """
    Recebe dicionário vértice -> lista de vizinhos (pode conter ambos u->v e v->u).
    Constrói lista de vértices e normaliza arestas (remove duplicatas).
    """
    vertices = list(adj.keys())
    edges_set = set()
    for u, neighs in adj.items():
        for v in neighs:
            if u == v:
                edges_set.add((u, v))
            else:
                # armazenar em ordem canônica para evitar duplicatas
                a, b = (u, v) if (str(u), str(v)) <= (str(v), str(u)) else (v, u)
                edges_set.add((a, b))
    edges = list(edges_set)
    return Graph(vertices, edges)

# 7) Implementar função que, dada uma descrição em uma das representações, gere as outras duas
def convert_representation(obj: Any, kind: str) -> Dict[str, Any]:
    """
    kind in {'graph', 'adj_matrix', 'incidence', 'adj_list'}
    Retorna dict com as três representações (graph, adj_matrix, incidence, adj_list)
    - Se for 'graph': obj deve ser Graph
    - Se for 'adj_matrix': obj deve ser M (lista de listas); vertices opcionais em obj? aqui assume rótulos 0..n-1
    - Se for 'incidence': obj deve ser I (lista de listas)
    - Se for 'adj_list': obj deve ser dict
    """
    result = {}
    if kind == 'graph':
        g = obj
    elif kind == 'adj_matrix':
        g = adj_matrix_to_graph(obj)
    elif kind == 'incidence':
        # assume rótulos 0..m-1
        g = incidence_matrix_to_graph(obj)
    elif kind == 'adj_list':
        g = adj_list_to_graph(obj)
    else:
        raise ValueError("kind inválido")

    result['graph'] = g
    result['adj_matrix'] = graph_to_adj_matrix(g)
    result['incidence'] = graph_to_incidence_matrix(g)
    result['adj_list'] = graph_to_adj_list(g)
    return result


def visualize_graph(g: Graph, title: str = "Grafo"):
    """
    Visualiza o grafo usando networkx. (Apenas visualização; não usa networkx para cálculos)
    Se o grafo tiver pesos, eles serão mostrados nas arestas.
    """
    plt.figure(figsize=(10, 8))
    plt.title(title)
    
    Gnx = nx.Graph()
    Gnx.add_nodes_from(g.vertices)
    
    # Adiciona arestas com seus pesos (se existirem)
    if hasattr(g, 'weights') and g.weights:
        for (u, v) in g.edges:
            weight = g.weights.get((u, v)) or g.weights.get((v, u))
            Gnx.add_edge(u, v, weight=weight)
    else:
        Gnx.add_edges_from(g.edges)
    
    # Define o layout
    pos = nx.spring_layout(Gnx)
    
    # Desenha o grafo
    nx.draw(Gnx, pos, with_labels=True, node_color='lightblue', 
            node_size=500, font_size=16, font_weight='bold',
            edge_color='gray', width=2)
    
    # Se houver pesos, adiciona os labels das arestas
    if hasattr(g, 'weights') and g.weights:
        edge_labels = {}
        for (u, v) in g.edges:
            weight = g.weights.get((u, v)) or g.weights.get((v, u))
            edge_labels[(u, v)] = f"{weight:.1f}"
        nx.draw_networkx_edge_labels(Gnx, pos, edge_labels=edge_labels)
    
    plt.tight_layout()
    plt.show()

# --- pequeno exemplo demonstrativo ---
if __name__ == "__main__":
    # Exemplo: grafo com 4 vértices e algumas arestas
    vertices = ['A', 'B', 'C', 'D']
    edges = [('A', 'B'), ('A', 'C'), ('B', 'C'), ('C', 'C')]  # nota: loop em C
    g = Graph(vertices, edges)

    print("G:", g)
    M = graph_to_adj_matrix(g)
    print("Matriz de adjacência:")
    for row in M:
        print(row)

    I = graph_to_incidence_matrix(g)
    print("Matriz de incidência (linhas=vértices, colunas=arestas):")
    for row in I:
        print(row)

    adj = graph_to_adj_list(g)
    print("Lista de adjacência:")
    for k, v in adj.items():
        print(f"{k}: {v}")

    # Converta de matriz de adjacência de volta ao grafo
    g2 = adj_matrix_to_graph(M, vertices)
    print("Grafo reconstituído de M:", g2)

    # Converta de matriz de incidência de volta ao grafo
    g3 = incidence_matrix_to_graph(I, vertices)
    print("Grafo reconstituído de I:", g3)

    # Visualize (requer networkx + matplotlib no ambiente)
    try:
        visualize_graph(g, "Exemplo")
    except Exception as e:
        print("Visualização falhou (talvez matplotlib não instalado):", e)
