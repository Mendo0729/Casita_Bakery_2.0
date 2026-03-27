-- Creación de la base de datos
CREATE DATABASE IF NOT EXISTS Casita_Bakery;
USE Casita_Bakery;

-- Tabla de Clientes (actualizada con campo activo)
CREATE TABLE clientes(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE
);

-- Tabla de Productos (solo postres)
CREATE TABLE productos(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    descripcion TEXT,
    activo BOOLEAN DEFAULT TRUE
);

-- Tabla de Ingredientes (inventario básico)
CREATE TABLE ingredientes(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    cantidad DECIMAL(10,2) NOT NULL,
    unidad_medida VARCHAR(20) DEFAULT 'unidades',
    punto_reorden DECIMAL(10,2) DEFAULT 5.00  -- Alerta de bajo stock
);

-- Tabla de Recetas (relación productos-ingredientes)
CREATE TABLE recetas(
    producto_id INT NOT NULL,
    ingrediente_id INT NOT NULL,
    cantidad DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (producto_id, ingrediente_id),
    FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE,
    FOREIGN KEY (ingrediente_id) REFERENCES ingredientes(id) ON DELETE CASCADE
);

-- Tabla de Pedidos (con estados simplificados)
CREATE TABLE pedidos(
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT NOT NULL,
    fecha_pedido DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_entrega DATE,
    estado ENUM('pendiente', 'entregado', 'cancelado') DEFAULT 'pendiente',
    total DECIMAL(10,2) DEFAULT 0.00,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE RESTRICT
);

-- Tabla de Detalles de Pedido (corregida sintaxis)
CREATE TABLE detalles_pedido(
    id INT AUTO_INCREMENT PRIMARY KEY,
    pedido_id INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL DEFAULT 1,
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id) ON DELETE CASCADE,
    FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE RESTRICT
);

-- Tabla de Usuarios
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(256) NOT NULL
);

-- Índices para mejorar rendimiento
CREATE INDEX idx_clientes_nombre ON clientes(nombre);
CREATE INDEX idx_clientes_activo ON clientes(activo);
CREATE INDEX idx_productos_nombre ON productos(nombre);
CREATE INDEX idx_productos_activo ON productos(activo);
CREATE UNIQUE INDEX uq_ingredientes_nombre ON ingredientes(nombre);
CREATE INDEX idx_pedidos_cliente ON pedidos(cliente_id);
CREATE INDEX idx_pedidos_estado ON pedidos(estado);
CREATE INDEX idx_pedidos_fecha ON pedidos(fecha_pedido);
CREATE INDEX idx_detalles_pedido ON detalles_pedido(pedido_id);
CREATE INDEX idx_detalles_producto ON detalles_pedido(producto_id);
