
import tkinter as tk
from tkinter import Toplevel, Label, Button
from tkinter import font
import tkinter as tk
from tkinter import ttk
import networkx as nx
from tkinter import messagebox
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
casas_cercanas= []

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


def filtrar_por_atributo(recommendations, filtro):
    # Filtrar seg�n el criterio especificado en el filtro
    if filtro == "dorms":
        # Ordenar casas por el atributo 'dorms'
        sorted_houses = sorted(recommendations, key=lambda x: grafo.nodos[x[0]]['dorms'])
        casas_ordenadas_por_dorms = [(casa, distancia) for casa, distancia in sorted_houses]
        return casas_ordenadas_por_dorms

    elif filtro == "baths":
        # Ordenar casas por el atributo 'baths'
        sorted_baths = sorted(recommendations, key=lambda x: grafo.nodos[x[0]]['baths'])
        casas_ordenadas_por_baths = [(casa, distancia) for casa, distancia in sorted_baths]
        return casas_ordenadas_por_baths

    elif filtro == "parking":
        # Ordenar casas por el atributo 'parking'
        sorted_park = sorted(recommendations, key=lambda x: grafo.nodos[x[0]]['parking'])
        casas_ordenadas_por_park = [(casa, distancia) for casa, distancia in sorted_park]
        return casas_ordenadas_por_park
    
    elif filtro == "price_usd":
        # Ordenar casas por el atributo 'price_usd'
        sorted_price_usd = sorted(recommendations, key=lambda x: grafo.nodos[x[0]]['price_usd'])
        casas_ordenadas_por_price_usd = [(casa, distancia) for casa, distancia in sorted_price_usd]
        return casas_ordenadas_por_price_usd

    elif filtro == "desc":
        # Filtrar casas que tengan 'desc' como True
        return [(casa, distancia) for casa, distancia in recommendations if grafo.nodos[casa]['desc']]
    
    elif filtro == "total_area":
        # Ordenar casas por el atributo 'price_usd'
        sorted_price_total_area = sorted(recommendations, key=lambda x: grafo.nodos[x[0]]['total_area'])
        casas_ordenadas_por_total_area = [(casa, distancia) for casa, distancia in sorted_price_total_area]
        return casas_ordenadas_por_total_area

    elif filtro == "todo":
        return recommendations  # Si el filtro no es reconocido, devolvemos la lista completa


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


#print(grafo)
#print("Resultados de las recomendaciones\n\n")
#obtener_recomendaciones()

def mostrar_fachada_aleatoria():
  
     todas_las_casas = list(grafo.obtener_nodos())

     casa_aleatoria = random.choice(todas_las_casas)
     ruta_imagen = f"imagenes_fachadas/fachada_{casa_aleatoria}.jpg"

     ventana_fachada = tk.Toplevel(root)
     ventana_fachada.title("Fachada de Casa Aleatoria")
     imagen = Image.open(ruta_imagen)
     imagen_tk = ImageTk.PhotoImage(imagen)
     label = tk.Label(ventana_fachada, image=imagen_tk)
     label.pack()
     boton_cerrar = tk.Button(ventana_fachada, text="Cerrar", command=lambda: cerrar_ventana(ventana_fachada))
     boton_cerrar.pack()

def cerrar_ventana(ventana):
     ventana.destroy()
     
root = tk.Tk()
root.title("Recomendador de Casas")
  
def get_recommendations():
    comuna = comuna_var.get()
    realtor = realtor_var.get()
    price_min = int(price_min_entry.get())
    price_max = int(price_max_entry.get())
    bedrooms = int(bedrooms_var.get())
    bathrooms = int(bathrooms_var.get())
    parking = int(parking_var.get())

    inicio = None
    for nodo in grafo.nodos:
        if grafo.nodos[nodo]['comuna'] == comuna:
            inicio = nodo
            break

    recommendations = dijkstra(grafo, inicio, comuna, realtor, price_min, price_max, bedrooms, bathrooms, parking)

    # Pass the recommendations and selected attribute to the filtering function
    filtro_seleccionado = atributo_var.get()
    casas_filtradas = filtrar_por_atributo(recommendations, filtro_seleccionado)

    # Update the Treeview with the filtered results
    for item in treeview.get_children():
        print(treeview.get_children())
        treeview.delete(item)

    for i, (casa, distancia) in enumerate(casas_filtradas):
        casa_data = [
            i + 1,
            grafo.nodos[casa]['comuna'],
            grafo.nodos[casa]['realtor'],
            grafo.nodos[casa]['price_usd'],
            grafo.nodos[casa]['dorms'],
            grafo.nodos[casa]['baths'],
            grafo.nodos[casa]['parking'],
            distancia
        ]
        treeview.insert('', 'end', values=casa_data)

