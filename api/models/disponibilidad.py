
from datetime import timedelta

class Disponibilidad():
    def __init__(self, row):
      
        self._id = row[0]
        self._profesional_id = row[1]
        self._dia_semana = row[2]
        self._hora_inicio = row[3] # Esto es un timedelta
        self._hora_fin = row[4]  # (Sería la diferencia de tiempo entre una y la otra)
    
    def to_json(self):
        # Convertimos los timedelta a string HH:MM
        hora_inicio_str = str(self._hora_inicio)[:-3]
        hora_fin_str = str(self._hora_fin)[:-3]

        if len(hora_inicio_str) == 4:
            hora_inicio_str = '0' + hora_inicio_str
        if len(hora_fin_str) == 4:
            hora_fin_str = '0' + hora_fin_str

        return {
            "id": self._id,
            "profesional_id": self._profesional_id,
            "dia_semana": self._dia_semana,
            "hora_inicio": hora_inicio_str,
            "hora_fin": hora_fin_str
        }