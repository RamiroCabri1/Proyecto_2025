
from datetime import datetime

class Turno():
    def __init__(self, row):
        
        self._id = row[0]
        self._fecha_hora = row[1] # Objeto datetime
        self._estado = row[2]
        self._cliente_id = row[3]
        self._profesional_id = row[4]
        self._servicio_id = row[5]
        self._negocio_id = row[6]
    
    def to_json(self):
        # Formateamos a string estándar
        fecha_hora_str = self._fecha_hora.strftime('%Y-%m-%d %H:%M:%S')

        return {
            "id": self._id,
            "fecha_hora": fecha_hora_str,
            "estado": self._estado,
            "cliente_id": self._cliente_id,
            "profesional_id": self._profesional_id,
            "servicio_id": self._servicio_id,
            "negocio_id": self._negocio_id
        }