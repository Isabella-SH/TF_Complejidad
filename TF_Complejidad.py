﻿
import csv
from Graph import Graph, drawG_al, drawG_al_2
from House import House
import matplotlib.pyplot as plt
import graphviz as gv
import heapq
from collections import deque




                                                                   #EXTRAER INFORMACION DEL C.S.V !!!!!!!!!!!!

# Abre el archivo CSV
with open ('Database/database.csv', 'r', encoding='utf-8') as archivo_csv:
    # Lee el contenido del archivo CSV
    lector_csv = csv.DictReader(archivo_csv)
    
    casas = []

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

        casa = House(
            id=id,
            price_clp=price_clp,
            price_uf=price_uf,
            price_usd=price_usd,
            comuna=comuna,
            ubicacion=ubicacion,
            dorms=dorms,
            baths=baths,
            built_area=built_area,
            total_area=total_area,
            parking=parking,
            realtor=realtor
        )
        #agrega todos los registros a objetos casas
        casas.append(casa)


#imprimir registros
'''
for idx, casa in enumerate(casas):
    print(f"Índice: {idx}")
    print(f"ID: {casa.id}")
    print(f"Precio CLP: {casa.price_clp}")
    print(f"Precio UF: {casa.price_uf}")
    print(f"Precio USD: {casa.price_usd}")
    print(f"Comuna: {casa.comuna}")
    print(f"Ubicacion: {casa.ubicacion}")
    print(f"Dormitorios: {casa.dorms}")
    print(f"Baños: {casa.baths}")
    print(f"Área Construida: {casa.built_area}")
    print(f"Área Total: {casa.total_area}")
    print(f"Parking: {casa.parking}")
    print(f"Realtor: {casa.realtor}")
    print("\n")
    
    if idx % 50 == 0:  # Imprimir cada 50 resultados
        input("Presiona Enter para continuar...")
'''
   

                                                                     
                                                                            #CREAR EL GRAFO !!!!!!!!!!!!
G = Graph()

# Añadir nodos
for casa in casas:
    G.add_node(casa)

# Añadir aristas basadas en comuna y asignar pesos
for i, casa_u in enumerate(casas):
    for j, casa_v in enumerate(casas):
        if i != j:  # Evitar agregar bucles
            if casa_u.Comuna() == casa_v.Comuna() :
                G.add_edge(casa_u, casa_v)

                # Inicializar weight
                weight = 10
                
                #print(f"Dorm u:{casa_u.Dorms()}")
                #print(f"Dorm v:{casa_v.Dorms()}")

                if casa_u.Dorms() == casa_v.Dorms():
                    weight -= 4

                if casa_u.Baths() == casa_v.Baths():
                    weight -= 3

                if casa_u.Parking() == casa_v.Parking():
                    weight -= 2
                #mientras menor sea el peso de la arista quiere decir que los nodos son mas iguales
                G.add_weighted_edge(casa_u, casa_v, weight)
                
#print(f"Se creo el grafo")
# Graficamos el grafo
#drawG_al(G, weighted=True, directed=False)

'''

def dijkstra(grafo, inicio, precio_min, precio_max, habitaciones_min, habitaciones_max, banos_min, banos_max, comuna, parking):

    distancias = {nodo: float('inf') for nodo in grafo.obtener_nodos()}
    distancias[inicio] = 0
    cola_prioridad = [(0, inicio)]
    visitados = set()

    while cola_prioridad:
        _, nodo_actual = heapq.heappop(cola_prioridad)
        if nodo_actual in visitados:
            continue
        visitados.add(nodo_actual)

        for nodo_vecino, peso in grafo.get_edges(nodo_actual):
            distancia_nueva = distancias[nodo_actual] + peso
            if distancia_nueva < distancias[nodo_vecino]:
                distancias[nodo_vecino] = distancia_nueva
                heapq.heappush(cola_prioridad, (distancia_nueva, nodo_vecino))

    # Filtrar las casas según los criterios especificados
    casas_filtradas = []

    for casa, distancia in distancias.items():
        if (
            precio_min <= casa.Price_USD() <= precio_max and
            habitaciones_min <= casa.Dorms() <= habitaciones_max and
            banos_min <= casa.Baths() <= banos_max and
            (comuna == "Todas" or casa.Comuna() == comuna) and
            casa.Parking() == parking
        ):
            casas_filtradas.append((casa, distancia))

    return sorted(casas_filtradas, key=lambda x: x[1])[:10]



resultados = dijkstra(
    G,
    10, 
    90000,
    100000, 
    1, 
    4, 
    1, 
    1, 
    "MaipÃº",
    1
)
'''

# Definimos la función de Dijkstra
def dijkstra(grafo, inicio, precio_min, precio_max, habitaciones_min, habitaciones_max, banos_min, banos_max, comuna, parking):

    distancias = {nodo: float('inf') for nodo in grafo.obtener_nodos()}
    distancias[inicio] = 0
    cola_prioridad = [(0, inicio)]
    visitados = set()

    while cola_prioridad:
        _, nodo_actual = heapq.heappop(cola_prioridad)
        if nodo_actual in visitados:
            continue
        visitados.add(nodo_actual)

        for nodo_vecino, peso in grafo.get_edges(nodo_actual):
            distancia_nueva = distancias[nodo_actual] + peso
            if distancia_nueva < distancias[nodo_vecino]:
                distancias[nodo_vecino] = distancia_nueva
                heapq.heappush(cola_prioridad, (distancia_nueva, nodo_vecino))

    # Filtrar las casas según los criterios especificados
    casas_filtradas = []

    for casa, distancia in distancias.items():
        if (
            precio_min <= casa.Price_USD <= precio_max and
            habitaciones_min <= casa.Dorms <= habitaciones_max and
            banos_min <= casa.Baths <= banos_max and
            (comuna == "Todas" or casa.Comuna == comuna) and
            casa.Parking == parking
        ):
            casas_filtradas.append((casa, distancia))

    return sorted(casas_filtradas, key=lambda x: x[1])[:10]

# Definimos una función para obtener las recomendaciones y mostrar resultados
def obtener_recomendaciones():
    global inicio

    # Obtener el nombre de la comuna de inicio desde la interfaz
    comuna_inicio = "Estación Central"

    # Buscar la comuna de inicio en el grafo
    inicio = None
    for casa in casas:
        if casa.Comuna() == comuna_inicio:
            inicio = casa
            break

    # Verificar si se encontró la comuna de inicio
    if inicio is None:
        # Mostrar un mensaje en la interfaz indicando que la comuna no se encuentra en el grafo
        print("No se encontró el inicio")
    else:
        recomendaciones = dijkstra(
            G,
            inicio,  # Cambiado a 'inicio'
            90000,
            100000, 
            1, 
            4, 
            1, 
            1, 
            "Maipú",
            1
        )
        print(recomendaciones)

        
#obtengo las recomendaciones
obtener_recomendaciones()











































































