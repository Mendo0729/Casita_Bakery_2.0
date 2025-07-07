
from app.models import Receta, Ingrediente
from app.utils.db import db

def obtener_por_producto(producto_id):
    return db.session.query(Receta, Ingrediente)\
        .join(Ingrediente, Receta.ingrediente_id == Ingrediente.id)\
        .filter(Receta.producto_id == producto_id)\
        .all()

def agregar_ingrediente_a_receta(producto_id, ingrediente_id, cantidad):
    existente = Receta.query.get((producto_id, ingrediente_id))
    if existente:
        return None  # O podrías lanzar una excepción o actualizar la cantidad
    nueva = Receta(
        producto_id=producto_id,
        ingrediente_id=ingrediente_id,
        cantidad=cantidad
    )
    db.session.add(nueva)
    db.session.commit()
    return nueva


def eliminar_ingrediente_de_receta(producto_id, ingrediente_id):
    receta = Receta.query.get((producto_id, ingrediente_id))
    if receta:
        db.session.delete(receta)
        db.session.commit()
    return receta

def actualizar_cantidad(producto_id, ingrediente_id, cantidad):
    receta = Receta.query.get((producto_id, ingrediente_id))
    if receta:
        receta.cantidad = cantidad
        db.session.commit()
    return receta
