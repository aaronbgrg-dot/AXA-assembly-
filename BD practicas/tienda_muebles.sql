CREATE DATABASE tienda_muebles;
USE tienda_muebles;

-- =====================================================
-- 1. TABLA USUARIOS
-- =====================================================

CREATE TABLE usuario (
    id_usuario INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    nombre VARCHAR(100) NOT NULL,

    apellido VARCHAR(100) NOT NULL,

    email VARCHAR(150) NOT NULL UNIQUE,

    contraseña VARCHAR(255) NOT NULL,

    telefono VARCHAR(20),

    direccion TEXT,

    fecha_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    rol ENUM('cliente', 'administrador', 'trabajador')
    NOT NULL DEFAULT 'cliente'
);

-- =====================================================
-- TABLA CATEGORÍAS
-- =====================================================

CREATE TABLE categoria (
    id_categoria INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    nombre VARCHAR(100) NOT NULL UNIQUE,

    descripcion TEXT
);

-- =====================================================
-- TABLA MUEBLES
-- =====================================================

CREATE TABLE mueble (
    id_mueble INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    nombre VARCHAR(150) NOT NULL,

    descripcion TEXT,

    precio DECIMAL(10,2)
    NOT NULL
    CHECK (precio >= 0),

    stock INT
    NOT NULL DEFAULT 0
    CHECK (stock >= 0),

    id_categoria INT UNSIGNED NOT NULL,

    FOREIGN KEY (id_categoria)
        REFERENCES categoria(id_categoria)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- =====================================================
-- TABLA IMÁGENES DE MUEBLES
-- =====================================================

CREATE TABLE imagen_mueble (
    id_imagen INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    id_mueble INT UNSIGNED NOT NULL,

    ruta_imagen VARCHAR(255) NOT NULL,

    principal BOOLEAN DEFAULT FALSE,

    FOREIGN KEY (id_mueble)
        REFERENCES mueble(id_mueble)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- =====================================================
-- TABLA CARRITO
-- =====================================================

CREATE TABLE carrito (
    id_carrito INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    id_usuario INT UNSIGNED NOT NULL,

    fecha_creacion DATETIME
    NOT NULL DEFAULT CURRENT_TIMESTAMP,

    estado ENUM('activo', 'finalizado', 'cancelado')
    NOT NULL DEFAULT 'activo',

    FOREIGN KEY (id_usuario)
        REFERENCES usuario(id_usuario)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- =====================================================
-- TABLA DETALLE CARRITO
-- =====================================================

CREATE TABLE carrito_detalle (
    id_carrito_detalle INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    id_carrito INT UNSIGNED NOT NULL,

    id_mueble INT UNSIGNED NOT NULL,

    cantidad INT
    NOT NULL DEFAULT 1
    CHECK (cantidad > 0),

    FOREIGN KEY (id_carrito)
        REFERENCES carrito(id_carrito)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    FOREIGN KEY (id_mueble)
        REFERENCES mueble(id_mueble)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- =====================================================
-- TABLA PEDIDOS
-- =====================================================

CREATE TABLE pedido (
    id_pedido INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    id_usuario INT UNSIGNED NOT NULL,

    fecha_pedido DATETIME
    NOT NULL DEFAULT CURRENT_TIMESTAMP,

    total DECIMAL(10,2)
    NOT NULL
    CHECK (total >= 0),

    FOREIGN KEY (id_usuario)
        REFERENCES usuario(id_usuario)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- =====================================================
-- TABLA DETALLE PEDIDOS
-- =====================================================

CREATE TABLE detalle_pedido (
    id_detalle INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    id_pedido INT UNSIGNED NOT NULL,

    id_mueble INT UNSIGNED NOT NULL,

    cantidad INT
    NOT NULL
    CHECK (cantidad > 0),

    precio_unitario DECIMAL(10,2)
    NOT NULL
    CHECK (precio_unitario >= 0),

    FOREIGN KEY (id_pedido)
        REFERENCES pedido(id_pedido)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    FOREIGN KEY (id_mueble)
        REFERENCES mueble(id_mueble)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- =====================================================
-- TABLA ESTADOS DE PEDIDO
-- =====================================================

CREATE TABLE estado_pedido (
    id_estado INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    nombre ENUM(
        'pendiente',
        'confirmado',
        'en_produccion',
        'preparando_envio',
        'en_reparto',
        'entregado',
        'recogido',
        'cancelado'
    ) NOT NULL UNIQUE
);

INSERT INTO estado_pedido (nombre)
VALUES
('pendiente'),
('confirmado'),
('en_produccion'),
('preparando_envio'),
('en_reparto'),
('entregado'),
('recogido'),
('cancelado');

-- =====================================================
-- HISTORIAL DE ESTADOS
-- =====================================================

CREATE TABLE historial_estado_pedido (
    id_historial INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    id_pedido INT UNSIGNED NOT NULL,

    id_estado INT UNSIGNED NOT NULL,

    fecha DATETIME
    NOT NULL DEFAULT CURRENT_TIMESTAMP,

    comentario TEXT,

    FOREIGN KEY (id_pedido)
        REFERENCES pedido(id_pedido)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    FOREIGN KEY (id_estado)
        REFERENCES estado_pedido(id_estado)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- =====================================================
-- TABLA ENVÍOS
-- =====================================================

CREATE TABLE envio (
    id_envio INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    id_pedido INT UNSIGNED NOT NULL,

    tipo ENUM(
        'domicilio',
        'recogida_tienda'
    ) NOT NULL,

    direccion_entrega TEXT,

    tienda_recogida VARCHAR(100),

    fecha_estimada DATETIME,

    fecha_entrega DATETIME,

    FOREIGN KEY (id_pedido)
        REFERENCES pedido(id_pedido)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- =====================================================
-- TABLA RESEÑAS
-- =====================================================

CREATE TABLE reseña (
    id_reseña INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    id_usuario INT UNSIGNED NOT NULL,

    id_mueble INT UNSIGNED NOT NULL,

    puntuacion INT
    NOT NULL
    CHECK (puntuacion BETWEEN 1 AND 5),

    comentario TEXT,

    fecha DATETIME
    NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (id_usuario)
        REFERENCES usuario(id_usuario)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    FOREIGN KEY (id_mueble)
        REFERENCES mueble(id_mueble)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- =====================================================
-- DATOS DE EJEMPLO
-- =====================================================

INSERT INTO categoria (nombre, descripcion)
VALUES
('sofás', 'Sofás de distintos tamaños'),
('mesas', 'Mesas de comedor y oficina'),
('sillas', 'Sillas para hogar y oficina');

INSERT INTO mueble (
    nombre,
    descripcion,
    precio,
    stock,
    id_categoria
)
VALUES
(
    'Sofá moderno',
    'Sofá gris de tres plazas',
    599.99,
    10,
    1
),
(
    'Mesa de roble',
    'Mesa de comedor grande',
    349.99,
    5,
    2
),
(
    'Silla ergonómica',
    'Silla cómoda para escritorio',
    129.99,
    20,
    3
);