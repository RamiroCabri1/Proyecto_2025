from flask import Blueprint, jsonify, request
from api.models.usuario import Usuario

usuarios_bp = Blueprint('usuarios', __name__)

# POST /registro
@usuarios_bp.route('/registro', methods=['POST'])
def registro():
    datos = request.get_json()
    
    
    if not datos or 'email' not in datos or 'password' not in datos or 'negocio_id' not in datos:
        return jsonify({"error": "Faltan datos (email, password, negocio_id)"}), 400
    
    try:
        
        nuevo_usuario = Usuario.crear_desde_datos(datos)
        
        # 3. Respuesta exitosa
        return jsonify(nuevo_usuario.to_json()), 201
        
    except ValueError as e:
        # Errores de validación de negocio (ej: email duplicado)
        return jsonify({"error": str(e)}), 409
    except Exception as e:
        # Errores inesperados de servidor
        return jsonify({"error": str(e)}), 500


# POST /login
@usuarios_bp.route('/login', methods=['POST'])
def login():
    datos = request.get_json()
    
    # 1. Validación básica de entrada
    if not datos or 'email' not in datos or 'password' not in datos:
        return jsonify({"error": "Faltan datos (email, password)"}), 400

    email = datos['email']
    password_plana = datos['password']

    try:
        # 2. Invocación al Modelo: "Usuario, búscate por este email"
        usuario = Usuario.buscar_por_email(email)

        if not usuario:
            return jsonify({"error": "Credenciales inválidas"}), 401

        # 3. Verificación de lógica: "¿Es correcta la contraseña?"
        if usuario.verificar_password(password_plana):
            
            # Delego la creacion del token al modelo, lo quito de la ruta
            token = usuario.generar_token()
            
            # 
            respuesta = usuario.to_json()
            respuesta['token'] = token
            
            return jsonify(respuesta), 200
        else:
            return jsonify({"error": "Credenciales inválidas"}), 401

    except Exception as e:
        return jsonify({"error": f"Error interno: {str(e)}"}), 500