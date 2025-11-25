from api.db.db import mysql
from typing import Dict, List, Optional, Tuple, Union # <--- ESTA LÍNEA FALTABA COSAS

class Servicio:
    def __init__(self, id: int, nombre: str, descripcion: str, duracion_turno_min: int, negocio_id: int) -> None:
        self._id = id
        self._nombre = nombre
        self._descripcion = descripcion
        self._duracion_turno_min = duracion_turno_min
        self._negocio_id = negocio_id
    
    def to_json(self) -> Dict:
        return {
            "id": self._id,
            "nombre": self._nombre,
            "descripcion": self._descripcion,
            "duracion_turno_min": self._duracion_turno_min,
            "negocio_id": self._negocio_id
        }

    @classmethod
    def from_row(cls, row: Optional[Tuple]) -> Union['Servicio', None]:
        if not row: return None
        return cls(
            id=row[0], 
            nombre=row[1], 
            descripcion=row[2], 
            duracion_turno_min=row[3], 
            negocio_id=row[4]
        )

    # --- LECTURA (Multi-Tenant) ---

    @classmethod
    def obtener_todos(cls, negocio_id: int = None) -> List['Servicio']:
        """
        Si recibe negocio_id, filtra. Si es None, devuelve TODOS (para público).
        """
        cursor = None
        try:
            cursor = mysql.connection.cursor()
            
            if negocio_id:
                sql = "SELECT * FROM Servicios WHERE negocio_id = %s"
                cursor.execute(sql, (negocio_id,))
            else:
                sql = "SELECT * FROM Servicios"
                cursor.execute(sql)
                
            filas = cursor.fetchall()
            
            lista = []
            for fila in filas:
                obj = cls.from_row(fila)
                if obj:
                    lista.append(obj)
            return lista
        except Exception as e:
            raise e
        finally:
            if cursor: cursor.close()

    @classmethod
    def obtener_por_id(cls, id: int) -> Optional['Servicio']:
        cursor = None
        try:
            cursor = mysql.connection.cursor()
            sql = "SELECT * FROM Servicios WHERE id = %s"
            cursor.execute(sql, (id,))
            return cls.from_row(cursor.fetchone())
        except Exception as e:
            raise e
        finally:
            if cursor: cursor.close()

    # --- CREACIÓN ---

    @classmethod
    def crear_desde_datos(cls, datos: Dict) -> 'Servicio':
        return cls.crear(
            nombre=datos.get('nombre'),
            descripcion=datos.get('descripcion'),
            duracion=datos.get('duracion_turno_min'),
            negocio_id=datos.get('negocio_id')
        )

    @classmethod
    def crear(cls, nombre, descripcion, duracion, negocio_id) -> 'Servicio':
        cursor = None
        try:
            cursor = mysql.connection.cursor()
            sql = "INSERT INTO Servicios (nombre, descripcion, duracion_turno_min, negocio_id) VALUES (%s, %s, %s, %s)"
            val = (nombre, descripcion, duracion, negocio_id)
            cursor.execute(sql, val)
            mysql.connection.commit()
            
            return cls(cursor.lastrowid, nombre, descripcion, duracion, negocio_id)
        except Exception as e:
            raise e
        finally:
            if cursor: cursor.close()

    # --- ELIMINACIÓN ---

    @classmethod
    def eliminar(cls, id: int) -> int:
        cursor = None
        try:
            cursor = mysql.connection.cursor()
            sql = "DELETE FROM Servicios WHERE id = %s"
            cursor.execute(sql, (id,))
            mysql.connection.commit()
            return cursor.rowcount
        except Exception as e:
            if "1451" in str(e):
                raise ValueError("No se puede eliminar el servicio porque tiene turnos asociados.")
            raise e
        finally:
            if cursor: cursor.close()