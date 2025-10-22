from flask import Flask, jsonify
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

# Iniciamos el .py
if __name__ == '__main__':
    app.run(debug=True, port=5000)