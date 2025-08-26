from ..utils.db import db


class Productos(db.Model):
    __tablename__ = 'Productos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    descripcion = db.Column(db.Text)
    activo = db.Column(db.Boolean, default=True)

    recetas = db.relationship('Receta', backref='producto', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'precio': float(self.precio) if self.precio else None,
            'descripcion': self.descripcion,
            'activo': self.activo
        } 