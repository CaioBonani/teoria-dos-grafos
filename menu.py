from graph_input import read_graph_from_terminal, read_graph_from_file
from matrix_input import (read_matrix_from_terminal, read_matrix_from_file,read_adj_list_from_terminal, read_adj_list_from_file)
from matrix_display import format_matrix, format_adj_list
from main import (
    convert_representation, visualize_graph, Graph, 
    adj_matrix_to_graph, incidence_matrix_to_graph, adj_list_to_graph,
    get_vertices_num, get_edge_num, get_adj_vertice, edge_exist,
    get_degree, list_all_degrees, caminho_simples, ciclo_vertice,
    is_subgraph
)
import os

def clear_screen():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_menu():
    """Imprime o menu principal"""
    print("\n=== Menu Principal ===")
    print("1. Inserir grafo via terminal (vértices e arestas)")
    print("2. Inserir grafo via arquivo (vértices e arestas)")
    print("3. Inserir grafo via matriz de adjacência")
    print("4. Inserir grafo via matriz de incidência")
    print("5. Inserir grafo via lista de adjacência")
    print("6. Visualizar grafo atual")
    print("7. Mostrar matriz de adjacência")
    print("8. Mostrar matriz de incidência")
    print("9. Mostrar lista de adjacência")
    print("10. Verificar número de vértices")
    print("11. Verificar número de arestas")
    print("12. Verificar vértices adjacentes")
    print("13. Verificar existência de aresta")
    print("14. Verificar grau de um vértice")
    print("15. Listar graus de todos os vértices")
    print("16. Encontrar caminho simples entre dois vértices")
    print("17. Encontrar ciclo para um vértice")
    print("18. Verificar subgrafo")
    print("0. Sair")
    print("===================")

def print_submenu_entrada():
    """Imprime o submenu para escolha do método de entrada"""
    print("\n=== Método de Entrada ===")
    print("1. Via terminal")
    print("2. Via arquivo")
    print("0. Voltar")
    print("===================")

def print_submenu_peso():
    """Imprime o submenu para escolha de grafo com ou sem peso"""
    print("\n=== Tipo de Grafo ===")
    print("1. Grafo sem peso nas arestas")
    print("2. Grafo com peso nas arestas")
    print("0. Voltar")
    print("===================")

def show_input_file_tutorial():
    """Mostra o tutorial de como deve ser o arquivo de entrada"""
    print("\n=== Tutorial do Arquivo de Entrada ===")
    print("O arquivo deve seguir o seguinte formato:")
    print("1. Primeira linha: vértices separados por espaço")
    print("2. Segunda linha: número de arestas (n)")
    print("3. Próximas n linhas: definição das arestas")
    print("\nExemplo sem peso:")
    print("A B C D")
    print("3")
    print("A B")
    print("B C")
    print("C D")
    print("\nExemplo com peso:")
    print("A B C D")
    print("3")
    print("A B 2.5")
    print("B C 1.0")
    print("C D 3.7")
    print("\nObservações:")
    print("- Use espaços para separar os elementos")
    print("- Pesos devem ser números decimais (use ponto, não vírgula)")
    print("- Cada aresta deve estar em uma nova linha")
    print("==========================================")

