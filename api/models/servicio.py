# api/models/servicio.py
class Servicio():
    def __init__(self, row):
        # (id, nombre, descripcion, duracion_turno_min, negocio_id)
        self._id = row[0]
        self._nombre = row[1]
        self._descripcion = row[2]
        self._duracion_turno_min = row[3]
        self._negocio_id = row[4]
    
    def to_json(self):
        return {
            "id": self._id,
            "nombre": self._nombre,
            "descripcion": self._descripcion,
            "duracion_turno_min": self._duracion_turno_min,
            "negocio_id": self._negocio_id
        }