-- Borra las tablas si ya existen, para empezar de cero.
DROP TABLE IF EXISTS Turnos, Disponibilidad, Profesional_Servicios, Clientes, Servicios, Profesionales, Usuarios, Negocios;

-- Negocios
CREATE TABLE Negocios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    direccion VARCHAR(255),
    telefono VARCHAR(50),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Usuarios
-- Solamente los profesionales, no hace falta que un cliente se registre
CREATE TABLE Usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL, -- Para que no acepte un texto vacio.
    negocio_id INT NOT NULL,
    FOREIGN KEY (negocio_id) REFERENCES Negocios(id) ON DELETE CASCADE
);

-- Profesionales
CREATE TABLE Profesionales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    negocio_id INT NOT NULL,
    FOREIGN KEY (negocio_id) REFERENCES Negocios(id) ON DELETE CASCADE
);

-- Servicios (Lo que ofrece cada profesional)
CREATE TABLE Servicios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT,
    duracion_turno_min INT NOT NULL, -- Vamos a manejarnos los turnos en minutos.
    negocio_id INT NOT NULL,
    FOREIGN KEY (negocio_id) REFERENCES Negocios(id) ON DELETE CASCADE
);

-- Profesional_Servicios
    CREATE TABLE Profesional_Servicios (
    profesional_id INT NOT NULL,
    servicio_id INT NOT NULL,
    PRIMARY KEY (profesional_id, servicio_id),
    FOREIGN KEY (profesional_id) REFERENCES Profesionales(id) ON DELETE CASCADE,
    FOREIGN KEY (servicio_id) REFERENCES Servicios(id) ON DELETE CASCADE
);

-- Disponibilidad
CREATE TABLE Disponibilidad (
    id INT AUTO_INCREMENT PRIMARY KEY,
    profesional_id INT NOT NULL,
    dia_semana INT NOT NULL, -- 1 para Lunes, 2 para Martes, ... 7 para Domingo.
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    FOREIGN KEY (profesional_id) REFERENCES Profesionales(id) ON DELETE CASCADE
);

-- Clientes ("Pacientes")
CREATE TABLE Clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    apellido VARCHAR(255),
    telefono VARCHAR(50),
    email VARCHAR(255),
    negocio_id INT NOT NULL,
    FOREIGN KEY (negocio_id) REFERENCES Negocios(id) ON DELETE CASCADE
);

-- Turnos
CREATE TABLE Turnos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha_hora DATETIME NOT NULL, -- Combinamos fecha y hora en un solo campo para simplificar.
    estado ENUM('Confirmado', 'Cancelado', 'Pendiente', 'Completado') NOT NULL DEFAULT 'Pendiente',
    cliente_id INT NOT NULL,
    profesional_id INT NOT NULL,
    servicio_id INT NOT NULL,
    negocio_id INT NOT NULL, -- Vemos si esto se mantiene
    FOREIGN KEY (cliente_id) REFERENCES Clientes(id),
    FOREIGN KEY (profesional_id) REFERENCES Profesionales(id),
    FOREIGN KEY (servicio_id) REFERENCES Servicios(id),
    FOREIGN KEY (negocio_id) REFERENCES Negocios(id) ON DELETE CASCADE
);