def main():
    graph = None
    while True:
        clear_screen()
        print_menu()
        
        try:
            choice = input("\nEscolha uma opção: ").strip()
            
            if choice == '0':
                print("\nEncerrando programa...")
                break
                
            elif choice in ('1', '2'):  # Inserir grafo via vértices e arestas
                clear_screen()
                print_submenu_peso()
                weight_choice = input("\nEscolha uma opção: ").strip()
                
                if weight_choice == '0':
                    continue
                    
                if weight_choice not in ('1', '2'):
                    raise ValueError("Opção inválida!")
                
                weighted = weight_choice == '2'
                
                if choice == '1':
                    graph = read_graph_from_terminal(weighted)
                    print("\nGrafo inserido com sucesso!")
                else:  # choice == '2'
                    show_input_file_tutorial()
                    filename = input("\nDigite o nome do arquivo: ").strip()
                    graph = read_graph_from_file(filename, weighted)
                    print("\nGrafo lido do arquivo com sucesso!")
            
            elif choice in ('3', '4', '5'):  # Inserir grafo via matriz/lista
                clear_screen()
                print_submenu_entrada()
                input_choice = input("\nEscolha uma opção: ").strip()
                
                if input_choice == '0':
                    continue
                
                if input_choice not in ('1', '2'):
                    raise ValueError("Opção inválida!")
                
                if choice == '3':  # Matriz de adjacência
                    if input_choice == '1':
                        matrix, vertices = read_matrix_from_terminal("adjacency")
                    else:
                        filename = input("\nDigite o nome do arquivo: ").strip()
                        matrix, vertices = read_matrix_from_file(filename, "adjacency")
                    graph = adj_matrix_to_graph(matrix, vertices)
                
                elif choice == '4':  # Matriz de incidência
                    if input_choice == '1':
                        matrix, vertices = read_matrix_from_terminal("incidence")
                    else:
                        filename = input("\nDigite o nome do arquivo: ").strip()
                        matrix, vertices = read_matrix_from_file(filename, "incidence")
                    graph = incidence_matrix_to_graph(matrix, vertices)
                
                else:  # Lista de adjacência
                    if input_choice == '1':
                        adj_list = read_adj_list_from_terminal()
                    else:
                        filename = input("\nDigite o nome do arquivo: ").strip()
                        adj_list = read_adj_list_from_file(filename)
                    graph = adj_list_to_graph(adj_list)
                
                print("\nGrafo criado com sucesso!")
            
            elif choice == '6':  # Visualizar grafo
                if graph is None:
                    print("\nNenhum grafo foi inserido ainda!")
                else:
                    print("\nVisualizando grafo...")
                    try:
                        visualize_graph(graph)
                        print("\nGrafo visualizado com sucesso!")
                    except ImportError:
                        print("\nErro: matplotlib não está instalado.")
                        print("Para instalar, execute: pip install matplotlib")
                    
            elif choice in ('7', '8', '9'):  # Mostrar representações
                if graph is None:
                    print("\nNenhum grafo foi inserido ainda!")
                else:
                    representations = convert_representation(graph, 'graph')
                    if choice == '7':
                        print("\nMatriz de Adjacência:")
                        print(format_matrix(representations['adj_matrix'], 
                                         graph.vertices, "adjacency"))
                    elif choice == '8':
                        print("\nMatriz de Incidência:")
                        print(format_matrix(representations['incidence'], 
                                         graph.vertices, "incidence"))
                    else:  # choice == '9'
                        print("\nLista de Adjacência:")
                        print(format_adj_list(representations['adj_list'],
                                           True if hasattr(graph, 'weights') else False,
                                           graph.weights if hasattr(graph, 'weights') else None))
            
            elif choice == '10':  # Número de vértices
                if graph is None:
                    print("\nNenhum grafo foi inserido ainda!")
                else:
                    n = get_vertices_num(g=graph)
                    print(f"\nNúmero de vértices: {n}")

            elif choice == '11':  # Número de arestas
                if graph is None:
                    print("\nNenhum grafo foi inserido ainda!")
                else:
                    m = get_edge_num(g=graph)
                    print(f"\nNúmero de arestas: {m}")

            elif choice == '12':  # Vértices adjacentes
                if graph is None:
                    print("\nNenhum grafo foi inserido ainda!")
                else:
                    print("\nVértices disponíveis:", graph.vertices)
                    vertice = input("Digite o vértice para verificar adjacências: ").strip()
                    if vertice not in graph.vertices:
                        print(f"\nVértice '{vertice}' não encontrado!")
                    else:
                        adj = get_adj_vertice(vertice, g=graph)
                        print(f"\nVértices adjacentes a {vertice}:", adj)

            elif choice == '13':  # Verificar existência de aresta
                if graph is None:
                    print("\nNenhum grafo foi inserido ainda!")
                else:
                    print("\nVértices disponíveis:", graph.vertices)
                    v1 = input("Digite o primeiro vértice: ").strip()
                    v2 = input("Digite o segundo vértice: ").strip()
                    if v1 not in graph.vertices or v2 not in graph.vertices:
                        print("\nUm ou mais vértices não encontrados!")
                    else:
                        exists = edge_exist(v1, v2, g=graph)
                        if exists:
                            print(f"\nExiste uma aresta entre {v1} e {v2}")
                        else:
                            print(f"\nNão existe aresta entre {v1} e {v2}")

            elif choice == '14':  # Grau de um vértice
                if graph is None:
                    print("\nNenhum grafo foi inserido ainda!")
                else:
                    print("\nVértices disponíveis:", graph.vertices)
                    vertice = input("Digite o vértice: ").strip()
                    if vertice not in graph.vertices:
                        print(f"\nVértice '{vertice}' não encontrado!")
                    else:
                        grau = get_degree(vertice, g=graph)
                        print(f"\nGrau do vértice {vertice}: {grau}")

            elif choice == '15':  # Listar graus
                if graph is None:
                    print("\nNenhum grafo foi inserido ainda!")
                else:
                    graus = list_all_degrees(g=graph)
                    print("\nGraus dos vértices:")
                    for v, g in graus.items():
                        print(f"  {v}: {g}")

            elif choice == '16':  # Caminho simples
                if graph is None:
                    print("\nNenhum grafo foi inserido ainda!")
                else:
                    print("\nVértices disponíveis:", graph.vertices)
                    v1 = input("Digite o vértice de origem: ").strip()
                    v2 = input("Digite o vértice de destino: ").strip()
                    if v1 not in graph.vertices or v2 not in graph.vertices:
                        print("\nUm ou mais vértices não encontrados!")
                    else:
                        caminho = caminho_simples([], v1, v2, g=graph)
                        if caminho:
                            print(f"\nCaminho encontrado: {' -> '.join(caminho)}")
                        else:
                            print(f"\nNão existe caminho entre {v1} e {v2}")

            elif choice == '17':  # Ciclo para vértice
                if graph is None:
                    print("\nNenhum grafo foi inserido ainda!")
                else:
                    print("\nVértices disponíveis:", graph.vertices)
                    vertice = input("Digite o vértice: ").strip()
                    if vertice not in graph.vertices:
                        print(f"\nVértice '{vertice}' não encontrado!")
                    else:
                        ciclo = ciclo_vertice(vertice, g=graph)
                        if ciclo:
                            print(f"\nCiclo encontrado: {' -> '.join(ciclo)}")
                        else:
                            print(f"\nNão existe ciclo para o vértice {vertice}")

            elif choice == '18':  # Verificar subgrafo
                if graph is None:
                    print("\nNenhum grafo foi inserido ainda!")
                else:
                    print("\nInsira o grafo que pode ser subgrafo:")
                    print_submenu_entrada()
                    sub_choice = input("\nEscolha uma opção: ").strip()
                    
                    if sub_choice == '0':
                        continue
                    elif sub_choice == '1':
                        subgraph = read_graph_from_terminal(False)
                    elif sub_choice == '2':
                        show_input_file_tutorial()
                        filename = input("\nDigite o nome do arquivo: ").strip()
                        subgraph = read_graph_from_file(filename, False)
                    else:
                        print("\nOpção inválida!")
                        continue

                    is_sub = is_subgraph(g1=graph, g2=subgraph)
                    if is_sub:
                        print("\nÉ um subgrafo!")
                    else:
                        print("\nNão é um subgrafo.")

            else:
                print("\nOpção inválida!")
                
            input("\nPressione Enter para continuar...")
            
        except Exception as e:
            print(f"\nErro: {e}")
            input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main()