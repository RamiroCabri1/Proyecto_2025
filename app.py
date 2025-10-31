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
            

#  CRUD PARA SERVICIOS
@app.route('/servicios', methods=['GET'])
def get_servicios():
    """
    Este endpoint devuelve una lista de todos los servicios.
    """
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM Servicios") 
        
        servicios = cursor.fetchall() # Obtenemos todos los resultados
        
        return jsonify(servicios)

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


@app.route('/servicios/<int:id>', methods=['GET'])
def get_servicio_por_id(id):
    """
    Este endpoint devuelve un servicio específico por su ID.
    """
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True) 
        
        sql = "SELECT * FROM Servicios WHERE id = %s"
        cursor.execute(sql, (id,))
        
        servicio = cursor.fetchone() 
        
        if servicio:
            return jsonify(servicio)
        else:
            return jsonify({"error": "Servicio no encontrado"}), 404

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

@app.route('/servicios', methods=['POST'])
def create_servicio():
    """
    Este endpoint crea un nuevo servicio.
    Espera un JSON con nombre, descripcion, duracion_turno_min y negocio_id.
    """
    datos = request.get_json()
    
    # Validamos que nos enviaron todos los datos necesarios
    campos_requeridos = ['nombre', 'descripcion', 'duracion_turno_min', 'negocio_id']
    if not datos or not all(campo in datos for campo in campos_requeridos):
        return jsonify({"error": f"Faltan datos. Se requiere: {campos_requeridos}"}), 400

    nombre = datos['nombre']
    descripcion = datos['descripcion']
    duracion = datos['duracion_turno_min']
    negocio_id = datos['negocio_id']

    conn = None
    cursor = None
    try:        
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        sql = "INSERT INTO Servicios (nombre, descripcion, duracion_turno_min, negocio_id) VALUES (%s, %s, %s, %s)"
        valores = (nombre, descripcion, duracion, negocio_id)

        cursor.execute(sql, valores)

        conn.commit()
        
        nuevo_id = cursor.lastrowid
        
        # Devolver la respuesta
        nuevo_servicio = {
            "id": nuevo_id,
            "nombre": nombre,
            "descripcion": descripcion,
            "duracion_turno_min": duracion,
            "negocio_id": negocio_id
        }
        return jsonify(nuevo_servicio), 201 # 201 significa "Creado"

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


@app.route('/servicios/<int:id>', methods=['PUT'])
def update_servicio(id):
    """
    Este endpoint actualiza un servicio existente por su ID.
    """
    conn = None
    cursor = None
    try:
        # Leemos los datos nuevos que nos envía el cliente
        datos = request.get_json()
        campos_requeridos = ['nombre', 'descripcion', 'duracion_turno_min', 'negocio_id']
        if not datos or not all(campo in datos for campo in campos_requeridos):
            return jsonify({"error": f"Faltan datos. Se requiere: {campos_requeridos}"}), 400

        nombre = datos['nombre']
        descripcion = datos['descripcion']
        duracion = datos['duracion_turno_min']
        negocio_id = datos['negocio_id']

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        sql = "UPDATE Servicios SET nombre = %s, descripcion = %s, duracion_turno_min = %s, negocio_id = %s WHERE id = %s"
        valores = (nombre, descripcion, duracion, negocio_id, id)
        cursor.execute(sql, valores)        
        conn.commit()

        # Verificamos si realmente se actualizó algo
        if cursor.rowcount == 0:
            # Si rowcount es 0, no se encontró un servicio con ese ID
            return jsonify({"error": "Servicio no encontrado"}), 404
        else:
            # Si salió bien, devolvemos el objeto actualizado
            servicio_actualizado = {
                "id": id,
                "nombre": nombre,
                "descripcion": descripcion,
                "duracion_turno_min": duracion,
                "negocio_id": negocio_id
            }
            return jsonify(servicio_actualizado), 200 # 200 OK

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

@app.route('/servicios/<int:id>', methods=['DELETE'])
def delete_servicio(id):
    """
    Este endpoint borra un servicio existente por su ID.
    """
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        sql = "DELETE FROM Servicios WHERE id = %s"
        cursor.execute(sql, (id,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Servicio no encontrado"}), 404
        else:
            return jsonify({"message": "Servicio eliminado correctamente"}), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

#  CRUD PARA PROFESIONALES (Es exactamente lo mismo que Servicio no me juzguen)
@app.route('/profesionales', methods=['GET'])
def get_profesionales():
    """
    Devuelve una lista de todos los profesionales.
    """
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True) 
        
        cursor.execute("SELECT * FROM Profesionales") 
        
        profesionales = cursor.fetchall()
        
        return jsonify(profesionales)

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

@app.route('/profesionales/<int:id>', methods=['GET'])
def get_profesional_por_id(id):
    """
    Devuelve un profesional específico por su ID.
    """
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True) 
        
        sql = "SELECT * FROM Profesionales WHERE id = %s"
        cursor.execute(sql, (id,))
        
        profesional = cursor.fetchone() 
        
        if profesional:
            return jsonify(profesional)
        else:
            return jsonify({"error": "Profesional no encontrado"}), 404

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

