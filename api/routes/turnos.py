from api.utils import token_required
from flask import Blueprint, jsonify, request
from api.models.turno import Turno 
from api.db.db import mysql 
from datetime import datetime


turnos_bp = Blueprint('turnos', __name__)

# POST (Crear Turno)
@turnos_bp.route('/turnos', methods=['POST'])
#@token_required
def create_turno():
    datos = request.get_json()
    
    campos_requeridos = ['fecha_hora', 'cliente_id', 'profesional_id', 'servicio_id', 'negocio_id']
    if not datos or not all(campo in datos for campo in campos_requeridos):
        return jsonify({"error": f"Faltan datos. Se requiere: {campos_requeridos}"}), 400

    try:
        
        nuevo_turno_obj = Turno.crear_desde_datos(datos)
        
        # Respuesta exitosa: 201 Created
        
        return jsonify(nuevo_turno_obj.to_json()), 201

    except ValueError as e:
        # Captura errores de validación de negocio (disponibilidad, formato de fecha, etc.)
        return jsonify({"error": str(e)}), 409 # 409 Conflict

    except Exception as err:
        # Captura errores de servidor o de base de datos
        return jsonify({"erroru": str(err)})

# GET Todos
@turnos_bp.route('/turnos', methods=['GET'])
@token_required
def get_turnos():
    try:
        
        lista_turnos = Turno.get_all() 
        if not lista_turnos:
            # Exito, pero sin turnos
            return jsonify({"message": "No existen turnos asignados"}), 200 
        
        # Exitos y devuelve turnos
        return jsonify(lista_turnos), 200
        
    except Exception as err:
       
        return jsonify({"error": "Error interno al obtener los turnos."}), 500
    
# GET por ID (Para el comprobante)
@turnos_bp.route('/turnos/<int:id>', methods=['GET'])
# @token_required
def get_turno_por_id(id):
    try:
        turno_obj = Turno.obtener_por_id(id) 
        
        if turno_obj:
            return jsonify(turno_obj.to_json()), 200
        else:
            return jsonify({"error": "Turno no encontrado"}), 404

    except Exception as err:
        return jsonify({"error": str(err)}), 500
    
# DELETE
@turnos_bp.route('/turnos/<int:id>', methods=['DELETE'])
@token_required
def delete_turno(id:int):
    try:
       
        filas_afectadas = Turno.delete(id)
        
        # Esta logica si la dejo aqui
        if filas_afectadas == 0:
            
            return jsonify({"error": f"Turno ID {id} no encontrado"}), 404
        else:
            #  Eliminación exitosa
            return jsonify({"message": f"Turno ID {id} eliminado correctamente"}), 200
            
    except Exception as err:
        # 500 Server Error
        return jsonify({"error": "Error interno del servidor al intentar eliminar el turno."}), 500
    
