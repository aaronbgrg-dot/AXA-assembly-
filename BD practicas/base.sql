# Código SQL - Base de Datos Mobiliario

CREATE DATABASE mobiliario;
USE mobiliario;

-- =========================
-- 1. TABLA USUARIO
-- =========================

CREATE TABLE usuario (
    id_usuario INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    contraseña VARCHAR(255) NOT NULL,
    telefono VARCHAR(20) UNIQUE,
    rol VARCHAR(20) NOT NULL,
    fecha_registro DATE NOT NULL
);

-- =========================
-- 2. TABLA DEPARTAMENTO
-- =========================

CREATE TABLE departamento (
    id_departamento INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT
);

-- =========================
-- 3. TABLA TRABAJADOR
-- =========================

CREATE TABLE trabajador (
    id_trabajador INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT UNSIGNED NOT NULL UNIQUE,
    id_departamento INT UNSIGNED NOT NULL,
    puesto VARCHAR(50) NOT NULL,
    salario DECIMAL(10,2) NOT NULL,
    fecha_contratacion DATE NOT NULL,

    FOREIGN KEY (id_usuario)
        REFERENCES usuario(id_usuario),

    FOREIGN KEY (id_departamento)
        REFERENCES departamento(id_departamento)
);

-- =========================
-- 4. TABLA PROVEEDOR
-- =========================

CREATE TABLE proveedor (
    id_proveedor INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre_empresa VARCHAR(100) NOT NULL,
    telefono VARCHAR(20) UNIQUE,
    email VARCHAR(100) UNIQUE,
    direccion VARCHAR(150) NOT NULL,
    ciudad VARCHAR(50) NOT NULL
);

-- =========================
-- 5. TABLA MUEBLE
-- =========================

CREATE TABLE mueble (
    id_mueble INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_proveedor INT UNSIGNED NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL,
    material VARCHAR(50),

    FOREIGN KEY (id_proveedor)
        REFERENCES proveedor(id_proveedor)
);

-- =========================
-- 6. TABLA PEDIDO
-- =========================

CREATE TABLE pedido (
    id_pedido INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT UNSIGNED NOT NULL,
    fecha DATE NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    estado VARCHAR(30) NOT NULL,

    FOREIGN KEY (id_usuario)
        REFERENCES usuario(id_usuario)
);

-- =========================
-- 7. TABLA DETALLE_PEDIDO
-- =========================

CREATE TABLE detalle_pedido (
    id_detalle INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_pedido INT UNSIGNED NOT NULL,
    id_mueble INT UNSIGNED NOT NULL,
    cantidad INT NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,

    FOREIGN KEY (id_pedido)
        REFERENCES pedido(id_pedido),

    FOREIGN KEY (id_mueble)
        REFERENCES mueble(id_mueble)
);

-- =========================
-- 8. TABLA DISEÑO_PERSONALIZADO
-- =========================

CREATE TABLE diseño_personalizado (
    id_diseño INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT UNSIGNED NOT NULL,
    id_mueble INT UNSIGNED NOT NULL,
    ancho DECIMAL(10,2) NOT NULL,
    alto DECIMAL(10,2) NOT NULL,
    profundidad DECIMAL(10,2) NOT NULL,
    color VARCHAR(50),
    material VARCHAR(50),
    descripcion TEXT,
    precio_estimado DECIMAL(10,2),
    estado VARCHAR(30) NOT NULL,

    FOREIGN KEY (id_usuario)
        REFERENCES usuario(id_usuario),

    FOREIGN KEY (id_mueble)
        REFERENCES mueble(id_mueble)
);

-- =========================
-- 9. TABLA SERVICIO
-- =========================

CREATE TABLE servicio (
    id_servicio INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10,2) NOT NULL
);

-- =========================
-- 10. TABLA PEDIDO_SERVICIO
-- =========================

CREATE TABLE pedido_servicio (
    id_pedido INT UNSIGNED NOT NULL,
    id_servicio INT UNSIGNED NOT NULL,

    PRIMARY KEY (id_pedido, id_servicio),

    FOREIGN KEY (id_pedido)
        REFERENCES pedido(id_pedido),

    FOREIGN KEY (id_servicio)
        REFERENCES servicio(id_servicio)
);

-- =========================
-- 11. TABLA OFERTA
-- =========================

CREATE TABLE oferta (
    id_oferta INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    descripcion TEXT,
    descuento DECIMAL(5,2) NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL
);

-- =========================
-- 12. TABLA MUEBLE_OFERTA
-- =========================

CREATE TABLE mueble_oferta (
    id_mueble INT UNSIGNED NOT NULL,
    id_oferta INT UNSIGNED NOT NULL,

    PRIMARY KEY (id_mueble, id_oferta),

    FOREIGN KEY (id_mueble)
        REFERENCES mueble(id_mueble),

    FOREIGN KEY (id_oferta)
        REFERENCES oferta(id_oferta)
);