@app.route('/profesionales', methods=['POST'])
def create_profesional():
    """
    Crea un nuevo profesional.
    Espera un JSON con nombre, activo y negocio_id.
    """
    datos = request.get_json()
    
    campos_requeridos = ['nombre', 'activo', 'negocio_id']
    if not datos or not all(campo in datos for campo in campos_requeridos):
        return jsonify({"error": f"Faltan datos. Se requiere: {campos_requeridos}"}), 400

    nombre = datos['nombre']
    activo = datos['activo']
    negocio_id = datos['negocio_id']

    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        sql = "INSERT INTO Profesionales (nombre, activo, negocio_id) VALUES (%s, %s, %s)"
        valores = (nombre, activo, negocio_id)
        
        cursor.execute(sql, valores)
        conn.commit()
        
        nuevo_id = cursor.lastrowid
        
        nuevo_profesional = {
            "id": nuevo_id,
            "nombre": nombre,
            "activo": activo,
            "negocio_id": negocio_id
        }
        return jsonify(nuevo_profesional), 201

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

@app.route('/profesionales/<int:id>', methods=['PUT'])
def update_profesional(id):
    """
    Actualiza un profesional existente por su ID.
    """
    conn = None
    cursor = None
    try:
        datos = request.get_json()
        campos_requeridos = ['nombre', 'activo', 'negocio_id']
        if not datos or not all(campo in datos for campo in campos_requeridos):
            return jsonify({"error": f"Faltan datos. Se requiere: {campos_requeridos}"}), 400

        nombre = datos['nombre']
        activo = datos['activo']
        negocio_id = datos['negocio_id']

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        sql = "UPDATE Profesionales SET nombre = %s, activo = %s, negocio_id = %s WHERE id = %s"
        valores = (nombre, activo, negocio_id, id)
        
        cursor.execute(sql, valores)
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Profesional no encontrado"}), 404
        else:
            profesional_actualizado = {
                "id": id,
                "nombre": nombre,
                "activo": activo,
                "negocio_id": negocio_id
            }
            return jsonify(profesional_actualizado), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

#Cree para más adelante una columna "activo", no la vamos a usar si llegamos justo
#Pero es para que todo lo que tenia el profesional se mantenga pero se oculte
#Los turnos que tuvo y sus datos para no registrarse de 0, para un negocio de verdad es buenisimo
#Pero tenemos que ver si llegamos, así que por ahora nos quedamos con DELETE
@app.route('/profesionales/<int:id>', methods=['DELETE']) 
def delete_profesional(id):
    """
    Borra un profesional existente por su ID.
    """
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        sql = "DELETE FROM Profesionales WHERE id = %s"
        cursor.execute(sql, (id,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Profesional no encontrado"}), 404
        else:
            return jsonify({"message": "Profesional eliminado correctamente"}), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

#  CRUD PARA CLIENTES

@app.route('/clientes', methods=['GET'])
def get_clientes():
    
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True) 
        
        cursor.execute("SELECT * FROM Clientes") 
        
        clientes = cursor.fetchall()
        
        return jsonify(clientes)

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

@app.route('/clientes/<int:id>', methods=['GET'])
def get_cliente_por_id(id):
    
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True) 
        
        sql = "SELECT * FROM Clientes WHERE id = %s"
        cursor.execute(sql, (id,))
        
        cliente = cursor.fetchone() 
        
        if cliente:
            return jsonify(cliente)
        else:
            return jsonify({"error": "Cliente no encontrado"}), 404

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

@app.route('/clientes', methods=['POST'])
def create_cliente():
    
    datos = request.get_json()
    
    # Dni y telefono obligatorio ya que es el maximo identificante y un contacto
    campos_requeridos = ['nombre', 'dni', 'telefono', 'negocio_id']
    if not datos or not all(campo in datos for campo in campos_requeridos):
        return jsonify({"error": f"Faltan datos. Se requiere: {campos_requeridos}"}), 400
    

    nombre = datos['nombre']
    dni = datos['dni']
    telefono = datos['telefono']
    negocio_id = datos['negocio_id']
    apellido = datos.get('apellido')
    telefono = datos.get('telefono')
    email = datos.get('email')

    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        sql = "INSERT INTO Clientes (nombre, apellido, dni, telefono, email, negocio_id) VALUES (%s, %s, %s, %s, %s, %s)"
        valores = (nombre, apellido, dni, telefono, email, negocio_id)
        
        cursor.execute(sql, valores)
        conn.commit()
        
        nuevo_id = cursor.lastrowid
        
        nuevo_cliente = {
            "id": nuevo_id,
            "nombre": nombre,
            "apellido": apellido,
            "dni": dni,
            "telefono": telefono,
            "email": email,
            "negocio_id": negocio_id
        }
        return jsonify(nuevo_cliente), 201

    except mysql.connector.Error as err:
        # Manejamos el error si el DNI ya existe
        if err.errno == 1062: # 1062 = "Duplicate entry"
            return jsonify({"error": "Ya existe un cliente con ese DNI para este negocio"}), 409 # 409 Conflict
        else:
            return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

