# api/utils.py
from functools import wraps
from flask import request, jsonify
import jwt
from api import app 

# Módulo de utilidades para convertir el día de Python a nombre de la DB
def get_dia_nombre(dia_numero):
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    try:
        return dias[dia_numero - 1] 
    except IndexError:
        return None

def token_required(func):
    """
    Este es el decorador que protege las rutas.
    Verifica que se envíe un token válido en los headers.
    """
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None
        
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Falta el token de autenticación'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'El token ha expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'El token es inválido'}), 401

        return func(*args, **kwargs)
    
    return decorated # <--- ¡ESTA LÍNEA TIENE QUE ESTAR ACÁ! (Indentada dentro de token_required)

def validar_campos(datos, campos_requeridos):
    """
    Valida que 'datos' contenga todas las claves de 'campos_requeridos'.
    Retorna True si está todo ok, False si falta algo.
    """
    if not datos:
        return False
    for campo in campos_requeridos:
        if campo not in datos:
            return False
    return True