from decimal import Decimal, InvalidOperation
import logging

from sqlalchemy.exc import SQLAlchemyError

from app.models import Productos
from app.utils.create_responses import create_response as response
from app.utils.db import db

logger = logging.getLogger(__name__)

def obtener_todos(pagina=1, por_pagina=10, buscar=None):
    try:
        query = Productos.query.filter(Productos.activo == True)

        if buscar:
            query = query.filter(Productos.nombre.ilike(f"%{buscar}%"))

        query = query.order_by(Productos.id.desc())
        paginacion = query.paginate(page=pagina, per_page=por_pagina, error_out=False)

        if not paginacion.items:
            logger.info("No hay productos para esta búsqueda/página")
            return response(
                success=True,
                data={
                    "productos": [],
                    "pagina": paginacion.page,
                    "por_pagina": paginacion.per_page,
                    "total_paginas": paginacion.pages,
                    "total_productos": paginacion.total
                },
                message="No hay productos en esta página o búsqueda",
                status_code=200
            )

        productos_data = [p.to_dict() for p in paginacion.items]

        return response(
            success=True,
            data={
                "productos": productos_data,
                "pagina": paginacion.page,
                "por_pagina": paginacion.per_page,
                "total_paginas": paginacion.pages,
                "total_productos": paginacion.total
            },
            message=f"Página {paginacion.page} de {paginacion.pages}",
            status_code=200
        )

        
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al obtener los productos: {str(e)}")
        return response(
            success=False,
            message="Error al obtener los productos",
            errors={
                "code": "database_error",
                "detail": "Error en la base de datos"
            },
            status_code=500
        )
    except Exception as e:
        logger.error(f"Error inesperado al obtener los productos: {str(e)}")
        return response(
            success=False,
            message="Error al obtener los productos",
            errors={
                "code": "internal_server_error",
                "detail": "Error interno del servidor"
            },
            status_code=500
        )

#-------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------------

def obtener_por_id(producto_id):

    try:
        if not isinstance(producto_id, int) or producto_id <= 0:
            logger.warning(f"ID inválido recibido: {producto_id}")
            return response(
                success=False,
                message="ID de producto inválido",
                errors={
                    "code": "invalid_input",
                    "detail": "El ID debe ser un entero positivo"
                },
                status_code=400
            )

        producto = Productos.query.filter(Productos.id == producto_id, Productos.activo == True).first()

        if not producto:
            logger.info(f"Producto no encontrado con ID: {producto_id}")
            return response(
                success=False,
                message="Producto no encontrado",
                errors={
                    "code": "not_found",
                    "detail": f"No existe producto con ID {producto_id}"
                },
                status_code=404
            )

        logger.info(f"Producto encontrado - ID: {producto_id}")
        return response(
            success=True,
            data=producto.to_dict(),
            message="Producto obtenido correctamente",
            status_code=200
        )

    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al buscar producto ID {producto_id}: {str(e)}")
        return response(
            success=False,
            message="Error en la base de datos",
            errors={
                "code": "database_error",
                "detail": "No se pudo completar la búsqueda"
            },
            status_code=500
        )
    except Exception as e:
        logger.error(f"Error inesperado al buscar producto ID {producto_id}: {str(e)}")
        return response(
            success=False,
            message="Error interno del servidor",
            errors={
                "code": "internal_server_error",
                "detail": "Ocurrió un error inesperado"
            },
            status_code=500
        )


#---------------------------------------------------------------------------------------------------------------

def crear_producto(data):
    try:
        if not data or not isinstance(data, dict):
            logger.warning("Datos de producto inválidos")
            return response(
                success=False,
                message="Datos de producto inválidos",
                errors={
                    "code": "invalid_input",
                    "detail": "Se esperaba un diccionario con los datos del producto"
                },
                status_code=400
            )

        nombre = data.get("nombre", "").strip()
        precio_raw = data.get("precio")

        if not nombre or not isinstance(nombre, str) or len(nombre) > 100:
            logger.warning(f"Nombre inválido: {nombre}")
            return response(
                success=False,
                message="Nombre de producto inválido",
                errors={
                    "code": "invalid_input",
                    "detail": "El nombre debe ser una cadena no vacía (máx 100 caracteres)"
                },
                status_code=400
            )

        try:
            precio = Decimal(str(precio_raw))
            if precio <= 0:
                logger.warning(f"Precio menor o igual a cero: {precio_raw}")
                return response(
                    success=False,
                    message="Precio inválido",
                    errors={
                        "code": "invalid_input",
                        "detail": "El precio debe ser un número decimal mayor a 0"
                    },
                    status_code=400
                )
        except (InvalidOperation, TypeError):
            logger.warning(f"Precio no válido: {precio_raw}")
            return response(
                success=False,
                message="Precio inválido",
                errors={
                    "code": "invalid_input",
                    "detail": "El precio debe ser un número decimal válido"
                },
                status_code=400
            )

        if Productos.query.filter(Productos.nombre.ilike(nombre)).first():
            logger.warning(f"Intento de crear producto existente: {nombre}")
            return response(
                success=False,
                message="El producto ya existe",
                errors={
                    "code": "already_exists",
                    "detail": f"Ya existe un producto con el nombre '{nombre}'"
                },
                status_code=409
            )

        nuevo_producto = Productos(
            nombre=nombre,
            precio=precio,
            activo=True
        )

        db.session.add(nuevo_producto)
        db.session.commit()

        logger.info(f"Producto creado exitosamente: {nombre}")
        return response(
            success=True,
            data=nuevo_producto.to_dict(),
            message="Producto creado exitosamente",
            status_code=201
        )

    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Error de base de datos al crear producto: {str(e)}")
        return response(
            success=False,
            message="Error al guardar el producto",
            errors={
                "code": "database_error",
                "detail": "Error al guardar en la base de datos"
            },
            status_code=500
        )
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error inesperado al crear producto: {str(e)}")
        return response(
            success=False,
            message="Error interno del servidor",
            errors={
                "code": "internal_server_error",
                "detail": "Ocurrió un error inesperado al crear el producto"
            },
            status_code=500
        )

