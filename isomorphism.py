"""
isomorphism.py
Módulo para verificação de isomorfismo de grafos.

Implementa uma estratégia hierárquica em 3 etapas:
1. Condições necessárias (O(n + m))
2. Invariantes estruturais (O(n²))
3. Busca estrutural (O(n!), apenas para grafos pequenos)

Série 4 - Teoria dos Grafos - UNIFESP
"""

from main import Graph, list_all_degrees, get_nodes_num, get_edge_num
from typing import Dict, Tuple, List, Optional
from collections import Counter
from itertools import permutations
import matplotlib.pyplot as plt
import networkx as nx
import os


# ==================== CONDIÇÕES NECESSÁRIAS ====================

def verificar_condicoes_necessarias(g1: Graph, g2: Graph) -> Tuple[bool, str]:
    """
    Verifica condições necessárias para isomorfismo.
    Se alguma falhar, os grafos NÃO são isomorfos.
    
    Args:
        g1: Primeiro grafo
        g2: Segundo grafo
    
    Returns:
        Tupla (é_possível, mensagem) indicando se as condições necessárias são satisfeitas
    
    Complexity: O(n + m)
    """
    # 1. Mesmo número de vértices
    n1 = get_nodes_num(g=g1)
    n2 = get_nodes_num(g=g2)
    if n1 != n2:
        return False, f"Número de vértices diferente: |V1|={n1}, |V2|={n2}"
    
    # 2. Mesmo número de arestas
    m1 = get_edge_num(g=g1)
    m2 = get_edge_num(g=g2)
    if m1 != m2:
        return False, f"Número de arestas diferente: |E1|={m1}, |E2|={m2}"
    
    # 3. Mesma sequência de graus
    graus1 = sorted(list_all_degrees(g=g1).values())
    graus2 = sorted(list_all_degrees(g=g2).values())
    if graus1 != graus2:
        return False, f"Sequência de graus diferente: {graus1} ≠ {graus2}"
    
    return True, "Condições necessárias satisfeitas"


# ==================== INVARIANTES ESTRUTURAIS ====================

def contar_triangulos(g: Graph) -> int:
    """
    Conta o número de triângulos (ciclos de tamanho 3) no grafo.
    
    Args:
        g: Grafo a analisar
    
    Returns:
        Número de triângulos encontrados
    
    Complexity: O(n³) - testa todas as triplas de vértices
    """
    triangulos = 0
    vertices = g.nodes
    
    for i, v1 in enumerate(vertices):
        for j, v2 in enumerate(vertices[i+1:], i+1):
            for k, v3 in enumerate(vertices[j+1:], j+1):
                # Verificar se formam um triângulo
                if ((v1, v2) in g.edges or (v2, v1) in g.edges) and \
                   ((v1, v3) in g.edges or (v3, v1) in g.edges) and \
                   ((v2, v3) in g.edges or (v3, v2) in g.edges):
                    triangulos += 1
    
    return triangulos


def calcular_invariantes(g: Graph) -> Dict:
    """
    Calcula invariantes estruturais do grafo para comparação rápida.
    Invariantes são propriedades que se preservam sob isomorfismo.
    
    Args:
        g: Grafo a analisar
    
    Returns:
        Dicionário com invariantes estruturais
    
    Complexity: O(n²) para grafos pequenos (devido à contagem de triângulos)
    """
    graus = list_all_degrees(g=g)
    
    invariantes = {
        'num_vertices': get_nodes_num(g=g),
        'num_arestas': get_edge_num(g=g),
        'sequencia_graus': tuple(sorted(graus.values())),
        'grau_max': max(graus.values()) if graus else 0,
        'grau_min': min(graus.values()) if graus else 0,
        'distribuicao_graus': dict(Counter(graus.values())),
        'soma_graus': sum(graus.values()),
    }
    
    # Calcular número de triângulos (apenas para grafos pequenos)
    if len(g.nodes) <= 20:
        invariantes['num_triangulos'] = contar_triangulos(g)
    
    return invariantes


