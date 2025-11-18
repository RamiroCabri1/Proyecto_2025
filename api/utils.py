# api/utils.py
from functools import wraps
from flask import request, jsonify
import jwt
from api import app # Importamos la 'app' para leer la SECRET_KEY

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



def token_required(func):
    """
    Este es el decorador que protege las rutas.
    Verifica que se envíe un token válido en los headers.
    """
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None
        
        # 1. Buscamos el token en los headers de la petición
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Falta el token de autenticación'}), 401

        try:
            # 2. Decodificamos el token usando nuestra SECRET_KEY
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            
            # (Opcional) Podríamos guardar 'data' en el request
            # para saber qué usuario está haciendo la petición
        
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'El token ha expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'El token es inválido'}), 401

        # 3. Si todo está bien, dejamos que la ruta original se ejecute
        return func(*args, **kwargs)
    
    return decorated