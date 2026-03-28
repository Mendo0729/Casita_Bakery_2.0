from decimal import Decimal
import logging

from sqlalchemy.exc import SQLAlchemyError

from app.models import Ingrediente
from app.utils.db import db
from app.utils.create_responses import create_response as response

logger = logging.getLogger(__name__)

def obtener_todos(pagina=1, por_pagina=10, buscar=None):
    try:
        query = Ingrediente.query

        if buscar:
            query = query.filter(Ingrediente.nombre.ilike(f"%{buscar}%"))

        query = query.order_by(Ingrediente.id.desc())
        paginacion = query.paginate(page=pagina, per_page=por_pagina, error_out=False)

        if not paginacion.items:
            logger.info("No hay ingredientes para esta búsqueda/página")
            return response(
                success=True,
                data={
                    "ingredientes": [],
                    "pagina": paginacion.page,
                    "por_pagina": paginacion.per_page,
                    "total_paginas": paginacion.pages,
                    "total_ingredientes": paginacion.total
                },
                message="No hay ingredientes en esta página o búsqueda",
                status_code=200
            )

        ingredientes_data = [i.to_dict() for i in paginacion.items]

        return response(
            success=True,
            data={
                "ingredientes": ingredientes_data,
                "pagina": paginacion.page,
                "por_pagina": paginacion.per_page,
                "total_paginas": paginacion.pages,
                "total_ingredientes": paginacion.total
            },
            message=f"Página {paginacion.page} de {paginacion.pages}",
            status_code=200
        )

    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al obtener los ingredientes: {str(e)}")
        return response(
            success=False,
            message="Error al obtener los ingredientes",
            errors={
                "code": "database_error",
                "detail": "Error en la base de datos"
            },
            status_code=500
        )
    except Exception as e:
        logger.error(f"Error inesperado al obtener los ingredientes: {str(e)}")
        return response(
            success=False,
            message="Error al obtener los ingredientes",
            errors={
                "code": "internal_server_error",
                "detail": "Error interno del servidor"
            },
            status_code=500
        )

def obtener_por_id(ingrediente_id):
    try:
        if not isinstance(ingrediente_id, int) or ingrediente_id <= 0:
            logger.warning(f"ID inválido recibido: {ingrediente_id}")
            return response(
                success=False,
                message="ID de ingrediente inválido",
                errors={
                    "code": "invalid_input",
                    "detail": "El ID debe ser un entero positivo"
                },
                status_code=400
            )
        
        ingrediente = Ingrediente.query.filter(Ingrediente.id == ingrediente_id).first()

        if not ingrediente:
            logger.info(f"Ingrediente no encontrado: {ingrediente_id}")
            return response(
                success=False,
                message="Ingrediente no encontrado",
                errors={
                    "code": "not_found",
                    "detail": f"No existe el ingrediente con ID {ingrediente_id}"
                },
                status_code=404
            )
        
        logger.info(f"Ingrediente encontrado - ID: {ingrediente_id}")
        return response(
            success=True,
            data=ingrediente.to_dict(),
            message="Ingrediente obtenido correctamente",
            status_code=200
        )
    
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al obtener el ingrediente: {str(e)}")
        return response(
            success=False,
            message="Error al obtener el ingrediente",
            errors={
                "code": "database_error",
                "detail": "Error en la base de datos"
            },
            status_code=500
        )
    except Exception as e:
        logger.error(f"Error inesperado al obtener el ingrediente: {str(e)}")
        return response(
            success=False,
            message="Error al obtener el ingrediente",
            errors={
                "code": "internal_server_error",
                "detail": "Error interno del servidor"
            },
            status_code=500
        )

def guardar_ingrediente(data):
    try:
        if not data or not isinstance(data, dict):
            logger.warning("Datos de ingrediente inválidos")
            return response(
                success=False,
                message="Datos de ingrediente inválidos",
                errors={
                    "code": "invalid_input",
                    "detail": "Se esperaba un diccionario con los datos del ingrediente"
                },
                status_code=400
            )
        
        nombre = data.get("nombre", "").strip()
        cantidad = data.get("cantidad", 0)
        unidad_medida = data.get("unidad_medida", "unidades")
        punto_reorden = data.get("punto_reorden", 5.00)

        if not nombre:
            logger.warning("Nombre de ingrediente inválido")
            return response(
                success=False,
                message="Nombre de ingrediente inválido",
                errors={
                    "code": "invalid_input",
                    "detail": "Se esperaba un nombre de ingrediente no vacío"
                },
                status_code=400
            )

        if len(nombre) > 100:
            logger.warning("Nombre de ingrediente demasiado largo")
            return response(
                success=False,
                message="Nombre de ingrediente invÃ¡lido",
                errors={
                    "code": "invalid_input",
                    "detail": "El nombre no puede exceder 100 caracteres"
                },
                status_code=400
            )

        try:
            cantidad = float(cantidad)
            punto_reorden = float(punto_reorden)
        except ValueError:
            return response(
                success=False,
                message="Cantidad o punto de reorden inválidos",
                errors={
                    "code": "invalid_input",
                    "detail": "Cantidad y punto de reorden deben ser numéricos"
                },
                status_code=400
            )

        if cantidad < 0 or punto_reorden < 0:
            return response(
                success=False,
                message="Valores inválidos",
                errors={
                    "code": "invalid_input",
                    "detail": "Cantidad y punto de reorden deben ser mayores o iguales a 0"
                },
                status_code=400
            )

        existente = Ingrediente.query.filter_by(nombre=nombre).first()
        if existente:
            return response(
                success=False,
                message="Ingrediente ya existe",
                errors={
                    "code": "already_exists",
                    "detail": f"Ya existe un ingrediente con el nombre '{nombre}'"
                },
                status_code=409
            )

        nuevo_ingrediente = Ingrediente(
            nombre=nombre,
            cantidad=cantidad,
            unidad_medida=unidad_medida,
            punto_reorden=punto_reorden
        )

        db.session.add(nuevo_ingrediente)
        db.session.commit()

        logger.info(f"Ingrediente guardado correctamente - ID: {nuevo_ingrediente.id}")
        return response(
            success=True,
            message="Ingrediente guardado correctamente",
            data=nuevo_ingrediente.to_dict(),
            status_code=201
        )

    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Error de base de datos al guardar el ingrediente: {str(e)}")
        return response(
            success=False,
            message="Error al guardar el ingrediente",
            errors={
                "code": "database_error",
                "detail": "Error en la base de datos"
            },
            status_code=500
        )
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error inesperado al guardar el ingrediente: {str(e)}")
        return response(
            success=False,
            message="Error al guardar el ingrediente",
            errors={
                "code": "internal_server_error",
                "detail": "Error interno del servidor"
            },
            status_code=500
        )

