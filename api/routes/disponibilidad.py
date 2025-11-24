from flask import Blueprint, jsonify, request
from api.utils import token_required, validar_campos
from api.models.disponibilidad import Disponibilidad
from api.models.profesional import Profesional 

disponibilidad_bp = Blueprint('disponibilidad', __name__)

# GET de horarios por Profesional
@disponibilidad_bp.route('/profesionales/<int:id_profesional>/disponibilidad', methods=['GET'])

def get_disponibilidad_profesional(id_profesional):
    try:
        # Verificar si el profesional existe
        profesional = Profesional.obtener_por_id(id_profesional)
        if not profesional:
            return jsonify({"error": "Profesional no encontrado"}), 404
        
        # Buscamos disponibilidad
        lista_objetos = Disponibilidad.obtener_por_profesional_id(id_profesional)
    
        
        # Convertimos a JSON
        lista_json = [d.to_json() for d in lista_objetos]            
        
        return jsonify(lista_json), 200

    except Exception as err:
        return jsonify({"error": str(err)}), 500

# POST (Crear horario para un Profesional)
@disponibilidad_bp.route('/profesionales/<int:id_profesional>/disponibilidad', methods=['POST'])
@token_required
def create_disponibilidad_profesional(id_profesional):
    datos = request.get_json()
    
    # validar_campos devuelve True si está todo bien
    if not validar_campos(datos, ['dia_semana', 'hora_inicio', 'hora_fin']):
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    try:
        # Verificamos profesional
        profesional = Profesional.obtener_por_id(id_profesional)
        if not profesional:
            return jsonify({"error": "Profesional no encontrado"}), 404

        # Inyectamos el ID
        datos['profesional_id'] = id_profesional
        
        # Usamos la Fachada del modelo
        nueva_disp = Disponibilidad.crear_desde_datos(datos)
        
        return jsonify(nueva_disp.to_json()), 201
        
    except Exception as err:
        return jsonify({"error": str(err)}), 500

# PUT (Actualizar un horario específico)
@disponibilidad_bp.route('/disponibilidad/<int:id>', methods=['PUT'])
@token_required
def update_disponibilidad(id):
    datos = request.get_json()
    
    # validación
    if not validar_campos(datos, ['dia_semana', 'hora_inicio', 'hora_fin', 'profesional_id']):
        return jsonify({"error": "Faltan datos obligatorios"}), 400
    
    try:
        # Verificar existencia
        disp_existente = Disponibilidad.obtener_por_id(id)
        if not disp_existente:
            return jsonify({"error": "Horario de disponibilidad no encontrado"}), 404

        # Actualizar
        disp_actualizada = Disponibilidad.actualizar_desde_datos(id, datos)
        
        return jsonify(disp_actualizada.to_json()), 200
        
    except Exception as err:
        return jsonify({"error": str(err)}), 500

# DELETE (Borrar un horario específico)
@disponibilidad_bp.route('/disponibilidad/<int:id>', methods=['DELETE'])
@token_required
def delete_disponibilidad(id):
    try:
        filas_afectadas = Disponibilidad.eliminar(id)

        if filas_afectadas == 0:
            return jsonify({"error": "Horario de disponibilidad no encontrado"}), 404
        else:
            return jsonify({"message": "Horario de disponibilidad eliminado correctamente"}), 200
            
    except Exception as err:
        return jsonify({"error": str(err)}), 500