def verificar_invariantes(g1: Graph, g2: Graph) -> Tuple[bool, str]:
    """
    Compara invariantes estruturais dos grafos.
    
    Args:
        g1: Primeiro grafo
        g2: Segundo grafo
    
    Returns:
        Tupla (são_iguais, mensagem) indicando se os invariantes são idênticos
    
    Complexity: O(n²)
    """
    inv1 = calcular_invariantes(g1)
    inv2 = calcular_invariantes(g2)
    
    for chave in inv1:
        if inv1[chave] != inv2[chave]:
            return False, f"Invariante '{chave}' diferente: {inv1[chave]} ≠ {inv2[chave]}"
    
    return True, "Invariantes estruturais idênticos"


# ==================== BUSCA ESTRUTURAL ====================

def construir_mapeamento_por_grau(g1: Graph, g2: Graph) -> Dict[int, Tuple[List, List]]:
    """
    Agrupa vértices por grau em ambos os grafos.
    Isomorfismo só pode mapear vértices de mesmo grau.
    
    Args:
        g1: Primeiro grafo
        g2: Segundo grafo
    
    Returns:
        Dicionário {grau: ([vértices_g1], [vértices_g2])}
    
    Complexity: O(n)
    """
    graus1 = list_all_degrees(g=g1)
    graus2 = list_all_degrees(g=g2)
    
    grupos = {}
    for v, grau in graus1.items():
        if grau not in grupos:
            grupos[grau] = ([], [])
        grupos[grau][0].append(v)
    
    for v, grau in graus2.items():
        if grau not in grupos:
            grupos[grau] = ([], [])
        grupos[grau][1].append(v)
    
    return grupos


def verificar_mapeamento(g1: Graph, g2: Graph, mapeamento: Dict) -> bool:
    """
    Verifica se um mapeamento específico preserva a estrutura (é isomorfismo).
    
    Para cada aresta (u, v) em G1, deve existir aresta (f(u), f(v)) em G2.
    
    Args:
        g1: Primeiro grafo
        g2: Segundo grafo
        mapeamento: Dicionário {vértice_g1: vértice_g2}
    
    Returns:
        True se o mapeamento preserva adjacências, False caso contrário
    
    Complexity: O(m) onde m é o número de arestas
    """
    # Verificar todas as arestas de G1
    for u, v in g1.edges:
        u_map = mapeamento[u]
        v_map = mapeamento[v]
        
        # Verificar se aresta mapeada existe em G2
        if (u_map, v_map) not in g2.edges and (v_map, u_map) not in g2.edges:
            return False
    
    # Verificar todas as arestas de G2 (garantir bijeção)
    for u, v in g2.edges:
        # Encontrar vértices originais em G1
        u_orig = [k for k, val in mapeamento.items() if val == u][0]
        v_orig = [k for k, val in mapeamento.items() if val == v][0]
        
        if (u_orig, v_orig) not in g1.edges and (v_orig, u_orig) not in g1.edges:
            return False
    
    return True