-- =========================
-- 13. TABLA CITA
-- =========================

CREATE TABLE cita (
    id_cita INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT UNSIGNED NOT NULL,
    id_pedido INT UNSIGNED NOT NULL,
    fecha DATETIME NOT NULL,
    tipo VARCHAR(30) NOT NULL,
    direccion VARCHAR(150),
    tienda_recogida VARCHAR(100),
    estado VARCHAR(30) NOT NULL,

    FOREIGN KEY (id_usuario)
        REFERENCES usuario(id_usuario),

    FOREIGN KEY (id_pedido)
        REFERENCES pedido(id_pedido)
);

-- =========================
-- INSERTS DE EJEMPLO
-- =========================

INSERT INTO usuario
(nombre, apellidos, email, contraseña, telefono, rol, fecha_registro)
VALUES
('Aaron', 'Benitez', 'aaron@gmail.com', '1234', '600111222', 'admin', '2026-01-10'),
('Aroa', 'Hernandez', 'aroa@gmail.com', '1234', '600333444', 'admin', '2026-02-01'),
('Xabier', 'Iglesias', 'xabier@gmail.com', '1234', '600555666', 'admin', '2026-02-15'),
('Ibon', 'Etxegia', 'pringles@gmail.com', '1234', '600234567', 'cliente', '2026-05-14'),
('Unax', 'Gahona', 'tolosa@gmail.com', '1234', '601234567', 'cliente', '2026-05-14'),
('Mikel', 'Villa', 'musculitos@gmail.com', '1234', '602987999', 'cliente', '2026-05-14'),
('Ibai', 'Lopez', 'ibai@gmail.com', '1234', '603098312', 'empleado', '2025-05-14'),
('Hugo', 'Rayo', 'hugo@gmail.com', '1234', '604891745', 'empleado', '2025-05-14'),
('Ibon', 'Ye Lin', 'ibon@gmail.com', '1234', '605656098', 'empleado', '202505-14');

INSERT INTO departamento
(nombre, descripcion)
VALUES
('Ventas', 'Gestion de ventas'),
('Diseño', 'Diseño personalizado'),
('Logistica', 'Envios y recogidas'),
('Dirección', 'Organización de productos'),
('Trabajadores', 'Comunicación y ayuda con el cliente');

INSERT INTO trabajador
(id_usuario, id_departamento, puesto, salario, fecha_contratacion)
VALUES
(7, 5, 'Vendedor', 2200.00, '2025-05-15'),
(8, 5, 'Vendedor', 2200.00, '2025-05-15'),
(9, 5, 'Vendedor', 2200.00, '2025-05-15');
INSERT INTO proveedor
(nombre_empresa, telefono, email, direccion, ciudad)
VALUES
('Muebles Norte', '944111222', 'contacto@mueblesnorte.com', 'Calle Mayor 12', 'Bilbao');

INSERT INTO mueble
(id_proveedor, nombre, categoria, precio, stock, material)
VALUES
(1, 'Sofa moderno', 'Salon', 550.00, 15, 'Cuero'),
(1, 'Mesa comedor', 'Comedor', 320.00, 10, 'Madera');

INSERT INTO pedido
(id_usuario, fecha, total, estado)
VALUES
(3, '2026-05-01', 870.00, 'confirmado');

INSERT INTO detalle_pedido
(id_pedido, id_mueble, cantidad, subtotal)
VALUES
(1, 1, 1, 550.00),
(1, 2, 1, 320.00);

INSERT INTO servicio
(nombre, descripcion, precio)
VALUES
('Montaje', 'Montaje de muebles en domicilio', 80.00),
('Transporte', 'Entrega a domicilio', 50.00);

INSERT INTO pedido_servicio
(id_pedido, id_servicio)
VALUES
(1, 1),
(1, 2);

INSERT INTO oferta
(titulo, descripcion, descuento, fecha_inicio, fecha_fin)
VALUES
('Oferta Primavera', 'Descuento de primavera', 10.00, '2026-04-01', '2026-05-01');

INSERT INTO mueble_oferta
(id_mueble, id_oferta)
VALUES
(1, 1);

INSERT INTO diseño_personalizado
(id_usuario, id_mueble, ancho, alto, profundidad, color, material, descripcion, precio_estimado, estado)
VALUES
(3, 1, 220.00, 90.00, 80.00, 'Negro', 'Cuero', 'Sofa personalizado para salon moderno', 780.00, 'en proceso');

INSERT INTO cita
(id_usuario, id_pedido, fecha, tipo, direccion, tienda_recogida, estado)
VALUES
(3, 1, '2026-05-10 17:00:00', 'entrega', 'Calle Real 15', NULL, 'confirmada');

```
