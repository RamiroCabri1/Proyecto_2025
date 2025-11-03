from api.utils import token_required
from flask import Blueprint, jsonify, request
from api.models.profesional import Profesional 
from api.db.db import mysql


profesionales_bp = Blueprint('profesionales', __name__)

# GET Todos
@profesionales_bp.route('/profesionales', methods=['GET'])
@token_required
def get_profesionales():
    cursor = None
    try:
        cursor = mysql.connection.cursor() 
        cursor.execute("SELECT * FROM Profesionales") 
        filas = cursor.fetchall()
        
        lista_profesionales = []
        for fila in filas:
            objProfesional = Profesional(fila) 
            lista_profesionales.append(objProfesional.to_json()) 
            
        return jsonify(lista_profesionales)
    except Exception as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()

# GET por ID
@profesionales_bp.route('/profesionales/<int:id>', methods=['GET'])
@token_required
def get_profesional_por_id(id):
    cursor = None
    try:
        cursor = mysql.connection.cursor() 
        sql = "SELECT * FROM Profesionales WHERE id = %s"
        cursor.execute(sql, (id,))
        fila = cursor.fetchone() 
        
        if fila:
            objProfesional = Profesional(fila)
            return jsonify(objProfesional.to_json())
        else:
            return jsonify({"error": "Profesional no encontrado"}), 404
    except Exception as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()

# POST (Crear)
@profesionales_bp.route('/profesionales', methods=['POST'])
@token_required
def create_profesional():
    datos = request.get_json()
    campos_requeridos = ['nombre', 'activo', 'negocio_id']
    if not datos or not all(campo in datos for campo in campos_requeridos):
        return jsonify({"error": f"Faltan datos. Se requiere: {campos_requeridos}"}), 400

    nombre = datos['nombre']
    activo = datos['activo']
    negocio_id = datos['negocio_id']

    cursor = None
    try:
        cursor = mysql.connection.cursor()
        sql = "INSERT INTO Profesionales (nombre, activo, negocio_id) VALUES (%s, %s, %s)"
        valores = (nombre, activo, negocio_id)
        
        cursor.execute(sql, valores)
        mysql.connection.commit() 
        
        nuevo_id = cursor.lastrowid
        nuevo_profesional = {
            "id": nuevo_id, "nombre": nombre, "activo": activo, "negocio_id": negocio_id
        }
        return jsonify(nuevo_profesional), 201
    except Exception as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()

# PUT (Actualizar)
@profesionales_bp.route('/profesionales/<int:id>', methods=['PUT'])
@token_required
def update_profesional(id):
    cursor = None
    try:
        datos = request.get_json()
        campos_requeridos = ['nombre', 'activo', 'negocio_id']
        if not datos or not all(campo in datos for campo in campos_requeridos):
            return jsonify({"error": f"Faltan datos. Se requiere: {campos_requeridos}"}), 400

        nombre = datos['nombre']
        activo = datos['activo']
        negocio_id = datos['negocio_id']

        cursor = mysql.connection.cursor()
        sql = "UPDATE Profesionales SET nombre = %s, activo = %s, negocio_id = %s WHERE id = %s"
        valores = (nombre, activo, negocio_id, id)
        
        cursor.execute(sql, valores)
        mysql.connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Profesional no encontrado"}), 404
        else:
            profesional_actualizado = {
                "id": id, "nombre": nombre, "activo": activo, "negocio_id": negocio_id
            }
            return jsonify(profesional_actualizado), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()

# DELETE
@profesionales_bp.route('/profesionales/<int:id>', methods=['DELETE'])
@token_required
def delete_profesional(id):
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        sql = "DELETE FROM Profesionales WHERE id = %s"
        cursor.execute(sql, (id,))
        mysql.connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Profesional no encontrado"}), 404
        else:
            return jsonify({"message": "Profesional eliminado correctamente"}), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()