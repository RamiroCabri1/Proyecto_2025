
from functools import wraps
from flask import request, jsonify
import jwt
from api import app 

# 1. Función para los días (La que te faltaba)
def get_dia_nombre(dia_numero):
    """Convierte el número de día de Python (0-6 o 1-7) a nombre."""
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    try:
        # Asumimos que dia_numero viene 1-indexado (Lunes=1)
        return dias[dia_numero - 1] 
    except IndexError:
        return None

# 2. El Guardián (Token)
def token_required(func):

    @wraps(func)
    def decorated(*args, **kwargs):
        token = None
        
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Falta el token de autenticación'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            request.negocio_id = data.get('negocio_id') # Guardamos el ID para usarlo después
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'El token ha expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'El token es inválido'}), 401

        return func(*args, **kwargs)
    
    return decorated

# 3. Validador de Campos
def validar_campos(datos, campos_requeridos):

    if not datos:
        return False
    for campo in campos_requeridos:
        if campo not in datos:
            return False
    return True