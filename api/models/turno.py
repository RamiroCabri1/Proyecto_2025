from datetime import datetime
from api.db.db import mysql
from api.utils import get_dia_nombre
from typing import Union, Optional, Tuple, List

class Turno:
    def __init__(self, id: int, fecha_hora: datetime, estado: str, cliente_id: int, profesional_id: int, servicio_id: int, negocio_id: int) -> None:
        self._id = id
        self._fecha_hora = fecha_hora
        self._estado = estado
        self._cliente_id = cliente_id
        self._profesional_id = profesional_id
        self._servicio_id = servicio_id
        self._negocio_id = negocio_id
        
    def to_json(self) -> dict:
        fecha_str = self._fecha_hora.strftime('%Y-%m-%d %H:%M:%S') if isinstance(self._fecha_hora, datetime) else str(self._fecha_hora)

        return {
            "id": self._id,
            "fecha_hora": fecha_str,
            "estado": self._estado,
            "cliente_id": self._cliente_id,
            "profesional_id": self._profesional_id,
            "servicio_id": self._servicio_id,
            "negocio_id": self._negocio_id
        }

    @classmethod
    def from_row(cls, row: Optional[Tuple]) -> Union['Turno', None]:
        if not row:
            return None
        
        return cls(
            id=row[0],
            fecha_hora=row[1], 
            estado=row[2],
            cliente_id=row[3],
            profesional_id=row[4],
            servicio_id=row[5],
            negocio_id=row[6]
        )

    @classmethod
    def crear_desde_datos(cls, datos: dict) -> 'Turno':
        return cls.crear(
            fecha_hora_str=datos.get('fecha_hora'),
            cliente_id=datos.get('cliente_id'),
            profesional_id=datos.get('profesional_id'),
            servicio_id=datos.get('servicio_id'),
            negocio_id=datos.get('negocio_id')
        )

    @classmethod
    def crear(cls, fecha_hora_str: str, cliente_id: int, profesional_id: int, servicio_id: int, negocio_id: int) -> 'Turno':
        cursor = None
        try:
            fecha_hora_obj = datetime.strptime(fecha_hora_str, '%Y-%m-%d %H:%M:%S')
            dia_semana_num = fecha_hora_obj.weekday() + 1 
            dia_semana_nombre = get_dia_nombre(dia_semana_num)
            hora_turno_inicio = fecha_hora_obj.time().strftime('%H:%M:%S')
            
            cursor = mysql.connection.cursor() 
            
            # Validación 1: Disponibilidad
            sql_disponibilidad = """
                SELECT hora_fin FROM Disponibilidad 
                WHERE profesional_id = %s 
                AND dia_semana = %s 
                AND TIME(%s) >= hora_inicio AND TIME(%s) <= hora_fin
            """
            cursor.execute(sql_disponibilidad, (profesional_id, dia_semana_num, hora_turno_inicio, hora_turno_inicio))
            if not cursor.fetchone():
                raise ValueError("El profesional no se encuentra disponible en ese día u horario.")

            # Validación 2: Turno ocupado
            sql_ocupado = "SELECT id FROM Turnos WHERE profesional_id = %s AND fecha_hora = %s"
            cursor.execute(sql_ocupado, (profesional_id, fecha_hora_str))
            if cursor.fetchone():
                raise ValueError("El turno ya se encuentra ocupado.")
                
            # Insertar
            sql_insert = """
                INSERT INTO Turnos (fecha_hora, estado, cliente_id, profesional_id, servicio_id, negocio_id) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            estado_inicial = 'Confirmado'
            valores = (fecha_hora_str, estado_inicial, cliente_id, profesional_id, servicio_id, negocio_id)
            
            cursor.execute(sql_insert, valores)
            mysql.connection.commit()
            
            nuevo_id = cursor.lastrowid
            
            return cls(
                id=nuevo_id,
                fecha_hora=fecha_hora_obj,
                estado=estado_inicial,
                cliente_id=cliente_id,
                profesional_id=profesional_id,
                servicio_id=servicio_id,
                negocio_id=negocio_id
            )

        except Exception as err:
            if cursor:
                mysql.connection.rollback()
            raise err 
        finally:
            if cursor:
                cursor.close()

    @classmethod
    def get_all(cls, negocio_id: int = None) -> List[dict]:
        """
        Trae todos los turnos con JOINs (Nombres reales).
        """
        cursor = None
        try:
            cursor = mysql.connection.cursor()
            
            sql = """
                SELECT 
                    t.id, t.fecha_hora, t.estado,
                    c.nombre AS cliente_nombre, c.apellido AS cliente_apellido, c.telefono AS cliente_telefono,
                    p.nombre AS profesional_nombre,
                    s.nombre AS servicio_nombre
                FROM Turnos t
                JOIN Clientes c ON t.cliente_id = c.id
                JOIN Profesionales p ON t.profesional_id = p.id
                JOIN Servicios s ON t.servicio_id = s.id
            """
            
            if negocio_id:
                sql += " WHERE t.negocio_id = %s"
                cursor.execute(sql, (negocio_id,))
            else:
                cursor.execute(sql)
                
            filas = cursor.fetchall()
            
            lista_completa = []
            for fila in filas:
                turno_full = {
                    "id": fila[0],
                    "fecha_hora": str(fila[1]),
                    "estado": fila[2],
                    "cliente_nombre": f"{fila[3]} {fila[4] or ''}".strip(),
                    "cliente_telefono": fila[5],
                    "profesional_nombre": fila[6],
                    "servicio_nombre": fila[7]
                }
                lista_completa.append(turno_full)
            
            return lista_completa

        except Exception as err:
            raise err 
        finally:
            if cursor: cursor.close()

            
    @classmethod
    def delete(cls, turno_id: int) -> int:
        cursor = None
        try:
            cursor = mysql.connection.cursor()
            sql = "DELETE FROM Turnos WHERE id = %s"
            cursor.execute(sql, (turno_id,))
            
            filas_afectadas = cursor.rowcount 
            mysql.connection.commit()
            return filas_afectadas

        except Exception as err:
            mysql.connection.rollback()
            raise err 
        finally:
            if cursor:
                cursor.close()

    @classmethod
    def obtener_por_id(cls, turno_id: int) -> Optional['Turno']:
        """
        Busca un turno específico por su ID.
        """
        cursor = None
        try:
            cursor = mysql.connection.cursor()
            sql = "SELECT * FROM Turnos WHERE id = %s"
            cursor.execute(sql, (turno_id,))
            fila = cursor.fetchone()
            
            return cls.from_row(fila)

        except Exception as err:
            raise err
        finally:
            if cursor:
                cursor.close()