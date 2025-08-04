from ..utils.db import db


class Ingrediente(db.Model):
    __tablename__ = 'Ingredientes'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Numeric(10, 2), nullable=False)
    unidad_medida = db.Column(db.String(20), default='unidades')
    punto_reorden = db.Column(db.Numeric(10, 2), default=5.00)

    recetas = db.relationship('Receta', backref='ingrediente', lazy=True) 