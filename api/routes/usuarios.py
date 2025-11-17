from api.utils import token_required
from flask import Blueprint, jsonify, request
from api.models.usuario import Usuario
from api.db.db import mysql
from api import app # Para la SECRET_KEY
import bcrypt # Hashear contraseñas
import jwt # Para crear tokens
import datetime # Para la expiración del token

usuarios_bp = Blueprint('usuarios', __name__)

# POST /registro
# Este endpoint crea un Usuario. 
@usuarios_bp.route('/registro', methods=['POST'])
def registro():
    datos = request.get_json()
    if not datos or 'email' not in datos or 'password' not in datos or 'negocio_id' not in datos:
        return jsonify({"error": "Faltan datos (email, password, negocio_id)"}), 400
    
    email = datos['email']
    password_plana = datos['password']
    negocio_id = datos['negocio_id'] # Asumimos que el negocio ya existe

    # 1. Hashear la contraseña
    password_hash = bcrypt.hashpw(password_plana.encode('utf-8'), bcrypt.gensalt())
    print(password_hash)    
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        sql = "INSERT INTO Usuarios (email, password_hash, negocio_id) VALUES (%s, %s, %s)"
        valores = (email, password_hash, negocio_id)
        
        cursor.execute(sql, valores)
        mysql.connection.commit()
        
        nuevo_id = cursor.lastrowid
        return jsonify({"id": nuevo_id, "email": email, "negocio_id": negocio_id}), 201
    
    except Exception as err:
        if "1062" in str(err): # Error de "Duplicate entry"
            return jsonify({"error": "Ese email ya está registrado"}), 409
        return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()

# POST /login
@usuarios_bp.route('/login', methods=['POST'])
def login():
    
    #Aqui la otra opcion seria sacar los datos no como request.get_jason()
    #Sino como datos = auth.email , auth.password. que es mejor y cual sera al diferencia? 
    # la forma usada seria la mejor
    datos = request.get_json()
    if not datos or 'email' not in datos or 'password' not in datos:
        return jsonify({"error": "Faltan datos (email, password)"}), 400

    email = datos['email']
    password_plana = datos['password']

    cursor = None
    try:
        cursor = mysql.connection.cursor()
        
        # 1. Buscamos al usuario por email
        sql = "SELECT * FROM Usuarios WHERE email = %s"
        cursor.execute(sql, (email,))
        fila_usuario = cursor.fetchone()

        if not fila_usuario:
            return jsonify({"error": "Credenciales inválidas"}), 401 # 401 No Autorizado

        # 2. Obtenemos el hash guardado de la BD
        # (id, email, password_hash, negocio_id) -> el hash es el índice 2
        hash_guardado = fila_usuario[2] 

        # 3. Verificamos la contraseña
        if bcrypt.checkpw(password_plana.encode('utf-8'), hash_guardado.encode('utf-8')):
            # ¡Contraseña CORRECTA! Creamos el token.
            payload = {
                'usuario_id': fila_usuario[0],
                'negocio_id': fila_usuario[3],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24) # Token dura 24 horas
            }
            token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm="HS256")
            
            # Falaria mas info. Es una apirestfull, la respuesta tiene q tener informar suficiente como para poder
            # continuar. aqui faltaria usuario o id y nombre ( o en este caso mail)
            return jsonify({"token": token})
        else:
            # Contraseña INCORRECTA
            return jsonify({"error": "Credenciales inválidas"}), 401

    except Exception as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()