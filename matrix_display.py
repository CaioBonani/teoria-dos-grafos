from typing import List, Dict, Any

def format_matrix(matrix: List[List[int]], vertices: List[str], matrix_type: str = "adjacency") -> str:
    """
    Formata uma matriz (adjacência ou incidência) para exibição com rótulos.
    """
    if not matrix or not vertices:
        return "Matriz vazia"
    
    # Determina a largura máxima necessária para cada coluna
    max_vertex_width = max(len(str(v)) for v in vertices)
    max_value_width = max(len(str(val)) for row in matrix for val in row)
    col_width = max(max_vertex_width, max_value_width) + 1
    
    # Cria o cabeçalho
    result = " " * (max_vertex_width + 2)  # Espaço para alinhar com a primeira coluna
    if matrix_type == "adjacency":
        # Para matriz de adjacência, usa os vértices como cabeçalho das colunas
        for v in vertices:
            result += str(v).center(col_width)
    else:
        # Para matriz de incidência, numera as arestas
        for i in range(len(matrix[0])):
            result += f"e{i+1}".center(col_width)
    result += "\n"
    
    # Adiciona uma linha separadora
    result += "-" * (max_vertex_width + 2 + col_width * len(matrix[0])) + "\n"
    
    # Adiciona cada linha da matriz com seu rótulo
    for v, row in zip(vertices, matrix):
        result += f"{str(v):>{max_vertex_width}} |"
        for val in row:
            result += str(val).center(col_width)
        result += "\n"
    
    return result

def format_adj_list(adj_list: Dict[Any, List[Any]], show_weights: bool = False, weights: Dict = None) -> str:
    """
    Formata uma lista de adjacência para exibição.
    Se show_weights for True e weights for fornecido, mostra os pesos das arestas.
    """
    if not adj_list:
        return "Lista de adjacência vazia"
    
    # Encontra o vértice com o nome mais longo para alinhar a saída
    max_vertex_width = max(len(str(v)) for v in adj_list.keys())
    result = ""
    
    for vertex, neighbors in adj_list.items():
        # Formata o vértice atual
        result += f"{str(vertex):>{max_vertex_width}} |"
        
        # Se não houver vizinhos
        if not neighbors:
            result += " ∅"  # Símbolo para conjunto vazio
        else:
            # Formata cada vizinho (com peso, se aplicável)
            formatted_neighbors = []
            for neighbor in neighbors:
                if show_weights and weights:
                    weight = weights.get((vertex, neighbor)) or weights.get((neighbor, vertex))
                    if weight is not None:
                        formatted_neighbors.append(f"{neighbor}({weight:.1f})")
                    else:
                        formatted_neighbors.append(str(neighbor))
                else:
                    formatted_neighbors.append(str(neighbor))
            
            result += " " + " ".join(formatted_neighbors)
        
        result += "\n"
    
    return result

# Exemplo de uso:
if __name__ == "__main__":
    # Exemplo de matriz de adjacência
    vertices = ['A', 'B', 'C']
    adj_matrix = [
        [0, 1, 1],
        [1, 0, 0],
        [1, 0, 0]
    ]
    print("Matriz de Adjacência:")
    print(format_matrix(adj_matrix, vertices, "adjacency"))
    
    # Exemplo de matriz de incidência
    inc_matrix = [
        [1, 0],
        [1, 1],
        [0, 1]
    ]
    print("\nMatriz de Incidência:")
    print(format_matrix(inc_matrix, vertices, "incidence"))
    
    # Exemplo de lista de adjacência
    adj_list = {
        'A': ['B', 'C'],
        'B': ['A'],
        'C': ['A']
    }
    weights = {('A', 'B'): 2.5, ('A', 'C'): 1.0}
    print("\nLista de Adjacência:")
    print(format_adj_list(adj_list))
    print("\nLista de Adjacência com pesos:")
    print(format_adj_list(adj_list, True, weights))