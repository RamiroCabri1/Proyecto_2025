
from flask import Blueprint, jsonify, request
from api.models.turno import Turno 
from api.db.db import mysql 
from datetime import datetime


turnos_bp = Blueprint('turnos', __name__)

# POST (Crear Turno)
@turnos_bp.route('/turnos', methods=['POST'])
def create_turno():
    datos = request.get_json()
    
    campos_requeridos = ['fecha_hora', 'cliente_id', 'profesional_id', 'servicio_id', 'negocio_id']
    if not datos or not all(campo in datos for campo in campos_requeridos):
        return jsonify({"error": f"Faltan datos. Se requiere: {campos_requeridos}"}), 400

    try:
        fecha_hora_obj = datetime.strptime(datos['fecha_hora'], '%Y-%m-%d %H:%M:%S')
        dia_semana = fecha_hora_obj.weekday() + 1
        hora_turno = fecha_hora_obj.time().strftime('%H:%M:%S')
    except ValueError:
        return jsonify({"error": "Formato de fecha_hora incorrecto. Usar YYYY-MM-DD HH:MM:SS"}), 400

    cliente_id = datos['cliente_id']
    profesional_id = datos['profesional_id']
    servicio_id = datos['servicio_id']
    negocio_id = datos['negocio_id']

    cursor = None
    try:
        cursor = mysql.connection.cursor() # Usamos dictionary=True para leer fácil

        # Validación 1: Disponibilidad
        sql_disponibilidad = """
            SELECT * FROM Disponibilidad 
            WHERE profesional_id = %s AND dia_semana = %s 
            AND TIME(%s) BETWEEN hora_inicio AND hora_fin
        """
        cursor.execute(sql_disponibilidad, (profesional_id, dia_semana, hora_turno))
        disponibilidad_encontrada = cursor.fetchall() 
        
        if not disponibilidad_encontrada:
            return jsonify({"error": "El profesional no se encuentra disponible en ese día u horario."}), 409

        # Validación 2: Turno Ocupado
        sql_ocupado = "SELECT id FROM Turnos WHERE profesional_id = %s AND fecha_hora = %s"
        cursor.execute(sql_ocupado, (profesional_id, datos['fecha_hora']))
        turno_encontrado = cursor.fetchall()
        
        if turno_encontrado:
            return jsonify({"error": "El turno ya se encuentra ocupado."}), 409
            
        # En este punto creamos el turno
        
        # Cerramos el cursor dictionary=True y abrimos uno normal para INSERT
        cursor.close()
        cursor = mysql.connection.cursor()
        
        sql_insert = """
            INSERT INTO Turnos (fecha_hora, estado, cliente_id, profesional_id, servicio_id, negocio_id) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        valores = (datos['fecha_hora'], 'Confirmado', cliente_id, profesional_id, servicio_id, negocio_id)
        
        cursor.execute(sql_insert, valores)
        mysql.connection.commit()
        
        nuevo_id = cursor.lastrowid
        
        nuevo_turno = {
            "id": nuevo_id, "fecha_hora": datos['fecha_hora'], "estado": "Confirmado",
            "cliente_id": cliente_id, "profesional_id": profesional_id,
            "servicio_id": servicio_id, "negocio_id": negocio_id
        }
        return jsonify(nuevo_turno), 201

    except Exception as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()

# GET Todos
@turnos_bp.route('/turnos', methods=['GET'])
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
            
        return jsonify(lista_turnos)
    except Exception as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()

# DELETE
@turnos_bp.route('/turnos/<int:id>', methods=['DELETE'])
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