#----------------------------------------------------------------------------------------------------------------------------------

def actualizar_producto(producto_id, data):
    try:
        if not isinstance(producto_id, int) or producto_id <= 0:
            logger.warning(f"ID inválido recibido: {producto_id}")
            return response(
                success=False,
                message="ID de producto inválido",
                errors={
                    "code": "invalid_input",
                    "detail": "El ID debe ser un entero positivo"
                },
                status_code=400
            )

        if not data or not isinstance(data, dict):
            logger.warning("Datos de producto inválidos")
            return response(
                success=False,
                message="Datos de producto inválidos",
                errors={
                    "code": "invalid_input",
                    "detail": "Se esperaba un diccionario con los datos del producto"
                },
                status_code=400
            )

        producto = Productos.query.get(producto_id)
        if not producto:
            logger.warning(f"Producto no encontrado con ID: {producto_id}")
            return response(
                success=False,
                message="Producto no encontrado",
                errors={
                    "code": "not_found",
                    "detail": f"No se encontró un producto con ID {producto_id}"
                },
                status_code=404
            )

        # --- Validaciones y actualizaciones parciales ---
        if "nombre" in data:
            nombre = str(data["nombre"]).strip()
            if not nombre or len(nombre) > 100:
                logger.warning(f"Nombre inválido: {nombre}")
                return response(
                    success=False,
                    message="Nombre de producto inválido",
                    errors={
                        "code": "invalid_input",
                        "detail": "El nombre debe ser una cadena no vacía (máx 100 caracteres)"
                    },
                    status_code=400
                )

            # Verificar duplicados si se cambió el nombre
            if Productos.query.filter(Productos.nombre.ilike(nombre), Productos.id != producto_id).first():
                logger.warning(f"Ya existe otro producto con el nombre: {nombre}")
                return response(
                    success=False,
                    message="El producto ya existe",
                    errors={
                        "code": "already_exists",
                        "detail": f"Ya existe otro producto con el nombre '{nombre}'"
                    },
                    status_code=409
                )

            producto.nombre = nombre

        if "precio" in data:
            precio_raw = data["precio"]
            try:
                precio = Decimal(str(precio_raw))
                if precio <= 0:
                    logger.warning(f"Precio menor o igual a cero: {precio_raw}")
                    return response(
                        success=False,
                        message="Precio inválido",
                        errors={
                            "code": "invalid_input",
                            "detail": "El precio debe ser un número decimal mayor a 0"
                        },
                        status_code=400
                    )
                producto.precio = precio
            except (InvalidOperation, TypeError):
                logger.warning(f"Precio no válido: {precio_raw}")
                return response(
                    success=False,
                    message="Precio inválido",
                    errors={
                        "code": "invalid_input",
                        "detail": "El precio debe ser un número decimal válido"
                    },
                    status_code=400
                )

        if "descripcion" in data:
            producto.descripcion = str(data["descripcion"]).strip()

        if "activo" in data:
            producto.activo = bool(data["activo"])

        # --- Guardar cambios ---
        db.session.commit()

        logger.info(f"Producto actualizado exitosamente: ID {producto_id}")
        return response(
            success=True,
            data=producto.to_dict(),
            message="Producto actualizado exitosamente",
            status_code=200
        )

    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Error de base de datos al actualizar producto: {str(e)}")
        return response(
            success=False,
            message="Error al actualizar el producto",
            errors={
                "code": "database_error",
                "detail": "Error al guardar en la base de datos"
            },
            status_code=500
        )
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error inesperado al actualizar producto: {str(e)}")
        return response(
            success=False,
            message="Error interno del servidor",
            errors={
                "code": "internal_server_error",
                "detail": "Ocurrió un error inesperado al actualizar el producto"
            },
            status_code=500
        )


#----------------------------------------------------------------------------------------------------------------------------------

def eliminar(producto_id):

    try:
        if not isinstance(producto_id, int) or producto_id <= 0:
            logger.warning(f"ID inválido recibido: {producto_id}")
            return response(
                success=False,
                message="ID de producto inválido",
                errors={
                    "code": "invalid_input",
                    "detail": "El ID debe ser un entero positivo"
                },
                status_code=400
            )

        producto = Productos.query.get(producto_id)
        if not producto:
            logger.warning(f"Producto no encontrado con ID: {producto_id}")
            return response(
                success=False,
                message="Producto no encontrado",
                errors={
                    "code": "not_found",
                    "detail": f"No se encontró un producto con ID {producto_id}"
                },
                status_code=404
            )

        db.session.delete(producto)
        db.session.commit()

        logger.info(f"Producto eliminado exitosamente - ID: {producto_id}")
        return response(
            success=True,
            data={"id": producto_id},
            message="Producto eliminado exitosamente",
            status_code=200 
        )
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Error inesperado al eliminar al producto {producto_id}: {str(e)}")
        return response(
            success=False,
            message="Error al eliminar al producto",
            errors={
                "code": "database_error",
                "detail": "Error en la base de datos"
                },
            status_code=500
        )

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error inesperado al eliminar al producto {producto_id}: {str(e)}")
        return response(
            success=False,
            message="Error interno del servidor",
            errors={
                "code": "server_error",
                "detail": "Error al procesar la solicitud"
            },
            status_code=500
        )
