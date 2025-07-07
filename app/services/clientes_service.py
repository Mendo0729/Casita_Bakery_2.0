from app.models import Clientes
from app.utils.db import db
from sqlalchemy.exc import SQLAlchemyError

def obtener_todos():
    return Clientes.query.order_by(Clientes.fecha_registro.desc()).all()

def buscar_por_nombre(nombre):
    return Clientes.query.filter(Clientes.nombre.ilike(f"%{nombre}%")).all()

#-----------------------------------------------------------------------------------------

def obtener_cliente_por_id(cliente_id):
    return Clientes.query.get(cliente_id)

#------------------------------------------------------------------------------------------

def crear_cliente(data):

    nombre = data.get('nombre', '').strip()

    if not nombre:
        raise ValueError("El nombre no puede estar vacio")
    
    if Clientes.query.filter(Clientes.nombre.ilike(nombre)).first():
        raise ValueError("Ya existe un cliente con ese nombre")
    
    try:
        nuevo_cliente = Clientes(nombre=nombre)
        db.session.add(nuevo_cliente)
        db.session.commit()
        return nuevo_cliente
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Error al crear cliente: {str(e)}")
    
#----------------------------------------------------------------------

def actualizar_cliente(cliente_id, data):
    cliente = Clientes.query.get(cliente_id)

    if not cliente:
        raise ValueError("Cliente no encontrado")
    
    nuevo_nombre = data.get('nombre', '').strip()
    if not nuevo_nombre:
        raise ValueError("El nombre no puede estar vacío")

    try:
        cliente.nombre = nuevo_nombre
        db.session.commit()
        return cliente
    except SQLAlchemyError as e:
        db.session.rollback()
        raise Exception(f"Error de base de datos: {str(e)}")
    
#-----------------------------------------------------------------------------

def eliminar_cliente(cliente_id):
    cliente = Clientes.query.get(cliente_id)
    if cliente:
        db.session.delete(cliente)
        db.session.commit()
    return cliente
