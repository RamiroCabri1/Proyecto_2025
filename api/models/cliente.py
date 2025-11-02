
class Cliente():
    def __init__(self, row):
        
        self._id = row[0]
        self._nombre = row[1]
        self._apellido = row[2]
        self._dni = row[3]
        self._telefono = row[4]
        self._email = row[5]
        self._negocio_id = row[6]
    
    def to_json(self):
        return {
            "id": self._id,
            "nombre": self._nombre,
            "apellido": self._apellido,
            "dni": self._dni,
            "telefono": self._telefono,
            "email": self._email,
            "negocio_id": self._negocio_id
        }