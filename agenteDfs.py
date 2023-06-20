import networkx as nx
from math import exp
import math

def algoritmo_busqueda_dfs(nodo_inicial, nodo_objetivo, copia_grafo):
    visitados = set()
    pila = [(nodo_inicial, [])]

    while pila:
        nodo_actual, camino_actual = pila.pop()

        if nodo_actual == nodo_objetivo:
            camino_actual.append(nodo_actual)
            return camino_actual

        if nodo_actual not in visitados:
            visitados.add(nodo_actual)

            vecinos = copia_grafo.neighbors(nodo_actual)

            for vecino in vecinos:
                nuevo_camino = camino_actual + [nodo_actual]
                pila.append((vecino, nuevo_camino))

    return None

def lista_callesdfs(copia_grafo, ruta_dfs):
    print("Calles de la ruta:")
    for i in range(len(ruta_dfs)):
        nodo_actual = ruta_dfs[i]
        if 'calles' in copia_grafo.nodes[nodo_actual]:
            calles = copia_grafo.nodes[nodo_actual]['calles']
            print(f"En el nodo {nodo_actual}: {', '.join(calles)}")
            if i < len(ruta_dfs) - 1:
                siguiente_nodo = ruta_dfs[i + 1]
                if copia_grafo.has_edge(nodo_actual, siguiente_nodo) and 'calles' in copia_grafo[nodo_actual][siguiente_nodo]:
                    calles_conexion = copia_grafo[nodo_actual][siguiente_nodo]['calles']
                    if calles_conexion:
                        calle_actual = calles[0]
                        calle_siguiente = calles_conexion[0]
                        if calle_actual == calle_siguiente:
                            print(f"Sigue por la calle {calle_actual}")
                        else:
                            print(f"Estás en la calle {calle_actual}")
                            print(f"Sigue por la calle {calle_siguiente}")
                    else:
                        print(f"Sigue por la calle {calle_actual}")
        else:
            print(f"No se encontraron calles para el nodo {nodo_actual}")

def distancia_totaldfs(ruta_dfs, posiciones):
    distancia_total = 0.0
    for i in range(1, len(ruta_dfs)):
        node1 = ruta_dfs[i - 1]
        node2 = ruta_dfs[i]
        x1, y1 = posiciones[node1]
        x2, y2 = posiciones[node2]
        distancia = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        distancia_total += distancia
    print("Distancia total de la ruta más corta:", distancia_total)