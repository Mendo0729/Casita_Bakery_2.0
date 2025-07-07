from app.utils.db import db
from app.models import Pedidos, DetallePedido, Productos, Clientes
from app.services import clientes_service
from decimal import Decimal
import pdfkit
from flask import render_template, make_response

config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

def obtener_todos():
    return Pedidos.query.order_by(Pedidos.fecha_pedido.desc()).all()

def obtener_por_estado(estado):
    estado = estado.strip().lower()

    if estado not in ["pendiente", "entregado", "cancelado"]:
        return []

    return Pedidos.query.filter(Pedidos.estado == estado).all()  

def obtener_pedido_por_cliente(cliente):
    if not cliente:
        return []
    busqueda = Pedidos.query.join(Clientes).filter(
            Clientes.nombre.ilike(f"%{cliente}%")
        ).all()
    return busqueda

#--------------------------------------------------------------------------------------------
def obtener_por_id(pedido_id):
    return Pedidos.query.get(pedido_id)

#----------------------------------------------------------------------------------------------

def crear_pedido(cliente_id, productos_seleccionados, fecha_entrega=None):
    cliente = clientes_service.obtener_cliente_por_id(cliente_id)
    if not cliente:
        raise ValueError("Cliente no encontrado")
    
    try:
        nuevo_pedido = Pedidos(
            cliente_id=cliente_id,
            estado='pendiente',
            fecha_entrega=fecha_entrega,
            total=Decimal('0.00')
        )
        
        db.session.add(nuevo_pedido)
        db.session.flush()

        total = Decimal('0.00')
        detalles = []
        
        for item in productos_seleccionados:
            producto = Productos.query.get(item['producto_id'])
            if not producto or not producto.activo:
                db.session.rollback()
                raise ValueError(f"Producto {item['producto_id']} no disponible")
            
            cantidad = int(item['cantidad'])
            if cantidad <= 0:
                db.session.rollback()
                raise ValueError("La cantidad debe ser mayor a 0")

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
        return nuevo_pedido
    except Exception as e:
        db.session.rollback()
        raise e

#-------------------------------------------------------------------------------------------------------

def cambiar_estado(pedido_id , estado):
    pedido = obtener_por_id(pedido_id)

    if not pedido:
        raise ValueError("Pedido no encontrado")
    
    estado = estado.lower()

    if estado not in ['pendiente', 'entregado', 'cancelado']:
        raise ValueError("Estado no valido")
    
    pedido.estado = estado
    db.session.commit()

    return pedido


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