def buscar_isomorfismo_forca_bruta(g1: Graph, g2: Graph, limite_vertices: int = 8) -> Tuple[bool, Dict]:
    """
    Busca exaustiva por isomorfismo testando todas as permutações.
    ATENÇÃO: Complexidade O(n!), usar apenas para grafos pequenos.
    
    Args:
        g1: Primeiro grafo
        g2: Segundo grafo
        limite_vertices: Número máximo de vértices para tentar busca exaustiva
    
    Returns:
        Tupla (é_isomorfo, mapeamento) onde mapeamento é vazio se não for isomorfo
    
    Complexity: O(n!) no pior caso, otimizado com agrupamento por grau
    """
    n = get_nodes_num(g=g1)
    
    if n > limite_vertices:
        return None, {}
    
    # Agrupar por grau para reduzir espaço de busca
    grupos = construir_mapeamento_por_grau(g1, g2)
    
    # Verificar se agrupamento é compatível
    for grau, (v1_list, v2_list) in grupos.items():
        if len(v1_list) != len(v2_list):
            return False, {}
    
    # Gerar permutações apenas dentro de cada grupo de grau
    def gerar_mapeamentos():
        """Gerador de mapeamentos candidatos otimizado por grau"""
        # Fixar ordem dos vértices de G1
        v1_ordem = g1.nodes
        
        # Para cada grupo de grau, gerar permutações dos vértices de G2
        grupos_permutacoes = {}
        for grau, (v1_list, v2_list) in grupos.items():
            grupos_permutacoes[grau] = list(permutations(v2_list))
        
        # Combinar permutações de todos os grupos
        def combinar_grupos(grau_idx: int, mapa_parcial: Dict):
            if grau_idx >= len(grupos):
                yield mapa_parcial.copy()
                return
            
            grau = list(grupos.keys())[grau_idx]
            v1_list, v2_list = grupos[grau]
            
            for perm in grupos_permutacoes[grau]:
                novo_mapa = mapa_parcial.copy()
                for v1, v2 in zip(v1_list, perm):
                    novo_mapa[v1] = v2
                
                yield from combinar_grupos(grau_idx + 1, novo_mapa)
        
        yield from combinar_grupos(0, {})
    
    # Testar cada mapeamento
    for mapeamento in gerar_mapeamentos():
        if verificar_mapeamento(g1, g2, mapeamento):
            return True, mapeamento
    
    return False, {}


# ==================== FUNÇÃO PRINCIPAL ====================

def verificar_isomorfismo(g1: Graph, g2: Graph, nome_g1: str = "G1", nome_g2: str = "G2", 
                         verbose: bool = True) -> Tuple[bool, str, Dict]:
    """
    Estratégia completa para verificar se dois grafos são isomorfos.
    
    Etapas hierárquicas:
    1. Condições necessárias (O(n + m)) - filtros rápidos
    2. Invariantes estruturais (O(n²)) - verificações intermediárias
    3. Busca estrutural (O(n!)) - apenas para n ≤ 8
    
    Args:
        g1: Primeiro grafo
        g2: Segundo grafo
        nome_g1: Nome do primeiro grafo (para saída verbosa)
        nome_g2: Nome do segundo grafo (para saída verbosa)
        verbose: Se True, imprime informações detalhadas do processo
    
    Returns:
        Tupla (são_isomorfos, explicação, mapeamento)
        - são_isomorfos: True/False/None (None = indeterminado para grafos grandes)
        - explicação: String descrevendo o resultado
        - mapeamento: Dicionário com correspondência de vértices (se isomorfos)
    
    Complexity: O(n + m) a O(n!) dependendo do tamanho do grafo
    
    Examples:
        >>> g1 = Graph(['A', 'B', 'C'], [('A', 'B'), ('B', 'C'), ('A', 'C')])
        >>> g2 = Graph(['X', 'Y', 'Z'], [('X', 'Y'), ('Y', 'Z'), ('X', 'Z')])
        >>> iso, msg, mapa = verificar_isomorfismo(g1, g2, verbose=False)
        >>> iso
        True
    """
    
    if verbose:
        print("="*80)
        print(f"VERIFICAÇÃO DE ISOMORFISMO: {nome_g1} e {nome_g2}")
        print("="*80)
    
    # ETAPA 1: Condições necessárias
    if verbose:
        print("\n[Etapa 1] Verificando condições necessárias...")
    
    possivel, msg = verificar_condicoes_necessarias(g1, g2)
    if not possivel:
        if verbose:
            print(f"  [FALHA] {msg}")
            print(f"\n  CONCLUSÃO: {nome_g1} e {nome_g2} NÃO são isomorfos")
        return False, msg, {}
    
    if verbose:
        print(f"  [OK] {msg}")
    
    # ETAPA 2: Invariantes estruturais
    if verbose:
        print("\n[Etapa 2] Verificando invariantes estruturais...")
    
    possivel, msg = verificar_invariantes(g1, g2)
    if not possivel:
        if verbose:
            print(f"  [FALHA] {msg}")
            print(f"\n  CONCLUSÃO: {nome_g1} e {nome_g2} NÃO são isomorfos")
        return False, msg, {}
    
    if verbose:
        print(f"  [OK] {msg}")
    
    # ETAPA 3: Busca estrutural
    if verbose:
        print("\n[Etapa 3] Busca por mapeamento estrutural...")
    
    n = get_nodes_num(g=g1)
    
    if n <= 8:
        if verbose:
            print(f"  Executando busca exaustiva (n={n} <= 8)...")
        
        iso, mapeamento = buscar_isomorfismo_forca_bruta(g1, g2)
        
        if iso:
            if verbose:
                print(f"  [OK] Isomorfismo encontrado!")
                print(f"\n  CONCLUSÃO: {nome_g1} e {nome_g2} SÃO isomorfos")
                print(f"\n  Mapeamento: {mapeamento}")
            return True, "Isomorfismo confirmado", mapeamento
        else:
            if verbose:
                print(f"  [FALHA] Nenhum isomorfismo encontrado após busca exaustiva")
                print(f"\n  CONCLUSÃO: {nome_g1} e {nome_g2} NÃO são isomorfos")
            return False, "Nenhum mapeamento válido encontrado", {}
    else:
        msg = f"Grafos grandes (n={n}). Condições necessárias satisfeitas mas verificação completa requer algoritmo especializado."
        if verbose:
            print(f"  [AVISO] {msg}")
            print(f"\n  CONCLUSÃO: Indeterminado (usar bibliotecas especializadas como NetworkX)")
        return None, msg, {}


