import graphviz
import pygraphviz as pgv
import re
# -*- coding: utf-8 -*-
def generar_pda():
    # Solicitar al usuario el número de estados
    num_estados = int(input("Ingrese el número de estados para el PDA: "))

    # Crear un objeto Digraph de Graphviz
    pda = graphviz.Digraph('PDA', format='png')

    # Diccionario para almacenar transiciones agrupadas por nodos de inicio y fin
    transiciones_dict = {}

    # Solicitar al usuario el estado inicial
    estado_inicial = input(f"Ingrese el estado inicial (uno de q0, q1, ..., q{num_estados - 1}): ")

    # Solicitar el alfabeto del PDA
    alfabeto_pda = input("Ingrese el alfabeto del PDA (separado por comas, ejemplo: a,b,c): ").split(',')

    # Solicitar el alfabeto de la pila
    alfabeto_pila = input("Ingrese el alfabeto de la pila (separado por comas, ejemplo: X,Y,Z): ").split(',')

    # Agregar nodos (estados)
    for i in range(num_estados):
        if i == int(estado_inicial[1:]):
            # Marcar el estado inicial cambiando la forma y el estilo
            pda.node(estado_inicial, shape='triangle', color='green', label=estado_inicial, style='filled')
        else:
            pda.node(f'q{i}', shape='circle', color='blue', label=f'q{i}', style='bold')

    while True:
        transicion_input = input("Ingrese la transición en el formato '(estado_actual, caracter_lee, pila_contenido)=(estado_destino, cola_contenido)' o escriba 'exit' para finalizar: ")

        if transicion_input.lower() == 'exit':
            break

        try:
            # Analizar la entrada de transición
            partes = transicion_input.split('=')
            inicio_partes = partes[0].strip('()').split(',')
            fin_partes = partes[1][:partes[1].rfind(')') + 1].strip('()').split(',')

            inicio = inicio_partes[0]
            fin = fin_partes[0]

            # Verificar el alfabeto del PDA
            if inicio_partes[1] != 'e' and inicio_partes[1] not in alfabeto_pda:
                raise ValueError(f"El caracter de lectura '{inicio_partes[1]}' no está en el alfabeto del PDA.")

            # Crear clave única para agrupar transiciones
            clave_transicion = f'{inicio}_{fin}'

            # Agregar transición al diccionario
            if clave_transicion not in transiciones_dict:
                transiciones_dict[clave_transicion] = {
                    'transiciones': [],
                }

            # Modificar el formato de la transición
            transicion = f'{inicio_partes[1]},{inicio_partes[2]};{",".join(fin_partes[1:])}'
            transiciones_dict[clave_transicion]['transiciones'].append(transicion)

        except (ValueError, IndexError) as e:
            print(f"Error: {e}. Por favor, inténtelo de nuevo.")
            continue

    # Agregar transiciones al grafo
    for clave, valores in transiciones_dict.items():
        inicio_fin_partes = clave.split('_')
        transiciones_str = '\n'.join(valores['transiciones'])

        # Modificar el formato de la etiqueta de la transición
        transicion_label = f'{transiciones_str}'
        pda.edge(inicio_fin_partes[0], inicio_fin_partes[1], label=transicion_label)

    # Solicitar los estados finales
    estados_finales = input("Ingrese los estados finales separados por comas (ejemplo: q1,q2): ").split(',')
    print('estados finales: ', estados_finales)

    # Agregar estados finales
    for estado_final in estados_finales:
        pda.node(estado_final, shape='doublecircle', color='red', label=estado_final, peripheries='2')

    # Unir todas las cadenas de pda.body para obtener el texto completo del grafo
    pda_body_str = '\n'.join(pda.body)
    # Utilizar una expresión regular para extraer los nombres de los nodos
    nombres_nodos = re.findall(r'(\w+)\s\[\w+', pda_body_str)
    # Eliminar duplicados convirtiendo la lista a un conjunto
    nombres_nodos_unicos = list(set(nombres_nodos))
    # Agregar texto adicional
    print(nombres_nodos_unicos)
    pda.attr(label=f'El estado en verde es el estado inicial\nLos estados en rojo son los estados finales\n'
                   f'PDA(final_state) = (Q, Σ, Γ, δ, q0, Z, F)\n'
                   f'Q = {{{", ".join(nombres_nodos_unicos)}}}\n'
                   f'Σ = {{{", ".join(alfabeto_pda)}}}\n'
                   f'Γ = {{{", ".join(alfabeto_pila)}}}\n'
                   f'q0 = {estado_inicial}\n'
                   f'Z = Z\n'
                   f'F = {{{", ".join(estados_finales)}}}')

    # Guardar la imagen en archivos PNG y DOT
    pda_file_name = 'pda_final_state'
    pda.render(pda_file_name, format='png', cleanup=True)
    pda.render(pda_file_name, format='dot', cleanup=False)

    print(f"Se ha generado un PDA con {num_estados} estados. La imagen se guarda en '{pda_file_name}.png' y el archivo DOT en '{pda_file_name}.dot'.")

    # Llamar a la función para generar el PDA con pila vacía
    generar_empty_stack(pda_file_name, estado_inicial, estados_finales,nombres_nodos_unicos,alfabeto_pda,alfabeto_pila)
    
