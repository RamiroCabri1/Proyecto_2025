from flask import Flask, jsonify, request
import mysql.connector
import os
from dotenv import load_dotenv

# Creamos una instancia de Flask
app = Flask(__name__)

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Configuración a la BD desde .env (Para entrar al JSON)
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

# Endpoint, lo usamos para que nos devuelva los negocios
@app.route('/negocios', methods=['GET'])
def get_negocios():
    conn = None
    cursor = None
    try:
        # Nos conectamos a la BD
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Ejecutamos el SQL
        cursor.execute("SELECT id, nombre, direccion, telefono FROM Negocios")

        # Reseteamos como una lista de diccionarios
        columnas = [col[0] for col in cursor.description]
        negocios = []
        for fila in cursor.fetchall():
            negocio = dict(zip(columnas, fila))
            negocios.append(negocio)

        # Devuelve en JSON
        return jsonify(negocios)

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        # Si encuentra un error cierra la conexión
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

@app.route('/negocios', methods=['POST'])
def create_negocio():
    """
    Creamos un nuevo negocio.
    Tendríamos que recibir un JSON con nombre, direccion y telefono.
    """
    
    # Leemos los datos JSON que nos envía el cliente
    datos = request.get_json()
    
    # Validamos que nos enviaron los datos mínimos
    if not datos or 'nombre' not in datos or 'direccion' not in datos or 'telefono' not in datos:
        return jsonify({"error": "Faltan datos (nombre, direccion, telefono)"}), 400

    nombre = datos['nombre']
    direccion = datos['direccion']
    telefono = datos['telefono']

    conn = None
    cursor = None
    try:
        # Conectar a la base de datos
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Preparar la consulta SQL
        sql = "INSERT INTO Negocios (nombre, direccion, telefono) VALUES (%s, %s, %s)"
        valores = (nombre, direccion, telefono)
        
        # Ejecutar la consulta
        cursor.execute(sql, valores)
        
        # Confirmamos los cambios
        conn.commit()
        
        # Obtenemos el ID del negocio que acabamos de crear
        nuevo_id = cursor.lastrowid
        
        # Devolver la respuesta
        nuevo_negocio = {
            "id": nuevo_id,
            "nombre": nombre,
            "direccion": direccion,
            "telefono": telefono
        }
        return jsonify(nuevo_negocio), 201 #Recordatorio = 201 significa "Creado" 

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

@app.route('/negocios/<int:id>', methods=['GET'])
def get_negocio_por_id(id):
    """
    Este endpoint devuelve un negocio específico por su ID.
    """
    conn = None
    cursor = None
    try:
        # Conectamos a la base de datos
        conn = mysql.connector.connect(**db_config)
        
        # Al crear el cursor, le pasamos "dictionary=True".
        # Esto le ordena al conector que nos devuelva los resultados
        # directamente como un diccionario (ej: {'id': 1, 'nombre': ...}) Evitamos formatear el JSON
        cursor = conn.cursor(dictionary=True) 
        
        # Recordatorio: el %s sirve para hacer una conexión segura
        sql = "SELECT id, nombre, direccion, telefono FROM Negocios WHERE id = %s"
        
        # Ejecutamos la consulta pasando el 'id' en una tupla.
        # Es CRUCIAL pasarlo como tupla (id,) para que sea seguro.
        cursor.execute(sql, (id,)) 
        
        # Obtenemos el resultado. 
        negocio = cursor.fetchone() 
        
        # Verificamos si encontramos algo
        if negocio:
            return jsonify(negocio)
        else:
            # Si 'negocio' está vacío devolvemos "error 404"
            return jsonify({"error": "Negocio no encontrado"}), 404

    except mysql.connector.Error as err:
        # Manejo de errores de la base de datos
        return jsonify({"error": str(err)}), 500
    finally:
        # Cerramos todo
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
            
@app.route('/negocios/<int:id>', methods=['PUT'])
def update_negocio(id):
    """
    Este endpoint actualiza un negocio existente por su ID.
    Espera recibir un JSON con los datos a modificar.
    """
    conn = None
    cursor = None
    try:
        # Leemos los datos nuevos que nos envía el cliente
        datos = request.get_json()
        if not datos or 'nombre' not in datos or 'direccion' not in datos or 'telefono' not in datos:
            return jsonify({"error": "Faltan datos (nombre, direccion, telefono)"}), 400

        nombre = datos['nombre']
        direccion = datos['direccion']
        telefono = datos['telefono']

        # Conectamos y preparamos la consulta SQL para actualizar
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        sql = "UPDATE Negocios SET nombre = %s, direccion = %s, telefono = %s WHERE id = %s"
        # Recordatorio: El orden de los valores es importante, el 'id' va al final.
        valores = (nombre, direccion, telefono, id)
        
        # Ejecutamos
        cursor.execute(sql, valores)
        
        conn.commit()

        # Verificamos si realmente se actualizó algo
        if cursor.rowcount == 0:
            # Si rowcount es 0, significa que no se encontró un negocio con ese ID
            return jsonify({"error": "Negocio no encontrado"}), 404
        else:
            # Si salió bien, devolvemos el objeto actualizado
            negocio_actualizado = {
                "id": id,
                "nombre": nombre,
                "direccion": direccion,
                "telefono": telefono
            }
            return jsonify(negocio_actualizado), 200 # 200 OK

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
            

@app.route('/negocios/<int:id>', methods=['DELETE'])
def delete_negocio(id):
    """
    Este endpoint borra un negocio existente por su ID.
    """
    conn = None
    cursor = None
    try:
        # Conectamos y preparamos la consulta SQL de BORRADO
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        sql = "DELETE FROM Negocios WHERE id = %s"
        
        # Ejecutamos
        cursor.execute(sql, (id,))
        
        conn.commit()

        # Verificamos si realmente se borró algo
        if cursor.rowcount == 0:
            # Si rowcount es 0, no se encontró ese ID
            return jsonify({"error": "Negocio no encontrado"}), 404
        else:
            # Si salió bien, devolvemos un mensaje de éxito
            return jsonify({"message": "Negocio eliminado correctamente"}), 200 # 200 OK

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
        
# Iniciamos el .py
if __name__ == '__main__':
    app.run(debug=True, port=5000)