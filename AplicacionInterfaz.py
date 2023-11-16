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
import heapq
import random

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
    # Filtrar las casas seg�n las preferencias de realtor, rango de precios, habitaciones, ba�os y parking
    casas_filtradas = []
        
    for casa, distancia in distancias.items():
        
        if comuna == "Todos" or grafo.nodos[casa]['comuna'] == comuna:

            if not realtor or realtor == "Todos" or grafo.nodos[casa]['realtor'] == realtor:  # luego el realtor

                precio = int(grafo.nodos[casa]['price_usd']) if grafo.nodos[casa]['price_usd'] else 0
                if (precio_min == "" or precio_min <= precio) and (precio_max == "" or precio <= precio_max):  # rango de precios

                    dormitorios = int(grafo.nodos[casa]['dorms']) if grafo.nodos[casa]['dorms'] else 0
                    if (dorms_min == "" or dorms_min <= dormitorios):  # dormitorios

                        banos = int(grafo.nodos[casa]['baths']) if grafo.nodos[casa]['baths'] else 0
                        if (baths_min == "" or baths_min <= banos):  # ba�os

                            parking = int(grafo.nodos[casa]['parking']) if grafo.nodos[casa]['parking'] else 0
                            if (parking_min == "" or parking_min <= parking):  # parking

                                casas_filtradas.append((casa, distancia))
    
    #key=lambda x: x[1] especifica que la clave de ordenaci�n es el segundo elemento de cada tupla, que es la distancia.                                                                                                !!!!!!!!!!!!!!!!!!!!!!
    recomendations_sorted = sorted(casas_filtradas, key=lambda x: x[1])                                                                                                                                                   #!!!!!!!!!!!!!!!!!!!!!!

    return recomendations_sorted[:20] #retorna los 20 primeros elementos                                                                                                                                                !!!!!!!!!!!!!!!!!!!!!!


def obtener_recomendaciones():
    
    # -*- coding: utf-8 -*-
    #comuna es para calcular el nodo inicio
    #Filtrar las casas seg�n las preferencias de realtor, rango de precios, habitaciones min, ba�os min y parking min
    comuna_deseada = "LasCondes"                     #-> OBLIGATORIO!!!!
    realtor_deseado = ""           #->pasar como comillas sin espacio "" si es que no recibe nada
    precio_minimo_deseado = 1000                 #-> OBLIGATORIO!!!!   
    precio_maximo_deseado = 800000             #-> OBLIGATORIO!!!!
    habitaciones_min_deseadas=1                  #-> pasar como 0 si no recibe nada
    banos_min_deseados= 1                        #-> pasar como 0 si no recibe nada
    parking_min_deseado= 2                       #-> pasar como 0 si no recibe nada
    
    global casas_cercanas
    global inicio
    
    # Buscar el nodo de inicio en base a la comuna
    inicio = None
    for nodo in grafo.nodos:
       if grafo.nodos[nodo]['comuna'] == comuna_deseada:
            inicio = nodo
            break

    # Verificar si se encontr� el nodo de inicio
    if inicio is None:
        print("la casa inicio no se encontro en el grafo")
    else:
        # Utilizar el algoritmo de Dijkstra para encontrar las distancias y filtrar por comuna
        casas_cercanas = dijkstra(grafo, inicio, comuna_deseada,realtor_deseado, precio_minimo_deseado,precio_maximo_deseado,habitaciones_min_deseadas,banos_min_deseados,parking_min_deseado)
        #print("Imprimir el arreglo")
        #print(casas_cercanas)
        #print("Antes de mostrar los resultados")
        mostrar_resultados(casas_cercanas, comuna_deseada)



