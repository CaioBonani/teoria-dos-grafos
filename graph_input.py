from typing import List, Tuple, Dict, Any
from main import Graph

def read_graph_from_terminal(weighted: bool = False) -> Graph:
    """
    Lê um grafo através do terminal.
    
    Tutorial de entrada:
    - Primeiro, digite os vértices separados por espaço
    - Depois, digite o número de arestas
    - Para cada aresta, digite:
      - Se não ponderado: "vertice1 vertice2"
      - Se ponderado: "vertice1 vertice2 peso"
    
    Exemplo sem peso:
    Vértices: A B C D
    Número de arestas: 3
    Aresta 1: A B
    Aresta 2: B C
    Aresta 3: C D
    
    Exemplo com peso:
    Vértices: A B C D
    Número de arestas: 3
    Aresta 1: A B 2.5
    Aresta 2: B C 1.0
    Aresta 3: C D 3.7
    """
    print("\n=== Tutorial de Entrada do Grafo ===")
    print("1. Digite os vértices separados por espaço (ex: A B C D)")
    print("2. Digite o número de arestas")
    print("3. Para cada aresta, digite:")
    if weighted:
        print("   vertice1 vertice2 peso (ex: A B 2.5)")
    else:
        print("   vertice1 vertice2 (ex: A B)")
    print("\nIniciando entrada do grafo...")
    
    # Lê os vértices
    vertices_input = input("\nDigite os vértices separados por espaço: ").strip()
    vertices = vertices_input.split()
    
    # Lê o número de arestas
    while True:
        try:
            num_edges = int(input("Digite o número de arestas: "))
            break
        except ValueError:
            print("Por favor, digite um número inteiro válido.")
    
    # Lê as arestas
    edges = []
    weights = {}
    print(f"\nDigite cada aresta {'com seu peso ' if weighted else ''}(uma por linha):")
    for i in range(num_edges):
        while True:
            try:
                edge_input = input(f"Aresta {i+1}: ").strip().split()
                if weighted:
                    if len(edge_input) != 3:
                        raise ValueError("Formato inválido. Use: vertice1 vertice2 peso")
                    u, v, w = edge_input
                    weight = float(w)
                    if u not in vertices or v not in vertices:
                        raise ValueError("Vértice não encontrado na lista de vértices")
                    edges.append((u, v))
                    weights[(u, v)] = weight
                else:
                    if len(edge_input) != 2:
                        raise ValueError("Formato inválido. Use: vertice1 vertice2")
                    u, v = edge_input
                    if u not in vertices or v not in vertices:
                        raise ValueError("Vértice não encontrado na lista de vértices")
                    edges.append((u, v))
                break
            except ValueError as e:
                print(f"Erro: {e}. Tente novamente.")
    
    return Graph(vertices, edges, weights if weighted else None)

def read_graph_from_file(filename: str, weighted: bool = False) -> Graph:
    """
    Lê um grafo de um arquivo texto.
    
    Formato do arquivo:
    - Primeira linha: vértices separados por espaço
    - Segunda linha: número de arestas (n)
    - Próximas n linhas: arestas no formato
      - Se não ponderado: "vertice1 vertice2"
      - Se ponderado: "vertice1 vertice2 peso"
    
    Exemplo de arquivo sem peso:
    A B C D
    3
    A B
    B C
    C D
    
    Exemplo de arquivo com peso:
    A B C D
    3
    A B 2.5
    B C 1.0
    C D 3.7
    """
    try:
        with open(filename, 'r') as f:
            # Lê os vértices
            vertices = f.readline().strip().split()
            
            # Lê o número de arestas
            num_edges = int(f.readline().strip())
            
            # Lê as arestas
            edges = []
            weights = {}
            for _ in range(num_edges):
                line = f.readline().strip().split()
                if weighted:
                    if len(line) != 3:
                        raise ValueError(f"Formato inválido de aresta: {' '.join(line)}")
                    u, v, w = line
                    weight = float(w)
                    if u not in vertices or v not in vertices:
                        raise ValueError(f"Vértice não encontrado na lista de vértices: {u} ou {v}")
                    edges.append((u, v))
                    weights[(u, v)] = weight
                else:
                    if len(line) != 2:
                        raise ValueError(f"Formato inválido de aresta: {' '.join(line)}")
                    u, v = line
                    if u not in vertices or v not in vertices:
                        raise ValueError(f"Vértice não encontrado na lista de vértices: {u} ou {v}")
                    edges.append((u, v))
                    
        return Graph(vertices, edges, weights if weighted else None)
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo não encontrado: {filename}")
    except ValueError as e:
        raise ValueError(f"Erro ao ler o arquivo: {e}")