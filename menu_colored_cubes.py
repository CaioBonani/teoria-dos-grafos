from colored_cubes import solve_cube_problem

def main():
    print('=== Problema dos 4 Cubos Coloridos ===')
    print('Você deverá informar as cores de cada face dos 4 cubos, separadas por vírgulas.')
    print('Para as 6 faces do cubo, as posições opostas devem ser digitadas lado a lado(1↔2, 3↔4, 5↔6)')
    print('As cores disponíveis são: R (vermelho), G (verde), B (azul) e W (branco).')
    print('Exemplo de entrada para um cubo: R,G,B,W,R,G')
    print()
    
    cube_list = []
    valid_colors = {'R', 'G', 'B', 'W'}
    for i in range(4):
        valid = False
        while not valid:
            color_list = input(f'Digite as cores do {i+1}° cubo: ').split(',')
            color_list = [c.strip().upper() for c in color_list]
            
            if len(color_list) != 6:
                print('Erro: o cubo deve ter exatamente 6 cores')
            elif not all(c in valid_colors for c in color_list):
                print('Erro: Há cores inválidas. Utilize apenas: R, G, B ou W')
            elif not valid_colors.issubset(set(color_list)):
                print('Erro: O cubo não contém todas as cores(R, G, B e W)')
            else:
                cube_list.append(color_list)
                valid = True
                
    v_order = ['R', 'G', 'B', 'W']
    solve_cube_problem(cube_list, v_order)

if __name__ == '__main__':
    main()