# Funci�n para mostrar los casas recomendados como "cards"
def mostrar_resultados(casas_cercanas, comuna_inicio):

    print(f"Las casas mas recomendadas en relacion a la comuna {comuna_inicio}:\n")
    
    print(casas_cercanas)
    print("\n")

    for i, (casa, distancia) in enumerate(casas_cercanas):

    #comuna es para calcular el nodo inicio
    # Filtrar las casas seg�n las preferencias de realtor, rango de precios, habitaciones, ba�os y parking
        print(f"Indice: {grafo.nodos[casa]['id']}")
        print(f"Comuna: {grafo.nodos[casa]['comuna']}")
        print(f"Realtor: {grafo.nodos[casa]['realtor']}")
        print(f"Precio en dolares: {grafo.nodos[casa]['price_usd']}")
        print(f"Habitaciones: {grafo.nodos[casa]['dorms']}")
        print(f"Banos: {grafo.nodos[casa]['baths']}")
        print(f"Parking: {grafo.nodos[casa]['parking']}")
        print(f"Descuento: {grafo.nodos[casa]['desc']}")
        print(f"Distancia: {distancia}")
        print("\n")
    
                                                                                                                                                                                                    #!!!!!!!!!!!!!!!!!!!!!!
    #filtrar por distancia                
    print("CASAS FILTRADAS")
    print("\n")
    casas_filtradas= filtrar_por_atributo(casas_cercanas,"total_area")
    
    for casa in casas_filtradas:

    #comuna es para calcular el nodo inicio
    # Filtrar las casas seg�n las preferencias de realtor, rango de precios, habitaciones, ba�os y parking
        print(f"Indice: {grafo.nodos[casa]['id']}")
        print(f"Comuna: {grafo.nodos[casa]['comuna']}")
        print(f"Realtor: {grafo.nodos[casa]['realtor']}")
        print(f"Precio en dolares: {grafo.nodos[casa]['price_usd']}")
        print(f"Habitaciones: {grafo.nodos[casa]['dorms']}")
        print(f"Banos: {grafo.nodos[casa]['baths']}")
        print(f"Parking: {grafo.nodos[casa]['parking']}")
        print(f"Total Area (m^2): {grafo.nodos[casa]['total_area']}")
        print(f"Descuento: {grafo.nodos[casa]['desc']}")
        print("\n")
    
    


                                                                                                                                                    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def filtrar_por_atributo(recommendations, filtro):
    
    # Filtrar seg�n el criterio especificado en el filtro
    if filtro == "dorms":
        # Ordenar casas por el atributo 'dorms'
        sorted_houses = sorted(recommendations, key=lambda x: grafo.nodos[x[0]]['dorms'])
        casas_ordenadas_por_dorms = [casa for casa, _ in sorted_houses]
        return casas_ordenadas_por_dorms

    elif filtro == "baths":
        # Ordenar casas por el atributo 'baths'
        sorted_baths = sorted(recommendations, key=lambda x: grafo.nodos[x[0]]['baths'])
        casas_ordenadas_por_baths = [casa for casa, _ in sorted_baths]
        return casas_ordenadas_por_baths

    elif filtro == "parking":
        # Ordenar casas por el atributo 'parking'
        sorted_park= sorted(recommendations, key=lambda x: grafo.nodos[x[0]]['parking'])
        casas_ordenadas_por_park = [casa for casa, _ in sorted_park]
        return casas_ordenadas_por_park
    
    elif filtro == "price_usd":
        # Ordenar casas por el atributo 'price_usd'
        sorted_price_usd= sorted(recommendations, key=lambda x: grafo.nodos[x[0]]['price_usd'])
        casas_ordenadas_por_price_usd = [casa for casa, _ in sorted_price_usd]
        return casas_ordenadas_por_price_usd

    elif filtro == "desc": #filtra casas que tengan como descuento true
        return [casa for casa, distancia in recommendations if grafo.nodos[casa]['desc']]
    
    elif filtro == "total_area":
        # Ordenar casas por el atributo 'price_usd'
        sorted_price_total_area= sorted(recommendations, key=lambda x: grafo.nodos[x[0]]['total_area'])
        casas_ordenadas_por_total_area= [casa for casa, _ in sorted_price_total_area]
        return casas_ordenadas_por_total_area

    elif filtro == "todo":
        return recommendations  # Si el filtro no es reconocido, devolvemos la lista completa
                                                                                                                                                    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


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
                price_clp = 0  # Valor predeterminado si el campo est� vac�o


            price_uf = fila['Price_UF']
            if price_uf:
                price_uf = int(price_uf)
            else:
                price_uf = 0  # Valor predeterminado si el campo est� vac�o


            price_usd = fila['Price_USD']
            if price_usd:
                price_usd = int(price_usd)
            else:
                price_usd = 0  # Valor predeterminado si el campo est� vac�o


            comuna = fila['Comuna']

            ubicacion = fila['Ubicacion']

            dorms = fila['Dorms']
            if dorms:
                dorms = int(float(dorms))
            else:
                dorms = 0  # Valor predeterminado si el campo est� vac�o


            baths = fila['Baths']
            if baths:
                baths = int(float(baths))
            else:
                baths = 0  # Valor predeterminado si el campo est� vac�o


            built_area = fila['Built Area']
            if built_area:
                built_area = int(float(built_area))
            else:
                built_area = 0  # Valor predeterminado si el campo est� vac�o


            total_area = fila['Total Area']
            if total_area:
                total_area = int(float(total_area))
            else:
                total_area = 0  # Valor predeterminado si el campo est� vac�o

            parking = fila['Parking']
            if parking:
                parking = int(float(parking))
            else:
                parking = 0  # Valor predeterminado si el campo est� vac�o


            id = int(fila['id'])
            if id:
                id = int(id)
            else:
                id = 0  # Valor predeterminado si el campo est� vac�o

            realtor = fila['Realtor']
        
        except ValueError as e:
            print(f"Error al procesar la fila: {e}")
            continue

        desc= random.choice([True, False])                                                                                                                                                              #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
        grafo.agregar_nodo(price_clp=price_clp,price_uf=price_uf,price_usd=price_usd,comuna=comuna,ubicacion=ubicacion,dorms=dorms,baths=baths,built_area=built_area,total_area=total_area,parking=parking,id=id,realtor=realtor, desc=desc)  #!!!!!!!!!!!!!!!!!!!

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