# ==================== CASOS DE TESTE ====================

def triangulo() -> Graph:
    """Cria um grafo triangular (K3)"""
    vertices = ['A', 'B', 'C']
    edges = [('A', 'B'), ('B', 'C'), ('A', 'C')]
    return Graph(vertices, edges)


def caminho(n: int = 3) -> Graph:
    """Cria um grafo caminho com n vértices"""
    vertices = [str(i) for i in range(1, n+1)]
    edges = [(str(i), str(i+1)) for i in range(1, n)]
    return Graph(vertices, edges)


def completo(n: int = 4, labels: Optional[List] = None) -> Graph:
    """Cria um grafo completo Kn"""
    if labels is None:
        labels = [chr(97 + i) for i in range(n)]  # a, b, c, d, ...
    edges = [(labels[i], labels[j]) for i in range(n) for j in range(i+1, n)]
    return Graph(labels, edges)


def ciclo(n: int = 4) -> Graph:
    """Cria um grafo ciclo Cn"""
    vertices = [str(i) for i in range(1, n+1)]
    edges = [(str(i), str(i+1)) for i in range(1, n)]
    edges.append((str(n), '1'))  # Fechar o ciclo
    return Graph(vertices, edges)


def bipartido_completo(m: int = 2, n: int = 2) -> Graph:
    """Cria um grafo bipartido completo Km,n"""
    set1 = [f'a{i}' for i in range(1, m+1)]
    set2 = [f'b{i}' for i in range(1, n+1)]
    vertices = set1 + set2
    edges = [(v1, v2) for v1 in set1 for v2 in set2]
    return Graph(vertices, edges)


def estrela(n: int = 4) -> Graph:
    """Cria um grafo estrela com n pontas"""
    vertices = ['centro'] + [str(i) for i in range(1, n+1)]
    edges = [('centro', str(i)) for i in range(1, n+1)]
    return Graph(vertices, edges)


# Aliases para compatibilidade
criar_grafo_k3 = triangulo
criar_grafo_caminho_3 = lambda: caminho(3)
criar_grafo_k4 = lambda: completo(4)
criar_grafo_k4_rotulado = lambda: completo(4, ['W', 'X', 'Y', 'Z'])
criar_grafo_quadrado = lambda: ciclo(4)
criar_grafo_k22 = lambda: bipartido_completo(2, 2)
criar_grafo_estrela_4 = lambda: estrela(4)


