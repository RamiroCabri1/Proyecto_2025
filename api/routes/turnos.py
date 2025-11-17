from api.utils import token_required
from flask import Blueprint, jsonify, request
from api.models.turno import Turno 
from api.db.db import mysql 
from datetime import datetime


turnos_bp = Blueprint('turnos', __name__)

# POST (Crear Turno)
@turnos_bp.route('/turnos', methods=['POST'])
@token_required
def create_turno():
    datos = request.get_json()
    
    campos_requeridos = ['fecha_hora', 'cliente_id', 'profesional_id', 'servicio_id', 'negocio_id']
    if not datos or not all(campo in datos for campo in campos_requeridos):
        return jsonify({"error": f"Faltan datos. Se requiere: {campos_requeridos}"}), 400

    try:
        # LLAMADA SIMPLE AL MODELO: Toda la complejidad está en el método de clase
        nuevo_turno = Turno.create_and_validate(datos) 
        
        # Respuesta exitosa: 201 Created
        return jsonify(nuevo_turno), 201

    except ValueError as e:
        # Captura errores de validación de negocio (disponibilidad, formato de fecha, etc.)
        return jsonify({"error": str(e)}), 409 # 409 Conflict

    except Exception as err:
        # Captura errores de servidor o de base de datos
        return jsonify({"error": str(err)})

# GET Todos
@turnos_bp.route('/turnos', methods=['GET'])
@token_required
def get_turnos():
    cursor = None
    try:
        cursor = mysql.connection.cursor() 
        cursor.execute("SELECT * FROM Turnos") 
        filas = cursor.fetchall()
        
        lista_turnos = []
        for fila in filas:
            objTurno = Turno(fila) 
            lista_turnos.append(objTurno.to_json()) 
        
        if len(lista_turnos) < 1:
            return jsonify({"message":"No existen turnos asignados"})
        
        return jsonify(lista_turnos)
    except Exception as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()

# DELETE
@turnos_bp.route('/turnos/<int:id>', methods=['DELETE'])
@token_required
def delete_turno(id):
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        sql = "DELETE FROM Turnos WHERE id = %s"
        cursor.execute(sql, (id,))
        mysql.connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Turno no encontrado"}), 404
        else:
            return jsonify({"message": "Turno eliminado correctamente"}), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()