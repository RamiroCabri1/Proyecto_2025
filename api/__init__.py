from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from api.db.db import mysql 
from datetime import datetime # Importante para los turnos
import os

load_dotenv()
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'esta-es-mi-clave-secreta-123'

app.config['MYSQL_HOST'] = os.getenv('DB_HOST')
app.config['MYSQL_USER'] = os.getenv('DB_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('DB_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('DB_NAME')

mysql.init_app(app)

# Importamos y Registramos las rutas
from api.routes.negocios import negocios_bp
app.register_blueprint(negocios_bp) 

from api.routes.servicios import servicios_bp
app.register_blueprint(servicios_bp) 

from api.routes.profesionales import profesionales_bp
app.register_blueprint(profesionales_bp) 

from api.routes.clientes import clientes_bp
app.register_blueprint(clientes_bp) 

from api.routes.disponibilidad import disponibilidad_bp
app.register_blueprint(disponibilidad_bp)

from api.routes.turnos import turnos_bp
app.register_blueprint(turnos_bp)
# chequeo pq no me funciona la ruta, esto deja en "/" la ruta
from api.routes.usuarios import usuarios_bp
app.register_blueprint(usuarios_bp)