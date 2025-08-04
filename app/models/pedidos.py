from ..utils.db import db


class Pedidos(db.Model):
    __tablename__ = 'Pedidos'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('Clientes.id'), nullable=False)
    fecha_pedido = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    fecha_entrega = db.Column(db.Date)
    estado = db.Column(db.Enum('pendiente', 'entregado', 'cancelado', name='estado_pedido'), default='pendiente')
    total = db.Column(db.Numeric(10, 2))

    detalles = db.relationship('DetallePedido', backref='pedido', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'fecha_pedido': self.fecha_pedido.isoformat() if self.fecha_pedido else None,
            'fecha_entrega': self.fecha_entrega.isoformat() if self.fecha_entrega else None,
            'estado': self.estado,
            'total': float(self.total) if self.total else None,
            'detalles': [detalle.to_dict() for detalle in self.detalles] if self.detalles else []
        }


class DetallePedido(db.Model):
    __tablename__ = 'Detalles_pedido'

    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('Pedidos.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('Productos.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False, default=1)
    precio_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)

    producto = db.relationship('Productos', backref='detalles', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'pedido_id': self.pedido_id,
            'producto_id': self.producto_id,
            'cantidad': self.cantidad,
            'precio_unitario': float(self.precio_unitario) if self.precio_unitario else None,
            'subtotal': float(self.subtotal) if self.subtotal else None,
            'producto': self.producto.to_dict() if self.producto else None
        } 