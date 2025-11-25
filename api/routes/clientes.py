
from flask import Blueprint, jsonify, request
from api.utils import token_required, validar_campos
from api.models.cliente import Cliente






clientes_bp = Blueprint('clientes', __name__)
# GET Todos (Filtrado por Negocio)
@clientes_bp.route('/clientes', methods=['GET'])
@token_required

def get_clientes():
    try:
        negocio_id_del_token = request.negocio_id
        
        lista_objetos = Cliente.obtener_todos(negocio_id_del_token)
        lista_json = [c.to_json() for c in lista_objetos]
        
        return jsonify(lista_json), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500
    

# GET por ID (lo dejamos público para el comprobante)
@clientes_bp.route('/clientes/<int:id>', methods=['GET'])

def get_cliente_por_id(id):
    try:
        cliente = Cliente.obtener_por_id(id)
        if cliente:
            return jsonify(cliente.to_json()), 200
        return jsonify({"error": "Cliente no encontrado"}), 404
    except Exception as err:
        return jsonify({"error": str(err)}), 500
    

# POST (Crear) - (publico para que la gente se registre sola)
@clientes_bp.route('/clientes', methods=['POST'])

def create_cliente():
    datos = request.get_json()
    
    # Validación simple
    if not validar_campos(datos, ['nombre', 'dni', 'telefono', 'negocio_id']):
        return jsonify({"error": "Faltan datos obligatorios (nombre, dni, telefono, negocio_id)"}), 400

    try:
        nuevo_cliente = Cliente.crear_desde_datos(datos)
        return jsonify(nuevo_cliente.to_json()), 201

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 409 # 409 Conflict (DNI duplicado)
    except Exception as err:
        return jsonify({"error": str(err)}), 500

# DELETE (borrar privado)
@clientes_bp.route('/clientes/<int:id>', methods=['DELETE'])
@token_required
def delete_cliente(id):

    try:
        filas = Cliente.eliminar(id)
        if filas > 0:
            return jsonify({"message": "Cliente eliminado"}), 200
        return jsonify({"error": "Cliente no encontrado"}), 404
    except Exception as err:
        return jsonify({"error": str(err)}), 500
    