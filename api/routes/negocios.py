from api.utils import token_required
from flask import Blueprint, jsonify, request
from api.models.negocio import Negocio 
from api.db.db import mysql

negocios_bp = Blueprint('negocios', __name__)

# GET Todos (Público - Para el dropdown de clientes)
@negocios_bp.route('/negocios', methods=['GET'])
def get_negocios():
    cursor = None
    try:
        cursor = mysql.connection.cursor() 
        
        # Consulta explícita
        cursor.execute("SELECT id, nombre, direccion, telefono FROM Negocios") 
        filas = cursor.fetchall()
        
        lista_negocios = []
        for fila in filas:
            # fila es una tupla: (id, nombre, direccion, telefono)
            negocio = {
                "id": fila[0],
                "nombre": fila[1],
                "direccion": fila[2],
                "telefono": fila[3]
            }
            lista_negocios.append(negocio)
            
        return jsonify(lista_negocios), 200

    except Exception as err:
        print(f"Error en GET /negocios: {err}") 
        return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()

# GET Mi Negocio
@negocios_bp.route('/negocios/mi-negocio', methods=['GET'])
@token_required
def get_mi_negocio():
    try:
        mi_id = request.negocio_id 
        negocio = Negocio.obtener_por_id(mi_id)
        
        if negocio:
            return jsonify(negocio.to_json()), 200
        else:
            return jsonify({"error": "Negocio no encontrado"}), 404

    except Exception as err:
        return jsonify({"error": str(err)}), 500

# GET por ID
@negocios_bp.route('/negocios/<int:id>', methods=['GET'])
@token_required
def get_negocio_por_id(id):
    try:
        negocio = Negocio.obtener_por_id(id)
        if negocio:
            return jsonify(negocio.to_json()), 200
        else:
            return jsonify({"error": "Negocio no encontrado"}), 404
    except Exception as err:
        return jsonify({"error": str(err)}), 500

# POST (Crear)
@negocios_bp.route('/negocios', methods=['POST'])
def create_negocio():
    datos = request.get_json()
    campos_requeridos = ['nombre', 'direccion', 'telefono']
    if not datos or not all(campo in datos for campo in campos_requeridos):
        return jsonify({"error": f"Faltan datos. Se requiere: {campos_requeridos}"}), 400

    try:
        nuevo_negocio = Negocio.crear_desde_datos(datos)
        return jsonify(nuevo_negocio.to_json()), 201
    except Exception as err:
        return jsonify({"error": str(err)}), 500

# PUT (Actualizar)
@negocios_bp.route('/negocios/<int:id>', methods=['PUT'])
@token_required
def update_negocio(id):
    datos = request.get_json()
    campos_requeridos = ['nombre', 'direccion', 'telefono']
    if not datos or not all(campo in datos for campo in campos_requeridos):
        return jsonify({"error": f"Faltan datos. Se requiere: {campos_requeridos}"}), 400

    try:
        negocio_existente = Negocio.obtener_por_id(id)
        if not negocio_existente:
            return jsonify({"error": "Negocio no encontrado"}), 404
            
        negocio_actualizado = Negocio.actualizar_desde_datos(id, datos)
        return jsonify(negocio_actualizado.to_json()), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500

# DELETE
@negocios_bp.route('/negocios/<int:id>', methods=['DELETE'])
@token_required
def delete_negocio(id):
    try:
        filas_afectadas = Negocio.eliminar(id)
        if filas_afectadas == 0:
            return jsonify({"error": "Negocio no encontrado"}), 404
        else:
            return jsonify({"message": "Negocio eliminado correctamente"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 409
    except Exception as err:
        return jsonify({"error": str(err)}), 500