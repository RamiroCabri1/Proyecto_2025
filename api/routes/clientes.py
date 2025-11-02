# api/routes/clientes.py
from flask import Blueprint, jsonify, request
from api.models.cliente import Cliente # Importamos el nuevo modelo
from api.db.db import mysql # Importamos el objeto mysql

# Creamos el "plano" (blueprint) de clientes
clientes_bp = Blueprint('clientes', __name__)

# GET Todos
@clientes_bp.route('/clientes', methods=['GET'])
def get_clientes():
    cursor = None
    try:
        cursor = mysql.connection.cursor() 
        cursor.execute("SELECT * FROM Clientes") 
        filas = cursor.fetchall()
        
        lista_clientes = []
        for fila in filas:
            objCliente = Cliente(fila) 
            lista_clientes.append(objCliente.to_json()) 
            
        return jsonify(lista_clientes)
    except Exception as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()

# GET por ID
@clientes_bp.route('/clientes/<int:id>', methods=['GET'])
def get_cliente_por_id(id):
    cursor = None
    try:
        cursor = mysql.connection.cursor() 
        sql = "SELECT * FROM Clientes WHERE id = %s"
        cursor.execute(sql, (id,))
        fila = cursor.fetchone() 
        
        if fila:
            objCliente = Cliente(fila)
            return jsonify(objCliente.to_json())
        else:
            return jsonify({"error": "Cliente no encontrado"}), 404
    except Exception as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()

# POST (Crear)
@clientes_bp.route('/clientes', methods=['POST'])
def create_cliente():
    datos = request.get_json()
    
    campos_requeridos = ['nombre', 'dni', 'telefono', 'negocio_id']
    if not datos or not all(campo in datos for campo in campos_requeridos):
        return jsonify({"error": f"Faltan datos. Se requiere: {campos_requeridos}"}), 400

    nombre = datos['nombre']
    dni = datos['dni']
    telefono = datos['telefono']
    negocio_id = datos['negocio_id']
    apellido = datos.get('apellido')
    email = datos.get('email')

    cursor = None
    try:
        cursor = mysql.connection.cursor()
        sql = "INSERT INTO Clientes (nombre, apellido, dni, telefono, email, negocio_id) VALUES (%s, %s, %s, %s, %s, %s)"
        valores = (nombre, apellido, dni, telefono, email, negocio_id)
        
        cursor.execute(sql, valores)
        mysql.connection.commit()
        
        nuevo_id = cursor.lastrowid
        
        nuevo_cliente = {
            "id": nuevo_id, "nombre": nombre, "apellido": apellido, "dni": dni,
            "telefono": telefono, "email": email, "negocio_id": negocio_id
        }
        return jsonify(nuevo_cliente), 201
    except Exception as err:
        # Manejamos el error si el DNI ya existe (1062 = Duplicate entry)
        if "1062" in str(err): 
            return jsonify({"error": "Ya existe un cliente con ese DNI para este negocio"}), 409
        else:
            return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()

# PUT (Actualizar)
@clientes_bp.route('/clientes/<int:id>', methods=['PUT'])
def update_cliente(id):
    cursor = None
    try:
        datos = request.get_json()
        campos_requeridos = ['nombre', 'dni', 'telefono', 'negocio_id']
        if not datos or not all(campo in datos for campo in campos_requeridos):
            return jsonify({"error": f"Faltan datos. Se requiere: {campos_requeridos}"}), 400

        nombre = datos['nombre']
        dni = datos['dni']
        telefono = datos['telefono']
        negocio_id = datos['negocio_id']
        apellido = datos.get('apellido')
        email = datos.get('email')

        cursor = mysql.connection.cursor()
        sql = "UPDATE Clientes SET nombre = %s, apellido = %s, dni = %s, telefono = %s, email = %s, negocio_id = %s WHERE id = %s"
        valores = (nombre, apellido, dni, telefono, email, negocio_id, id)
        
        cursor.execute(sql, valores)
        mysql.connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Cliente no encontrado"}), 404
        else:
            cliente_actualizado = {
                "id": id, "nombre": nombre, "apellido": apellido, "dni": dni,
                "telefono": telefono, "email": email, "negocio_id": negocio_id
            }
            return jsonify(cliente_actualizado), 200
    except Exception as err:
        if "1062" in str(err):
            return jsonify({"error": "Ya existe un cliente con ese DNI para este negocio"}), 409
        else:
            return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()

# DELETE
@clientes_bp.route('/clientes/<int:id>', methods=['DELETE'])
def delete_cliente(id):
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        sql = "DELETE FROM Clientes WHERE id = %s"
        cursor.execute(sql, (id,))
        mysql.connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Cliente no encontrado"}), 404
        else:
            return jsonify({"message": "Cliente eliminado correctamente"}), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()