@app.route('/clientes/<int:id>', methods=['PUT'])
def update_cliente(id):
    
    conn = None
    cursor = None
    try:
        datos = request.get_json()
        
        # Agregamos dni y telefono a los campos requeridos
        campos_requeridos = ['nombre', 'dni', 'telefono', 'negocio_id']
        if not datos or not all(campo in datos for campo in campos_requeridos):
            return jsonify({"error": f"Faltan datos. Se requiere: {campos_requeridos}"}), 400

        nombre = datos['nombre']
        dni = datos['dni']
        telefono = datos['telefono']
        negocio_id = datos['negocio_id']
        apellido = datos.get('apellido')
        telefono = datos.get('telefono')
        email = datos.get('email')
        

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        sql = "UPDATE Clientes SET nombre = %s, apellido = %s, dni = %s, telefono = %s, email = %s, negocio_id = %s WHERE id = %s"
        valores = (nombre, apellido, dni, telefono, email, negocio_id, id)
        
        cursor.execute(sql, valores)
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Cliente no encontrado"}), 404
        else:
            cliente_actualizado = {
                "id": id, "nombre": nombre, "apellido": apellido, "dni": dni,
                "telefono": telefono, "email": email, "negocio_id": negocio_id
            }
            return jsonify(cliente_actualizado), 200

    except mysql.connector.Error as err:
        # Manejamos el error si el DNI ya existe
        if err.errno == 1062:
            return jsonify({"error": "Ya existe un cliente con ese DNI para este negocio"}), 409
        else:
            return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

@app.route('/clientes/<int:id>', methods=['DELETE'])
def delete_cliente(id):    
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        sql = "DELETE FROM Clientes WHERE id = %s"
        cursor.execute(sql, (id,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Cliente no encontrado"}), 404
        else:
            return jsonify({"message": "Cliente eliminado correctamente"}), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

#  CRUD PARA DISPONIBILIDAD

@app.route('/profesionales/<int:id_profesional>/disponibilidad', methods=['GET'])
def get_disponibilidad_profesional(id_profesional):
    """
    Devuelve la lista de horarios de un profesional específico.
    """
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True) 
        
        # Primero, verificamos si el profesional existe para evitar un error 404
        cursor.execute("SELECT id FROM Profesionales WHERE id = %s", (id_profesional,))
        if not cursor.fetchone():
            return jsonify({"error": "Profesional no encontrado"}), 404
        
        # Si el profesional existe, buscamos su disponibilidad
        sql = "SELECT * FROM Disponibilidad WHERE profesional_id = %s"
        cursor.execute(sql, (id_profesional,))
        
        disponibilidades = cursor.fetchall()        
        return jsonify(disponibilidades)

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
            
@app.route('/profesionales/<int:id_profesional>/disponibilidad', methods=['POST'])
def create_disponibilidad_profesional(id_profesional):
    """
    Crea un nuevo horario de disponibilidad para un profesional específico.
    """
    conn = None
    cursor = None
    
    # Leemos los datos del JSON
    datos = request.get_json()
    
    campos_requeridos = ['dia_semana', 'hora_inicio', 'hora_fin']
    if not datos or not all(campo in datos for campo in campos_requeridos):
        return jsonify({"error": f"Faltan datos. Se requiere: {campos_requeridos}"}), 400

    dia_semana = datos['dia_semana']
    hora_inicio = datos['hora_inicio']
    hora_fin = datos['hora_fin']
    
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Verificamos que el profesional exista
        cursor.execute("SELECT id FROM Profesionales WHERE id = %s", (id_profesional,))
        if not cursor.fetchone():
            return jsonify({"error": "Profesional no encontrado"}), 404

        # Insertamos el nuevo horario
        sql = "INSERT INTO Disponibilidad (profesional_id, dia_semana, hora_inicio, hora_fin) VALUES (%s, %s, %s, %s)"
        # Usamos el id_profesional de la URL y los datos del JSON
        valores = (id_profesional, dia_semana, hora_inicio, hora_fin)
        
        cursor.execute(sql, valores)
        conn.commit()
        
        # Devolvemos el horario recién creado
        nuevo_id = cursor.lastrowid
        nuevo_horario = {
            "id": nuevo_id,
            "profesional_id": id_profesional,
            "dia_semana": dia_semana,
            "hora_inicio": hora_inicio,
            "hora_fin": hora_fin
        }
        
        return jsonify(nuevo_horario), 201

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