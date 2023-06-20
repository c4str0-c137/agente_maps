import heapq
import networkx as nx
from math import exp
import math

def algoritmo_A_estrella(nodo_inicial, nodo_objetivo, copia_grafo):
    cola_prioridad = [(0, nodo_inicial, [])]
    visitados = set()

    while cola_prioridad:
        costo_actual, nodo_actual, camino_actual = heapq.heappop(cola_prioridad)

        if nodo_actual == nodo_objetivo:
            camino_actual.append(nodo_actual)
            return camino_actual

        if nodo_actual not in visitados:
            visitados.add(nodo_actual)

            vecinos = copia_grafo.neighbors(nodo_actual)

            for vecino in vecinos:
                nuevo_camino = camino_actual + [nodo_actual]
                nuevo_costo = costo_actual + copia_grafo[nodo_actual][vecino]['distancia']
                costo_total = nuevo_costo + costo_heuristico(vecino, nodo_objetivo, copia_grafo)
                heapq.heappush(cola_prioridad, (costo_total, vecino, nuevo_camino))

    return None

def costo_heuristico(u, v, copia_grafo):
    return nx.shortest_path_length(copia_grafo, u, v)

def costo_camino(camino, copia_grafo):
    return nx.path_length(copia_grafo, camino)

def lista_calles(copia_grafo, ruta_dfs):
    print("Calles de la ruta:")
    i = 0
    while i < len(ruta_dfs) - 1:
        nodo_actual = ruta_dfs[i]
        nodo_siguiente = ruta_dfs[i + 1]
        if 'calles' in copia_grafo.nodes[nodo_actual] and 'calles' in copia_grafo.nodes[nodo_siguiente]:
            calles_actual = copia_grafo.nodes[nodo_actual]['calles']
            calles_siguiente = copia_grafo.nodes[nodo_siguiente]['calles']
            #print(f"En el nodo {nodo_actual}: {', '.join(calles_actual)}")
            if calles_actual and calles_siguiente:
                for calle_actual in calles_actual:
                    if calle_actual in calles_siguiente:
                        print(f"Estás en la calle {calle_actual}")
                        break
                print(f"Sigue por la calle {calles_siguiente[0]}")
            elif calles_actual:
                print(f"Sigue por la calle {calles_actual[0]}")
            else:
                print("No se encontraron calles para el nodo actual")
        else:
            print("No se encontraron calles para el nodo actual o el siguiente")
        i += 1
    if i < len(ruta_dfs):
        nodo_ultimo = ruta_dfs[i]
        if 'calles' in copia_grafo.nodes[nodo_ultimo]:
            calles_ultimo = copia_grafo.nodes[nodo_ultimo]['calles']
            #print(f"En el nodo {nodo_ultimo}: {', '.join(calles_ultimo)}")
        else:
            print("No se encontraron calles para el último nodo")
            
def distancia_total(ruta_A_estrella, posiciones):
    distancia_total = 0.0
    for i in range(1, len(ruta_A_estrella)):
        node1 = ruta_A_estrella[i - 1]
        node2 = ruta_A_estrella[i]
        x1, y1 = posiciones[node1]
        x2, y2 = posiciones[node2]
        distancia = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        distancia_total += distancia
    print("Distancia total de la ruta más corta:", distancia_total)
