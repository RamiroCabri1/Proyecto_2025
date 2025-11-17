from datetime import datetime, timedelta
from api.db.db import mysql
from api.utils import get_dia_nombre


class Turno():
    def __init__(self, row):
        # Asumo que el SELECT de la ruta GET devuelve estos 7 campos
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
        
    @classmethod
    def create_and_validate(cls, datos):
        cursor = None
        try:
            # Parseo de fecha y hora
            fecha_hora_obj = datetime.strptime(datos['fecha_hora'], '%Y-%m-%d %H:%M:%S')
            
            # Aca es donde usamos la funcion nueva ( Ubicada en utils )
            dia_semana_num = fecha_hora_obj.weekday() + 1 
            dia_semana_nombre = get_dia_nombre(dia_semana_num)
            
            hora_turno_inicio = fecha_hora_obj.time().strftime('%H:%M:%S') # Hora de inicio del turno
            
            
            profesional_id = datos['profesional_id']
            servicio_id = datos['servicio_id']
            
            cursor = mysql.connection.cursor() 
            
            # Valida disponibilidad
            sql_disponibilidad = """
                SELECT hora_fin FROM disponibilidades 
                WHERE profesional_id = %s 
                AND dia_semana = %s 
                AND TIME(%s) >= hora_inicio AND TIME(%s) <= hora_fin
            """
            valores_disp = (profesional_id, dia_semana_nombre, hora_turno_inicio, hora_turno_inicio)
            
            cursor.execute(sql_disponibilidad, valores_disp)
            disponibilidad_encontrada = cursor.fetchone() 
            
            if not disponibilidad_encontrada:
                raise ValueError("El profesional no se encuentra disponible en ese día u horario.")

            # 2da validacion, turno ocupado ( o no )
            
            sql_ocupado = "SELECT id FROM Turnos WHERE profesional_id = %s AND fecha_hora = %s"
            cursor.execute(sql_ocupado, (profesional_id, datos['fecha_hora']))
            if cursor.fetchone():
                raise ValueError("El turno ya se encuentra ocupado.")
                
            # Insert
            sql_insert = """
                INSERT INTO Turnos (fecha_hora, estado, cliente_id, profesional_id, servicio_id, negocio_id) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            valores = (datos['fecha_hora'], 'Confirmado', datos['cliente_id'], profesional_id, datos['servicio_id'], datos['negocio_id'])
            
            cursor.execute(sql_insert, valores)
            mysql.connection.commit()
            
            nuevo_id = cursor.lastrowid
            
            # Return de un dic con los datos del turno
            return {
                "id": nuevo_id, "fecha_hora": datos['fecha_hora'], "estado": "Confirmado",
                "cliente_id": datos['cliente_id'], "profesional_id": profesional_id,
                "servicio_id": datos['servicio_id'], "negocio_id": datos['negocio_id']
            }
        except ValueError:
            # Captura errores de lógica de negocio (lanzados por raise ValueError)
            raise 
        except Exception as err:
            # Captura errores SQL o de Python
            if cursor:
                mysql.connection.rollback()
            raise err 
        finally:
            if cursor:
                cursor.close()
    @classmethod               
    def get_all_turnos(cls):
        """
        Extrae todos los turnos de la DB, los convierte a objetos Turno 
        y devuelve una lista de diccionarios (JSON-ready).
        
        Si no hay turnos, devuelve una lista vacía [].
        """
        cursor = None
        try:
            cursor = mysql.connection.cursor() 
            cursor.execute("SELECT * FROM Turnos") # segun lo leido, mejor seria seleccionar todos los elementos y no usar *
            filas = cursor.fetchall()
            
            if not filas:
                return [] # Devuelve una lista vacía si no hay resultados
            lista_turnos_json = []
            for fila in filas:
                objTurno = Turno(fila) 
                lista_turnos_json.append(objTurno.to_json()) 
            
            return lista_turnos_json # Devuelve la lista de diccionarios 

        except Exception as err:
            # El modelo solo lanza errores de Python o SQL
            raise err 
            
        finally:
            if cursor:
                cursor.close()
                
    @classmethod
    def delete_turno(cls, turno_id: int) -> int:
        """
        Elimina un turno de la base de datos por id
        Retorna el número de filas afectadas (0 si no se encontró).
        """
        cursor = None
        try:
            cursor = mysql.connection.cursor()
            sql = "DELETE FROM Turnos WHERE id = %s"
            cursor.execute(sql, (turno_id,))
            
            # Guarda el número de filas afectadas ANTES de hacer commit
            filas_afectadas = cursor.rowcount 
            mysql.connection.commit()
            return filas_afectadas

        except Exception as err:
            mysql.connection.rollback()
            # El modelo debe lanzar la excepción para que la ruta la capture
            raise err 
            
        finally:
            if cursor:
                cursor.close()