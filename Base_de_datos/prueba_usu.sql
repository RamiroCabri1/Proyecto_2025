-- Indicamos que vamos a usar nuestra base de datos
USE BD_negocio;

-- BORRADO DE DATOS. Nos permite ejecutar el script varias veces sin errores.
DELETE FROM Turnos;
DELETE FROM Profesional_Servicios;
DELETE FROM Disponibilidad;
DELETE FROM Clientes;
DELETE FROM Servicios;
DELETE FROM Profesionales;
DELETE FROM Usuarios;
DELETE FROM Negocios;

-- CREACIÓN DE NEGOCIOS
INSERT INTO Negocios (id, nombre, direccion, telefono) VALUES
(1, 'Peluquería Estilo Único', 'Calle Falsa 123', '291-111111'),
(2, 'Consultorio Odontológico Sonrisas', 'Avenida Siempre Viva 742', '291-222222');

-- CREACIÓN DE USUARIOS (Profesionales)
-- Dato (La contraseña no se guarda así. Luego, con Python, la reemplazaremos por un HASH seguro.)
INSERT INTO Usuarios (email, password_hash, negocio_id) VALUES
('admin.peluqueria@mail.com', 'hash_temporal_para_clave123', 1),
('admin.consultorio@mail.com', 'hash_temporal_para_clave456', 2);

-- CREACIÓN DE PROFESIONALES (Asociados a cada negocio)
INSERT INTO Profesionales (nombre, negocio_id) VALUES
('Roberto Gómez', 1), -- Peluquero del negocio 1
('Ana Martínez', 1),   -- Peluquera del negocio 1
('Dra. Claudia Fernandez', 2); -- Dentista del negocio 2

-- CREACIÓN DE SERVICIOS (Lo que ofrece cada negocio)
INSERT INTO Servicios (nombre, descripcion, duracion_turno_min, negocio_id) VALUES
('Corte de Hombre', 'Corte de pelo masculino con navaja.', 30, 1),
('Corte de Mujer', 'Corte de pelo femenino y brushing.', 60, 1),
('Teñido', 'Aplicación de tintura y lavado.', 90, 1),
('Consulta General', 'Revisión y diagnóstico dental.', 45, 2),
('Limpieza Dental', 'Limpieza profunda con ultrasonido.', 50, 2);

-- Vinvculamos PROFESIONAL-SERVICIOS
INSERT INTO Profesional_Servicios (profesional_id, servicio_id) VALUES
(1, 1), -- Roberto Gómez hace Corte de Hombre (IDs: prof=1, serv=1)
(2, 2), -- Ana Martínez hace Corte de Mujer (IDs: prof=2, serv=2)
(2, 3), -- Ana Martínez también hace Teñido (IDs: prof=2, serv=3)
(3, 4), -- Dra. Fernandez hace Consulta General (IDs: prof=3, serv=4)
(3, 5); -- Dra. Fernandez también hace Limpieza Dental (IDs: prof=3, serv=5)

-- CREACIÓN DE CLIENTES
INSERT INTO Clientes (nombre, apellido, telefono, email, negocio_id) VALUES
('Juan Pérez', 'García', '291-333333', 'juan@mail.com', 1), -- Cliente de la Peluquería
('María Rodríguez', 'Lopez', '291-444444', 'maria@mail.com', 2); -- Cliente del Consultorio