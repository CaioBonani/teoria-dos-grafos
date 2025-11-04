import matplotlib.pyplot as plt
import networkx as nx
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def gerar_cubo(z_inferior=0, altura=2):
    v = [
        [-1, -1, z_inferior],
        [ 1, -1, z_inferior],
        [ 1,  1, z_inferior],
        [-1,  1, z_inferior],
        [-1, -1, z_inferior + altura],
        [ 1, -1, z_inferior + altura],
        [ 1,  1, z_inferior + altura],
        [-1,  1, z_inferior + altura]
    ]
    return v


def faces_do_cubo(v):
    return [
        [v[0], v[1], v[2], v[3]],
        [v[4], v[5], v[6], v[7]],
        [v[0], v[1], v[5], v[4]],
        [v[2], v[3], v[7], v[6]],
        [v[1], v[2], v[6], v[5]],
        [v[4], v[7], v[3], v[0]]
    ]

                
def set_cores(cubes, sub, sol, s):
    left_colors = []
    right_colors = []
    labels = []
    edge_labels = nx.get_edge_attributes(sub[sol[s]], 'label')
    keys = edge_labels.keys()

    for vertice in sub[sol[s]].nodes:
        choice = 2

        if sub[sol[s]].degree(vertice) == 2:
            vizinhos = list(sub[sol[s]].neighbors(vertice))
            if vertice not in left_colors:
                left_colors.append(vertice)
                if vizinhos[0] not in right_colors:
                    right_colors.append(vizinhos[0])
                    if (vertice,vizinhos[0]) in keys:
                        labels.append(edge_labels[(vertice,vizinhos[0])])
                    elif (vizinhos[0],vertice) in keys:
                        labels.append(edge_labels[(vizinhos[0],vertice)])
                    choice = 0
                elif vizinhos[1] not in right_colors:
                    right_colors.append(vizinhos[1])
                    if (vertice,vizinhos[1]) in keys:
                        labels.append(edge_labels[(vertice,vizinhos[1])])
                    elif (vizinhos[1],vertice) in keys:
                        labels.append(edge_labels[(vizinhos[1],vertice)])
                    choice = 1

            if vertice not in right_colors:
                right_colors.append(vertice)
                if vizinhos[0] not in left_colors and (choice == 1 or choice == 2):
                    left_colors.append(vizinhos[0])
                    if (vertice,vizinhos[0]) in keys:
                        labels.append(edge_labels[(vertice,vizinhos[0])])
                    elif (vizinhos[0],vertice) in keys:
                        labels.append(edge_labels[(vizinhos[0],vertice)])
                elif vizinhos[1] not in right_colors and (choice == 0 or choice == 2):
                    left_colors.append(vizinhos[1])
                    if (vertice,vizinhos[1]) in keys:
                        labels.append(edge_labels[(vertice,vizinhos[1])])
                    elif (vizinhos[1],vertice) in keys:
                        labels.append(edge_labels[(vizinhos[1],vertice)])

    for vertice in sub[sol[s]].nodes:
        if sub[sol[s]].degree(vertice) == 1:
            vizinhos = list(sub[sol[s]].neighbors(vertice))
            if vertice not in left_colors and vertice not in right_colors:
                if vertice not in left_colors:
                    left_colors.append(vertice)
                    right_colors.append(vizinhos[0])
                    if (vertice,vizinhos[0]) in keys:
                        labels.append(edge_labels[(vertice,vizinhos[0])])
                    elif (vizinhos[0],vertice) in keys:
                        labels.append(edge_labels[(vizinhos[0],vertice)])

    for i in range(4):
        cubes[int(labels[i])-1].append(left_colors[i])
        cubes[int(labels[i])-1].append(right_colors[i])   


def get_cores_cubo(sub, sol):
    cubes = []
    for i in range(4):
        pre_cube = ['black', 'black']
        cubes.append(pre_cube)

    set_cores(cubes, sub, sol, 0)
    set_cores(cubes, sub, sol, 1)

    return cubes



def draw_cubes(cores_cubos, num):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    altura_cubo = 2
    for i in range(4):
        z_base = i * altura_cubo
        v = gerar_cubo(z_base, altura_cubo)
        faces = faces_do_cubo(v)
        cores = cores_cubos[i % len(cores_cubos)]

        for face, cor in zip(faces, cores):
            poly3d = [face]
            ax.add_collection3d(Poly3DCollection(poly3d, facecolors=cor, edgecolors='black', alpha=0.9))

    ax.set_box_aspect([1, 1, 2.5])  
    ax.set_xlim([-1.5, 1.5])
    ax.set_ylim([-1.5, 1.5])
    ax.set_zlim([0, altura_cubo * 4])
    ax.set_axis_off()

    plt.title("Solução " + num)
    
    plt.show()


def draw_cube_solution(sub: list[object], solution: list[object]):
    cores_cubos = [
        ['red', 'green', 'blue', 'yellow', 'orange', 'purple'],
        ['cyan', 'magenta', 'lime', 'gold', 'pink', 'gray'],
        ['brown', 'olive', 'navy', 'coral', 'teal', 'black'],
        ['darkred', 'darkgreen', 'darkblue', 'darkorange', 'purple', 'gray']
    ]

    for i in range(len(solution)):    
        cores_cubos = get_cores_cubo(sub, solution[i])
        title = str(i+1)
        draw_cubes(cores_cubos, title)