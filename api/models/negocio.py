from api.db.db import mysql
from typing import Union, Optional, Tuple, Dict, List

class Negocio:
    def __init__(self, id: int, nombre: str, direccion: str, telefono: str) -> None:
        """
        Constructor explícito.
        Asigna los valores a atributos protegidos.
        """
        self._id = id
        self._nombre = nombre
        self._direccion = direccion
        self._telefono = telefono # Telefono str quizas no sea la mejor opcion.
        #Para no complicar y siendo que es facil modificar, se deja asi.

    @classmethod
    def from_row(cls, row: Optional[Tuple]) -> Union['Negocio', None]:
        """
        Mapea la tupla de la BD al Objeto.
        Orden asumido: (id, nombre, direccion, telefono)
        """
        if not row:
            return None
        return cls(
            id=row[0], 
            nombre=row[1], 
            direccion=row[2], 
            telefono=row[3]
        )

    def to_json(self) -> Dict:
        """
        Serializa el objeto.
        """
        return {
            "id": self._id,
            "nombre": self._nombre,
            "direccion": self._direccion,
            "telefono": self._telefono
        }

    # Creacion

    @classmethod
    def crear_desde_datos(cls, datos: Dict) -> 'Negocio':
        """
        Fachada: Limpia el JSON y llama a crear.
        
        """
        return cls.crear(
            nombre=datos.get('nombre'),
            direccion=datos.get('direccion'),
            telefono=datos.get('telefono')
        )

    @classmethod
    def crear(cls, nombre: str, direccion: str, telefono: str) -> 'Negocio':
        """
        Inserta un nuevo negocio.
        """
        cursor = None
        try:
            cursor = mysql.connection.cursor()
            sql = "INSERT INTO Negocios (nombre, direccion, telefono) VALUES (%s, %s, %s)"
            valores = (nombre, direccion, telefono)
            
            cursor.execute(sql, valores)
            mysql.connection.commit()
            
            nuevo_id = cursor.lastrowid
            
            return cls(nuevo_id, nombre, direccion, telefono)
            
        except Exception as err:
            raise err
        finally:
            if cursor:
                cursor.close()

    # lectura

    @classmethod
    def obtener_todos(cls) -> List['Negocio']:
        """
        Retorna lista de objetos Negocio.
        """
        cursor = None
        try:
            cursor = mysql.connection.cursor() 
            cursor.execute("SELECT id, nombre, direccion, telefono FROM Negocios") 
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
    def obtener_por_id(cls, id: int) -> Optional['Negocio']:
        """
        Retorna un Negocio o None.
        """
        cursor = None
        try:
            cursor = mysql.connection.cursor() 
            sql = "SELECT id, nombre, direccion, telefono FROM Negocios WHERE id = %s"
            cursor.execute(sql, (id,))
            fila = cursor.fetchone()
            
            return cls.from_row(fila)
            
        except Exception as err:
            raise err
        finally:
            if cursor:
                cursor.close()

    # actualizar

    @classmethod
    def actualizar_desde_datos(cls, id: int, datos: Dict) -> Optional['Negocio']:
        """
        Fachada para actualizar.
        """
        return cls.actualizar(
            id=id,
            nombre=datos.get('nombre'),
            direccion=datos.get('direccion'),
            telefono=datos.get('telefono')
        )

    @classmethod
    def actualizar(cls, id: int, nombre: str, direccion: str, telefono: str) -> Optional['Negocio']:
        """
        Actualiza y retorna el objeto actualizado.
        """
        cursor = None
        try:
            cursor = mysql.connection.cursor()
            sql = "UPDATE Negocios SET nombre = %s, direccion = %s, telefono = %s WHERE id = %s"
            valores = (nombre, direccion, telefono, id)
            
            cursor.execute(sql, valores)
            mysql.connection.commit()

            # Retornamos el objeto con los nuevos datos
            

            return cls(id, nombre, direccion, telefono)

        except Exception as err:
            raise err
        finally:
            if cursor:
                cursor.close()

    # Delete

    @classmethod
    def eliminar(cls, id: int) -> int:
        """
        Elimina el negocio. Maneja error de FK (Usuarios/Servicios asociados).
        """
        cursor = None
        try:
            cursor = mysql.connection.cursor()
            sql = "DELETE FROM Negocios WHERE id = %s"
            cursor.execute(sql, (id,))
            mysql.connection.commit()
            
            return cursor.rowcount
            
        except Exception as err:
            mensaje = str(err)
            # Error 1451: Foreign Key Constraint
            if "1451" in mensaje:
                raise ValueError("No se puede eliminar el negocio porque tiene usuarios, servicios o profesionales asociados. Elimine estos registros primero.")
            raise err
        finally:
            if cursor:
                cursor.close()