# def mostrar_fachada_aleatoria():
  
#     todas_las_casas = list(grafo.obtener_nodos())

#     casa_aleatoria = random.choice(todas_las_casas)
#     ruta_imagen = f"imagenes_fachadas/fachada_{casa_aleatoria}.jpg"

#     ventana_fachada = tk.Toplevel(root)
#     ventana_fachada.title("Fachada de Casa Aleatoria")
#     imagen = Image.open(ruta_imagen)
#     imagen_tk = ImageTk.PhotoImage(imagen)
#     label = tk.Label(ventana_fachada, image=imagen_tk)
#     label.pack()
#     boton_cerrar = tk.Button(ventana_fachada, text="Cerrar", command=lambda: cerrar_ventana(ventana_fachada))
#     boton_cerrar.pack()

# def cerrar_ventana(ventana):
#     ventana.destroy()
    
# def get_recommendations():
#     comuna = comuna_var.get()
#     realtor = realtor_var.get()
#     price_min = int(price_min_entry.get())
#     price_max = int(price_max_entry.get())
#     bedrooms = int(bedrooms_var.get())
#     bathrooms = int(bathrooms_var.get())
#     parking = int(parking_var.get())
    
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
# comuna_options = ["Vitacura", "Las Condes", "Providencia", "Santiago"]
# comuna_var = tk.StringVar(value=comuna_options[0])
# comuna_entry = ttk.Combobox(input_frame, textvariable=comuna_var, values=comuna_options)
# comuna_entry.grid(row=0, column=1, padx=5, pady=5)

# realtor_label = ttk.Label(input_frame, text="Realtor:")
# realtor_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
# realtor_options = ["Realtor1", "Realtor2", "Realtor3", "Realtor4"]
# realtor_var = tk.StringVar(value=realtor_options[-1])
# realtor_entry = ttk.Combobox(input_frame, textvariable=realtor_var, values=realtor_options)
# realtor_entry.grid(row=1, column=1, padx=5, pady=5)

# price_range_label = ttk.Label(input_frame, text="Price Range (USD):")
# price_range_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
# price_min_entry = ttk.Entry(input_frame)
# price_min_entry.grid(row=2, column=1, padx=5, pady=5)
# price_max_entry = ttk.Entry(input_frame)
# price_max_entry.grid(row=2, column=2, padx=5, pady=5)

# bedrooms_label = ttk.Label(input_frame, text="Bedrooms:")
# bedrooms_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
# bedrooms_options = ["0", "1", "2", "3", "4", "5", "6"]
# bedrooms_var = tk.StringVar(value=bedrooms_options[0])
# bedrooms_entry = ttk.Combobox(input_frame, textvariable=bedrooms_var, values=bedrooms_options)
# bedrooms_entry.grid(row=3, column=1, padx=5, pady=5)

# bathrooms_label = ttk.Label(input_frame, text="Bathrooms:")
# bathrooms_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
# bathrooms_options = ["0", "1", "2", "3", "4", "5"] 
# bathrooms_var = tk.StringVar(value=bathrooms_options[0])
# bathrooms_entry = ttk.Combobox(input_frame, textvariable=bathrooms_var, values=bathrooms_options)
# bathrooms_entry.grid(row=4, column=1, padx=5, pady=5)

# parking_label = ttk.Label(input_frame, text="Parking Spaces:")
# parking_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")
# parking_options = ["0", "1", "2", "3", "4"]
# parking_var = tk.StringVar(value=parking_options[0])
# parking_entry = ttk.Combobox(input_frame, textvariable=parking_var, values=parking_options)
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

