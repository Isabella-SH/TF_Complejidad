class Grafo:
    def __init__(self):
        self.nodos = {}
        self.aristas = {}

    def agregar_nodo(self, price_clp=None,price_uf=None,price_usd=None,comuna=None,ubicacion=None,dorms=None,baths=None,built_area=None,total_area=None,parking=None,id=None,realtor=None):
        self.nodos[id] = {
            'id':id,
            'price_clp': price_clp,
            'price_uf': price_uf,
            'price_usd': price_usd,
            'comuna': comuna,
            'ubicacion': ubicacion,
            'dorms': dorms,
            'baths':baths,
            'built_area':built_area,
            'total_area':total_area,
            'parking':parking,
            'realtor':realtor
        }
        self.aristas[id] = {}

    def agregar_arista(self, id_origen, id_destino, peso):
        self.aristas[id_origen][id_destino] = peso
        self.aristas[id_destino][id_origen] = peso

    def obtener_nodos(self):
        return self.nodos.keys()

    def obtener_aristas(self):
        aristas = []
        for id_origen in self.aristas:
            for id_destino in self.aristas[id_origen]:
                if (id_destino, id_origen) not in aristas:
                    aristas.append((id_origen, id_destino, self.aristas[id_origen][id_destino]))
        return aristas
    
    def __str__(self):
        nodos_str = ""
        for nodo_id in self.obtener_nodos():
            for destino, peso in self.aristas[nodo_id].items():
                nodos_str += f"Nodo {nodo_id} -> Nodo {destino} = Peso {peso}\n"
        return nodos_str




