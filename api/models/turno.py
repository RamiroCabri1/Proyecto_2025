from datetime import datetime, timedelta
from api.db.db import mysql

# Módulo de utilidades para convertir el día de Python a nombre de la DB
def get_dia_nombre(dia_numero):
    """Convierte el número de día de Python (1=Lunes a 7=Domingo) a nombre."""
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    # Los días de Python (0-6)
    try:
        # El día_numero viene de weekday() + 1, así que restamos 1 para el índice
        return dias[dia_numero - 1] 
    except IndexError:
        return None


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
            # 1. Parseo de Fecha y Hora y Conversión de Día
            fecha_hora_obj = datetime.strptime(datos['fecha_hora'], '%Y-%m-%d %H:%M:%S')
            
            # **CORRECCIÓN CRÍTICA 1:** Obtenemos el NOMBRE del día para alinear con la tabla VARCHAR(20)
            dia_semana_num = fecha_hora_obj.weekday() + 1 
            dia_semana_nombre = get_dia_nombre(dia_semana_num)
            
            hora_turno_inicio = fecha_hora_obj.time().strftime('%H:%M:%S') # Hora de inicio del turno
            
            # 2. Asignación de variables
            profesional_id = datos['profesional_id']
            servicio_id = datos['servicio_id']
            
            cursor = mysql.connection.cursor() 
            
            # 5. Validación 1: Disponibilidad (Chequeando INICIO)
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

            # 6. Validación 2: Turno Ocupado (Doble Reserva)
            # OJO: Chequear el campo Turnos.fecha_hora (que es el inicio del turno)
            sql_ocupado = "SELECT id FROM Turnos WHERE profesional_id = %s AND fecha_hora = %s"
            cursor.execute(sql_ocupado, (profesional_id, datos['fecha_hora']))
            if cursor.fetchone():
                raise ValueError("El turno ya se encuentra ocupado.")
                
            # 7. Inserción del Turno
            sql_insert = """
                INSERT INTO Turnos (fecha_hora, estado, cliente_id, profesional_id, servicio_id, negocio_id) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            valores = (datos['fecha_hora'], 'Confirmado', datos['cliente_id'], profesional_id, datos['servicio_id'], datos['negocio_id'])
            
            cursor.execute(sql_insert, valores)
            mysql.connection.commit()
            
            nuevo_id = cursor.lastrowid
            
            # 8. Retornamos el diccionario del turno creado
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