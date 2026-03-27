USE Casita_Bakery;

SET FOREIGN_KEY_CHECKS = 0;

TRUNCATE TABLE detalles_pedido;
TRUNCATE TABLE recetas;
TRUNCATE TABLE pedidos;
TRUNCATE TABLE ingredientes;
TRUNCATE TABLE productos;
TRUNCATE TABLE clientes;

SET FOREIGN_KEY_CHECKS = 1;

INSERT INTO clientes (nombre, activo) VALUES
('Ana Martinez', TRUE),
('Carlos Rivera', TRUE),
('Lucia Gomez', TRUE),
('Pedro Santos', TRUE),
('Mariana Lopez', TRUE);

INSERT INTO productos (nombre, precio, descripcion, activo) VALUES
('Cheesecake de Fresa', 18.50, 'Cheesecake artesanal con topping de fresa', TRUE),
('Brownie de Chocolate', 4.25, 'Brownie humedo con chocolate semiamargo', TRUE),
('Cupcake Vainilla', 3.75, 'Cupcake suave con buttercream de vainilla', TRUE),
('Tarta de Limon', 16.00, 'Tarta fresca con crema de limon', TRUE),
('Galletas de Mantequilla', 2.10, 'Galleta clasica crocante', TRUE);

INSERT INTO ingredientes (nombre, cantidad, unidad_medida, punto_reorden) VALUES
('Harina', 50.00, 'kg', 10.00),
('Azucar', 35.00, 'kg', 8.00),
('Mantequilla', 20.00, 'kg', 5.00),
('Huevos', 180.00, 'unidades', 30.00),
('Chocolate', 12.00, 'kg', 4.00),
('Fresas', 10.00, 'kg', 3.00),
('Limon', 9.00, 'kg', 3.00),
('Queso Crema', 14.00, 'kg', 4.00),
('Vainilla', 3.00, 'litros', 1.00);

INSERT INTO recetas (producto_id, ingrediente_id, cantidad) VALUES
(1, 1, 1.20),
(1, 2, 0.80),
(1, 6, 0.60),
(1, 8, 1.00),
(2, 1, 0.40),
(2, 2, 0.25),
(2, 3, 0.20),
(2, 5, 0.50),
(3, 1, 0.25),
(3, 2, 0.15),
(3, 3, 0.10),
(3, 4, 2.00),
(3, 9, 0.05),
(4, 1, 0.70),
(4, 2, 0.40),
(4, 3, 0.25),
(4, 7, 0.35),
(5, 1, 0.20),
(5, 2, 0.10),
(5, 3, 0.12);

INSERT INTO pedidos (cliente_id, fecha_entrega, estado, total) VALUES
(1, DATE_ADD(CURDATE(), INTERVAL 2 DAY), 'pendiente', 26.00),
(2, DATE_ADD(CURDATE(), INTERVAL 1 DAY), 'entregado', 24.50),
(3, DATE_ADD(CURDATE(), INTERVAL 3 DAY), 'pendiente', 16.40);

INSERT INTO detalles_pedido (pedido_id, producto_id, cantidad, precio_unitario, subtotal) VALUES
(1, 1, 1, 18.50, 18.50),
(1, 3, 2, 3.75, 7.50),
(2, 2, 2, 4.25, 8.50),
(2, 4, 1, 16.00, 16.00),
(3, 5, 4, 2.10, 8.40),
(3, 3, 1, 3.75, 3.75),
(3, 2, 1, 4.25, 4.25);
