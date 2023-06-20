import sys
import pygame
import networkx as nx
import json
import matplotlib.pyplot as plt
import heapq
import random
import math
import time
import numpy as np
from math import exp
from pygame.locals import *

from agenteAestrella import algoritmo_A_estrella, lista_calles, distancia_total 
from agenteManhatan import algoritmo_distancia_manhattan, lista_callesM, distancia_totalM
from agenteDfs import algoritmo_busqueda_dfs, lista_callesdfs, distancia_totaldfs
imagenes = {
    "hospital": pygame.image.load("./pngImagen/hospital.png"),
    "clinica": pygame.image.load("./pngImagen/clinica.png"),
    "iglesia": pygame.image.load("./pngImagen/iglesia.png"),
    "supermercado": pygame.image.load("./pngImagen/supermercado.png"),
    "restaurante": pygame.image.load("./point.png"),
    "cinema": pygame.image.load("./pngImagen/cine.png"),
    "puente": pygame.image.load("./point.png"),
    "stadium": pygame.image.load("./point.png"),
    "parque": pygame.image.load("./point.png"),
    "u.e": pygame.image.load("./pngImagen/colegio.png"),
    "universidad": pygame.image.load("./pngImagen/universidad.png"),
    "estacion": pygame.image.load("./pngImagen/estacion.png"),
    "default": pygame.image.load("./point.png")
}

def init():
    # Inicializar Pygame
    pygame.init()

    # Cargar la imagen de fondo
    background_image = pygame.image.load("mapa1.jpg")

    # Obtener las dimensiones de la imagen de fondo
    bg_width, bg_height = background_image.get_size()

    # Crear la ventana con las dimensiones de la imagen
    screen = pygame.display.set_mode((bg_width, bg_height), pygame.SRCALPHA)
    pygame.display.set_caption("Agregar Puntos")

    # Cargar la imagen del punto
    point_image = pygame.image.load("point.png")
    point_image = pygame.transform.scale(point_image, (30, 30))

    # Lista para almacenar los puntos
    points = []

    # Variable para verificar si se han marcado dos posiciones
    marked_two_positions = False

    # Nombre del archivo JSON con la copia del grafo
    archivo_json = 'copia_grafo.json'

    # Leer el archivo JSON y convertirlo en un diccionario
    with open(archivo_json, 'r') as f:
        grafo_dict = json.load(f)

    # Crear el grafo a partir del diccionario
    copia_grafo = nx.node_link_graph(grafo_dict)

    # Obtener las posiciones de los nodos
    posiciones = nx.get_node_attributes(copia_grafo, 'coordenadas')

    return screen, background_image, point_image, points, marked_two_positions, copia_grafo, posiciones


def main():
    # Inicializar el juego
    screen, background_image, point_image, points, marked_two_positions, copia_grafo, posiciones = init()

    # Lista para almacenar las líneas dibujadas
    lines = []

    # Bucle principal del juego
    while True:
        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_y:  # Si se presiona la tecla 'Y'
                    print("Buscar otros puntos")  # Acción: buscar otros puntos
                    lines = []
                    points = []
                elif event.key == K_n:  # Si se presiona la tecla 'N'
                    print("No buscar otros puntos")  # Acción: no buscar otros puntos
                    pygame.quit()
                    sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botón izquierdo del mouse
                    # Obtener las coordenadas del punto seleccionado
                    x, y = pygame.mouse.get_pos()
                    # Agregar el punto a la lista
                    points.append((x, y))

                    # Verificar si se han marcado dos posiciones
                    if len(points) == 2:
                        marked_two_positions = True
                        print("Se han marcado dos posiciones.")
                        print(points)

                        # Ejecutar el algoritmo A* y guardar la ruta más corta
                        nodos_iniciales = transformar_puntos_a_nodos([points[0]], copia_grafo)
                        nodos_finales = transformar_puntos_a_nodos([points[1]], copia_grafo)

                        # Verificar si se encontraron nodos cercanos válidos
                        if nodos_iniciales and nodos_finales:
                            nodo_inicial = nodos_iniciales[0]
                            nodo_objetivo = nodos_finales[0]

                            # Realizar la búsqueda utilizando el algoritmo A*
                            ruta_A_estrella = algoritmo_A_estrella(nodo_inicial, nodo_objetivo, copia_grafo)
                            #ruta_dfs        = algoritmo_busqueda_dfs(nodo_inicial, nodo_objetivo, copia_grafo)
                            ruta_manhattan  = algoritmo_distancia_manhattan(nodo_inicial, nodo_objetivo, copia_grafo)
                            print("Ruta más corta encontrada por A*:")
                            print(ruta_A_estrella)
                            lista_calles(copia_grafo, ruta_A_estrella)
                            distancia_total(ruta_A_estrella, posiciones)
                            print("Ruta más corta encontrada por dfs:")
                            #print(ruta_dfs)
                            #lista_callesdfs(copia_grafo, ruta_dfs)
                            #distancia_totaldfs(ruta_dfs, posiciones)
                            print("Ruta más corta encontrada por manhattan:")
                            print(ruta_manhattan)
                            lista_callesM(copia_grafo, ruta_manhattan)
                            distancia_totalM(ruta_manhattan, posiciones)
                            # Animación de los nodos de la ruta
                            mostrarRutas(ruta_A_estrella, posiciones, screen, background_image, point_image, points, lines)
                            mostrarRutas(ruta_manhattan, posiciones, screen, background_image, point_image, points,lines)
        # Dibujar la imagen de fondo
        screen.blit(background_image, (0, 0))
        # Dibujar los datos en la pantalla
        dibujar_datos(screen)
        # Dibujar los puntos en la pantalla
        for point in points:
            x, y = point
            # Dibujar la imagen del punto en las coordenadas especificadas
            screen.blit(point_image, (x - 15, y - 15))

        # Dibujar todas las líneas almacenadas
        for line in lines:
            pygame.draw.line(screen, (255, 0, 0), line[0], line[1], 3)

        # Actualizar la pantalla
        pygame.display.flip()
        
        #lines = []

