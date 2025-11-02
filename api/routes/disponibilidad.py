# api/routes/disponibilidad.py
from flask import Blueprint, jsonify, request
from api.models.disponibilidad import Disponibilidad # Importamos el nuevo modelo
from api.db.db import mysql # Importamos el objeto mysql

# Creamos el "plano" (blueprint)
disponibilidad_bp = Blueprint('disponibilidad', __name__)

# GET de horarios por Profesional
@disponibilidad_bp.route('/profesionales/<int:id_profesional>/disponibilidad', methods=['GET'])
def get_disponibilidad_profesional(id_profesional):
    cursor = None
    try:
        cursor = mysql.connection.cursor() 
        
        # Verificamos si el profesional existe
        cursor.execute("SELECT id FROM Profesionales WHERE id = %s", (id_profesional,))
        if not cursor.fetchone():
            return jsonify({"error": "Profesional no encontrado"}), 404
        
        # Si existe, buscamos su disponibilidad
        sql = "SELECT * FROM Disponibilidad WHERE profesional_id = %s"
        cursor.execute(sql, (id_profesional,))
        
        filas = cursor.fetchall()
        
        lista_disponibilidad = []
        for fila in filas:
            objDisponibilidad = Disponibilidad(fila) 
            lista_disponibilidad.append(objDisponibilidad.to_json()) 
            
        return jsonify(lista_disponibilidad)
    except Exception as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()

# POST (Crear horario para un Profesional)
@disponibilidad_bp.route('/profesionales/<int:id_profesional>/disponibilidad', methods=['POST'])
def create_disponibilidad_profesional(id_profesional):
    datos = request.get_json()
    
    campos_requeridos = ['dia_semana', 'hora_inicio', 'hora_fin']
    if not datos or not all(campo in datos for campo in campos_requeridos):
        return jsonify({"error": f"Faltan datos. Se requiere: {campos_requeridos}"}), 400

    dia_semana = datos['dia_semana']
    hora_inicio = datos['hora_inicio']
    hora_fin = datos['hora_fin']
    
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        
        # Verificamos que el profesional exista
        cursor.execute("SELECT id FROM Profesionales WHERE id = %s", (id_profesional,))
        if not cursor.fetchone():
            return jsonify({"error": "Profesional no encontrado"}), 404

        # Insertamos el nuevo horario
        sql = "INSERT INTO Disponibilidad (profesional_id, dia_semana, hora_inicio, hora_fin) VALUES (%s, %s, %s, %s)"
        valores = (id_profesional, dia_semana, hora_inicio, hora_fin)
        
        cursor.execute(sql, valores)
        mysql.connection.commit()
        
        nuevo_id = cursor.lastrowid
        nuevo_horario = {
            "id": nuevo_id, "profesional_id": id_profesional, "dia_semana": dia_semana,
            "hora_inicio": hora_inicio, "hora_fin": hora_fin
        }
        
        return jsonify(nuevo_horario), 201
    except Exception as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()

# PUT (Actualizar un horario específico)
@disponibilidad_bp.route('/disponibilidad/<int:id>', methods=['PUT'])
def update_disponibilidad(id):
    cursor = None
    try:
        datos = request.get_json()
        campos_requeridos = ['dia_semana', 'hora_inicio', 'hora_fin', 'profesional_id']
        if not datos or not all(campo in datos for campo in campos_requeridos):
            return jsonify({"error": f"Faltan datos. Se requiere: {campos_requeridos}"}), 400

        dia_semana = datos['dia_semana']
        hora_inicio = datos['hora_inicio']
        hora_fin = datos['hora_fin']
        profesional_id = datos['profesional_id']

        cursor = mysql.connection.cursor()
        
        sql = "UPDATE Disponibilidad SET profesional_id = %s, dia_semana = %s, hora_inicio = %s, hora_fin = %s WHERE id = %s"
        valores = (profesional_id, dia_semana, hora_inicio, hora_fin, id)
        
        cursor.execute(sql, valores)
        mysql.connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Horario de disponibilidad no encontrado"}), 404
        else:
            horario_actualizado = {
                "id": id, "profesional_id": profesional_id, "dia_semana": dia_semana,
                "hora_inicio": hora_inicio, "hora_fin": hora_fin
            }
            return jsonify(horario_actualizado), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()

# DELETE (Borrar un horario específico)
@disponibilidad_bp.route('/disponibilidad/<int:id>', methods=['DELETE'])
def delete_disponibilidad(id):
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        
        sql = "DELETE FROM Disponibilidad WHERE id = %s"
        cursor.execute(sql, (id,))
        mysql.connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Horario de disponibilidad no encontrado"}), 404
        else:
            return jsonify({"message": "Horario de disponibilidad eliminado correctamente"}), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()