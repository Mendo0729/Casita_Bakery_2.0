from app.models import Productos
from app.utils.db import db
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import BadRequest, NotFound
from decimal import Decimal

def obtener_todos():
    return Productos.query.filter(Productos.activo == True).order_by(Productos.id.desc()).all()

def obtener_por_nombre(nombre):
    return Productos.query.filter(Productos.nombre.ilike(f"%{nombre}%")).all()

#-------------------------------------------------------------------------------------------------------------

def obtener_por_id(producto_id):
    producto = Productos.query.get(producto_id)
    if not producto:
        raise NotFound("Producto no encontrado")
    return producto

#---------------------------------------------------------------------------------------------------------------

def crear(data):
    
    try:
        nombre = data.get("nombre", "").strip()
        precio = data.get("precio")
        descripcion = data.get("descripcion", "").strip()
        if not nombre:
            raise BadRequest("El nombre del producto es obligatorio")
        
        if Productos.query.filter(Productos.nombre.ilike(nombre), Productos.activo==True).first():
            raise BadRequest("Ya existe un producto activo con ese nombre")
        
        try:
            precio = Decimal(str(precio))
            if precio <= 0:
                raise ValueError
        except (ValueError, TypeError):
            raise BadRequest("El precio debe ser un número positivo")
        

        nuevo_producto = Productos(
            nombre=nombre,
            precio=precio,
            descripcion=descripcion
        )

        db.session.add(nuevo_producto)
        db.session.commit()
        return nuevo_producto
    
    except SQLAlchemyError as e:
        db.session.rollback()
        raise BadRequest("No se pudo crear el producto") from e

#----------------------------------------------------------------------------------------------------------------------------------

def actualizar(producto_id, datos):
    try:
        producto = obtener_por_id(producto_id)
        
        # Validar nombre
        nuevo_nombre = datos.get("nombre", "").strip()
        if not nuevo_nombre:
            raise BadRequest("El nombre no puede estar vacío")
        producto.nombre = nuevo_nombre
        
        # Validar precio
        if "precio" in datos:
            try:
                nuevo_precio = Decimal(str(datos["precio"]))
                if nuevo_precio <= 0:
                    raise ValueError
                producto.precio = nuevo_precio
            except (ValueError, TypeError):
                raise BadRequest("El precio debe ser un número positivo")
        
        producto.descripcion = datos.get("descripcion", producto.descripcion).strip()
        
        db.session.commit()
        return producto
    except SQLAlchemyError as e:
        db.session.rollback()
        raise BadRequest(f"Error al actualizar producto: {str(e)}") from e

#----------------------------------------------------------------------------------------------------------------------------------

def eliminar(producto_id):
    try:
        producto = obtener_por_id(producto_id)
        if not producto:
            raise ValueError("Producto no encontrado")
        producto.activo = False
        db.session.commit()
        return producto  # <- necesario
    except SQLAlchemyError as e:
        db.session.rollback()
        raise BadRequest("No se pudo eliminar el producto") from e
