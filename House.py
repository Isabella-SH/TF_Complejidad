class House:

    def __init__(self, id, price_clp, price_uf, price_usd, comuna, ubicacion, dorms, baths, built_area, total_area, parking, realtor):
        self.id = id
        self.price_clp = price_clp
        self.price_uf = price_uf
        self.price_usd = price_usd
        self.comuna = comuna
        self.ubicacion = ubicacion
        self.dorms = dorms
        self.baths = baths
        self.built_area = built_area
        self.total_area = total_area
        self.parking = parking
        self.realtor = realtor

    def Price_CLP(self):
        return self.price_clp

    def Price_UF(self):
        return self.price_uf

    def Price_USD(self):
        return self.price_usd

    def Comuna(self):
        return self.comuna

    def Ubicacion(self):
        return self.ubicacion

    def Dorms(self):
        return self.dorms

    def Baths(self):
        return self.baths

    def Built_Area(self):
        return self.built_area

    def Total_Area(self):
        return self.total_area

    def Parking(self):
        return self.parking

    def ID(self):
        return self.id

    def Realtor(self):
        return self.realtor

#ejemplo de prueba

'''
casa = House(id=1, price_clp=100000000, price_uf=5000, price_usd=1500, comuna="Providencia", ubicacion="Santiago", dorms=4, baths=3, built_area=200, total_area=400, parking=True, realtor="Juan Perez")

precio_en_clp = casa.Price_CLP()
print(f"Precio en CLP: {precio_en_clp}")

'''
