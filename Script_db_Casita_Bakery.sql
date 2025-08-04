-- Creación de la base de datos
CREATE DATABASE IF NOT EXISTS Casita_Bakery;
USE Casita_Bakery;

-- Tabla de Clientes (actualizada con campo activo)
CREATE TABLE Clientes(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE
);

-- Tabla de Productos (solo postres)
CREATE TABLE Productos(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    descripcion TEXT,
    activo BOOLEAN DEFAULT TRUE
);

-- Tabla de Ingredientes (inventario básico)
CREATE TABLE Ingredientes(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    cantidad DECIMAL(10,2) NOT NULL,
    unidad_medida VARCHAR(20) DEFAULT 'unidades',
    punto_reorden DECIMAL(10,2) DEFAULT 5.00  -- Alerta de bajo stock
);

-- Tabla de Recetas (relación productos-ingredientes)
CREATE TABLE Recetas(
    producto_id INT NOT NULL,
    ingrediente_id INT NOT NULL,
    cantidad DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (producto_id, ingrediente_id),
    FOREIGN KEY (producto_id) REFERENCES Productos(id) ON DELETE CASCADE,
    FOREIGN KEY (ingrediente_id) REFERENCES Ingredientes(id) ON DELETE CASCADE
);

-- Tabla de Pedidos (con estados simplificados)
CREATE TABLE Pedidos(
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT NOT NULL,
    fecha_pedido DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_entrega DATE,
    estado ENUM('pendiente', 'entregado', 'cancelado') DEFAULT 'pendiente',
    total DECIMAL(10,2) DEFAULT 0.00,
    FOREIGN KEY (cliente_id) REFERENCES Clientes(id) ON DELETE RESTRICT
);

-- Tabla de Detalles de Pedido (corregida sintaxis)
CREATE TABLE Detalles_pedido(
    id INT AUTO_INCREMENT PRIMARY KEY,
    pedido_id INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL DEFAULT 1,
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (pedido_id) REFERENCES Pedidos(id) ON DELETE CASCADE,
    FOREIGN KEY (producto_id) REFERENCES Productos(id) ON DELETE RESTRICT
);

-- Tabla de Usuarios
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(128) NOT NULL
);

-- Índices para mejorar rendimiento
CREATE INDEX idx_clientes_nombre ON Clientes(nombre);
CREATE INDEX idx_clientes_activo ON Clientes(activo);
CREATE INDEX idx_productos_nombre ON Productos(nombre);
CREATE INDEX idx_productos_activo ON Productos(activo);
CREATE INDEX idx_pedidos_cliente ON Pedidos(cliente_id);
CREATE INDEX idx_pedidos_estado ON Pedidos(estado);
CREATE INDEX idx_pedidos_fecha ON Pedidos(fecha_pedido);
CREATE INDEX idx_detalles_pedido ON Detalles_pedido(pedido_id);
CREATE INDEX idx_detalles_producto ON Detalles_pedido(producto_id);
