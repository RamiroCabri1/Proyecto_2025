from flask import Flask, jsonify
import mysql.connector
import os
from dotenv import load_dotenv

# Crear una instancia de Flask
app = Flask(__name__)

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Configuración de la conexión a la BD leída desde .env
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

# --- NUESTRO PRIMER ENDPOINT REAL ---
@app.route('/negocios', methods=['GET'])
def get_negocios():
    """
    Este endpoint se conecta a la base de datos real
    y devuelve una lista de todos los negocios.
    """
    conn = None
    cursor = None
    try:
        # Conectar a la base de datos
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Ejecutar la consulta SQL
        cursor.execute("SELECT id, nombre, direccion, telefono FROM Negocios")

        # Formatear los resultados como una lista de diccionarios
        columnas = [col[0] for col in cursor.description]
        negocios = []
        for fila in cursor.fetchall():
            negocio = dict(zip(columnas, fila))
            negocios.append(negocio)

        # Devolver la respuesta en formato JSON
        return jsonify(negocios)

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        # Cerrar el cursor y la conexión
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

# Esto inicia la aplicación
if __name__ == '__main__':
    app.run(debug=True, port=5000)