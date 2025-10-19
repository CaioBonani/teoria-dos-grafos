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

def get_vertices_num(g: Graph = None, M = None, I = None, adj = None) -> int:
    """
    De acordo com g, M, I ou adj for passado como parâmetro trata como a representação respectiva
    usa a variável count para contar quantos vértices tem em cada representação e retorna esse número
    """
    count = 0
    if g:
        for u in g.vertices:
            count += 1
    elif M:
        for u in M:
            count += 1
    elif I:
        for u in I:
            count += 1
    elif adj:
        for u in adj:
            count += 1

    return count

def get_edge_num(g: Graph = None, M = None, I = None, adj = None) -> int:
    """
    De acordo com g, M, I ou adj for passado como parâmetro trata como a representação respectiva
    usa a variável count para contar as arestas
    em g simplesmente conta as arestas, em M e adj conta o número de arestas de cada vertice e divide por 2
    em I conta o número de colunas
    retorna o número de arestas
    """
    count = 0
    if g:
        for u in g.edges:
            count += 1
    elif M:
        l = get_vertices_num(M = M)
        for u in range(l):
            for v in range(l):
                if M[u][v] == 1:
                    count += 1
                    if u == v:
                        count += 1
        count /= 2
    elif I:
        for u in I[0]:
            count += 1
    elif adj:
        for u in adj:
            for v in adj[u]:
                count += 1
                if u == v:
                    count += 1
        count /= 2

    return int(count)

def get_adj_vertice(vertice: object, g: Graph = None, M = None, I = None, adj = None) -> List[object]:
    """
    De acordo com g, M, I ou adj for passado como parâmetro trata como a representação respectiva
    em g adiciona na lista o outro vértice que participa da mesma aresta
    em M adiciona na lista se na linha do vertice tiver alguma aresta indicada a aquele vertice
    em I ve na linha do vertice se existe alguma aresta e percorre na vertical para ver a qual outro vertice é associada
    em adj apenas adiciona a lista de adjacencia do vertice
    e depois retorna a lista que tem os vértices adjacentes
    """
    list = []
    if g:
        for (u, v) in g.edges:
            if u == vertice and v not in list:
                list.append(v)
            if v == vertice and u not in list:
                list.append(u)
    elif M:
        len = get_vertices_num(M = M)
        for i in range(len):
            if M[vertice][i] == 1:
                list.append(i)
    elif I:
        n_vertice = get_vertices_num(I = I)
        n_edge = get_edge_num(I = I)
        for i in range(n_edge):
            if I[vertice][i] == 2:
                list.append(vertice)
            if I[vertice][i] == 1:
                for j in range(n_vertice):
                    if j != vertice and I[j][i] == 1:
                        list.append(j)
    elif adj:
        for u in adj[vertice]:
            list.append(u)

    #print("lista: ",list)
    return list

def edge_exist(vertice1: object, vertice2: object, g: Graph = None, M = None, I = None, adj = None) -> bool:
    """
    De acordo com g, M, I ou adj for passado como parâmetro trata como a representação respectiva
    em todos os casos ve se os vertices adjacentes de vertice1 inclui o vertice1
    se isso acontece existe a aresta
    """

    if g:
        if vertice2 in get_adj_vertice(vertice = vertice1, g = g):
            return True
        else:
            return False

    elif M:
        if vertice2 in get_adj_vertice(vertice = vertice1, M = M):
            return True
        else:
            return False

    elif I:
        if vertice2 in get_adj_vertice(vertice = vertice1, I = I):
            return True
        else:
            return False
    elif adj:
        if vertice2 in get_adj_vertice(vertice = vertice1, adj = adj):
            return True
        else:
            return False

def get_degree(vertice: object, g: Graph = None, M = None, I = None, adj = None) -> int:
    """
    De acordo com g, M, I ou adj for passado como parâmetro trata como a representação respectiva
    usa variavel count para contar cada vertice adjacente e retornar esse número para todos os casos
    """
    count = 0
    if g:
        adj_list = get_adj_vertice(vertice, g = g)
        for i in adj_list:
            count += 1
    elif M:
        adj_list = get_adj_vertice(vertice, M = M)
        for i in adj_list:
            count += 1
    elif I:
        adj_list = get_adj_vertice(vertice, I = I)
        for i in adj_list:
            count += 1
    elif adj:
        adj_list = get_adj_vertice(vertice, adj = adj)
        for i in adj_list:
            count += 1

    return count

