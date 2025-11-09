-- ======================================
-- ESTRUCTURA BASE DE DATOS: PROYECTO_2025
-- ======================================

CREATE DATABASE IF NOT EXISTS proyecto_2025 CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE proyecto_2025;

-- ----------------------
-- Tabla: negocios
-- ----------------------
CREATE TABLE IF NOT EXISTS negocios (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(150) NOT NULL,
  direccion VARCHAR(255),
  telefono VARCHAR(30)
);

-- ----------------------
-- Tabla: usuarios
-- ----------------------
CREATE TABLE IF NOT EXISTS usuarios (
  id INT AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(120) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  negocio_id INT,
  FOREIGN KEY (negocio_id) REFERENCES negocios(id)
);

-- ----------------------
-- Tabla: clientes
-- ----------------------
CREATE TABLE IF NOT EXISTS clientes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  apellido VARCHAR(100),
  dni VARCHAR(20) NOT NULL,
  telefono VARCHAR(30),
  email VARCHAR(120),
  negocio_id INT,
  UNIQUE (dni, negocio_id),
  FOREIGN KEY (negocio_id) REFERENCES negocios(id)
);

-- ----------------------
-- Tabla: profesionales
-- ----------------------
CREATE TABLE IF NOT EXISTS profesionales (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  negocio_id INT,
  activo BOOLEAN DEFAULT TRUE,
  FOREIGN KEY (negocio_id) REFERENCES negocios(id)
);

-- ----------------------
-- Tabla: servicios
-- ----------------------
CREATE TABLE IF NOT EXISTS servicios (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  descripcion TEXT,
  duracion_turno_min INT,
  negocio_id INT,
  FOREIGN KEY (negocio_id) REFERENCES negocios(id)
);

-- ----------------------
-- Tabla: disponibilidades
-- ----------------------
CREATE TABLE IF NOT EXISTS disponibilidades (
  id INT AUTO_INCREMENT PRIMARY KEY,
  profesional_id INT NOT NULL,
  dia_semana VARCHAR(20) NOT NULL,
  hora_inicio TIME NOT NULL,
  hora_fin TIME NOT NULL,
  FOREIGN KEY (profesional_id) REFERENCES profesionales(id)
);

-- ----------------------
-- Tabla: turnos
-- ----------------------
CREATE TABLE IF NOT EXISTS turnos (
  id INT AUTO_INCREMENT PRIMARY KEY,
  fecha_hora DATETIME NOT NULL,
  estado VARCHAR(50) DEFAULT 'pendiente',
  cliente_id INT,
  profesional_id INT,
  servicio_id INT,
  negocio_id INT,
  FOREIGN KEY (cliente_id) REFERENCES clientes(id),
  FOREIGN KEY (profesional_id) REFERENCES profesionales(id),
  FOREIGN KEY (servicio_id) REFERENCES servicios(id),
  FOREIGN KEY (negocio_id) REFERENCES negocios(id)
);