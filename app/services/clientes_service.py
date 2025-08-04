import logging

from sqlalchemy.exc import SQLAlchemyError

from app.models import Clientes
from app.utils.create_responses import create_response as response
from app.utils.db import db

logger = logging.getLogger(__name__)

def obtener_todos(pagina=1, por_pagina=10, buscar=None):

    try:

        try:
            pagina = int(pagina)
            por_pagina = int(por_pagina)
            if pagina <= 0:
                logger.warning(f"Número de página inválido: {pagina}. Se ajusta a 1.")
                pagina = 1
            if por_pagina <= 0 or por_pagina > 100:
                logger.warning(f"Cantidad por página inválida: {por_pagina}. Se ajusta a 10.")
                por_pagina = 10
        except (ValueError, TypeError) as e:
            logger.warning(f"Error de tipo en parámetros de paginación: {str(e)}. Se usan valores por defecto.")
            pagina = 1
            por_pagina = 10


        query = Clientes.query.filter(Clientes.activo == True)

        if buscar:
            query = query.filter(Clientes.nombre.ilike(f"%{buscar}%"))

        query = query.order_by(Clientes.id.desc())
        paginacion = query.paginate(page=pagina, per_page=por_pagina, error_out=False)

        if not paginacion.items:
            logger.info("No hay clientes para esta búsqueda/página")
            return response(
                success=True,
                data={
                    "clientes": [],
                    "pagina": paginacion.page,
                    "por_pagina": paginacion.per_page,
                    "total_paginas": paginacion.pages,
                    "total_clientes": paginacion.total
                },
                message="No hay clientes en esta página o búsqueda",
                status_code=200
            )

        clientes_data = [c.to_dict() for c in paginacion.items]

        return response(
            success=True,
            data={
                "clientes": clientes_data,
                "pagina": paginacion.page,
                "por_pagina": paginacion.per_page,
                "total_paginas": paginacion.pages,
                "total_clientes": paginacion.total
            },
            message=f"Página {paginacion.page} de {paginacion.pages}",
            status_code=200
        )

    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al obtener clientes: {str(e)}")
        return response(
            success=False,
            message="Error al obtener los clientes",
            errors={
                "code": "database_error",
                "detail": "Error en la base de datos"
            },
            status_code=500
        )
    except Exception as e:
        logger.error(f"Error inesperado al obtener clientes: {str(e)}")
        return response(
            success=False,
            message="Error al obtener los clientes",
            errors={
                "code": "internal_server_error",
                "detail": "Error interno del servidor"
            },
            status_code=500
        )


#-----------------------------------------------------------------------------------------

def obtener_cliente_modelo_por_id(cliente_id):
    """Retorna el objeto Cliente si existe, de lo contrario None."""
    if not isinstance(cliente_id, int) or cliente_id <= 0:
        logger.warning(f"ID inválido recibido: {cliente_id}")
        return None
    return Clientes.query.get(cliente_id)

def obtener_cliente_por_id(cliente_id):
    try:
        cliente = obtener_cliente_modelo_por_id(cliente_id)

        if not cliente:
            logger.info(f"Cliente no encontrado con ID: {cliente_id}")
            return response(
                success=False,
                message="Cliente no encontrado",
                errors={
                    "code": "not_found",
                    "detail": f"No existe cliente con ID {cliente_id}"
                },
                status_code=404
            )

        return response(
            success=True,
            data=cliente.to_dict(),
            message="Cliente obtenido correctamente",
            status_code=200
        )

    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al buscar cliente ID {cliente_id}: {str(e)}")
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
        logger.error(f"Error inesperado al buscar cliente ID {cliente_id}: {str(e)}")
        return response(
            success=False,
            message="Error interno del servidor",
            errors={
                "code": "internal_server_error",
                "detail": "Ocurrió un error inesperado"
            },
            status_code=500
        )


#------------------------------------------------------------------------------------------

def crear_cliente(data):
    
    try:
        if not data or not isinstance(data, dict):
            logger.warning("Datos de cliente inválidos")
            return response(
                success=False,
                message="Datos de cliente inválidos",
                errors={
                    "code": "invalid_input",
                    "detail": "Se esperaba un diccionario con los datos del cliente"
                },
                status_code=400
            )

        nombre = data.get('nombre', '').strip()
        
        if not nombre or not isinstance(nombre, str) or len(nombre) > 100:
            logger.warning(f"Nombre inválido: {nombre}")
            return response(
                success=False,
                message="Nombre de cliente inválido",
                errors={
                    "code": "invalid_input",
                    "detail": "El nombre debe ser una cadena no vacía (máx 100 caracteres)"
                },
                status_code=400
            )


        if Clientes.query.filter(Clientes.nombre.ilike(nombre)).first():
            logger.warning(f"Intento de crear cliente existente: {nombre}")
            return response(
                success=False,
                message="El cliente ya existe",
                errors={
                    "code": "already_exists",
                    "detail": f"Ya existe un cliente con el nombre '{nombre}'"
                },
                status_code=409  
            )
        
        # Crear nuevo cliente
        nuevo_cliente = Clientes(
            nombre=nombre,
            # Añadir otros campos aquí
            # email=data.get('email'),
            # telefono=data.get('telefono')
        )
        
        db.session.add(nuevo_cliente)
        db.session.commit()

        logger.info(f"Cliente creado exitosamente: {nombre}")
        return response(
            success=True,
            data=nuevo_cliente.to_dict(),
            message="Cliente creado exitosamente",
            status_code=201
        )

    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Error de base de datos al crear cliente: {str(e)}")
        return response(
            success=False,
            message="Error al guardar el cliente",
            errors={
                "code": "database_error",
                "detail": "Error al guardar en la base de datos"
            },
            status_code=500
        )
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error inesperado al crear cliente: {str(e)}")
        return response(
            success=False,
            message="Error interno del servidor",
            errors={
                "code": "internal_server_error",
                "detail": "Ocurrió un error inesperado al crear el cliente"
            },
            status_code=500
        )