def list_all_degrees(g: Graph = None, M = None, I = None, adj = None) -> dict[object, object]:
    """
    De acordo com g, M, I ou adj for passado como parâmetro trata como a representação respectiva
    para todos os vertices calcula seu grau e adiciona no dicionario que é retornado posteriormente
    """
    all_degrees = {}

    if g:
        for i in g.vertices:
            all_degrees[i] = get_degree(vertice = i, g = g)
    elif M:
        for i in range(get_vertices_num(M = M)):
            all_degrees[i] = get_degree(vertice = i, M = M)
    elif I:
        for i in range(get_vertices_num(I = I)):
            all_degrees[i] = get_degree(vertice = i, I = I)
    elif adj:
        for i in list(adj.keys()):
            all_degrees[i] = get_degree(vertice = i, adj = adj)

    return all_degrees

def caminho_simples(caminho: list[object], vertice1: object, vertice2: object, g: Graph = None, M = None, I = None, adj = None) -> list[object]:
    """
    De acordo com g, M, I ou adj for passado como parâmetro trata como a representação respectiva
    para todos os casos vai colocando no caminho os vertices visitados a partir dos vertices adjacentes
    vai percorrendo recursivamente, se achar um resultado ele é propagado até a primeira chamada da recursão
    caso contrario é retirado o ultimo elemento do caminho e retorna None
    """
    resultado = None
    caminho.append(vertice1)
    if vertice1 == vertice2:
        return caminho.copy()
    
    if g:
        v_adj = get_adj_vertice(vertice = vertice1, g = g)
    elif M:
        v_adj = get_adj_vertice(vertice = vertice1, M = M)
    elif I:
        v_adj = get_adj_vertice(vertice = vertice1, I = I)
    elif adj:
        v_adj = get_adj_vertice(vertice = vertice1, adj = adj)

    for i in v_adj:
        if i not in caminho:

            if g:
                resultado = caminho_simples(caminho = caminho, vertice1 = i, vertice2 = vertice2, g = g)
            elif M:
                resultado = caminho_simples(caminho = caminho, vertice1 = i, vertice2 = vertice2, M = M)
            elif I:
                resultado = caminho_simples(caminho = caminho, vertice1 = i, vertice2 = vertice2, I = I)
            elif adj:
                resultado = caminho_simples(caminho = caminho, vertice1 = i, vertice2 = vertice2, adj = adj)

            if resultado != None:
                return resultado
    caminho.pop()
    return None

def ciclo_vertice(vertice: object, g: Graph = None, M = None, I = None, adj = None):
    """
    De acordo com g, M, I ou adj for passado como parâmetro trata como a representação respectiva
    para todos os casos pega os vertices adjacentes do primeiro vertice
    para cada um deles tenta pegar um terceiro vertice distinto dos que ja estao sendo considerados
    ao ter 3 vertices distintos tenta achar um caminho entre o terceiro vertice e o primeiro
    se achar algum caminho este sera um ciclo
    """

    if g:
        v1_adj = get_adj_vertice(vertice = vertice, g = g)
    elif M:
        v1_adj = get_adj_vertice(vertice = vertice, M = M)
    elif I:
        v1_adj = get_adj_vertice(vertice = vertice, I = I)
    elif adj:
        v1_adj = get_adj_vertice(vertice = vertice, adj = adj)

    for i in v1_adj:

        if g:
            v2_adj = get_adj_vertice(vertice = i, g = g)
        elif M:
            v2_adj = get_adj_vertice(vertice = i, M = M)
        elif I:
            v2_adj = get_adj_vertice(vertice = i, I = I)
        elif adj:
            v2_adj = get_adj_vertice(vertice = i, adj = adj)

        if vertice in v2_adj:
            v2_adj.remove(vertice)
        if i in v2_adj:
            v2_adj.remove(i)

        for j in v2_adj:
            cam = []
            cam.append(i)

            if g:
                ciclo = caminho_simples(caminho = cam, vertice1 = j, vertice2 = vertice, g = g)
            elif M:
                ciclo = caminho_simples(caminho = cam, vertice1 = j, vertice2 = vertice, M = M)
            elif I:
                ciclo = caminho_simples(caminho = cam, vertice1 = j, vertice2 = vertice, I = I)
            elif adj:
                ciclo = caminho_simples(caminho = cam, vertice1 = j, vertice2 = vertice, adj = adj)

            if ciclo != None:
                ciclo.insert(0, vertice)
                return ciclo
    return None
    
