from app.models import Pedidos, Clientes, DetallePedido, Productos
from sqlalchemy import func
from app import db
from datetime import datetime, timedelta

def obtener_datos_dashboard():
    hoy = datetime.today()
    D7 = hoy + timedelta(days=7)

    total_pedidos = Pedidos.query.count()
    pedidos_pendientes = Pedidos.query.filter(Pedidos.estado == 'pendiente').count()
    pedidos_entregados = Pedidos.query.filter(Pedidos.estado == 'entregados').count()
    pedidos_cancelados = Pedidos.query.filter(Pedidos.estado == 'cancelado').count()

    total_productos = Productos.query.count()
    total_clientes = Clientes.query.count()

    ingresos_ultimos_7_dias = (
        db.session.query(
            func.date(Pedidos.fecha_pedido).label('fecha'),
            func.sum(Pedidos.total)
        )
        .filter(Pedidos.fecha_pedido >= hoy - timedelta(days=7))
        .group_by(func.date(Pedidos.fecha_pedido))
        .order_by(func.date(Pedidos.fecha_pedido))
        .all()
    )

    pedidos_proximos_7_dias = (
        db.session.query(
            Pedidos.id,
            Pedidos.estado,
            Pedidos.fecha_pedido,
            Clientes.nombre.label('cliente'),
            Pedidos.total
        )
        .join(Clientes, Pedidos.cliente_id == Clientes.id)
        .filter(Pedidos.estado == 'pendiente')
        .filter(Pedidos.fecha_pedido >= hoy)
        .filter(Pedidos.fecha_entrega <= D7)
        .order_by(Pedidos.fecha_pedido)
        .all()
    )

    top_productos = (
        db.session.query(
            Productos.nombre,
            func.sum(DetallePedido.cantidad).label('total_vendido')
        )
        .join(DetallePedido, Productos.id == DetallePedido.producto_id)
        .group_by(Productos.nombre)
        .order_by(func.sum(DetallePedido.cantidad).desc())
        .limit(5)
        .all()
    )

    return {
        "total_pedidos": total_pedidos,
        "pendientes": pedidos_pendientes,
        "entregados": pedidos_entregados,
        "cancelados": pedidos_cancelados,
        "total_clientes": total_clientes,
        "total_productos": total_productos,
        "ingresos_7_dias": [
            {"fecha": str(f), "total": float(t)} for f, t in ingresos_ultimos_7_dias
        ],
        "pedidos_proximos_7_dias": [
            {
                "id": p.id,
                "estado": p.estado,
                "fecha_entrega": p.fecha_entrega.strftime("%Y-%m-%d"),
                "cliente": p.cliente,
                "total": float(p.total)
            } for p in pedidos_proximos_7_dias
        ],
        "top_productos": [
            {"nombre": nombre, "total_vendido": int(cant)} for nombre, cant in top_productos
        ]
    }
