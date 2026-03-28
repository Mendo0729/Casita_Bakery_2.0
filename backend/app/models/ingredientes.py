from ..utils.db import db

class Ingrediente(db.Model):
    __tablename__ = 'ingredientes'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Numeric(10, 2), nullable=False)
    unidad_medida = db.Column(db.String(20), default='unidades')
    punto_reorden = db.Column(db.Numeric(10, 2), default=5.00)

    recetas = db.relationship(
        "Receta",
        backref="ingrediente",
        lazy=True,
        passive_deletes=True,
    )

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "cantidad": float(self.cantidad),  # lo convertimos a float porque Decimal no se serializa bien
            "unidad_medida": self.unidad_medida,
            "punto_reorden": float(self.punto_reorden)
        }
