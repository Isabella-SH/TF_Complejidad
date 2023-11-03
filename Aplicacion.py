import pandas as pd
import heapq
import tkinter as tk
from tkinter import Toplevel, Label, Button
from tkinter import font
import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from Grafo import Grafo
import os
import csv

#casas_cercanas = []
inicio = None
imagen_grafico = None
nro_resultados_casas = 0


def dijkstra(grafo, inicio,comuna,realtor, precio_min, precio_max, dorms, baths, parking):
    distancias = {nodo: float('inf') for nodo in grafo.obtener_nodos()}
    distancias[inicio] = 0
    cola_prioridad = [(0, inicio)]
    visitados = set()

    while cola_prioridad:
        _, nodo_actual = heapq.heappop(cola_prioridad)
        if nodo_actual in visitados:
            continue
        visitados.add(nodo_actual)

        for nodo_vecino in grafo.aristas[nodo_actual]:
            peso = grafo.aristas[nodo_actual][nodo_vecino]
            distancia_nueva = distancias[nodo_actual] + peso
            if distancia_nueva < distancias[nodo_vecino]:
                distancias[nodo_vecino] = distancia_nueva
                heapq.heappush(cola_prioridad, (distancia_nueva, nodo_vecino))

    #comuna es para calcular el nodo inicio
    # Filtrar las casas según las preferencias de realtor, rango de precios, habitaciones, baños y parking
    casas_filtradas = []
        
    for casa, distancia in distancias.items():
        if comuna == "Todos" or grafo.nodos[casa]['comuna'] == comuna:
            if realtor == "Todos" or grafo.nodos[casa]['realtor'] == realtor: #luego el realtor
                precio = int(grafo.nodos[casa]['price_usd']) 
                if precio_min <= precio <= precio_max:                         #rango de precios                    
                    if int(grafo.nodos[casa]['dorms']) == dorms:                #dormitorios
                        if int(grafo.nodos[casa]['baths']) == baths:             #baños
                            if int(grafo.nodos[casa]['parking']) == parking:      #parking
                                casas_filtradas.append((casa, distancia))
                              
    return casas_filtradas[:20] #retorna los 20 elementos

def obtener_recomendaciones():
    
    global nro_resultados_casas

    #comuna es para calcular el nodo inicio
    # Filtrar las casas según las preferencias de realtor, rango de precios, habitaciones, baños y parking
    id_inicio=8493024
    comuna_deseada = "QuintaNormal"
    realtor_deseado = "Paula Vivanco Arenas"
    precio_minimo_deseado = 100000
    precio_maximo_deseado = 600000
    habitaciones_deseadas=4
    banos_deseados=1
    parking_deseado=2
    nro_resultados_casas = 5
    
    global casas_cercanas
    global inicio
    
    # Buscar el nodo de inicio en base a la comuna
    inicio = None
    for nodo in grafo.nodos:
       if grafo.nodos[nodo]['comuna'] == comuna_deseada:
            inicio = nodo
            break

    # Verificar si se encontró el nodo de inicio
    if inicio is None:
        print("la casa inicio no se encontro en el grafo")
    else:
        # Utilizar el algoritmo de Dijkstra para encontrar las distancias y filtrar por comuna
        casas_cercanas = dijkstra(grafo, inicio, comuna_deseada,realtor_deseado, precio_minimo_deseado,precio_maximo_deseado,habitaciones_deseadas,banos_deseados,parking_deseado)
        #print("Imprimir el arreglo")
        #print(casas_cercanas)
        #print("Antes de mostrar los resultados")
        mostrar_resultados(casas_cercanas, comuna_deseada, nro_resultados_casas)



# Función para mostrar los casas recomendados como "cards"
def mostrar_resultados(casas_cercanas, comuna_inicio, nro_resultados_casas):

    print(f"Las {nro_resultados_casas} casas mas recomendadas en relacion a la comuna {comuna_inicio}:\n")
    
    print(casas_cercanas)
    print("\n")

    for i, (casa, distancia) in enumerate(casas_cercanas[:nro_resultados_casas]):

    #comuna es para calcular el nodo inicio
    # Filtrar las casas según las preferencias de realtor, rango de precios, habitaciones, baños y parking
        print(f"Indice: {grafo.nodos[casa]['id']}")
        print(f"Comuna: {grafo.nodos[casa]['comuna']}")
        print(f"Realtor: {grafo.nodos[casa]['realtor']}")
        print(f"Precio en dolares: {grafo.nodos[casa]['price_usd']}")
        print(f"Habitaciones: {grafo.nodos[casa]['dorms']}")
        print(f"Banos: {grafo.nodos[casa]['baths']}")
        print(f"Parking: {grafo.nodos[casa]['parking']}")
        print(f"Distancia: {distancia}")
        print("\n")


# Ejemplo de uso
grafo = Grafo()

# Abre el archivo CSV
with open ('Database/database.csv', 'r', encoding='utf-8') as archivo_csv:
    # Lee el contenido del archivo CSV
    lector_csv = csv.DictReader(archivo_csv)
    
    for fila in lector_csv:
        try:

            price_clp = fila['Price_CLP']
            if price_clp:
                price_clp = int(price_clp)
            else:
                price_clp = 0  # Valor predeterminado si el campo está vacío


            price_uf = fila['Price_UF']
            if price_uf:
                price_uf = int(price_uf)
            else:
                price_uf = 0  # Valor predeterminado si el campo está vacío


            price_usd = fila['Price_USD']
            if price_usd:
                price_usd = int(price_usd)
            else:
                price_usd = 0  # Valor predeterminado si el campo está vacío


            comuna = fila['Comuna']

            ubicacion = fila['Ubicacion']

            dorms = fila['Dorms']
            if dorms:
                dorms = int(float(dorms))
            else:
                dorms = 0  # Valor predeterminado si el campo está vacío


            baths = fila['Baths']
            if baths:
                baths = int(float(baths))
            else:
                baths = 0  # Valor predeterminado si el campo está vacío


            built_area = fila['Built Area']
            if built_area:
                built_area = int(float(built_area))
            else:
                built_area = 0  # Valor predeterminado si el campo está vacío


            total_area = fila['Total Area']
            if total_area:
                total_area = int(float(total_area))
            else:
                total_area = 0  # Valor predeterminado si el campo está vacío

            parking = fila['Parking']
            if parking:
                parking = float(parking)
            else:
                parking = 0.0  # Valor predeterminado si el campo está vacío


            id = int(fila['id'])
            if id:
                id = int(id)
            else:
                id = 0  # Valor predeterminado si el campo está vacío

            realtor = fila['Realtor']

        except ValueError as e:
            print(f"Error al procesar la fila: {e}")
            continue

        grafo.agregar_nodo(price_clp=price_clp,price_uf=price_uf,price_usd=price_usd,comuna=comuna,ubicacion=ubicacion,dorms=dorms,baths=baths,built_area=built_area,total_area=total_area,parking=parking,id=id,realtor=realtor)

        for nodo in grafo.obtener_nodos():
          peso = 11
          if nodo != id:
            if grafo.nodos[nodo]['comuna'] == comuna:
              peso-=4
            if grafo.nodos[nodo]['dorms'] == dorms:
              peso-=3
            if grafo.nodos[nodo]['baths'] == baths:
              peso-=2
            if grafo.nodos[nodo]['parking'] == parking:
              peso-=1
          if peso < 11 and peso > 0:
            grafo.agregar_arista(id, nodo, peso)

#el grafo esta lleno
#print(grafo)

#print("Resultados de las recomendaciones\n\n")
obtener_recomendaciones()






















