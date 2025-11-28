
from api.db.db import mysql
from typing import Dict, List, Optional

class Disponibilidad:
    def __init__(self, row):
        self._id = row[0]
        self._profesional_id = row[1]
        self._dia_semana = row[2]
        self._hora_inicio = row[3]
        self._hora_fin = row[4]
    
    def to_json(self) -> Dict:
        # funcion para limpiar la hora, quitamos segundos
        def limpiar_hora(tiempo):
            # Convertimos a string (por si viene como timedelta o time)
            s = str(tiempo)
            # Si es largo (09:00:00), cortamos los últimos 3
            if len(s) >= 5:
                return s[:5] 
            return s

        return {
            "id": self._id,
            "profesional_id": self._profesional_id,
            "dia_semana": self._dia_semana,
            "hora_inicio": limpiar_hora(self._hora_inicio),
            "hora_fin": limpiar_hora(self._hora_fin)
        }
    


    @classmethod

    def from_row(cls, row):
        if not row: return None
        return cls(row)

    # -Lectura

    @classmethod
    def obtener_por_profesional(cls, profesional_id: int) -> List['Disponibilidad']:
        """Trae los horarios de un profesional específico"""
        cursor = None
        try:
            cursor = mysql.connection.cursor()
            # Nombre de tabla: Disponibilidad (Singular)
            sql = "SELECT * FROM Disponibilidad WHERE profesional_id = %s"
            cursor.execute(sql, (profesional_id,))
            filas = cursor.fetchall()
            
            lista = []
            for fila in filas:
                lista.append(cls(fila))
            return lista
        except Exception as e:
            raise e
        finally:
            if cursor: cursor.close()

    @classmethod
    def obtener_por_id(cls, id: int) -> Optional['Disponibilidad']:

        cursor = None
        try:
            cursor = mysql.connection.cursor()
            sql = "SELECT * FROM Disponibilidad WHERE id = %s"
            cursor.execute(sql, (id,))
            return cls.from_row(cursor.fetchone())
        except Exception as e:
            raise e
        finally:
            if cursor: cursor.close()

    # Creacion

    @classmethod
    def crear(cls, profesional_id, dia_semana, hora_inicio, hora_fin) -> 'Disponibilidad':
        cursor = None
        try:
            cursor = mysql.connection.cursor()
            sql = "INSERT INTO Disponibilidad (profesional_id, dia_semana, hora_inicio, hora_fin) VALUES (%s, %s, %s, %s)"
            val = (profesional_id, dia_semana, hora_inicio, hora_fin)
            
            cursor.execute(sql, val)
            mysql.connection.commit()
            
            # Retornamos objeto 'fake' para la respuesta
            row_fake = (cursor.lastrowid, profesional_id, dia_semana, hora_inicio, hora_fin)
            return cls(row_fake)
        except Exception as e:
            raise e
        finally:
            if cursor: cursor.close()

    # Modificamos

    @classmethod
    def actualizar(cls, id, profesional_id, dia_semana, hora_inicio, hora_fin) -> 'Disponibilidad':
        cursor = None
        try:
            cursor = mysql.connection.cursor()
            sql = "UPDATE Disponibilidad SET profesional_id=%s, dia_semana=%s, hora_inicio=%s, hora_fin=%s WHERE id=%s"
            val = (profesional_id, dia_semana, hora_inicio, hora_fin, id)
            
            cursor.execute(sql, val)
            mysql.connection.commit()
            
            if cursor.rowcount == 0: return None
            
            row_fake = (id, profesional_id, dia_semana, hora_inicio, hora_fin)
            return cls(row_fake)
        except Exception as e:
            raise e
        finally:
            if cursor: cursor.close()

    # Eliminación

    @classmethod
    def eliminar(cls, id: int) -> int:

        cursor = None
        try:
            cursor = mysql.connection.cursor()
            sql = "DELETE FROM Disponibilidad WHERE id = %s"
            cursor.execute(sql, (id,))
            mysql.connection.commit()

            return cursor.rowcount
        except Exception as e:
            raise e
        finally:
            if cursor: cursor.close()