def criar_grafo_nao_isomorfo_k22() -> Graph:
    """K2,2 com uma aresta adicional (não isomorfo a C4)"""
    g = bipartido_completo(2, 2)
    # Adicionar aresta entre vértices do mesmo conjunto
    g.edges.append(('a1', 'a2'))
    return g


# ==================== VISUALIZAÇÃO ====================

def graph_to_networkx(g: Graph) -> nx.Graph:
    """Converte Graph customizado para NetworkX"""
    nx_graph = nx.Graph()
    nx_graph.add_nodes_from(g.nodes)
    nx_graph.add_edges_from(g.edges)
    return nx_graph


def visualizar_grafo(
    g: Graph,
    titulo: str = "Grafo",
    arquivo: Optional[str] = None,
    pos: Optional[dict] = None
) -> None:
    """
    Visualiza um grafo individualmente
    
    Args:
        g: Grafo a ser visualizado
        titulo: Título do grafo
        arquivo: Caminho para salvar a imagem (opcional)
        pos: Posicionamento customizado dos nós (opcional)
    """
    fig, ax = plt.subplots(figsize=(8, 8))
    
    nx_g = graph_to_networkx(g)
    
    # Layout automático se não especificado
    if pos is None:
        if len(g.nodes) <= 5:
            pos = nx.spring_layout(nx_g, k=2, iterations=100, seed=42)
        else:
            pos = nx.spring_layout(nx_g, k=1.5, iterations=100, seed=42)
    
    # Desenhar arestas com estilo melhorado
    nx.draw_networkx_edges(
        nx_g, pos, ax=ax,
        edge_color='#2C3E50',
        width=2.5,
        alpha=0.6
    )
    
    # Desenhar nós com estilo melhorado
    nx.draw_networkx_nodes(
        nx_g, pos, ax=ax,
        node_color='#3498DB',
        node_size=1200,
        alpha=0.9,
        edgecolors='#2C3E50',
        linewidths=2
    )
    
    # Desenhar labels com melhor contraste
    nx.draw_networkx_labels(
        nx_g, pos, ax=ax,
        font_size=12,
        font_weight='bold',
        font_color='white'
    )
    
    ax.set_title(titulo, fontsize=16, fontweight='bold', pad=20)
    ax.axis('off')
    ax.margins(0.15)
    
    plt.tight_layout()
    
    if arquivo:
        plt.savefig(arquivo, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"Imagem salva: {arquivo}")
    else:
        plt.show()
    
    plt.close()


