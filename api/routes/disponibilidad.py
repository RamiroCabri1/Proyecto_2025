from flask import Blueprint, jsonify, request
from api.utils import token_required, validar_campos
from api.models.disponibilidad import Disponibilidad
from api.models.profesional import Profesional 

disponibilidad_bp = Blueprint('disponibilidad', __name__)

# GET Horarios (publico para que el cliente vea cuándo reservar)
@disponibilidad_bp.route('/profesionales/<int:id_profesional>/disponibilidad', methods=['GET'])

def get_disponibilidad_profesional(id_profesional):
    try:
        # Verificamos si el profesional existe (usando su modelo)
        # (Si no tenés Profesional importado o falla, podés comentar estas 3 lineas)
        prof = Profesional.obtener_por_id(id_profesional)
        if not prof:
            return jsonify({"error": "Profesional no encontrado"}), 404

        # Buscamos horarios
        lista_objetos = Disponibilidad.obtener_por_profesional(id_profesional)
        lista_json = [d.to_json() for d in lista_objetos]
        
        return jsonify(lista_json), 200
    
    except Exception as err:
        return jsonify({"error": str(err)}), 500

# POST (Crear Horario) - (Solo Admin)
@disponibilidad_bp.route('/profesionales/<int:id_profesional>/disponibilidad', methods=['POST'])
@token_required
def create_disponibilidad(id_profesional):
    datos = request.get_json()
    

    if not validar_campos(datos, ['dia_semana', 'hora_inicio', 'hora_fin']):
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    try:
        # Validamos profesional
        if not Profesional.obtener_por_id(id_profesional):
             return jsonify({"error": "Profesional no encontrado"}), 404

        nueva = Disponibilidad.crear(
            profesional_id=id_profesional,
            dia_semana=datos['dia_semana'],
            hora_inicio=datos['hora_inicio'],
            hora_fin=datos['hora_fin']
        )
        return jsonify(nueva.to_json()), 201
    except Exception as err:
        return jsonify({"error": str(err)}), 500

# PUT (Actualizar) - PRIVADO
@disponibilidad_bp.route('/disponibilidad/<int:id>', methods=['PUT'])
@token_required
def update_disponibilidad(id):
    datos = request.get_json()
   
    if not validar_campos(datos, ['dia_semana', 'hora_inicio', 'hora_fin', 'profesional_id']):
        return jsonify({"error": "Faltan datos"}), 400

    try:
        actualizada = Disponibilidad.actualizar(
            id, 
            datos['profesional_id'], 
            datos['dia_semana'], 
            datos['hora_inicio'], 
            datos['hora_fin']
        )
        if actualizada:
            return jsonify(actualizada.to_json()), 200
        return jsonify({"error": "Horario no encontrado"}), 404
    except Exception as err:
        return jsonify({"error": str(err)}), 500

# DELETE - PRIVADO

@disponibilidad_bp.route('/disponibilidad/<int:id>', methods=['DELETE'])
@token_required
def delete_disponibilidad(id):
    try:
        filas = Disponibilidad.eliminar(id)
        if filas > 0:
            return jsonify({"message": "Horario eliminado"}), 200
        return jsonify({"error": "Horario no encontrado"}), 404
    except Exception as err:
        return jsonify({"error": str(err)}), 500