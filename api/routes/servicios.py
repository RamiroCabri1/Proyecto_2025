# api/routes/servicios.py
from flask import Blueprint, jsonify, request
from api.utils import token_required, validar_campos
from api.models.servicio import Servicio

servicios_bp = Blueprint('servicios', __name__)

# GET Todos (Híbrido: Público o Privado según token)
@servicios_bp.route('/servicios', methods=['GET'])
def get_servicios():
    try:
        negocio_id = None

        # Intentamos leer el token manualmente
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            try:
                from api import app
                import jwt
                data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
                negocio_id = data.get('negocio_id')
            except:
                pass 
        
        # Llamamos al modelo
        lista_objetos = Servicio.obtener_todos(negocio_id)
        lista_json = [s.to_json() for s in lista_objetos]
        
        return jsonify(lista_json), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500

# GET por ID
@servicios_bp.route('/servicios/<int:id>', methods=['GET'])
def get_servicio_por_id(id):
    try:
        servicio = Servicio.obtener_por_id(id)
        if servicio:
            return jsonify(servicio.to_json()), 200
        return jsonify({"error": "Servicio no encontrado"}), 404
    except Exception as err:
        return jsonify({"error": str(err)}), 500

# POST (Crear) - Privado
@servicios_bp.route('/servicios', methods=['POST'])
@token_required
def create_servicio():
    datos = request.get_json()
    
    if not validar_campos(datos, ['nombre', 'descripcion', 'duracion_turno_min']):
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    try:
        # Forzamos el negocio_id del token
        datos['negocio_id'] = request.negocio_id
        
        nuevo = Servicio.crear_desde_datos(datos)
        return jsonify(nuevo.to_json()), 201

    except Exception as err:
        return jsonify({"error": str(err)}), 500

# DELETE (Borrar) - Privado
@servicios_bp.route('/servicios/<int:id>', methods=['DELETE'])
@token_required
def delete_servicio(id):
    try:
        filas = Servicio.eliminar(id)
        if filas > 0:
            return jsonify({"message": "Servicio eliminado"}), 200
        return jsonify({"error": "Servicio no encontrado"}), 404
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 409
    except Exception as err:
        return jsonify({"error": str(err)}), 500