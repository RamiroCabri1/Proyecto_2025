# api/utils.py
from functools import wraps
from flask import request, jsonify
import jwt
from api import app # Importamos la 'app' para leer la SECRET_KEY

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