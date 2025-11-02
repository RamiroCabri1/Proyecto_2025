class Negocio():
    def __init__(self, row):
        # El 'row' es la tupla que viene de la BD
        # (id, nombre, direccion, telefono)
        # Adaptamos los índices según tu consulta
        self._id = row[0]
        self._nombre = row[1]
        self._direccion = row[2]
        self._telefono = row[3]
    
    def to_json(self):
        # Este método convierte el objeto en un diccionario
        return {
            "id": self._id,
            "nombre": self._nombre,
            "direccion": self._direccion,
            "telefono": self._telefono
        }