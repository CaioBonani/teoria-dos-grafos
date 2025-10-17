from typing import List, Dict, Any, Tuple
from main import Graph, adj_matrix_to_graph, incidence_matrix_to_graph, adj_list_to_graph

def read_matrix_from_terminal(matrix_type: str = "adjacency") -> Tuple[List[List[int]], List[str]]:
    """
    Lê uma matriz do terminal (adjacência ou incidência).
    Retorna a matriz e a lista de vértices.
    """
    print(f"\n=== Tutorial de Entrada da Matriz de {matrix_type.title()} ===")
    print("1. Digite os rótulos dos vértices separados por espaço (ex: A B C D)")
    if matrix_type == "adjacency":
        print("2. Digite cada linha da matriz de adjacência, números separados por espaço")
        print("\nExemplo para grafo com 3 vértices (A B C):")
        print("A B C")
        print("0 1 1  # conexões do vértice A")
        print("1 0 0  # conexões do vértice B")
        print("1 0 0  # conexões do vértice C")
    else:  # incidence
        print("2. Digite o número de arestas")
        print("3. Digite cada linha da matriz de incidência, números separados por espaço")
        print("\nExemplo para grafo com 3 vértices e 2 arestas:")
        print("A B C")
        print("2  # número de arestas")
        print("1 0  # conexões do vértice A")
        print("1 1  # conexões do vértice B")
        print("0 1  # conexões do vértice C")
    
    # Lê os vértices
    vertices = input("\nDigite os rótulos dos vértices: ").strip().split()
    n = len(vertices)
    
    if matrix_type == "adjacency":
        # Lê matriz de adjacência
        print(f"\nDigite as {n} linhas da matriz de adjacência:")
        matrix = []
        for i in range(n):
            while True:
                try:
                    row = [int(x) for x in input(f"Linha {i+1} ({vertices[i]}): ").strip().split()]
                    if len(row) != n:
                        raise ValueError(f"A linha deve ter {n} números")
                    matrix.append(row)
                    break
                except ValueError as e:
                    print(f"Erro: {e}. Tente novamente.")
    
    else:  # incidence
        # Lê número de arestas
        while True:
            try:
                m = int(input("\nDigite o número de arestas: "))
                break
            except ValueError:
                print("Por favor, digite um número inteiro válido.")
        
        # Lê matriz de incidência
        print(f"\nDigite as {n} linhas da matriz de incidência:")
        matrix = []
        for i in range(n):
            while True:
                try:
                    row = [int(x) for x in input(f"Linha {i+1} ({vertices[i]}): ").strip().split()]
                    if len(row) != m:
                        raise ValueError(f"A linha deve ter {m} números")
                    matrix.append(row)
                    break
                except ValueError as e:
                    print(f"Erro: {e}. Tente novamente.")
    
    return matrix, vertices

def read_adj_list_from_terminal() -> Dict[Any, List[Any]]:
    """
    Lê uma lista de adjacência do terminal.
    """
    print("\n=== Tutorial de Entrada da Lista de Adjacência ===")
    print("1. Digite os rótulos dos vértices separados por espaço (ex: A B C D)")
    print("2. Para cada vértice, digite seus vizinhos separados por espaço")
    print("\nExemplo:")
    print("A B C D")
    print("A: B C    # vizinhos do vértice A")
    print("B: A      # vizinhos do vértice B")
    print("C: A      # vizinhos do vértice C")
    print("D:        # D não tem vizinhos")
    
    # Lê os vértices
    vertices = input("\nDigite os rótulos dos vértices: ").strip().split()
    
    # Lê as listas de adjacência
    adj_list = {}
    print("\nPara cada vértice, digite seus vizinhos (ou pressione Enter se não houver):")
    for v in vertices:
        while True:
            try:
                neighbors = input(f"{v}: ").strip().split()
                if not all(n in vertices for n in neighbors):
                    raise ValueError("Todos os vizinhos devem ser vértices válidos")
                adj_list[v] = neighbors
                break
            except ValueError as e:
                print(f"Erro: {e}. Tente novamente.")
    
    return adj_list

def read_matrix_from_file(filename: str, matrix_type: str = "adjacency") -> Tuple[List[List[int]], List[str]]:
    """
    Lê uma matriz de um arquivo (adjacência ou incidência).
    
    Formato do arquivo para matriz de adjacência:
    A B C D    # vértices
    0 1 1 0    # linha 1
    1 0 0 1    # linha 2
    1 0 0 0    # linha 3
    0 1 0 0    # linha 4
    
    Formato do arquivo para matriz de incidência:
    A B C D    # vértices
    3          # número de arestas
    1 0 0      # linha 1
    1 1 0      # linha 2
    0 1 1      # linha 3
    0 0 1      # linha 4
    """
    try:
        with open(filename, 'r') as f:
            # Lê os vértices
            vertices = f.readline().strip().split()
            n = len(vertices)
            
            if matrix_type == "adjacency":
                # Lê matriz de adjacência
                matrix = []
                for _ in range(n):
                    row = [int(x) for x in f.readline().strip().split()]
                    if len(row) != n:
                        raise ValueError(f"Cada linha deve ter {n} números")
                    matrix.append(row)
            
            else:  # incidence
                # Lê número de arestas
                m = int(f.readline().strip())
                
                # Lê matriz de incidência
                matrix = []
                for _ in range(n):
                    row = [int(x) for x in f.readline().strip().split()]
                    if len(row) != m:
                        raise ValueError(f"Cada linha deve ter {m} números")
                    matrix.append(row)
            
            return matrix, vertices
            
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo não encontrado: {filename}")
    except ValueError as e:
        raise ValueError(f"Erro ao ler o arquivo: {e}")

def read_adj_list_from_file(filename: str) -> Dict[Any, List[Any]]:
    """
    Lê uma lista de adjacência de um arquivo.
    
    Formato do arquivo:
    A B C D    # vértices
    A: B C     # vizinhos de A
    B: A       # vizinhos de B
    C: A       # vizinhos de C
    D:         # vizinhos de D (nenhum)
    """
    try:
        with open(filename, 'r') as f:
            # Lê os vértices
            vertices = f.readline().strip().split()
            vertex_set = set(vertices)
            
            # Lê as listas de adjacência
            adj_list = {}
            for line in f:
                if not line.strip():
                    continue
                parts = line.strip().split(':')
                if len(parts) != 2:
                    raise ValueError(f"Formato inválido na linha: {line}")
                
                vertex = parts[0].strip()
                neighbors = parts[1].strip().split()
                
                if vertex not in vertex_set:
                    raise ValueError(f"Vértice inválido: {vertex}")
                if not all(n in vertex_set for n in neighbors):
                    raise ValueError(f"Vizinho inválido na linha: {line}")
                
                adj_list[vertex] = neighbors
            
            # Verifica se todos os vértices estão presentes
            for v in vertices:
                if v not in adj_list:
                    adj_list[v] = []
            
            return adj_list
            
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo não encontrado: {filename}")
    except ValueError as e:
        raise ValueError(f"Erro ao ler o arquivo: {e}")