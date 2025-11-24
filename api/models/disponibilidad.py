from api.db.db import mysql
from datetime import timedelta
from typing import Union, Optional, Tuple, Dict, List

class Disponibilidad:
    def __init__(self, id: int, profesional_id: int, dia_semana: str, hora_inicio: Union[timedelta, str], hora_fin: Union[timedelta, str]) -> None:
        """
        Constructor explícito.
        """
        self._id = id
        self._profesional_id = profesional_id
        self._dia_semana = dia_semana
        self._hora_inicio = hora_inicio
        self._hora_fin = hora_fin

    @classmethod
    def from_row(cls, row: Optional[Tuple]) -> Union['Disponibilidad', None]:
        """
        Mapea la tupla de la BD al Objeto.
        Orden asumido: (id, profesional_id, dia_semana, hora_inicio, hora_fin)
        """
        if not row:
            return None
        return cls(
            id=row[0], 
            profesional_id=row[1], 
            dia_semana=row[2], 
            hora_inicio=row[3], 
            hora_fin=row[4]
        )

    def to_json(self) -> Dict:
        """
        Serializa el objeto.
        Maneja la conversión de timedelta a string HH:MM.
        """
        def format_time(t):
            if isinstance(t, timedelta):
                # Convertimos timedelta a string "H:MM:SS"
                t_str = str(t)
                if "day" in t_str:
                    t_str = t_str.split(", ")[1]
                
                # Quitamos los segundos finales (:00) si queremos formato HH:MM
                return t_str[:-3] if len(t_str) > 5 else t_str
            return str(t)

        h_inicio = format_time(self._hora_inicio)
        h_fin = format_time(self._hora_fin)
        
        # Aseguramos el '0' adelante si quedó como 9:00 -> 09:00
        if len(h_inicio) == 4: h_inicio = '0' + h_inicio
        if len(h_fin) == 4: h_fin = '0' + h_fin

        return {
            "id": self._id,
            "profesional_id": self._profesional_id,
            "dia_semana": self._dia_semana,
            "hora_inicio": h_inicio,
            "hora_fin": h_fin
        }

    # --- Logica de creacion

    @classmethod
    def crear_desde_datos(cls, datos: Dict) -> 'Disponibilidad':
        """
        Fachada: Limpia el JSON y llama a crear.
        """
        return cls.crear(
            profesional_id=datos.get('profesional_id'),
            dia_semana=datos.get('dia_semana'),
            hora_inicio=datos.get('hora_inicio'),
            hora_fin=datos.get('hora_fin')
        )

    @classmethod
    def crear(cls, profesional_id: int, dia_semana: str, hora_inicio: str, hora_fin: str) -> 'Disponibilidad':
        """
        Inserta una nueva disponibilidad en la tabla 'Disponibilidad'.
        """
        cursor = None
        try:
            cursor = mysql.connection.cursor()
            sql = "INSERT INTO Disponibilidad (profesional_id, dia_semana, hora_inicio, hora_fin) VALUES (%s, %s, %s, %s)"
            valores = (profesional_id, dia_semana, hora_inicio, hora_fin)
            
            cursor.execute(sql, valores)
            mysql.connection.commit()
            
            nuevo_id = cursor.lastrowid
            
            return cls(nuevo_id, profesional_id, dia_semana, hora_inicio, hora_fin)
            
        except Exception as err:
            raise err
        finally:
            if cursor:
                cursor.close()

    # --- Logica de lectura

    @classmethod
    def obtener_por_profesional_id(cls, profesional_id: int) -> List['Disponibilidad']:
        """
        Retorna todas las Disponibilidad de un profesional específico.
        """
        cursor = None
        try:
            cursor = mysql.connection.cursor() 
            sql = "SELECT * FROM Disponibilidad WHERE profesional_id = %s"
            cursor.execute(sql, (profesional_id,))
            filas = cursor.fetchall()
            
            lista = []
            for fila in filas:
                obj = cls.from_row(fila)
                if obj:
                    lista.append(obj)
            return lista 
            
        except Exception as err:
            raise err
        finally:
            if cursor:
                cursor.close()
    
    @classmethod
    def obtener_por_id(cls, id: int) -> Optional['Disponibilidad']:
        """
        Busca una disponibilidad específica por su ID.
        """
        cursor = None
        try:
            cursor = mysql.connection.cursor() 
            sql = "SELECT * FROM Disponibilidad WHERE id = %s"
            cursor.execute(sql, (id,))
            fila = cursor.fetchone()
            
            return cls.from_row(fila)
            
        except Exception as err:
            raise err
        finally:
            if cursor:
                cursor.close()

    # --- Logica de actualizacion

    @classmethod
    def actualizar_desde_datos(cls, id: int, datos: Dict) -> Optional['Disponibilidad']:
        """
        Fachada para actualizar.
        """
        return cls.actualizar(
            id=id,
            profesional_id=datos.get('profesional_id'),
            dia_semana=datos.get('dia_semana'),
            hora_inicio=datos.get('hora_inicio'),
            hora_fin=datos.get('hora_fin')
        )

    @classmethod
    def actualizar(cls, id: int, profesional_id: int, dia_semana: str, hora_inicio: str, hora_fin: str) -> Optional['Disponibilidad']:
        """
        Actualiza y retorna el objeto actualizado.
        """
        cursor = None
        try:
            cursor = mysql.connection.cursor()
            sql = "UPDATE Disponibilidad SET profesional_id = %s, dia_semana = %s, hora_inicio = %s, hora_fin = %s WHERE id = %s"
            valores = (profesional_id, dia_semana, hora_inicio, hora_fin, id)
            
            cursor.execute(sql, valores)
            mysql.connection.commit()

            return cls(id, profesional_id, dia_semana, hora_inicio, hora_fin)

        except Exception as err:
            raise err
        finally:
            if cursor:
                cursor.close()

    # --- Logica de eliminacion

    @classmethod
    def eliminar(cls, id: int) -> int:
        """
        Elimina la disponibilidad teniendo en cuenta el id de la misma.
        """
        cursor = None
        try:
            cursor = mysql.connection.cursor()
            sql = "DELETE FROM Disponibilidad WHERE id = %s"
            cursor.execute(sql, (id,))
            mysql.connection.commit()
            
            return cursor.rowcount
            
        except Exception as err:
            raise err
        finally:
            if cursor:
                cursor.close()