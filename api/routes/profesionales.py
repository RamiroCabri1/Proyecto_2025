from api.utils import token_required
from flask import Blueprint, jsonify, request
from api.models.profesional import Profesional 

profesionales_bp = Blueprint('profesionales', __name__)

# GET Todos
@profesionales_bp.route('/profesionales', methods=['GET'])
# @token_required  <-- LO SACAMOS PARA QUE SEA PÚBLICO
def get_profesionales():
    try:
        negocio_id = None

        # Intentamos leer el token manualmente para ver si es un Admin
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            try:
                from api import app
                import jwt
                data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
                negocio_id = data.get('negocio_id')
            except:
                pass # Si el token es inválido, asumimos público (negocio_id = None)
        
        # Llamamos al modelo (si negocio_id es None, trae todo; si tiene valor, filtra)
        lista_objetos = Profesional.obtener_todos(negocio_id)
        lista_json = [p.to_json() for p in lista_objetos]
        
        return jsonify(lista_json), 200
        
    except Exception as err:
        return jsonify({"error": str(err)}), 500

# GET por ID
@profesionales_bp.route('/profesionales/<int:id>', methods=['GET'])
@token_required
def get_profesional_por_id(id):
    try:
        profesional = Profesional.obtener_por_id(id)
        
        if profesional:
            return jsonify(profesional.to_json()), 200
        else:
            return jsonify({"error": "Profesional no encontrado"}), 404
            
    except Exception as err:
        return jsonify({"error": str(err)}), 500

# POST (Crear)
@profesionales_bp.route('/profesionales', methods=['POST'])
@token_required
def create_profesional():
    datos = request.get_json()
    
    # Esta logica de control, pienso que se puede hacer en los modelos.
    campos_requeridos = ['nombre', 'activo', 'negocio_id']
    if not datos or not all(campo in datos for campo in campos_requeridos):
        return jsonify({"error": f"Faltan datos. Se requiere: {campos_requeridos}"}), 400

    try:
        # Usamos la Fachada
        nuevo_profesional = Profesional.crear_desde_datos(datos)
        
        return jsonify(nuevo_profesional.to_json()), 201
        
    except Exception as err:
        return jsonify({"error": str(err)}), 500

# PUT (Actualizar)
@profesionales_bp.route('/profesionales/<int:id>', methods=['PUT'])
@token_required
def update_profesional(id):
    datos = request.get_json()
    
    campos_requeridos = ['nombre', 'activo', 'negocio_id']
    if not datos or not all(campo in datos for campo in campos_requeridos):
        return jsonify({"error": f"Faltan datos. Se requiere: {campos_requeridos}"}), 400

    try:
        # Verificamos existencia primero
        profesional_existente = Profesional.obtener_por_id(id)
        if not profesional_existente:
            return jsonify({"error": "Profesional no encontrado"}), 404

        # Actualizamos
        profesional_actualizado = Profesional.actualizar_desde_datos(id, datos)
        
        return jsonify(profesional_actualizado.to_json()), 200
        
    except Exception as err:
        return jsonify({"error": str(err)}), 500

# DELETE
@profesionales_bp.route('/profesionales/<int:id>', methods=['DELETE'])
@token_required
def delete_profesional(id):
    try:
        filas_afectadas = Profesional.eliminar(id)

        if filas_afectadas == 0:
            return jsonify({"error": "Profesional no encontrado"}), 404
        else:
            return jsonify({"message": "Profesional eliminado correctamente"}), 200
            
    except ValueError as e:
        # Capturamos error de FK (Turnos/Disponibilidades asociados)
        # Recordar al equipo que aca existe quizas un problema en el diseño de la base. Poco tiempo para modificaciones.
        return jsonify({"error": str(e)}), 409
        
    except Exception as err:
        return jsonify({"error": str(err)}), 500