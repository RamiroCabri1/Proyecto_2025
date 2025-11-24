import datetime
import bcrypt
import jwt
from api.db.db import mysql
from api import app 
from typing import Union, Optional, Tuple, Dict, List

# Recordar type hints!!!!!

class Usuario:
    def __init__(self, id:int, email:str, password_hash:Union[str, bytes], negocio_id:int)->None:
        """
        Constructor explícito.
        Ventaja: Sabemos exactamente qué atributos tiene el objeto.
        Desacopla la lógica de la base de datos de la lógica del objeto.
        De Igual forma se crea una funcion que tiene la logica anterior por orden y no
        tan explicita.
        """
        self._id = id
        self._email = email
        self._password_hash = password_hash
        self._negocio_id = negocio_id

    @classmethod
    def from_row(cls, row: Optional[Tuple]) -> Union['Usuario', None]:
        """
        Si el dia de mañana no se cambia la base de datos esto ( como estaba antes )sirve muy bien 
        para el constructor. 
        """
        if not row:
            return None
        # Desempaquetamos la tupla aquí, creando el objeto de la forma anterior.
        return cls(id=row[0], email=row[1], password_hash=row[2], negocio_id=row[3])

    def to_json(self):
        """
        Serializa el objeto para devolverlo al cliente.
        """
        return {
            "id": self._id,
            "email": self._email,
            "negocio_id": self._negocio_id
        }
    @classmethod
    def crear_desde_datos(cls, datos: Dict) -> 'Usuario':
        """
        
        Recibe el diccionario crudo (JSON) y extrae los datos para llamar a crear().
        Esto limpia la ruta significativamente.
        """
        
        return cls.crear(
            email=datos.get('email'),
            password_plana=datos.get('password'), 
            negocio_id=datos.get('negocio_id')
        )    
    
    

    @classmethod
    def crear(cls, email: str, password_plana: str, negocio_id: int) -> 'Usuario':
        """
        Registra un nuevo usuario.
        
        paramatros:
            email: str
            password_plana:str
            negocio_id:int
        
        """
        # 1. Hashear
        password_hash = bcrypt.hashpw(password_plana.encode('utf-8'), bcrypt.gensalt())

        cursor = None
        try:
            cursor = mysql.connection.cursor()
            sql = "INSERT INTO Usuarios (email, password_hash, negocio_id) VALUES (%s, %s, %s)"
            valores = (email, password_hash, negocio_id)
            
            cursor.execute(sql, valores)
            mysql.connection.commit()
            
            nuevo_id = cursor.lastrowid
            
            # Como ahora los argumentos son explicitos, el el objeto se construye mas facil
            
            return cls(nuevo_id, email, password_hash, negocio_id)

        except Exception as err:
            if "1062" in str(err): 
                raise ValueError("El email ya está registrado")
            raise err
        finally:
            if cursor:
                cursor.close()

    @classmethod
    def buscar_por_email(cls, email:str)-> Optional["Usuario"]:
        """
        Busca en la base y retorna una instancia de Usuario o none si no encuentra datos en la base.
        
        parametros:
            email:str
        """
        cursor = None
        try:
            cursor = mysql.connection.cursor()
            sql = "SELECT id, email, password_hash, negocio_id FROM Usuarios WHERE email = %s"
            cursor.execute(sql, (email,))
            row = cursor.fetchone()

            
            return cls.from_row(row)

        except Exception as err:
            raise err
        finally:
            if cursor:
                cursor.close()

    
    # Agrego esta funcion que creo que simplifica.
    def verificar_password(self, password_plana:str)->bool:
        if isinstance(self._password_hash, str):
            self._password_hash = self._password_hash.encode('utf-8')
        return bcrypt.checkpw(password_plana.encode('utf-8'), self._password_hash)

    def generar_token(self):
        payload = {
            'usuario_id': self._id,
            'negocio_id': self._negocio_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }
        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm="HS256")
        return token