def comparar_grafos(
    g1: Graph,
    g2: Graph,
    titulo1: str = "Grafo 1",
    titulo2: str = "Grafo 2",
    arquivo: Optional[str] = None,
    sao_isomorfos: bool = False
) -> None:
    """
    Visualiza dois grafos lado a lado para comparação
    
    Args:
        g1, g2: Grafos a serem comparados
        titulo1, titulo2: Títulos dos grafos
        arquivo: Caminho para salvar a imagem (opcional)
        sao_isomorfos: Se True, usa cor verde (isomorfos), senão vermelho
    """
    fig = plt.figure(figsize=(16, 7))
    
    nx_g1 = graph_to_networkx(g1)
    nx_g2 = graph_to_networkx(g2)
    
    # Layouts com seed para consistência
    pos1 = nx.spring_layout(nx_g1, k=2, iterations=100, seed=42)
    pos2 = nx.spring_layout(nx_g2, k=2, iterations=100, seed=42)
    
    # Cores baseadas no resultado
    if sao_isomorfos:
        cor_node = '#27AE60'  # Verde profissional
        cor_borda_node = '#1E8449'
        cor_edge = '#34495E'
        resultado_texto = "ISOMORFOS"
        cor_resultado = '#27AE60'
    else:
        cor_node = '#E74C3C'  # Vermelho profissional
        cor_borda_node = '#C0392B'
        cor_edge = '#34495E'
        resultado_texto = "NÃO ISOMORFOS"
        cor_resultado = '#E74C3C'
    
    # Grafo 1
    ax1 = fig.add_subplot(1, 2, 1)
    ax1.set_title(titulo1, fontsize=14, fontweight='bold', pad=15)
    
    nx.draw_networkx_edges(nx_g1, pos1, ax=ax1, edge_color=cor_edge, width=2.5, alpha=0.6)
    nx.draw_networkx_nodes(nx_g1, pos1, ax=ax1, node_color=cor_node, node_size=1200, 
                          alpha=0.9, edgecolors=cor_borda_node, linewidths=2.5)
    nx.draw_networkx_labels(nx_g1, pos1, ax=ax1, font_size=12, font_weight='bold', 
                           font_color='white')
    
    ax1.axis('off')
    ax1.margins(0.15)
    
    # Grafo 2
    ax2 = fig.add_subplot(1, 2, 2)
    ax2.set_title(titulo2, fontsize=14, fontweight='bold', pad=15)
    
    nx.draw_networkx_edges(nx_g2, pos2, ax=ax2, edge_color=cor_edge, width=2.5, alpha=0.6)
    nx.draw_networkx_nodes(nx_g2, pos2, ax=ax2, node_color=cor_node, node_size=1200,
                          alpha=0.9, edgecolors=cor_borda_node, linewidths=2.5)
    nx.draw_networkx_labels(nx_g2, pos2, ax=ax2, font_size=12, font_weight='bold',
                           font_color='white')
    
    ax2.axis('off')
    ax2.margins(0.15)
    
    # Título principal com resultado
    fig.suptitle(resultado_texto, fontsize=16, fontweight='bold', color=cor_resultado, y=0.98)
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    
    if arquivo:
        plt.savefig(arquivo, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"Comparação salva: {arquivo}")
    else:
        plt.show()
    
    plt.close()


def gerar_visualizacoes_teste(pasta_saida: str = "visualizacoes") -> None:
    """
    Gera imagens de todos os casos de teste
    
    Args:
        pasta_saida: Pasta onde salvar as imagens
    """
    # Criar pasta se não existir
    os.makedirs(pasta_saida, exist_ok=True)
    
    print(f"\n{'='*60}")
    print("GERANDO VISUALIZAÇÕES DOS CASOS DE TESTE")
    print(f"{'='*60}\n")
    
    casos = [
        (triangulo(), triangulo(), "Caso 1: K3 vs K3", True),
        (caminho(3), triangulo(), "Caso 2: P3 vs K3", False),
        (completo(4), completo(4, ['W', 'X', 'Y', 'Z']), "Caso 3: K4 vs K4", True),
        (ciclo(4), bipartido_completo(2, 2), "Caso 4: C4 vs K2,2", True),
        (estrela(4), ciclo(4), "Caso 5: S4 vs C4", False),
        (ciclo(4), criar_grafo_nao_isomorfo_k22(), "Caso 6: C4 vs K2,2+", False),
    ]
    
    for idx, (g1, g2, titulo, resultado) in enumerate(casos, 1):
        arquivo = os.path.join(pasta_saida, f"caso_{idx}.png")
        comparar_grafos(g1, g2, f"Grafo 1", f"Grafo 2", arquivo, resultado)
    
    print(f"\nTodas as {len(casos)} visualizações foram geradas em '{pasta_saida}/'")



# ==================== TESTE PRINCIPAL ====================


