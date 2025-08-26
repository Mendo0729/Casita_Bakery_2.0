from ..utils.db import db


class Receta(db.Model):
    __tablename__ = 'Recetas'

    producto_id = db.Column(db.Integer, db.ForeignKey('Productos.id'), primary_key=True)
    ingrediente_id = db.Column(db.Integer, db.ForeignKey('Ingredientes.id'), primary_key=True)
    cantidad = db.Column(db.Numeric(10, 2), nullable=False) 