def is_subgraph(g1: Graph = None, g2: Graph = None, M1 = None, M2 = None, I1 = None, I2 = None, adj1 = None, adj2 = None, v_list: List = None, v_list2: List = None) -> bool:
    """
    De acordo com g, M, I ou adj for passado como parâmetro trata como a representação respectiva
    em todos os casos primeiro checa se os vertices estao contidos em g1 e entao se as arestas tambem estao
    e se estas tem vertices que estao em g2
    para M e I foi preciso de uma lista com o nome dos vertices para serem identificados em grafos diferentes
    """
    if g1 and g2:
        for i in g2.vertices:
            if i not in g1.vertices:
                return False
        for j in g2.edges:
            u, v = j
            if j not in g1.edges or u not in g2.vertices or v not in g2.vertices:
                return False
        return True
    elif M1 and M2:
        for i in v_list2:
            if i not in v_list:
                return False
        num_vertices = get_vertices_num(M = M2)
        for i in range(num_vertices):
            for j in range(num_vertices):
                value = M2[i][j]
                if M1[v_list.index(v_list2[i])][v_list.index(v_list2[j])] != value:
                    return False
        return True
    elif I1 and I2:
        for i in v_list2:
            if i not in v_list:
                print("teste1")
                return False
        
        for i in range(get_edge_num(I = I2)):
            list = []
            found = False
            for j in range(get_vertices_num(I = I2)):
                if I2[j][i] == 1:
                    list.append(v_list.index(v_list2[j]))
                elif I2[j][i] == 2:
                    list.append(v_list.index(v_list2[j]))
                    list.append(v_list.index(v_list2[j]))
            for k in range(get_edge_num(I = I1)):
                if I1[list[0]][k] >= 1:
                    if I1[list[1]][k] >= 1:
                        found = True
            if found == False:
                return False
            
        return True
    elif adj1 and adj2:
        a1k = adj1.keys()
        for i in adj2.keys():
            if i not in a1k:
                return False
            for j in adj2[i]:
                if j not in adj1[i]:
                    return False
        return True






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

    #um segundo grafo para testar a funcao de subgrafo
    vertices2 = ['A', 'C', 'D']
    edges2 = [('A', 'C'), ('C', 'C')]
    g2 = Graph(vertices2, edges2)

    print("G:", g2)
    M2 = graph_to_adj_matrix(g2)
    print("Matriz de adjacência:")
    for row in M2:
        print(row)

    I2 = graph_to_incidence_matrix(g2)
    print("Matriz de incidência (linhas=vértices, colunas=arestas):")
    for row in I2:
        print(row)

    adj2 = graph_to_adj_list(g2)
    print("Lista de adjacência:")
    for k, v in adj2.items():
        print(f"{k}: {v}")

    # Converta de matriz de adjacência de volta ao grafo
    g_adjm = adj_matrix_to_graph(M, vertices)
    print("Grafo reconstituído de M:", g_adjm)

    # Converta de matriz de incidência de volta ao grafo
    g_im = incidence_matrix_to_graph(I, vertices)
    print("Grafo reconstituído de I:", g_im)

    print("Número de vértices do Grafo: ", get_vertices_num(g = g))
    print("Número de vértices da Matriz de Adjacência: ", get_vertices_num(M = M))
    print("Número de vértices da Matriz de Incidência: ", get_vertices_num(I = I))
    print("Número de vértices da Lista de Adjacência", get_vertices_num(adj = adj))

    print("Número de arestas do Grafo: ", get_edge_num(g = g))
    print("Número de arestas da Matriz de Adjacência: ", get_edge_num(M = M))
    print("Número de arestas da Matriz de Incidência: ", get_edge_num(I = I))
    print("Número de arestas da Lista de Adjacência: ", get_edge_num(adj = adj))

    v0 = 'C'
    v1 = 2
    v2 = 2
    v3 = 'C'
    print("Lista de vértices adjacentes de ", v0, ": ", get_adj_vertice(vertice = v0, g = g))
    print("Lista de vértices adjacentes de ", v1, ": ", get_adj_vertice(vertice = v1, M = M))
    print("Lista de vértices adjacentes de ", v2, ": ", get_adj_vertice(vertice = v2, I = I))
    print("Lista de vértices adjacentes de ", v3, ": ", get_adj_vertice(vertice = v3, adj = adj))

    v4 = 'A'
    v5 = 'B'
    v6 = 0
    v7 = 1
    v8 = 0
    v9 = 1
    v10 = 'A'
    v11 = 'B'
    print("Existência da aresta ", v4, "-", v5, edge_exist(vertice1 = v4, vertice2 = v5, g = g))
    print("Existência da aresta ", v6, "-", v7, edge_exist(vertice1 = v6, vertice2 = v7, M = M))
    print("Existência da aresta ", v8, "-", v9, edge_exist(vertice1 = v8, vertice2 = v9, I = I))
    print("Existência da aresta ", v10, "-", v11, edge_exist(vertice1 = v10, vertice2 = v11, adj = adj))

    v12 = 'A'
    v13 = 0
    v14 = 0
    v15 = 'A'
    print("Grau de ", v12, ": ", get_degree(vertice = v12, g = g))
    print("Grau de ", v13, ": ", get_degree(vertice = v13, M = M))
    print("Grau de ", v14, ": ", get_degree(vertice = v14, I = I))
    print("Grau de ", v15, ": ", get_degree(vertice = v15, adj = adj))

    print("Grau de todos os vértices do Grafo: ", list_all_degrees(g = g))
    print("Grau de todos os vértices da Matriz de Adjacência: ", list_all_degrees(M = M))
    print("Grau de todos os vértices da Matriz de Incidência: ", list_all_degrees(I = I))
    print("Grau de todos os vértices da Lista de Adjacência: ", list_all_degrees(adj = adj))

    v16 = 'A'
    v17 = 'C'
    v18 = 0
    v19 = 2
    v20 = 0
    v21 = 2
    v22 = 'A'
    v23 = 'C'
    caminho0 = []
    caminho1 = []
    caminho2 = []
    caminho3 = []
    print("Caminho simples de ", v16, "a", v17, ": ", caminho_simples(caminho = caminho0, vertice1 = v16, vertice2 = v17, g = g))
    print("Caminho simples de ", v18, "a", v19, ": ", caminho_simples(caminho = caminho1, vertice1 = v18, vertice2 = v19, M = M))
    print("Caminho simples de ", v20, "a", v21, ": ", caminho_simples(caminho = caminho2, vertice1 = v20, vertice2 = v21, I = I))
    print("Caminho simples de ", v22, "a", v23, ": ", caminho_simples(caminho = caminho3, vertice1 = v22, vertice2 = v23, adj = adj))
    
    v24 = 'A'
    v25 = 1
    v26 = 1
    v27 = 'A'
    print("Ciclo de ", v24, ": ", ciclo_vertice(vertice = v24, g = g))
    print("Ciclo de ", v25, ": ", ciclo_vertice(vertice = v25, M = M))
    print("Ciclo de ", v26, ": ", ciclo_vertice(vertice = v26, I = I))
    print("Ciclo de ", v27, ": ", ciclo_vertice(vertice = v27, adj = adj))

    print("g2 é subgrafo de g1: ", is_subgraph(g1 = g, g2 = g2))
    print("M2 é subgrafo de M1: ", is_subgraph(M1 = M, M2 = M2, v_list = vertices, v_list2 = vertices2))
    print("I2 é subgrafo de I1: ", is_subgraph(I1 = I, I2 = I2, v_list = vertices, v_list2 = vertices2))
    print("adj2 é subgrafo de adj1: ", is_subgraph(adj1 = adj, adj2 = adj2))

    # Visualize (requer networkx + matplotlib no ambiente)
    try:
        visualize_graph(g, "Exemplo")
    except Exception as e:
        print("Visualização falhou (talvez matplotlib não instalado):", e)