def mostrarRutas(ruta, posiciones, screen, background_image, point_image, points, lines):
    for i in range(len(ruta)):
        # Dibujar la imagen de fondo
        screen.blit(background_image, (0, 0))

        # Dibujar los puntos en la pantalla
        for point in points:
            x, y = point
            # Dibujar la imagen del punto en las coordenadas especificadas
            screen.blit(point_image, (x - 15, y - 15))

        # Dibujar las líneas entre los nodos
        if i > 0:
            node1 = ruta[i - 1]
            node2 = ruta[i]
            x1, y1 = posiciones[node1]
            x2, y2 = posiciones[node2]
            lines.append(((x1, y1), (x2, y2)))  # Agregar la línea a la lista

        # Dibujar todas las líneas almacenadas
        for line in lines:
            pygame.draw.line(screen, (0, 0, 255), line[0], line[1], 3)

        # Dibujar el nodo actual de la ruta
        node = ruta[i]
        x, y = posiciones[node]
        screen.blit(point_image, (x - 15, y - 15))
        
        # Actualizar la pantalla
        pygame.display.flip()
        pygame.time.wait(500)  # Esperar un tiempo antes de mostrar el siguiente nodo


def encontrar_nodo_mas_cercano(coordenada, grafo):
    posiciones = nx.get_node_attributes(grafo, 'coordenadas')
    nodos = np.array(list(posiciones.keys()))
    coordenadas = np.array(list(posiciones.values()))

    # Calcular la distancia euclidiana entre la coordenada y los nodos existentes
    distancias = np.linalg.norm(coordenadas - coordenada, axis=1)

    # Encontrar el nodo más cercano
    nodo_cercano = nodos[np.argmin(distancias)]

    return nodo_cercano

def transformar_puntos_a_nodos(puntos, grafo):
    nodos = []
    for punto in puntos:
        nodo_cercano = encontrar_nodo_mas_cercano(punto, grafo)
        nodos.append(nodo_cercano)

    return nodos

def dibujar_datos(screen):
    datos = [
    (40, 707, "hospital buenaventura"),
    (378, 570, "hospital viedma"),
    (607, 757, "hospital san juan de dios"),
    (53, 61, "clinica coroico"),
    (728, 64, "clinica buenas nuevas"),
    (85, 277, "clinica san vicente"),
    (199, 489, "clinica santo domingo"),
    (734, 428, "clinica san felipe de austria"),
    (544, 364, "universidad publica de la nacion"),
    (79, 601, "U.E don bosco"),
    (770, 665, "U.E. 6 de agosto"),
    (197, 142, "U.E. bolivar"),
    (692, 103, "U.E. sucre"),
    (85, 256, "iglesia pare de sufrir"),
    (356, 103, "iglesia misioneros de cristo"),
    (540, 41, "iglesia mormones unidos"),
    (759, 466, "iglesia catolica san pedro"),
    (294, 590, "iglesia luz del camino"),
    (515, 651, "iglesia salvacion"),
    (159, 411, "cinema center"),
    (781, 161, "cinema premium"),
    (552, 36, "cinema skybox"),
    (207, 531, "estacion de trenes"),
    (238, 2, "supermercado doña magui"),
    (215, 137, "supermercado don luis"),
    (28, 252, "supermercado los angeles"),
    (98, 512, "supermercado hioermaxi"),
    (176, 725, "supermercado huajchito"),
    (387, 601, "supermercado tren del sur"),
    (583, 581, "supermercado lolita"),
    (782, 389, "supermercado el buen amigo"),
    (772, 175, "restaurante el buen gusto"),
    (485, 106, "restaurante punto de encuentro"),
    (697, 98, "restaurante llajtita"),
    (646, 248, "restaurante la buena pasta"),
    (154, 288, "puente cobija"),
    (322, 218, "puente heroes del chaco"),
    (409, 335, "puente ecologico"),
    (529, 456, "puente independencia"),
    (647, 333, "puente centenario"),
    (590, 117, "puente muyurina"),
    (48, 133, "stadium Lezo"),
    (372, 41, "parque cartagena de indias"),
    (610, 105, "parque de la alianza"),
    (686, 305, "parque vial"),
    (726, 688, "plaza de los recuerdos"),
    (460, 487, "plazuela aranibar"),
    (404, 744, "plazuela siglo xx"),
    (182, 466, "plazuela del arquitecto"),
    (513, 366, "plazuela colón"),
    (393, 298, "plazuela verde"),
    (470, 615, "plaza de los animales"),
    (143, 626, "parque ferroviario")
]
    for x, y, nombre in datos:
        # Obtener la primera cadena del nombre
        categoria = nombre.split()[0].lower()
        for categoriaImg, imagen in imagenes.items():
            imagenes[categoriaImg] = pygame.transform.scale(imagen, (20, 20))

        # Obtener la imagen correspondiente a la categoría o la imagen por defecto si no se encuentra
        point_image = imagenes.get(categoria, pygame.transform.scale(pygame.image.load("./point.png"), (30, 30)))        # Dibujar la imagen del punto en las coordenadas especificadas
        screen.blit(point_image, (x - 15, y - 15))
        # Dibujar el nombre del dato cerca del punto
        font = pygame.font.SysFont(None, 16)
        text = font.render(nombre, True, (0, 0, 0))
        screen.blit(text, (x + 10, y))



# Iniciar el juego
main()
