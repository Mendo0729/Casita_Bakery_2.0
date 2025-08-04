from decimal import Decimal
import logging

from flask import make_response, render_template
from flask_sqlalchemy import SQLAlchemy
import pdfkit
from sqlalchemy.exc import SQLAlchemyError

from app.models import Clientes, DetallePedido, Pedidos, Productos
from app.services import clientes_service as CS
from app.utils.create_responses import create_response as response
from app.utils.db import db

# config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

def obtener_todos(pagina=1, por_pagina=10, buscar_estado=None, buscar_clientes=None):
    try:
        try:
            pagina = int(pagina)
            por_pagina = int(por_pagina)
            if pagina <= 0:
                logging.warning(f"Número de página inválido: {pagina}. Se ajusta a 1.")
                pagina = 1
            if por_pagina <= 0 or por_pagina > 100:
                logging.warning(f"Cantidad por página inválida: {por_pagina}. Se ajusta a 10.")
                por_pagina = 10
        except (ValueError, TypeError) as e:
            logging.warning(f"Error de tipo en parámetros de paginación: {str(e)}. Se usan valores por defecto.")
            pagina = 1
            por_pagina = 10

        query = Pedidos.query

        if buscar_clientes:
            query = query.join(Clientes).filter(Clientes.nombre.ilike(f"%{buscar_clientes}%"))

        if buscar_estado:
            query = query.filter(Pedidos.estado == buscar_estado)

        query = query.order_by(Pedidos.id.desc())
        paginacion = query.paginate(page=pagina, per_page=por_pagina, error_out=False)

        if not paginacion.items:
            logging.info("No hay Pedidos para esta búsqueda/página")
            return response(
                success=True,
                data={
                    "pedidos": [],
                    "pagina": paginacion.page,
                    "por_pagina": paginacion.per_page,
                    "total_paginas": paginacion.pages,
                    "total_pedidos": paginacion.total
                },
                message="No hay pedidos en esta página o búsqueda",
                status_code=200
            )

        pedidos_data = [pd.to_dict() for pd in paginacion.items]

        return response(
            success=True,
            data={
                "pedidos": pedidos_data,
                "pagina": paginacion.page,
                "por_pagina": paginacion.per_page,
                "total_paginas": paginacion.pages,
                "total_pedidos": paginacion.total
            },
            message=f"Página {paginacion.page} de {paginacion.pages}",
            status_code=200
        )

    except SQLAlchemyError as e:
        logging.error(f"Error de base de datos al obtener los pedidos: {str(e)}")
        return response(
            success=False,
            message="Error al obtener los pedidos",
            errors={
                "code": "database_error",
                "detail": "Error en la base de datos"
            },
            status_code=500
        )
    except Exception as e:
        logging.error(f"Error inesperado al obtener los pedidos: {str(e)}")
        return response(
            success=False,
            message="Error al obtener los pedidos",
            errors={
                "code": "internal_server_error",
                "detail": "Error interno del servidor"
            },
            status_code=500
        )

#----------------------------------------------------------------------------------------------

