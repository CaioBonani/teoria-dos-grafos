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
    
def is_subgraph_21(g1: Graph = None, g2: Graph = None, M1 = None, M2 = None, I1 = None, I2 = None, adj1 = None, adj2 = None, v_list: List = None, v_list2: List = None) -> bool:
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


def is_subgraph(g1: Graph = None, g2: Graph = None, M1 = None, M2 = None, I1 = None, I2 = None, adj1 = None, adj2 = None, v_list: List = None, v_list2: List = None) -> int:
    if g1 and g2:
        if is_subgraph_21(g1 = g1, g2 = g2):
            return 2
        elif is_subgraph_21(g1 = g2, g2 = g1):
            return 1
        else:
            return 0

    elif M1 and M2:
        if is_subgraph_21(M1 = M1, M2 = M2, v_list = v_list, v_list2 = v_list2):
            return 2
        elif is_subgraph_21(M1 = M2, M2 = M1, v_list = v_list2, v_list2 = v_list):
            return 1
        else:
            return 0

    elif I1 and I2:
        if is_subgraph_21(I1 = I1, I2 = I2, v_list = v_list, v_list2 = v_list2):
            return 2
        elif is_subgraph_21(I1 = I2, I2 = I1, v_list = v_list2, v_list2 = v_list):
            return 1
        else:
            return 0

    elif adj1 and adj2:
        if is_subgraph_21(adj1 = adj1, adj2 = adj2):
            return 2
        elif is_subgraph_21(adj1 = adj2, adj2 = adj1):
            return 1
        else:
            return 0


# --- Exemplo demonstrativo com dois grafos ---
if __name__ == "__main__":
    print("\n=== Criando o grafo principal (G1) ===")
    # Grafo principal com 6 vértices representando uma casa
    vertices_g1 = ['Sala', 'Cozinha', 'Quarto1', 'Quarto2', 'Banheiro', 'Varanda']
    edges_g1 = [
        ('Sala', 'Cozinha'), ('Sala', 'Quarto1'), ('Sala', 'Quarto2'),
        ('Quarto1', 'Banheiro'), ('Quarto2', 'Banheiro'), ('Sala', 'Varanda')
    ]
    g1 = Graph(vertices_g1, edges_g1)
    print("Grafo G1 (Casa completa):", g1)

    # Criar todas as representações para G1
    M1 = graph_to_adj_matrix(g1)
    I1 = graph_to_incidence_matrix(g1)
    adj1 = graph_to_adj_list(g1)

    print("\nMatriz de adjacência do G1:")
    for row in M1:
        print(row)
    
    print("\nLista de adjacência do G1:")
    for k, v in adj1.items():
        print(f"{k}: {v}")

    print("\n=== Criando o subgrafo (G2) ===")
    # Subgrafo representando apenas uma parte da casa
    vertices_g2 = ['Sala', 'Quarto1', 'Banheiro']
    edges_g2 = [('Sala', 'Quarto1'), ('Quarto1', 'Banheiro')]
    g2 = Graph(vertices_g2, edges_g2)
    print("Grafo G2 (Parte da casa):", g2)

    # Criar todas as representações para G2
    M2 = graph_to_adj_matrix(g2)
    I2 = graph_to_incidence_matrix(g2)
    adj2 = graph_to_adj_list(g2)

    print("\n=== Análise dos grafos ===")
    print(f"Número de vértices G1: {get_vertices_num(g=g1)}")
    print(f"Número de arestas G1: {get_edge_num(g=g1)}")
    print(f"Número de vértices G2: {get_vertices_num(g=g2)}")
    print(f"Número de arestas G2: {get_edge_num(g=g2)}")

    print("\n=== Vértices adjacentes ===")
    print(f"Adjacentes à Sala em G1: {get_adj_vertice('Sala', g=g1)}")
    print(f"Adjacentes à Sala em G2: {get_adj_vertice('Sala', g=g2)}")

    print("\n=== Verificação de arestas ===")
    print(f"Existe aresta Sala-Cozinha em G1? {edge_exist('Sala', 'Cozinha', g=g1)}")
    print(f"Existe aresta Sala-Cozinha em G2? {edge_exist('Sala', 'Cozinha', g=g2)}")

    print("\n=== Graus dos vértices ===")
    print("Graus em G1:", list_all_degrees(g=g1))
    print("Graus em G2:", list_all_degrees(g=g2))

    print("\n=== Caminhos simples ===")
    caminho1 = []
    caminho2 = []
    print("Caminho Sala->Banheiro em G1:", caminho_simples(caminho1, 'Sala', 'Banheiro', g=g1))
    print("Caminho Sala->Banheiro em G2:", caminho_simples(caminho2, 'Sala', 'Banheiro', g=g2))

    print("\n=== Procurando ciclos ===")
    print("Ciclo partindo da Sala em G1:", ciclo_vertice('Sala', g=g1))
    print("Ciclo partindo da Sala em G2:", ciclo_vertice('Sala', g=g2))

    print("\n=== Verificação de subgrafo ===")
    print("0 = não, 1 = G1 é subgrafo de G2, 2 = G2 é subgrafo de G1")
    print("Dado G1 e G2, são subgrafos entre si?", is_subgraph(g1=g1, g2=g2))
    print("Verificando outras representações:")
    print("- Matriz de adjacência:", is_subgraph(M1=M1, M2=M2, v_list=vertices_g1, v_list2=vertices_g2))
    print("- Matriz de incidência:", is_subgraph(I1=I1, I2=I2, v_list=vertices_g1, v_list2=vertices_g2))
    print("- Lista de adjacência:", is_subgraph(adj1=adj1, adj2=adj2))

    print("\n=== Visualização dos grafos ===")
    try:
        print("\nVisualizando G1 (Casa completa):")
        visualize_graph(g1, "Casa Completa (G1)")
        print("\nVisualizando G2 (Parte da casa):")
        visualize_graph(g2, "Parte da Casa (G2)")
    except Exception as e:
        print("Visualização falhou (talvez matplotlib não instalado):", e)
