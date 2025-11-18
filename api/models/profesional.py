
class Profesional():
    def __init__(self, row):
        # Recordatorio: el orden correcto de SELECT * es (id, nombre, negocio_id, activo)
        self._id = row[0]
        self._nombre = row[1]
        self._negocio_id = row[2]
        self._activo = row[3]
    
    def to_json(self):
        return {
            "id": self._id,
            "nombre": self._nombre,
            "activo": self._activo,
            "negocio_id": self._negocio_id
        }