def crear_pedido(cliente_id, productos_seleccionados, fecha_entrega=None):
    try:
        cliente_response = CS.obtener_cliente_por_id(cliente_id)
        if not cliente_response.get('success'):
            return cliente_response
        cliente = CS.obtener_cliente_modelo_por_id(cliente_id)
        if not cliente:
            return response(
                success=False,
                message="Cliente no encontrado",
                errors={
                    "code": "not_found",
                    "detail": "El cliente no existe"
                    },
                status_code=404
            )

        if not productos_seleccionados or not isinstance(productos_seleccionados, list):
            return response(
                success=False,
                message="Lista de productos inválida o vacía",
                errors={
                    "code": "invalid_data",
                    "detail": "Debes seleccionar al menos un producto"
                    },
                status_code=400
            )

        nuevo_pedido = Pedidos(
            cliente_id=cliente.id,
            estado='pendiente',
            fecha_entrega=fecha_entrega,
            total=Decimal('0.00')
        )
        db.session.add(nuevo_pedido)
        db.session.flush()  # Para obtener el ID del nuevo pedido

        total = Decimal('0.00')
        detalles = []

        for item in productos_seleccionados:
            producto_id = item.get('producto_id')
            cantidad = item.get('cantidad')

            if not producto_id or not cantidad:
                db.session.rollback()
                return response(
                    success=False,
                    message="Datos de producto incompletos",
                    errors={
                        "code": "invalid_data",
                        "detail": "Cada producto debe tener ID y cantidad"
                        },
                    status_code=400
                )

            producto = Productos.query.get(producto_id)
            if not producto or not producto.activo:
                db.session.rollback()
                return response(
                    success=False,
                    message=f"Producto no disponible: ID {producto_id}",
                    errors={
                        "code": "invalid_product",
                        "detail": f"Producto {producto_id} no encontrado o inactivo"
                        },
                    status_code=400
                )

            cantidad = int(cantidad)
            if cantidad <= 0:
                db.session.rollback()
                return response(
                    success=False,
                    message="Cantidad inválida",
                    errors={"code": "invalid_quantity", "detail": "La cantidad debe ser mayor a cero"},
                    status_code=400
                )

            precio_unitario = Decimal(str(producto.precio))
            subtotal = precio_unitario * cantidad

            detalles.append(DetallePedido(
                pedido_id=nuevo_pedido.id,
                producto_id=producto.id,
                cantidad=cantidad,
                precio_unitario=precio_unitario,
                subtotal=subtotal
            ))
            total += subtotal

        nuevo_pedido.total = total
        db.session.add_all(detalles)
        db.session.commit()

        return response(
            success=True,
            message="Pedido creado correctamente",
            data=nuevo_pedido.to_dict(),
            status_code=201
        )

    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error(f"Error de base de datos al crear el pedido: {str(e)}")
        return response(
            success=False,
            message="Error al guardar el pedido",
            errors={
                "code": "database_error",
                "detail": "Error en la base de datos"
            },
            status_code=500
        )
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error inesperado al crear el pedido: {str(e)}")
        return response(
            success=False,
            message="Error interno del servidor",
            errors={
                "code": "internal_server_error",
                "detail": str(e)
            },
            status_code=500
        )


#----------------------------------------------------------------------------------------------

def cambiar_estado(pedido_id, estado):

    try:
        if not isinstance(pedido_id, int) or pedido_id <= 0:
            return response(
                success=False,
                message="ID de pedido inválido",
                errors={"code": "invalid_input", "detail": "El ID debe ser un entero positivo"},
                status_code=400
            )

        pedido = Pedidos.query.get(pedido_id)

        if not pedido:
            return response(
                success=False,
                message="Pedido no encontrado",
                errors={"code": "not_found", "detail": f"No existe pedido con ID {pedido_id}"},
                status_code=404
            )

        estado = estado.lower().strip()

        estados_validos = ['pendiente', 'entregado', 'cancelado']
        if estado not in estados_validos:
            return response(
                success=False,
                message="Estado inválido",
                errors={"code": "invalid_state", "detail": f"Estado '{estado}' no permitido"},
                status_code=400
            )

        pedido.estado = estado
        db.session.commit()

        return response(
            success=True,
            message=f"Estado del pedido actualizado a '{estado}'",
            data=pedido.to_dict(),
            status_code=200
        )

    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error(f"Error de base de datos al cambiar estado del pedido {pedido_id}: {str(e)}")
        return response(
            success=False,
            message="Error de base de datos al actualizar el pedido",
            errors={"code": "database_error", "detail": "No se pudo guardar el nuevo estado"},
            status_code=500
        )

    except Exception as e:
        db.session.rollback()
        logging.error(f"Error inesperado al cambiar estado del pedido {pedido_id}: {str(e)}")
        return response(
            success=False,
            message="Error interno del servidor",
            errors={"code": "internal_server_error", "detail": str(e)},
            status_code=500
        )

"""
#-------------------------------------------------------------------------------------------------------

def generar_factura_pdf(pedido):
    try:
        rendered = render_template('pedidos/factura.html', pedido=pedido)
        options = {
            'enable-local-file-access': None,
            'page-size': 'Letter',
            'encoding': "UTF-8"
        }
        pdf = pdfkit.from_string(rendered, False, options=options, configuration=config)
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'inline; filename="factura_pedido_{pedido.id}.pdf"'
        return response
    except Exception as e:
        raise RuntimeError(f"Error al generar PDF: {str(e)}")
"""