def executar_casos_teste(gerar_imagens: bool = False, pasta_imagens: str = "visualizacoes"):
    """
    Testa a estratégia em vários casos conhecidos.
    
    Args:
        gerar_imagens: Se True, gera visualizações dos grafos
        pasta_imagens: Pasta para salvar as imagens
    """
    print("\n" + "="*80)
    print("CASOS DE TESTE - ISOMORFISMO DE GRAFOS")
    print("="*80)
    
    casos = [
        # Caso 1: K3 vs K3 (isomorfos)
        {
            'g1': triangulo(),
            'g2': triangulo(),
            'nome_g1': 'K3 (triângulo)',
            'nome_g2': 'K3 (triângulo)',
            'esperado': True,
            'descricao': 'Dois triângulos completos'
        },
        
        # Caso 2: K3 vs P3 (não isomorfos - diferentes estruturas)
        {
            'g1': triangulo(),
            'g2': caminho(3),
            'nome_g1': 'K3',
            'nome_g2': 'P3 (caminho)',
            'esperado': False,
            'descricao': 'Triângulo vs caminho (mesmos n e m, mas graus diferentes)'
        },
        
        # Caso 3: K4 com rótulos diferentes (isomorfos)
        {
            'g1': completo(4),
            'g2': completo(4, ['W', 'X', 'Y', 'Z']),
            'nome_g1': 'K4 (a,b,c,d)',
            'nome_g2': 'K4 (W,X,Y,Z)',
            'esperado': True,
            'descricao': 'Mesma estrutura K4, rótulos diferentes'
        },
        
        # Caso 4: C4 vs K2,2 (isomorfos)
        {
            'g1': ciclo(4),
            'g2': bipartido_completo(2, 2),
            'nome_g1': 'C4 (quadrado)',
            'nome_g2': 'K2,2 (bipartido)',
            'esperado': True,
            'descricao': 'Ciclo 4 e K2,2 são isomorfos (estrutura idêntica)'
        },
        
        # Caso 5: C4 vs K2,2+aresta (não isomorfos)
        {
            'g1': ciclo(4),
            'g2': criar_grafo_nao_isomorfo_k22(),
            'nome_g1': 'C4',
            'nome_g2': 'K2,2 + aresta',
            'esperado': False,
            'descricao': 'Número de arestas diferente'
        },
        
        # Caso 6: Grafo vs ele mesmo (trivialmente isomorfo)
        {
            'g1': estrela(4),
            'g2': estrela(4),
            'nome_g1': 'Estrela S4',
            'nome_g2': 'Estrela S4',
            'esperado': True,
            'descricao': 'Mesmo grafo (identidade)'
        },
    ]
    
    resultados = []
    
    for i, caso in enumerate(casos, 1):
        print(f"\n{'='*80}")
        print(f"CASO {i}: {caso['descricao']}")
        print(f"{'='*80}")
        
        resultado, msg, mapeamento = verificar_isomorfismo(
            caso['g1'], caso['g2'], 
            caso['nome_g1'], caso['nome_g2'],
            verbose=True
        )
        
        # Verificar se resultado está correto
        correto = (resultado == caso['esperado']) or (resultado is None and caso['esperado'] is None)
        resultados.append({
            'caso': i,
            'descricao': caso['descricao'],
            'esperado': caso['esperado'],
            'obtido': resultado,
            'correto': correto
        })
        
        print(f"\n{'='*80}")
        if correto:
            print(f"[PASSOU] Teste {i}")
        else:
            print(f"[FALHOU] Teste {i} - esperado: {caso['esperado']}, obtido: {resultado}")
        print(f"{'='*80}")
    
    # Resumo final
    print("\n\n" + "="*80)
    print("RESUMO DOS TESTES")
    print("="*80)
    
    for r in resultados:
        status = "[OK]" if r['correto'] else "[FALHA]"
        print(f"{status} Caso {r['caso']}: {r['descricao']}")
        print(f"     Esperado: {r['esperado']}, Obtido: {r['obtido']}")
    
    aprovados = sum(1 for r in resultados if r['correto'])
    print(f"\nResultado: {aprovados}/{len(resultados)} testes aprovados")
    print("="*80)
    
    # Gerar visualizações se solicitado
    if gerar_imagens:
        print("\n")
        gerar_visualizacoes_teste(pasta_imagens)


# ==================== ANÁLISE DE LIMITAÇÕES ====================

