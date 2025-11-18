class Negocio():
    def __init__(self, row):
        
        # El 'row' es la tupla que viene de la BD        
        self._id = row[0]
        self._nombre = row[1]
        self._direccion = row[2]
        self._telefono = row[3]
    
    def to_json(self):
        # Lo pasamos a diccionario
        
        return {
            "id": self._id,
            "nombre": self._nombre,
            "direccion": self._direccion,
            "telefono": self._telefono
        }