#----------------------------------------------------------------------

def actualizar_cliente(cliente_id, data):

    try:

        if not isinstance(cliente_id, int) or cliente_id <= 0:
            logger.warning(f"ID inválido recibido: {cliente_id}")
            return response(
                success=False,
                message="ID de cliente inválido",
                errors={
                    "code": "invalid_input",
                    "detail": "El ID debe ser un entero positivo"
                },
                status_code=400
            )
        
        cliente = Clientes.query.get(cliente_id)
        if not cliente:
            logger.info(f"Cliente no encontrado con ID: {cliente_id}")
            return response(
                success=False,
                message="Cliente no encontrado",
                errors={
                    "code": "not_found",
                    "detail": f"No existe cliente con ID {cliente_id}"
                },
                status_code=404
            )
    
        nuevo_nombre = data.get('nombre', '').strip()
        if not nuevo_nombre or not isinstance(nuevo_nombre, str) or len(nuevo_nombre) > 100:
            logger.warning(f"Nombre inválido: {nuevo_nombre}")
            return response(
                success=False,
                message="Nombre de cliente inválido",
                errors={
                    "code": "invalid_input",
                    "detail": "El nombre debe ser una cadena no vacía (máx 100 caracteres)"
                },
                status_code=400
            )

        if (Clientes.query
                .filter(Clientes.nombre.ilike(nuevo_nombre))
                .filter(Clientes.id != cliente_id)
                .first()):
            logger.warning(f"Intento de actualizar a nombre existente: {nuevo_nombre}")
            return response(
                success=False,
                message="Nombre no disponible",
                errors={
                    "code": "already_exists",
                    "detail": f"Ya existe otro cliente con el nombre '{nuevo_nombre}'"
                },
                status_code=409
            )

        cliente.nombre = nuevo_nombre
        db.session.commit()

        logger.info(f"Cliente {cliente_id} actualizado correctamente")
        return response(
            success=True,
            data=cliente.to_dict(),
            message="Cliente actualizado correctamente",
            status_code=200 
        )

    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Error de BD al actualizar cliente {cliente_id}: {str(e)}")
        return response(
            success=False,
            message="Error al actualizar el cliente",
            errors={
                "code": "database_error",
                "detail": "Error en la base de datos"
            },
            status_code=500
        )

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error inesperado al actualizar cliente {cliente_id}: {str(e)}")
        return response(
            success=False,
            message="Error interno del servidor",
            errors={
                "code": "server_error",
                "detail": "Error al procesar la solicitud"
            },
            status_code=500
        )
#-----------------------------------------------------------------------------

def eliminar_cliente(cliente_id):

    try:
        if not isinstance(cliente_id, int) or cliente_id <= 0:
            logger.warning(f"ID inválido recibido: {cliente_id}")
            return response(
                success=False,
                message="ID de cliente inválido",
                errors={
                    "code": "invalid_input",
                    "detail": "El ID debe ser un entero positivo"
                },
                status_code=400
            )

        cliente = Clientes.query.get(cliente_id)
        if not cliente:
            logger.info(f"Cliente no encontrado con ID: {cliente_id}")
            return response(
                success=False,
                message="Cliente no encontrado",
                errors={
                    "code": "not_found",
                    "detail": f"No existe cliente con ID {cliente_id}"
                },
                status_code=404
            )

        db.session.delete(cliente)
        db.session.commit()
        
        logger.info(f"Cliente eliminado exitosamente - ID: {cliente_id}")
        return response(
            success=True,
            data={"id": cliente_id},
            message="Cliente eliminado exitosamente",
            status_code=204 
        )

    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Error inesperado al eliminar al cliente {cliente_id}: {str(e)}")
        return response(
            success=False,
            message="Error al eliminar al cliente",
            errors={
                "code": "database_error",
                "detail": "Error en la base de datos"
                },
            status_code=500
        )

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error inesperado al eliminar al cliente {cliente_id}: {str(e)}")
        return response(
            success=False,
            message="Error interno del servidor",
            errors={
                "code": "server_error",
                "detail": "Error al procesar la solicitud"
            },
            status_code=500
        )