def actualizar_ingrediente(ingrediente_id, data):
    try:
        # Validar ID
        if not isinstance(ingrediente_id, int) or ingrediente_id <= 0:
            logger.warning(f"ID inválido recibido: {ingrediente_id}")
            return response(
                success=False,
                message="ID de ingrediente inválido",
                errors={"code": "invalid_input", "detail": "El ID debe ser un entero positivo"},
                status_code=400
            )
        
        # Validar datos
        if not data or not isinstance(data, dict):
            logger.warning("Datos de ingrediente inválidos")
            return response(
                success=False,
                message="Datos de ingrediente inválidos",
                errors={"code": "invalid_input", "detail": "Se esperaba un diccionario con los datos del ingrediente"},
                status_code=400
            )

        ingrediente = Ingrediente.query.get(ingrediente_id)
        if not ingrediente:
            logger.warning(f"Ingrediente no encontrado con ID: {ingrediente_id}")
            return response(
                success=False,
                message="Ingrediente no encontrado",
                errors={"code": "not_found", "detail": f"No se encontró un ingrediente con ID {ingrediente_id}"},
                status_code=404
            )

        # === Validar y asignar nombre solo si viene en la petición ===
        if "nombre" in data:
            nuevo_nombre = data.get("nombre", "").strip()
            if not nuevo_nombre:
                return response(
                    success=False,
                    message="Nombre de ingrediente inválido",
                    errors={"code": "invalid_input", "detail": "Se esperaba un nombre de ingrediente no vacío"},
                    status_code=400
                )

            if len(nuevo_nombre) > 100:
                return response(
                    success=False,
                    message="Nombre de ingrediente invÃ¡lido",
                    errors={"code": "invalid_input", "detail": "El nombre no puede exceder 100 caracteres"},
                    status_code=400
                )

            # Verificar duplicados
            existente = Ingrediente.query.filter_by(nombre=nuevo_nombre).first()
            if existente and existente.id != ingrediente_id:
                return response(
                    success=False,
                    message="Ingrediente ya existe",
                    errors={"code": "already_exists", "detail": f"Ya existe un ingrediente con el nombre '{nuevo_nombre}'"},
                    status_code=409
                )

            ingrediente.nombre = nuevo_nombre

        # === Validar y asignar cantidad si viene ===
        if "cantidad" in data:
            try:
                cantidad = float(data["cantidad"])
                if cantidad < 0:
                    raise ValueError
                ingrediente.cantidad = cantidad
            except (ValueError, TypeError):
                return response(
                    success=False,
                    message="Cantidad inválida",
                    errors={"code": "invalid_input", "detail": "Cantidad debe ser un número mayor o igual a 0"},
                    status_code=400
                )

        # === Validar y asignar unidad_medida si viene ===
        if "unidad_medida" in data:
            unidad_medida = data.get("unidad_medida", "").strip()
            if unidad_medida:
                ingrediente.unidad_medida = unidad_medida

        # === Validar y asignar punto_reorden si viene ===
        if "punto_reorden" in data:
            try:
                punto_reorden = float(data["punto_reorden"])
                if punto_reorden < 0:
                    raise ValueError
                ingrediente.punto_reorden = punto_reorden
            except (ValueError, TypeError):
                return response(
                    success=False,
                    message="Punto de reorden inválido",
                    errors={"code": "invalid_input", "detail": "Punto de reorden debe ser un número mayor o igual a 0"},
                    status_code=400
                )

        db.session.commit()
        logger.info(f"Ingrediente actualizado exitosamente - ID {ingrediente_id}")
        return response(
            success=True,
            data=ingrediente.to_dict(),
            message="Ingrediente actualizado exitosamente",
            status_code=200
        )

    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Error de base de datos al actualizar el ingrediente: {str(e)}")
        return response(
            success=False,
            message="Error al actualizar el ingrediente",
            errors={"code": "database_error", "detail": "Error en la base de datos"},
            status_code=500
        )
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error inesperado al actualizar el ingrediente: {str(e)}")
        return response(
            success=False,
            message="Error al actualizar el ingrediente",
            errors={"code": "internal_server_error", "detail": "Error interno del servidor"},
            status_code=500
        )



"""def eliminar_ingrediente(ingrediente_id):
    
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
    return ingrediente"""
