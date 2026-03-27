from ..utils.db import db


class Receta(db.Model):
    __tablename__ = 'recetas'

    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), primary_key=True)
    ingrediente_id = db.Column(db.Integer, db.ForeignKey('ingredientes.id'), primary_key=True)
    cantidad = db.Column(db.Numeric(10, 2), nullable=False) 
