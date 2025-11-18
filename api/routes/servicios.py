from api.utils import token_required
from flask import Blueprint, jsonify, request
from api.models.servicio import Servicio 
from api.db.db import mysql 



servicios_bp = Blueprint('servicios', __name__)

# GET Todos
@servicios_bp.route('/servicios', methods=['GET'])
@token_required
def get_servicios():
    cursor = None
    try:
        cursor = mysql.connection.cursor() 
        cursor.execute("SELECT * FROM Servicios") 
        filas = cursor.fetchall()
        
        lista_servicios = []
        for fila in filas:
            objServicio = Servicio(fila) 
            lista_servicios.append(objServicio.to_json()) 
            
        # aclaro en caso que no exista servicios disponibles    
        if len(lista_servicios) <= 0:
            return jsonify({"message":"No existen servicios asociados en este negocio"})
            
        return jsonify(lista_servicios)
    except Exception as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()

# GET por ID
@servicios_bp.route('/servicios/<int:id>', methods=['GET'])
@token_required
def get_servicio_por_id(id):
    cursor = None
    try:
        cursor = mysql.connection.cursor() 
        sql = "SELECT * FROM Servicios WHERE id = %s"
        cursor.execute(sql, (id,))
        fila = cursor.fetchone() 
        
        if fila:
            objServicio = Servicio(fila)
            return jsonify(objServicio.to_json())
        else:
            return jsonify({"error": "Servicio no encontrado"}), 404
    except Exception as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()

# POST (Crear)
@servicios_bp.route('/servicios', methods=['POST'])
@token_required
def create_servicio():
    datos = request.get_json()
    campos_requeridos = ['nombre', 'descripcion', 'duracion_turno_min', 'negocio_id']
    if not datos or not all(campo in datos for campo in campos_requeridos):
        return jsonify({"error": f"Faltan datos. Se requiere: {campos_requeridos}"}), 400

    nombre = datos['nombre']
    descripcion = datos['descripcion']
    duracion = datos['duracion_turno_min']
    negocio_id = datos['negocio_id']

    cursor = None
    try:
        cursor = mysql.connection.cursor()
        sql = "INSERT INTO Servicios (nombre, descripcion, duracion_turno_min, negocio_id) VALUES (%s, %s, %s, %s)"
        valores = (nombre, descripcion, duracion, negocio_id)
        
        cursor.execute(sql, valores)
        mysql.connection.commit() 
        
        nuevo_id = cursor.lastrowid
        nuevo_servicio = {
            "id": nuevo_id, "nombre": nombre, "descripcion": descripcion,
            "duracion_turno_min": duracion, "negocio_id": negocio_id
        }
        return jsonify(nuevo_servicio), 201
    except Exception as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()

# PUT (Actualizar)
@servicios_bp.route('/servicios/<int:id>', methods=['PUT'])
@token_required
def update_servicio(id):
    cursor = None
    try:
        datos = request.get_json()
        campos_requeridos = ['nombre', 'descripcion', 'duracion_turno_min', 'negocio_id']
        if not datos or not all(campo in datos for campo in campos_requeridos):
            return jsonify({"error": f"Faltan datos. Se requiere: {campos_requeridos}"}), 400

        nombre = datos['nombre']
        descripcion = datos['descripcion']
        duracion = datos['duracion_turno_min']
        negocio_id = datos['negocio_id']

        cursor = mysql.connection.cursor()
        sql = "UPDATE Servicios SET nombre = %s, descripcion = %s, duracion_turno_min = %s, negocio_id = %s WHERE id = %s"
        valores = (nombre, descripcion, duracion, negocio_id, id)
        
        cursor.execute(sql, valores)
        mysql.connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Servicio no encontrado"}), 404
        else:
            servicio_actualizado = {
                "id": id, "nombre": nombre, "descripcion": descripcion,
                "duracion_turno_min": duracion, "negocio_id": negocio_id
            }
            return jsonify(servicio_actualizado), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()

# DELETE
@servicios_bp.route('/servicios/<int:id>', methods=['DELETE'])
@token_required
def delete_servicio(id):
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        sql = "DELETE FROM Servicios WHERE id = %s"
        cursor.execute(sql, (id,))
        mysql.connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Servicio no encontrado"}), 404
        else:
            return jsonify({"message": "Servicio eliminado correctamente"}), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()