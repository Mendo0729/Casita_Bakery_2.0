import logging

from sqlalchemy.exc import SQLAlchemyError

from app.models import Clientes
from app.utils.create_responses import create_response as response
from app.utils.db import db


def obtener_todos():

    try:
        clientes = Clientes.query.order_by(Clientes.nombre.asc()).all()
        
        if not clientes:
            logging.info("No hay clientes registrados en la base de datos")
            return response(
                success=True,
                data=[],
                message="No hay clientes registrados",
                status_code=200
            )

        serializacion_clientes = [cliente.to_dict() for cliente in clientes]

        logging.info(f"Se obtuvieron {len(clientes)} clientes correctamente")
        return response(
            success=True,
            data=serializacion_clientes,
            message="Clientes obtenidos correctamente",
            status_code=200
        )

    except SQLAlchemyError as e:
        logging.error(f"Error de base de datos al obtener clientes: {str(e)}")
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
        logging.error(f"Error inesperado al obtener clientes: {str(e)}")
        return response(
            success=False,
            message="Error al obtener los clientes",
            errors={
                "code": "internal_server_error",
                "detail": "Error interno del servidor"
            },
            status_code=500
        )

def buscar_por_nombre(nombre):

    try:
        if not nombre or not isinstance(nombre, str):
            logging.warning("Parámetro de búsqueda inválido")
            return response(
                success=False,
                message="Parámetro de búsqueda inválido",
                errors={
                    "code": "invalid_input",
                    "detail": "El nombre debe ser una cadena de texto no vacía"
                },
                status_code=400
            )

        nombre_limpio = nombre.strip()
        if not nombre_limpio:
            logging.warning("Parámetro de búsqueda vacío después de limpiar")
            return response(
                success=False,
                message="Parámetro de búsqueda inválido",
                errors={
                    "code": "invalid_input",
                    "detail": "El nombre no puede estar vacío"
                },
                status_code=400
            )


        total_clientes = Clientes.query.count()
        if total_clientes == 0:
            logging.info("No hay clientes registrados en la base de datos")
            return response(
                success=False,
                message="No hay clientes registrados",
                errors={
                    "code": "not_found",
                    "detail": "No hay clientes registrados en el sistema"
                },
                status_code=404
            )


        clientes = Clientes.query.filter(Clientes.nombre.ilike(f"%{nombre_limpio}%")).all()
        
        if not clientes:
            logging.info(f"No se encontraron clientes con el nombre: '{nombre_limpio}'")
            return response(
                success=False,
                message="No se encontraron clientes",
                errors={
                    "code": "not_found",
                    "detail": f"No se encontraron clientes que coincidan con '{nombre_limpio}'"
                },
                status_code=404
            )
        
        serializacion_clientes = [cliente.to_dict() for cliente in clientes]

        logging.info(f"Se encontraron {len(clientes)} clientes con el nombre '{nombre_limpio}'")
        return response(
            success=True,
            data=serializacion_clientes,
            message="Clientes encontrados correctamente",
            status_code=200
        )

    except SQLAlchemyError as e:
        logging.error(f"Error de base de datos al buscar clientes: {str(e)}")
        return response(
            success=False,
            message="Error al buscar los clientes",
            errors={
                "code": "database_error",
                "detail": "Error en la base de datos"
            },
            status_code=500
        )

    except Exception as e:
        logging.error(f"Error inesperado al buscar clientes: {str(e)}")
        return response(
            success=False,
            message="Error al buscar los clientes",
            errors={
                "code": "internal_server_error",
                "detail": "Error interno del servidor"
            },
            status_code=500
        )

#-----------------------------------------------------------------------------------------

def obtener_cliente_por_id(cliente_id):
    
    try:
        if not isinstance(cliente_id, int) or cliente_id <= 0:
            logging.warning(f"ID inválido recibido: {cliente_id}")
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
            logging.info(f"Cliente no encontrado con ID: {cliente_id}")
            return response(
                success=False,
                message="Cliente no encontrado",
                errors={
                    "code": "not_found",
                    "detail": f"No existe cliente con ID {cliente_id}"
                },
                status_code=404
            )

        serializacion_clientes = [cliente.to_dict() for cliente in cliente]

        logging.info(f"Cliente encontrado - ID: {cliente_id}")
        return response(
            success=True,
            data=serializacion_clientes,  # Serializa el objeto individual
            message="Cliente obtenido correctamente",
            status_code=200
        )
        
    except SQLAlchemyError as e:
        logging.error(f"Error de base de datos al buscar cliente ID {cliente_id}: {str(e)}")
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
        logging.error(f"Error inesperado al buscar cliente ID {cliente_id}: {str(e)}")
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
            logging.warning("Datos de cliente inválidos")
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
            logging.warning(f"Nombre inválido: {nombre}")
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
            logging.warning(f"Intento de crear cliente existente: {nombre}")
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

        logging.info(f"Cliente creado exitosamente: {nombre}")
        return response(
            success=True,
            data=nuevo_cliente.to_dict(),
            message="Cliente creado exitosamente",
            status_code=201
        )

    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error(f"Error de base de datos al crear cliente: {str(e)}")
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
        logging.error(f"Error inesperado al crear cliente: {str(e)}")
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
            logging.warning(f"ID inválido recibido: {cliente_id}")
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
            logging.info(f"Cliente no encontrado con ID: {cliente_id}")
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
            logging.warning(f"Nombre inválido: {nuevo_nombre}")
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
            logging.warning(f"Intento de actualizar a nombre existente: {nuevo_nombre}")
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

        logging.info(f"Cliente {cliente_id} actualizado correctamente")
        return response(
            success=True,
            data=cliente.to_dict(),
            message="Cliente actualizado correctamente",
            status_code=200 
        )

    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error(f"Error de BD al actualizar cliente {cliente_id}: {str(e)}")
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
        logging.error(f"Error inesperado al actualizar cliente {cliente_id}: {str(e)}")
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
            logging.warning(f"ID inválido recibido: {cliente_id}")
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
            logging.info(f"Cliente no encontrado con ID: {cliente_id}")
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
        
        logging.info(f"Cliente eliminado exitosamente - ID: {cliente_id}")
        return response(
            success=True,
            data={"id": cliente_id},
            message="Cliente eliminado exitosamente",
            status_code=204 
        )

    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error(f"Error inesperado al eliminar al cliente {cliente_id}: {str(e)}")
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
        db.session.reollback()
        logging.error(f"Error inesperado al eliminar al cliente {cliente_id}: {str(e)}")
        return response(
            success=False,
            message="Error interno del servidor",
            errors={
                "code": "server_error",
                "detail": "Error al procesar la solicitud"
            },
            status_code=500
        )