# Crear el widget Treeview para mostrar las recomendaciones
columns = ('#', 'Comuna', 'Realtor', 'Precio USD', 'Dormitorios', 'Banos', 'Estacionamientos', 'Distancia')
treeview = ttk.Treeview(root, columns=columns, show='headings')

# Configurar las columnas
for col in columns:
    treeview.heading(col, text=col)

treeview.grid(row=9, column=0, columnspan=2)


comuna_var = tk.StringVar()
realtor_var = tk.StringVar()
bedrooms_var = tk.StringVar()
bathrooms_var = tk.StringVar()
parking_var = tk.StringVar()

# Etiquetas y entradas para las opciones del usuario
tk.Label(root, text="Comuna:").grid(row=0, column=0)
comuna_entry = ttk.Combobox(root, textvariable=comuna_var, values=["Tiltil","SanMiguel","Talagante","Recoleta","Renca","Paine","Pirque","Melipilla","PadreHurtado","LoPrado","Macul","LaPintana","LoEspejo","LaCisterna","LaGranja","Independencia","IsladeMaipo","ElBosque","ElMonte","Cerrillos","CerroNavia","Buin","CaleradeTango","Pudahuel","Huechuraba","Providencia","LaReina","Vitacura","LoBarnechea","PuenteAlto", "LasCondes", "QuintaNormal","PedroAguirreCerda", "Colina","LaFlorida", "SanBernardo","Santiago", "LasCondes", "Lampa", "Quilicura"])
comuna_entry.grid(row=0, column=1)

tk.Label(root, text="Realtor:").grid(row=1, column=0)
realtor_entry = ttk.Combobox(root, textvariable=realtor_var, values=["","Viel la Dehesa SPA","Viel Propiedades dos Ltda","Schumacher Propiedades","OSSANDON CORREDORES ASOCIADOS S.A","Easyprop","Lyon y Balmaceda Ltda.","Bofill y Asociados Ltda","Nieto & Stone Propiedades","Invictus Spa","Unne","Hobbins Vitacura","Welink Propiedades SpA","Vidal Riedel Propiedades - Las Condes","Nexxos","Mocahome Corredores Integrados","Manterola Propiedades","Tzani Propiedades","Legale y Propiedades Spa", "Propiedadesrs", "Patricia Gajardo propiedades", "Todo Propiedades","Paula Vivanco Arenas", "Fe Propiedades Spa", "Ecorredores Getion Inmobiliaria","Behouse", "Propital", "Cgs Corretaje Inmobiliario Spa", "Giordano Propiedades"])
realtor_entry.grid(row=1, column=1)

tk.Label(root, text="Precio Minimo:").grid(row=2, column=0)
price_min_entry = tk.Entry(root, validate="key", validatecommand=(root.register(lambda char: char.isdigit() or char == ""), "%S"))
price_min_entry.grid(row=2, column=1)

tk.Label(root, text="Precio Maximo:").grid(row=3, column=0)
price_max_entry = tk.Entry(root, validate="key", validatecommand=(root.register(lambda char: char.isdigit() or char == ""), "%S"))
price_max_entry.grid(row=3, column=1)

tk.Label(root, text="Dormitorios Minimos:").grid(row=4, column=0)
bedrooms_entry = ttk.Combobox(root, textvariable=bedrooms_var, values=["0","1", "2", "3","4", "5", "6","7","8","9","10","11","12","13","14","15","16"])
bedrooms_entry.grid(row=4, column=1)

tk.Label(root, text="Banos Minimos:").grid(row=5, column=0)
bathrooms_entry = ttk.Combobox(root, textvariable=bathrooms_var, values=["0","1", "2", "3","4", "5", "6","7","8","9","10","11","12"])
bathrooms_entry.grid(row=5, column=1)

tk.Label(root, text="Estacionamientos Minimos:").grid(row=6, column=0)
parking_entry = ttk.Combobox(root, textvariable=parking_var, values=["0","1", "2", "3","4", "5", "6","7","8","9","10","11","12","13","14","15","16","17","20"])
parking_entry.grid(row=6, column=1)

recomendaciones_btn = tk.Button(root, text="Obtener Recomendaciones", command=get_recommendations)
recomendaciones_btn.grid(row=7, column=0, columnspan=2, pady=10)

atributo_var = tk.StringVar()
atributo_var.set("todo") 

atributo_label = tk.Label(root, text="Filtrar por Atributo:")
atributo_label.grid(row=10, column=0)

atributo_entry = ttk.Combobox(root, textvariable=atributo_var, values=["todo", "dorms", "baths", "parking", "price_usd", "desc", "total_area"])
atributo_entry.grid(row=10, column=1)


root.main