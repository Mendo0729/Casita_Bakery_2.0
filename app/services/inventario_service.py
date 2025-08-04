from sqlalchemy.exc import SQLAlchemyError
from app.models import Ingrediente
from app.utils.db import db
from decimal import Decimal

def obtener_todos():

    try:
        pass
    except SQLAlchemyError as e:
        pass
    except Exception as e:
        pass
    return Ingrediente.query.order_by(Ingrediente.nombre).all()

def obtener_por_id(ingrediente_id):
    return Ingrediente.query.get(ingrediente_id)


def crear(data):

    try:
        pass
    except SQLAlchemyError as e:
        pass
    except Exception as e:
        pass

    nuevo = Ingrediente(
        nombre=data['nombre'],
        cantidad=Decimal(data['cantidad']),
        unidad_medida=data.get('unidad_medida', 'unidades'),
        punto_reorden=Decimal(data.get('punto_reorden', 5.00))
    )
    db.session.add(nuevo)
    db.session.commit()
    return nuevo

def actualizar(ingrediente_id, data):

    try:
        pass
    except SQLAlchemyError as e:
        pass
    except Exception as e:
        pass

    ingrediente = Ingrediente.query.get(ingrediente_id)
    if ingrediente:
        ingrediente.nombre = data['nombre']
        ingrediente.cantidad = Decimal(data['cantidad'])
        ingrediente.unidad_medida = data.get('unidad_medida', ingrediente.unidad_medida)
        ingrediente.punto_reorden = Decimal(data.get('punto_reorden', ingrediente.punto_reorden))
        db.session.commit()
    return ingrediente

def eliminar(ingrediente_id):
    
    try:
        pass
    except SQLAlchemyError as e:
        pass
    except Exception as e:
        pass

    ingrediente = Ingrediente.query.get(ingrediente_id)
    if ingrediente:
        db.session.delete(ingrediente)
        db.session.commit()
    return ingrediente
