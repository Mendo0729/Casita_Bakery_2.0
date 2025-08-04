from ..utils.db import db


class Clientes(db.Model):
    __tablename__ = 'Clientes'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    fecha_registro = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    activo = db.Column(db.Boolean, default=True)

    pedidos = db.relationship('Pedidos', backref='cliente', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None,
            'activo': self.activo
        } 