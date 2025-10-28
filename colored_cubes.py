import networkx as nx
import matplotlib.pyplot as plt
from main import get_degree
import copy


def draw_graph(G: nx.Graph, v_order: list = None, title: str = None):
    """
    Plota o grafo usando posicoes fixas
    """
    pos = {}
    a = 1
    b = 1
    if v_order != None:
        order = v_order
    else:
        order = G.nodes

    if title != None:
        plt.title(title)

    for u in order:
        pos[u] = (a,b)
        b = -b
        if b == 1:
            a = -a
    edge_labels = nx.get_edge_attributes(G, 'label')

    nx.draw(G, pos, with_labels=True, node_color='lightblue', 
            node_size=500, font_size=16, font_weight='bold',
            edge_color='gray', width=2)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black', label_pos = 0.4)
    plt.show()


def build_graph(G: nx.Graph, cube: list, num: str):
    """
    Constroi o grafo de acordo com os pares de faces opostas
    """
    even = [0, 2, 4]

    for i in range(len(cube)):
        if i in even:
            if (cube[i], cube[i+1]) in G.edges:
                G[cube[i]][cube[i+1]]['label'] += num
            else:
                G.add_edge(cube[i], cube[i+1], label = num)


def is_new_subgraph(subgraphs: list, new_subgraph: nx.Graph) -> bool:
    """
    Retorna se o subgrafo em questao nao esta na lista de grafos
    """
    for g in subgraphs:
        equal_edges = 0
        for edge in g.edges:
            if edge in new_subgraph.edges and new_subgraph[edge[0]][edge[1]]['label'] == g[edge[0]][edge[1]]['label']:
                equal_edges += 1
        if equal_edges == 4:
            return False
    return True


def disj_graph(graphs: list[nx.Graph]) -> list[object]:
    """
    Retorna uma lista dos pares de grafos cujas arestas sao disjuntas
    """
    disj_list = []
    for i in range(len(graphs)):
        for j in range(len(graphs)):
            if i < j:
                disj = True
                for edge in graphs[i].edges:
                    if edge in graphs[j].edges and graphs[j][edge[0]][edge[1]]['label'] == graphs[i][edge[0]][edge[1]]['label']:
                        disj = False
                if disj == True:
                    disj_list.append((i,j))
    return disj_list


def list_subgraphs(G: nx.Graph, label_arestas: list, subgraphs: list = None, cube_list: list = None, new_graph: nx.Graph = None) -> list[nx.Graph]:
    """
    Lista os subgrafos de 4 arestas entre vertices diferentes em que o grau de cada vertice eh 2
    """
    if subgraphs == None:
        subgraphs = []
    if cube_list == None:
        cube_list = []
    if new_graph == None:
        new_graph = nx.Graph()
   
    for i in G.edges:
        if i not in new_graph.edges:
            new_graph.add_edge(i[0], i[1], label = '')
            if get_degree(vertice = i[0], g = new_graph) <= 2 and get_degree(vertice = i[1], g = new_graph) <= 2:
                
                for j in label_arestas[i]:
                    if j not in cube_list:
                        new_graph[i[0]][i[1]]['label'] = j
                        cube_list.append(j)

                        if len(cube_list) < 4:
                            list_subgraphs(G = G, label_arestas = label_arestas, subgraphs = subgraphs, cube_list = cube_list, new_graph = new_graph)
                        elif len(cube_list) == 4:
                            if is_new_subgraph(subgraphs, new_graph) == True:
                                subgraphs.append(copy.deepcopy(new_graph))

                        cube_list.remove(j)
            new_graph.remove_edge(i[0], i[1])

    if len(cube_list) == 0: 
        return subgraphs
    return None

def solve_cube_problem(cubes: list, v_order: list):
    """
    Resolve o problema dos cubos coloridos e printa as solucoes caso ache
    """
    G_cubes = nx.Graph()
    nc = 1
    for cube in cubes:
        build_graph(G_cubes, cube, str(nc))
        nc += 1
    draw_graph(G_cubes, v_order, title = "Grafo Principal")

    labels_arestas = nx.get_edge_attributes(G_cubes, 'label')
    sub = list_subgraphs(G_cubes, labels_arestas)

    print("Foram encontrados ", len(sub), " subgrafos")
    for i in range(len(sub)):
        title = "Grafo " + str(i)
        draw_graph(sub[i], v_order, title = title)

    disj = disj_graph(sub)
    print("========== Soluções ==========")
    if len(disj) == 0:
        print("Não foi encontrado nenhuma solução")
    else:
        for i in disj:
            print("Grafo ", i[0], " e ", i[1])
    
    

if __name__ == "__main__":
    # define as cores das faces de cada cubo
    # sendo que as faces sao dadas em pares(posicao 0 e 1, 2 e 3, 4 e 5 sao opostas)
    cubes = [
        ['R', 'R', 'R', 'G', 'B', 'W'],
        ['B', 'W', 'W', 'G', 'G', 'R'],
        ['W', 'G', 'R', 'W', 'B', 'R'],
        ['B', 'R', 'G', 'G', 'B', 'W']
    ]
    #define a ordem que as 4 cores vao ser posicionadas no grafo
    v_order = ['R', 'G', 'B', 'W']
    solve_cube_problem(cubes, v_order)