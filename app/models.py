from .utils.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Clientes(db.Model):
    __tablename__ = 'Clientes'
    
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(100), nullable = False)
    fecha_registro = db.Column(db.DateTime, server_default = db.func.current_timestamp())

    pedidos = db.relationship('Pedidos', backref = 'cliente', lazy = True)

class Productos(db.Model):
    __tablename__ = 'Productos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    descripcion = db.Column(db.Text)
    activo = db.Column(db.Boolean, default=True)

    recetas = db.relationship('Receta', backref='producto', lazy=True)

class Ingrediente(db.Model):
    __tablename__ = 'Ingredientes'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Numeric(10, 2), nullable=False)
    unidad_medida = db.Column(db.String(20), default='unidades')
    punto_reorden = db.Column(db.Numeric(10, 2), default=5.00)

    recetas = db.relationship('Receta', backref='ingrediente', lazy=True)

class Receta(db.Model):
    __tablename__ = 'Recetas'

    producto_id = db.Column(db.Integer, db.ForeignKey('Productos.id'), primary_key=True)
    ingrediente_id = db.Column(db.Integer, db.ForeignKey('Ingredientes.id'), primary_key=True)
    cantidad = db.Column(db.Numeric(10, 2), nullable=False)


class Pedidos(db.Model):
    __tablename__ = 'Pedidos'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('Clientes.id'), nullable=False)
    fecha_pedido = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    fecha_entrega = db.Column(db.Date)
    estado = db.Column(db.Enum('pendiente', 'entregado', 'cancelado', name='estado_pedido'), default='pendiente')
    total = db.Column(db.Numeric(10, 2))

    detalles = db.relationship('DetallePedido', backref='pedido', lazy=True)



class DetallePedido(db.Model):
    __tablename__ = 'Detalles_pedido'

    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('Pedidos.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('Productos.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False, default=1)
    precio_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)

    producto = db.relationship('Productos', backref='detalles', lazy=True)


class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