def discutir_limitacoes():
    """
    Apresenta as limitações da estratégia implementada.
    """
    print("\n\n" + "="*80)
    print("LIMITAÇÕES E SITUAÇÕES ONDE A ESTRATÉGIA NÃO FUNCIONA")
    print("="*80)
    
    print("""
1. GRAFOS GRANDES (n > 8):
   - Busca exaustiva tem complexidade O(n!)
   - Exemplo: n=10 -> 10! = 3.628.800 permutações
   - Solução: usar algoritmos especializados (VF2, Weisfeiler-Lehman)

2. GRAFOS REGULARES:
   - Todos os vértices têm o mesmo grau
   - Exemplos: K_n (completo), ciclos, hipercubos
   - Problema: agrupamento por grau não reduz espaço de busca
   - Solução: usar invariantes mais sofisticados

3. GRAFOS COM MUITA SIMETRIA:
   - Exemplos: grafos bipartidos completos, Petersen
   - Múltiplos isomorfismos possíveis
   - Nossa estratégia retorna apenas um mapeamento

4. GRAFOS NÃO-CONEXOS:
   - Componentes desconexas podem ser permutadas
   - Solução: analisar cada componente separadamente

5. LIMITAÇÃO DE INVARIANTES:
   - Alguns grafos não-isomorfos têm mesmos invariantes
   - Exemplo: árvores diferentes com mesma sequência de graus
   - Solução: calcular mais invariantes (espectro, polinômio cromático)

6. GRAFOS DIRECIONADOS E PONDERADOS:
   - Implementação atual só trata grafos simples não-direcionados
   - Extensão requer adaptação dos invariantes

7. CASOS INDETERMINÁVEIS:
   - Para grafos grandes, retornamos "indeterminado"
   - Não é "falso negativo", apenas reconhece limitação
    """)
    
    print("="*80)
    print("RECOMENDAÇÕES:")
    print("="*80)
    print("""
- Para grafos pequenos (n <= 8): usar esta implementação
- Para grafos médios (8 < n <= 100): usar NetworkX (algoritmo VF2)
- Para grafos grandes (n > 100): considerar heurísticas probabilísticas
- Para grafos especiais: explorar propriedades específicas
    """)
    print("="*80)


# ==================== MAIN ====================

def main():
    """
    Executa a demonstração completa da estratégia de isomorfismo.
    """
    print("\n" + "="*80)
    print("MÓDULO DE ISOMORFISMO DE GRAFOS")
    print("="*80)
    
    print("""
ESTRATÉGIA IMPLEMENTADA:

A verificação de isomorfismo é feita em 3 etapas hierárquicas:

1. CONDIÇÕES NECESSÁRIAS (O(n + m)):
   - Mesmo número de vértices
   - Mesmo número de arestas  
   - Mesma sequência de graus
   >> Se falhar: grafos NÃO são isomorfos

2. INVARIANTES ESTRUTURAIS (O(n²)):
   - Distribuição de graus
   - Número de triângulos
   - Grau máximo/mínimo
   >> Se falhar: grafos NÃO são isomorfos

3. BUSCA ESTRUTURAL (O(n!), apenas n <= 8):
   - Agrupa vértices por grau
   - Testa permutações dentro de cada grupo
   - Verifica preservação de adjacências
   >> Se encontrar mapeamento: grafos SÃO isomorfos
   >> Se não encontrar: grafos NÃO são isomorfos
    """)
    
    # Perguntar se deseja gerar imagens
    print("\nOPÇÕES:")
    print("1. Executar testes + gerar visualizações")
    print("2. Apenas executar testes")
    
    opcao = input("\nEscolha (1/2) [padrão: 2]: ").strip()
    gerar_imgs = (opcao == "1")
    
    if gerar_imgs:
        print("\n> Visualizações serão geradas na pasta 'visualizacoes/'\n")
        input("Pressione ENTER para continuar...")
    
    executar_casos_teste(gerar_imagens=gerar_imgs)
    
    input("\nPressione ENTER para ver as limitações da estratégia...")
    
    discutir_limitacoes()
    
    print("\n" + "="*80)
    print("ANÁLISE CONCLUÍDA")
    print("="*80)


if __name__ == "__main__":
    main()
