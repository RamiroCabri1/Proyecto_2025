
from api.db.db import mysql
from typing import Dict, List, Optional

class Cliente:
    def __init__(self, row):
        # (id, nombre, apellido, dni, telefono, email, negocio_id)
        self._id = row[0]
        self._nombre = row[1]
        self._apellido = row[2]
        self._dni = row[3]
        self._telefono = row[4]
        self._email = row[5]
        self._negocio_id = row[6]

    def to_json(self) -> Dict:
        return {
            "id": self._id,
            "nombre": self._nombre,
            "apellido": self._apellido,
            "dni": self._dni,
            "telefono": self._telefono,
            "email": self._email,
            "negocio_id": self._negocio_id
        }

    @classmethod
    def from_row(cls, row):
        if not row: return None
        return cls(row)

    # logica de lectura

    @classmethod
    def obtener_todos(cls, negocio_id: int) -> List['Cliente']:
        """Trae los clientes SOLO del negocio_id especificado"""
        cursor = None
        try:
            cursor = mysql.connection.cursor()
            sql = "SELECT * FROM Clientes WHERE negocio_id = %s"
            cursor.execute(sql, (negocio_id,))
            filas = cursor.fetchall()
            
            lista = []
            for fila in filas:
                lista.append(cls(fila)) # Creamos el objeto Cliente
            return lista
        except Exception as e:
            raise e
        finally:
            if cursor: cursor.close()

    @classmethod
    def obtener_por_id(cls, id: int) -> Optional['Cliente']:
        """Busca un cliente por su ID único"""
        cursor = None
        try:
            cursor = mysql.connection.cursor()
            sql = "SELECT * FROM Clientes WHERE id = %s"
            cursor.execute(sql, (id,))
            fila = cursor.fetchone()
            return cls.from_row(fila)
        except Exception as e:
            raise e
        finally:
            if cursor: cursor.close()

    # logica de creacion

    @classmethod
    def crear_desde_datos(cls, datos: Dict) -> 'Cliente':
        return cls.crear(
            nombre=datos.get('nombre'),
            apellido=datos.get('apellido'),
            dni=datos.get('dni'),
            telefono=datos.get('telefono'),
            email=datos.get('email'),
            negocio_id=datos.get('negocio_id')
        )

    @classmethod
    def crear(cls, nombre, apellido, dni, telefono, email, negocio_id):
        cursor = None
        try:
            cursor = mysql.connection.cursor()
            sql = "INSERT INTO Clientes (nombre, apellido, dni, telefono, email, negocio_id) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (nombre, apellido, dni, telefono, email, negocio_id)
            cursor.execute(sql, val)
            mysql.connection.commit()
            
            nuevo_id = cursor.lastrowid
            # Armamos una tupla "fake" para crear el objeto y devolverlo
            row_fake = (nuevo_id, nombre, apellido, dni, telefono, email, negocio_id)
            return cls(row_fake)
            
        except Exception as e:
            # Error 1062: DNI duplicado
            if "1062" in str(e): 
                raise ValueError("Ya existe un cliente con ese DNI para este negocio")
            raise e
        finally:
            if cursor: cursor.close()

    # logica de eliminación

    @classmethod
    def eliminar(cls, id: int) -> int:
        cursor = None
        try:
            cursor = mysql.connection.cursor()
            sql = "DELETE FROM Clientes WHERE id = %s"
            cursor.execute(sql, (id,))
            mysql.connection.commit()
            return cursor.rowcount
        except Exception as e:
            raise e
        finally:
            if cursor: cursor.close()