def generar_empty_stack(pda_file_name, estado_inicial, estados_finales,nombres_nodos_unicos,alfabeto_pda,alfabeto_pila):
    print(estado_inicial)
    print(estados_finales)
    # Cargar el grafo desde el archivo DOT original
    dot_file_path = f"{pda_file_name}.dot"
    pda_graph = pgv.AGraph(dot_file_path)

    # Crear nuevos nodos 'p0' (triángulo verde) y 'p' (círculo azul) y transiciones a q0
    nuevo_nodo_p0 = 'p0'
    nuevo_nodo_p = 'p'
    nuevo_estado_destino = estado_inicial

    # Crear el objeto de diccionario para las propiedades de la transición
    propiedades_transicion_p0 = {
        'label': 'e,X;XZ'
    }
    
    propiedades_transicion_p = {
        'label': 'e,Z;e'
    }

    # Agregar el nuevo nodo y la transición al grafo
    pda_graph.add_node(nuevo_nodo_p0, color='green', style='filled', shape='triangle', label=nuevo_nodo_p0)
    pda_graph.add_edge('p0', nuevo_estado_destino, **propiedades_transicion_p0)
    pda_graph.add_node(nuevo_nodo_p, color='blue', style='bold', shape='circle', label=nuevo_nodo_p)
    
    for estado_final in estados_finales:
        pda_graph.add_edge(estado_final, nuevo_nodo_p, **propiedades_transicion_p)
    # Cambiar el estilo del nodo con el nombre del estado inicial a un círculo azul
    pda_graph.get_node(nuevo_estado_destino).attr.update(color='blue', shape='circle', style='bold',height='0.55906',width='0.55906')
    
    # Cambiar el estilo de los nodos finales a círculos con borde azul
    for estado_final in estados_finales:
        pda_graph.get_node(estado_final).attr.update(color='blue', shape='circle', style='bold',height='0.55906',width='0.55906',peripheries='1')
    
    # Modificar el texto adicional en el label del grafo
    pda_graph.graph_attr.update(label=f'El estado en verde es el estado inicial\n'
                                      f'PDA(empty_stack) = (Q, Σ, Γ, δ, p0, X)\n'
                                      f'Q = {{{", ".join(nombres_nodos_unicos)}}} U {{p0, p}}\n'
                                      f'Σ = {{{", ".join(alfabeto_pda)}}}\n'
                                      f'Γ = {{{", ".join(alfabeto_pila)}}} U {{X}}\n'
                                      f'p0 = p0\n'
                                      f'X = X\n')
    # Configurar el grafo para que Graphviz calcule automáticamente las posiciones
    pda_graph.graph_attr.update(constraint='false')

    # Guardar el grafo modificado en un nuevo archivo DOT
    nuevo_dot_file_path = f"{pda_file_name}_to_empty_stack.dot"
    pda_graph.write(nuevo_dot_file_path)

    # Renderizar el nuevo archivo DOT a un archivo PNG
    pda_graph.draw(f"{pda_file_name}_to_empty_stack.png", format='png', prog='dot')

    print(f"Se ha generado un nuevo archivo DOT: {nuevo_dot_file_path}")
if __name__ == "__main__":
    generar_pda()
