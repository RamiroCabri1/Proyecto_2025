
from flask import Blueprint, jsonify, request
from api.models.negocio import Negocio 
from api.db.db import mysql

negocios_bp = Blueprint('negocios', __name__)

# GET Todos
@negocios_bp.route('/negocios', methods=['GET'])
def get_negocios():
    cursor = None
    try:

        cursor = mysql.connection.cursor() 
        
        cursor.execute("SELECT id, nombre, direccion, telefono FROM Negocios") 
        filas = cursor.fetchall()
        

        lista_negocios = []
        for fila in filas:
            objNegocio = Negocio(fila) 
            lista_negocios.append(objNegocio.to_json()) 
            
        return jsonify(lista_negocios)

    except Exception as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()

# GET por ID
@negocios_bp.route('/negocios/<int:id>', methods=['GET'])
def get_negocio_por_id(id):
    cursor = None
    try:
        cursor = mysql.connection.cursor() 
        
        sql = "SELECT id, nombre, direccion, telefono FROM Negocios WHERE id = %s"
        cursor.execute(sql, (id,))
        
        fila = cursor.fetchone() 
        
        if fila:
            objNegocio = Negocio(fila) # Usamos el modelo
            return jsonify(objNegocio.to_json())
        else:
            return jsonify({"error": "Negocio no encontrado"}), 404

    except Exception as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()

# POST (Crear)
@negocios_bp.route('/negocios', methods=['POST'])
def create_negocio():
    datos = request.get_json()
    if not datos or 'nombre' not in datos or 'direccion' not in datos or 'telefono' not in datos:
        return jsonify({"error": "Faltan datos (nombre, direccion, telefono)"}), 400

    nombre = datos['nombre']
    direccion = datos['direccion']
    telefono = datos['telefono']

    cursor = None
    try:
        cursor = mysql.connection.cursor()
        sql = "INSERT INTO Negocios (nombre, direccion, telefono) VALUES (%s, %s, %s)"
        valores = (nombre, direccion, telefono)
        
        cursor.execute(sql, valores)
        # El commit se hace sobre la conexión
        mysql.connection.commit() 
        
        nuevo_id = cursor.lastrowid
        
        nuevo_negocio = {
            "id": nuevo_id, "nombre": nombre, "direccion": direccion, "telefono": telefono
        }
        return jsonify(nuevo_negocio), 201

    except Exception as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()

# PUT (Actualizar)
@negocios_bp.route('/negocios/<int:id>', methods=['PUT'])
def update_negocio(id):
    cursor = None
    try:
        datos = request.get_json()
        if not datos or 'nombre' not in datos or 'direccion' not in datos or 'telefono' not in datos:
            return jsonify({"error": "Faltan datos (nombre, direccion, telefono)"}), 400

        nombre = datos['nombre']
        direccion = datos['direccion']
        telefono = datos['telefono']

        cursor = mysql.connection.cursor()
        
        sql = "UPDATE Negocios SET nombre = %s, direccion = %s, telefono = %s WHERE id = %s"
        valores = (nombre, direccion, telefono, id)
        
        cursor.execute(sql, valores)
        mysql.connection.commit() # Guardamos

        if cursor.rowcount == 0:
            return jsonify({"error": "Negocio no encontrado"}), 404
        else:
            negocio_actualizado = {
                "id": id, "nombre": nombre, "direccion": direccion, "telefono": telefono
            }
            return jsonify(negocio_actualizado), 200

    except Exception as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()


@negocios_bp.route('/negocios/<int:id>', methods=['DELETE'])
def delete_negocio(id):
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        
        sql = "DELETE FROM Negocios WHERE id = %s"
        cursor.execute(sql, (id,))
        mysql.connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Negocio no encontrado"}), 404
        else:
            return jsonify({"message": "Negocio eliminado correctamente"}), 200

    except Exception as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()