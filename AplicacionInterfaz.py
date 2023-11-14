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

inicio = None
imagen_grafico = None
nro_resultados_casas = 0


def dijkstra(grafo, inicio,comuna,realtor, precio_min, precio_max, dorms_min, baths_min, parking_min):
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
                    
                    dormitorios=int(grafo.nodos[casa]['dorms']) 
                    if dorms_min<= dormitorios:                                  #dormitorios
                        
                        banos=int(grafo.nodos[casa]['baths']) 
                        if baths_min<= banos:                                      #baños
                            
                            parking=int(grafo.nodos[casa]['parking']) 
                            if parking_min<=parking:                              #parking
                                
                                casas_filtradas.append((casa, distancia))
                              
    return casas_filtradas[:20] #retorna los 20 elementos

def obtener_recomendaciones():
    
    global nro_resultados_casas

    #comuna es para calcular el nodo inicio
    # Filtrar las casas según las preferencias de realtor, rango de precios, habitaciones, baños y parking
    comuna_deseada = "LoBarnechea"
    realtor_deseado = "OSSANDON CORREDORES ASOCIADOS S.A."
    precio_minimo_deseado = 1000
    precio_maximo_deseado = 10000
    habitaciones_min_deseadas=1
    banos_min_deseados=1
    parking_min_deseado=1
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
        casas_cercanas = dijkstra(grafo, inicio, comuna_deseada,realtor_deseado, precio_minimo_deseado,precio_maximo_deseado,habitaciones_min_deseadas,banos_min_deseados,parking_min_deseado)
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

# def get_recommendations():
#     comuna = comuna_entry.get()
#     realtor = realtor_entry.get()
#     price_min = int(price_min_entry.get())
#     price_max = int(price_max_entry.get())
#     bedrooms = int(bedrooms_entry.get())
#     bathrooms = int(bathrooms_entry.get())
#     parking = int(parking_entry.get())
    
#     inicio = None
#     for nodo in grafo.nodos:
#         if grafo.nodos[nodo]['comuna'] == comuna:
#             inicio = nodo
#             break

#     recommendations = dijkstra(grafo, inicio, comuna, realtor, price_min, price_max, bedrooms, bathrooms, parking)
    
#     for item in results_treeview.get_children():
#         results_treeview.delete(item)
    
#     for i, (casa, distancia) in enumerate(recommendations):
#         casa_data = [
#             i + 1, 
#             grafo.nodos[casa]['comuna'],
#             grafo.nodos[casa]['realtor'],
#             grafo.nodos[casa]['price_usd'],
#             grafo.nodos[casa]['dorms'],
#             grafo.nodos[casa]['baths'],
#             grafo.nodos[casa]['parking'],
#             distancia
#         ]
#         results_treeview.insert('', 'end', values=casa_data)


# root = tk.Tk()
# root.title("Departamento Ideal")


# input_frame = ttk.LabelFrame(root, text="Preferencias")
# input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")


# comuna_label = ttk.Label(input_frame, text="Comuna:")
# comuna_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
# comuna_entry = ttk.Entry(input_frame)
# comuna_entry.grid(row=0, column=1, padx=5, pady=5)

# realtor_label = ttk.Label(input_frame, text="Realtor:")
# realtor_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
# realtor_entry = ttk.Entry(input_frame)
# realtor_entry.grid(row=1, column=1, padx=5, pady=5)

# price_range_label = ttk.Label(input_frame, text="Price Range (USD):")
# price_range_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
# price_min_entry = ttk.Entry(input_frame)
# price_min_entry.grid(row=2, column=1, padx=5, pady=5)
# price_max_entry = ttk.Entry(input_frame)
# price_max_entry.grid(row=2, column=2, padx=5, pady=5)

# bedrooms_label = ttk.Label(input_frame, text="Bedrooms:")
# bedrooms_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
# bedrooms_entry = ttk.Entry(input_frame)
# bedrooms_entry.grid(row=3, column=1, padx=5, pady=5)

# bathrooms_label = ttk.Label(input_frame, text="Bathrooms:")
# bathrooms_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
# bathrooms_entry = ttk.Entry(input_frame)
# bathrooms_entry.grid(row=4, column=1, padx=5, pady=5)

# parking_label = ttk.Label(input_frame, text="Parking Spaces:")
# parking_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")
# parking_entry = ttk.Entry(input_frame)
# parking_entry.grid(row=5, column=1, padx=5, pady=5)


# recommend_button = ttk.Button(input_frame, text="Obtener recomendaciones", command=get_recommendations)
# recommend_button.grid(row=6, columnspan=3, pady=10)

# results_frame = ttk.LabelFrame(root, text="Recomendacion")
# results_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")


# results_treeview = ttk.Treeview(results_frame, columns=("Index", "Comuna", "Realtor", "Price (USD)", "Bedrooms", "Bathrooms", "Parking", "Distance"))
# results_treeview.heading("#1", text="Index")
# results_treeview.heading("#2", text="Comuna")
# results_treeview.heading("#3", text="Realtor")
# results_treeview.heading("#4", text="Price (USD)")
# results_treeview.heading("#5", text="Bedrooms")
# results_treeview.heading("#6", text="Bathrooms")
# results_treeview.heading("#7", text="Parking")
# results_treeview.heading("#8", text="Distance")
# results_treeview.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")


# scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=results_treeview.yview)
# scrollbar.grid(row=0, column=1, sticky="ns")
# results_treeview.configure(yscrollcommand=scrollbar.set)

# root.columnconfigure(0, weight=1)
# root.rowconfigure(0, weight=1)
# results_frame.columnconfigure(0, weight=1)
# results_frame.rowconfigure(0, weight=1)

# root.mainloop()
