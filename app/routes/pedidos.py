from flask import Blueprint, render_template, request, redirect, url_for, make_response, flash, current_app, jsonify, abort
from app.services import pedidos_service, clientes_service, productos_service
from werkzeug.exceptions import BadRequest
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from flask_login import login_required


pedidos = Blueprint('pedidos', __name__, url_prefix='/pedidos')

@pedidos.route('/')
@login_required
def listar():
    return render_template('pedidos/listar.html')

@pedidos.route('/api', methods=['GET'])
@login_required
def api_pedidos():
    try:
        cliente = request.args.get('cliente', '').strip()
        estado = request.args.get('estado', '').strip()

        if cliente:
            current_app.logger.info(f"[PEDIDOS] Búsqueda por nombre: '{cliente}'")
            pedidos_lista = pedidos_service.obtener_pedido_por_cliente(cliente)
        elif estado:
            current_app.logger.info(f"[PEDIDOS] Listado de pedidos con estado: {estado}")
            pedidos_lista = pedidos_service.obtener_por_estado(estado)
        else:
            current_app.logger.info("[PEDIDOS] Listando todos los pedidos")
            pedidos_lista = pedidos_service.obtener_todos()

        pedidos_json = [{
            "id": pedido.id,
            "cliente": pedido.cliente.nombre if pedido.cliente else "Sin cliente",
            "estado": pedido.estado,
            "fecha_pedido": pedido.fecha_pedido.strftime('%d/%m/%Y') if pedido.fecha_pedido else "Sin fecha",
            "fecha_entrega": pedido.fecha_entrega.strftime('%d/%m/%Y') if pedido.fecha_entrega else "Sin fecha",
            "total": float(pedido.total) if pedido.total is not None else 0.0
        } for pedido in pedidos_lista]

        return jsonify(pedidos_json)

    except Exception as e:
        current_app.logger.error(f"[PEDIDOS] Error al obtener pedidos: {str(e)}", exc_info=True)
        raise BadRequest("No se pudieron obtener los pedidos")

#---------------------------------------------------------------------------------------------------------------------------------------------------------

@pedidos.route('/crear', methods=['GET'])
@login_required
def crear():
    return render_template('pedidos/crear.html')


@pedidos.route('/api/crear', methods=['POST'])
@login_required
def api_crear_pedido():
    try:
        data = request.get_json()
        cliente_id = data.get('cliente_id')
        fecha_entrega = data.get('fecha_entrega')
        productos = data.get('productos', [])

        if not cliente_id or not productos:
            return jsonify({"success": False, "message": "Datos incompletos"}), 400

        # Formatear fecha
        fecha_obj = datetime.strptime(fecha_entrega, '%Y-%m-%d').date() if fecha_entrega else None

        pedido = pedidos_service.crear_pedido(cliente_id, productos, fecha_obj)

        return jsonify({
            "success": True,
            "message": "Pedido creado exitosamente",
            "pedido_id": pedido.id
        })
    except Exception as e:
        current_app.logger.error(f"[PEDIDOS] Error al crear pedido: {str(e)}")
        return jsonify({"success": False, "message": "Error al crear el pedido"}), 500

#---------------------------------------------------------------------------------------------------------------------------------

@pedidos.route('/<int:pedido_id>')
@login_required
def detalle_pedido(pedido_id):
    pedido = pedidos_service.obtener_por_id(pedido_id)
    if not pedido:
        abort(404)
    return render_template('pedidos/detalle.html', pedido=pedido)

@pedidos.route('/<int:pedido_id>/factura')
def ver_factura(pedido_id):
    pedido = pedidos_service.obtener_por_id(pedido_id)
    if not pedido:
        return "Pedido no encontrado", 404
    return pedidos_service.generar_factura_pdf(pedido)

@pedidos.route('/api/<int:pedido_id>/estado', methods=['POST'])
@login_required
def cambiar_estado_pedido(pedido_id):
    try:
        data = request.get_json()
        estado = data.get('estado')

        if estado not in ['entregado', 'cancelado']:
            return jsonify({'success': False, 'message': 'Estado inválido'}), 400

        pedido = pedidos_service.cambiar_estado(pedido_id, estado)
        if pedido:
            return jsonify({'success': True, 'message': f'Pedido marcado como {estado}.'})
        else:
            return jsonify({'success': False, 'message': 'Pedido no encontrado'}), 404

    except Exception as e:
        current_app.logger.error(f"[PEDIDOS] Error al cambiar estado: {str(e)}")
        return jsonify({'success': False, 'message': 'Error al cambiar el estado del pedido'}), 500




