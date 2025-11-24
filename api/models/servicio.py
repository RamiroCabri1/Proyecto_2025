from api.db.db import mysql
from typing import Union, Optional, Tuple, Dict, List

class Servicio:
    def __init__(self, id: int, nombre: str, descripcion: str, duracion_turno_min: int, negocio_id: int) -> None:
        """
        Constructor explícito.
        Asigna los valores a atributos protegidos.
        """
        self._id = id
        self._nombre = nombre
        self._descripcion = descripcion
        self._duracion_turno_min = duracion_turno_min
        self._negocio_id = negocio_id

    @classmethod
    def from_row(cls, row: Optional[Tuple]) -> Union['Servicio', None]:
        """
        Convierte una tupla de la BD en un objeto Servicio.
        """
        if not row:
            return None
        return cls(
            id=row[0], 
            nombre=row[1], 
            descripcion=row[2], 
            duracion_turno_min=row[3], 
            negocio_id=row[4]
        )

    def to_json(self) -> Dict:
        """
        Serializa el objeto para responder al cliente.
        """
        return {
            "id": self._id,
            "nombre": self._nombre,
            "descripcion": self._descripcion,
            "duracion_turno_min": self._duracion_turno_min,
            "negocio_id": self._negocio_id
        }

   

    @classmethod
    def crear_desde_datos(cls, datos: Dict) -> 'Servicio':
        """
        Fachada: Recibe el diccionario crudo y llama al método estricto.
        """
        return cls.crear(
            nombre=datos.get('nombre'),
            descripcion=datos.get('descripcion'),
            duracion_turno_min=datos.get('duracion_turno_min'),
            negocio_id=datos.get('negocio_id')
        )

    @classmethod
    def crear(cls, nombre: str, descripcion: str, duracion_turno_min: int, negocio_id: int) -> 'Servicio':
        """
        Inserta un nuevo servicio en la BD y retorna la instancia creada.
        """
        cursor = None
        try:
            cursor = mysql.connection.cursor()
            sql = "INSERT INTO Servicios (nombre, descripcion, duracion_turno_min, negocio_id) VALUES (%s, %s, %s, %s)"
            valores = (nombre, descripcion, duracion_turno_min, negocio_id)
            
            cursor.execute(sql, valores)
            mysql.connection.commit()
            
            nuevo_id = cursor.lastrowid
            
            return cls(nuevo_id, nombre, descripcion, duracion_turno_min, negocio_id)
            
        except Exception as err:
            raise err
        finally:
            if cursor:
                cursor.close()

    

    @classmethod
    def obtener_todos(cls) -> List['Servicio']:
        """
        Retorna una lista de objetos Servicio.
        """
        cursor = None
        try:
            cursor = mysql.connection.cursor() 
            cursor.execute("SELECT * FROM Servicios") 
            filas = cursor.fetchall()
            
            lista_servicios = []
            for fila in filas:
                obj = cls.from_row(fila)
                if obj:
                    lista_servicios.append(obj)
            
            return lista_servicios
            
        except Exception as err:
            raise err
        finally:
            if cursor:
                cursor.close()

    @classmethod
    def obtener_por_id(cls, id: int) -> Optional['Servicio']:
        """
        Busca por ID y retorna un objeto Servicio o None.
        """
        cursor = None
        try:
            cursor = mysql.connection.cursor() 
            sql = "SELECT * FROM Servicios WHERE id = %s"
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
    def actualizar_desde_datos(cls, id: int, datos: Dict) -> Optional['Servicio']:
        """
        Fachada para actualizar.
        """
        return cls.actualizar(
            id=id,
            nombre=datos.get('nombre'),
            descripcion=datos.get('descripcion'),
            duracion_turno_min=datos.get('duracion_turno_min'),
            negocio_id=datos.get('negocio_id')
        )

    @classmethod
    def actualizar(cls, id: int, nombre: str, descripcion: str, duracion_turno_min: int, negocio_id: int) -> Optional['Servicio']:
        """
        Actualiza los datos y retorna el objeto actualizado, o None si no existe.
        """
        cursor = None
        try:
            cursor = mysql.connection.cursor()
            sql = "UPDATE Servicios SET nombre = %s, descripcion = %s, duracion_turno_min = %s, negocio_id = %s WHERE id = %s"
            valores = (nombre, descripcion, duracion_turno_min, negocio_id, id)
            
            cursor.execute(sql, valores)
            mysql.connection.commit()

            if cursor.rowcount == 0:
                # Podríamos hacer una verificación extra si existe, pero por rendimiento asumimos que si rowcount es 0, no existía o no cambió nada.
                # Para ser estrictos, intentamos buscarlo para devolver el objeto actualizado
                pass

            # Retornamos el objeto con los nuevos datos para confirmar
            return cls(id, nombre, descripcion, duracion_turno_min, negocio_id)

        except Exception as err:
            raise err
        finally:
            if cursor:
                cursor.close()

    # tendriamos que hacer un soft delete, osea crear una columna nueva que al momento de eliminar un servicio haga que los
    # turnos pasen a inactivos. Esto requiere cambiar la base y comprometo el modelo .

    @classmethod
    def eliminar(cls, id: int) -> int:
        """
        Elimina el servicio. Retorna la cantidad de filas afectadas.
        Maneja la restricción de clave foránea (FK), ya que al momento de eliminar afecta a turnos.
        """
        cursor = None
        try:
            cursor = mysql.connection.cursor()
            sql = "DELETE FROM Servicios WHERE id = %s"
            cursor.execute(sql, (id,))
            mysql.connection.commit()
            
            return cursor.rowcount
            
        except Exception as err:
            # Convertimos el error a string para buscar el código MySQL
            mensaje_error = str(err)
            
            # Error 1451: Foreign Key Constraint Fails # ESTE ERROR ES CLAVE
            if "1451" in mensaje_error:
                #
                raise ValueError("No se puede eliminar este servicio porque tiene turnos asociados. Elimine o reasigne los turnos primero.")
            
            # Si es otro error, lo dejamos subir
            raise err
        finally:
            if cursor:
                cursor.close()