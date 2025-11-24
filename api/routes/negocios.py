from api.utils import token_required
from flask import Blueprint, jsonify, request
from api.models.negocio import Negocio 

negocios_bp = Blueprint('negocios', __name__)

# GET Todos
@negocios_bp.route('/negocios', methods=['GET'])
@token_required
def get_negocios():
    try:
        lista_objetos = Negocio.obtener_todos()
        
        # Convertimos a JSON
        lista_json = [n.to_json() for n in lista_objetos]
        
        return jsonify(lista_json), 200

    except Exception as err:
        return jsonify({"error": str(err)}), 500

# GET por ID
@negocios_bp.route('/negocios/<int:id>', methods=['GET'])
@token_required
def get_negocio_por_id(id):
    try:
        negocio = Negocio.obtener_por_id(id)
        
        if negocio:
            return jsonify(negocio.to_json()), 200
        else:
            return jsonify({"error": "Negocio no encontrado"}), 404

    except Exception as err:
        return jsonify({"error": str(err)}), 500

# POST (Crear)
@negocios_bp.route('/negocios', methods=['POST'])
#@token_required
def create_negocio():
    datos = request.get_json()
    
    campos_requeridos = ['nombre', 'direccion', 'telefono']
    if not datos or not all(campo in datos for campo in campos_requeridos):
        return jsonify({"error": f"Faltan datos. Se requiere: {campos_requeridos}"}), 400

    try:
        # Fachada
        nuevo_negocio = Negocio.crear_desde_datos(datos)
        
        return jsonify(nuevo_negocio.to_json()), 201

    except Exception as err:
        return jsonify({"error": str(err)}), 500

# PUT (Actualizar)
@negocios_bp.route('/negocios/<int:id>', methods=['PUT'])
@token_required
def update_negocio(id):
    datos = request.get_json()
    
    campos_requeridos = ['nombre', 'direccion', 'telefono']
    if not datos or not all(campo in datos for campo in campos_requeridos):
        return jsonify({"error": f"Faltan datos. Se requiere: {campos_requeridos}"}), 400

    try:
        # Verificar existencia
        negocio_existente = Negocio.obtener_por_id(id)
        if not negocio_existente:
            return jsonify({"error": "Negocio no encontrado"}), 404
            
        # Actualizar
        negocio_actualizado = Negocio.actualizar_desde_datos(id, datos)
        
        return jsonify(negocio_actualizado.to_json()), 200

    except Exception as err:
        return jsonify({"error": str(err)}), 500


@negocios_bp.route('/negocios/<int:id>', methods=['DELETE'])
@token_required
def delete_negocio(id):
    try:
        filas_afectadas = Negocio.eliminar(id)

        if filas_afectadas == 0:
            return jsonify({"error": "Negocio no encontrado"}), 404
        else:
            return jsonify({"message": "Negocio eliminado correctamente"}), 200

    except ValueError as e:
        # Captura de error FK (1451)
        # Hago incapie en la idea de un soft delete. Ya que no se podra borrar ningun negocio que tenga 
        # asignado un profesional/turno.
        return jsonify({"error": str(e)}), 409

    except Exception as err:
        return jsonify({"error": str(err)}), 500