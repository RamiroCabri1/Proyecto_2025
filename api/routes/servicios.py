from api.utils import token_required
from flask import Blueprint, jsonify, request
from api.models.servicio import Servicio 

servicios_bp = Blueprint('servicios', __name__)

# GET Todos
@servicios_bp.route('/servicios', methods=['GET'])
@token_required
def get_servicios():
    try:
        # 1. Obtener lista de objetos
        lista_objetos = Servicio.obtener_todos()
        
        if not lista_objetos:
            return jsonify({"message": "No existen servicios asociados en este negocio"}), 200
            
        # 2. Convertir a JSON
        lista_json = [s.to_json() for s in lista_objetos]
        
        return jsonify(lista_json), 200
        
    except Exception as err:
        return jsonify({"error": str(err)}), 500

# GET por ID
@servicios_bp.route('/servicios/<int:id>', methods=['GET'])
@token_required
def get_servicio_por_id(id):
    try:
        # 1. Obtener objeto
        servicio = Servicio.obtener_por_id(id)
        
        if servicio:
            return jsonify(servicio.to_json()), 200
        else:
            return jsonify({"error": "Servicio no encontrado"}), 404
            
    except Exception as err:
        return jsonify({"error": str(err)}), 500

# POST (Crear)
@servicios_bp.route('/servicios', methods=['POST'])
@token_required
def create_servicio():
    datos = request.get_json()
    
    # Validación HTTP
    campos_requeridos = ['nombre', 'descripcion', 'duracion_turno_min', 'negocio_id']
    if not datos or not all(campo in datos for campo in campos_requeridos):
        return jsonify({"error": f"Faltan datos. Se requiere: {campos_requeridos}"}), 400

    try:
        # FACHADA: Pasamos el diccionario directo
        nuevo_servicio = Servicio.crear_desde_datos(datos)
        
        return jsonify(nuevo_servicio.to_json()), 201
        
    except Exception as err:
        return jsonify({"error": str(err)}), 500

# PUT (Actualizar)
@servicios_bp.route('/servicios/<int:id>', methods=['PUT'])
@token_required
def update_servicio(id):
    datos = request.get_json()
    
    campos_requeridos = ['nombre', 'descripcion', 'duracion_turno_min', 'negocio_id']
    if not datos or not all(campo in datos for campo in campos_requeridos):
        return jsonify({"error": f"Faltan datos. Se requiere: {campos_requeridos}"}), 400

    try:
        # FACHADA DE ACTUALIZACIÓN
        # Primero verificamos si existe (opcional, pero recomendado)
        servicio_existente = Servicio.obtener_por_id(id)
        if not servicio_existente:
            return jsonify({"error": "Servicio no encontrado"}), 404

        # Actualizamos
        servicio_actualizado = Servicio.actualizar_desde_datos(id, datos)
        
        return jsonify(servicio_actualizado.to_json()), 200
        
    except Exception as err:
        return jsonify({"error": str(err)}), 500

# DELETE
@servicios_bp.route('/servicios/<int:id>', methods=['DELETE'])
@token_required
def delete_servicio(id):
    try:
        filas_afectadas = Servicio.eliminar(id)

        if filas_afectadas == 0:
            return jsonify({"error": "Servicio no encontrado"}), 404
        else:
            return jsonify({"message": "Servicio eliminado correctamente"}), 200
            
    except ValueError as e:
        # CAPTURAMOS EL ERROR DE NEGOCIO (FK CONSTRAINT)
        return jsonify({"error": str(e)}), 409

    except Exception as err:
        # Errores inesperados
        return jsonify({"error": str(err)}), 500