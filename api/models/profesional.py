from api.db.db import mysql
from typing import Union, Optional, Tuple, Dict, List

class Profesional:
    def __init__(self, id: int, nombre: str, negocio_id: int, activo: int) -> None:
        """
        Constructor explícito.
        Asigna los valores a atributos protegidos.
        """
        self._id = id
        self._nombre = nombre
        self._negocio_id = negocio_id
        self._activo = activo

    @classmethod
    def from_row(cls, row: Optional[Tuple]) -> Union['Profesional', None]:
        """
        Mapea la tupla de la BD al Objeto.
        Funcion que sirve ( en este caso ) luego para busqueda por id. Si 
        la busqueda en la bd es infructuosa con el it not, nos aseguramos el none que se usa en la busqueda x id
        """
        if not row:
            return None
        return cls(
            id=row[0], 
            nombre=row[1], 
            negocio_id=row[2], 
            activo=row[3]
        )

    def to_json(self) -> Dict:
        """
        Serializa el objeto.
        """
        return {
            "id": self._id,
            "nombre": self._nombre,
            "activo": self._activo,  # recordar que puede ser binario o bool (01,truefalse)
            "negocio_id": self._negocio_id
        }

    # --- LÓGICA DE CREACIÓN ---

    @classmethod
    def crear_desde_datos(cls, datos: Dict) -> 'Profesional':
        """
        Fachada: Limpia el JSON y llama a crear.
        """
        return cls.crear(
            nombre=datos.get('nombre'),
            activo=datos.get('activo'),
            negocio_id=datos.get('negocio_id')
        )

    @classmethod
    def crear(cls, nombre: str, activo: int, negocio_id: int) -> 'Profesional':
        """
        Inserta un nuevo profesional.
        """
        cursor = None
        try:
            cursor = mysql.connection.cursor()
            sql = "INSERT INTO Profesionales (nombre, activo, negocio_id) VALUES (%s, %s, %s)"
            valores = (nombre, activo, negocio_id)
            
            cursor.execute(sql, valores)
            mysql.connection.commit()
            
            nuevo_id = cursor.lastrowid
            
            # Retornamos la instancia creada
            return cls(nuevo_id, nombre, negocio_id, activo)
            
        except Exception as err:
            raise err
        finally:
            if cursor:
                cursor.close()

    # --- LÓGICA DE LECTURA ---

    @classmethod
    def obtener_todos(cls) -> List['Profesional']:
        """
        Retorna lista de objetos Profesional.
        """
        cursor = None
        try:
            cursor = mysql.connection.cursor() 
            cursor.execute("SELECT * FROM Profesionales") 
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
    def obtener_por_id(cls, id: int) -> Optional['Profesional']:
        """
        Retorna un Profesional o None.
        """
        cursor = None
        try:
            cursor = mysql.connection.cursor() 
            sql = "SELECT * FROM Profesionales WHERE id = %s"
            cursor.execute(sql, (id,))
            fila = cursor.fetchone()
            
            return cls.from_row(fila)
            
        except Exception as err:
            raise err
        finally:
            if cursor:
                cursor.close()

    # --- LÓGICA DE ACTUALIZACIÓN ---

    @classmethod
    def actualizar_desde_datos(cls, id: int, datos: Dict) -> Optional['Profesional']:
        """
        Fachada para actualizar.
        """
        return cls.actualizar(
            id=id,
            nombre=datos.get('nombre'),
            activo=datos.get('activo'),
            negocio_id=datos.get('negocio_id')
        )

    @classmethod
    def actualizar(cls, id: int, nombre: str, activo: int, negocio_id: int) -> Optional['Profesional']:
        """
        Actualiza y retorna el objeto actualizado.
        """
        cursor = None
        try:
            cursor = mysql.connection.cursor()
            sql = "UPDATE Profesionales SET nombre = %s, activo = %s, negocio_id = %s WHERE id = %s"
            valores = (nombre, activo, negocio_id, id)
            
            cursor.execute(sql, valores)
            mysql.connection.commit()

            
            if cursor.rowcount == 0:
                
                pass 

            return cls(id, nombre, negocio_id, activo)

        except Exception as err:
            raise err
        finally:
            if cursor:
                cursor.close()

    # --- LÓGICA DE ELIMINACIÓN ---

    @classmethod
    def eliminar(cls, id: int) -> int:
        """
        Elimina el profesional. Maneja error de FK (Turnos asociados).
        """
        cursor = None
        try:
            cursor = mysql.connection.cursor()
            sql = "DELETE FROM Profesionales WHERE id = %s"
            cursor.execute(sql, (id,))
            mysql.connection.commit()
            
            return cursor.rowcount
            
        except Exception as err:
            mensaje = str(err)
            # Error 1451: No se puede borrar si tiene hijos (Turnos o Disponibilidades)
            # Hablar con el equipo.
            if "1451" in mensaje:
                raise ValueError("No se puede eliminar al profesional porque tiene turnos o disponibilidades asociadas.")
            raise err
        finally:
            if cursor:
                cursor.close()