import logging

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.services.pedidos_service import (
    actualizar_pedido,
    crear_pedido,
    obtener_por_id,
    obtener_todos,
)
from app.utils.create_responses import create_response as response

logger = logging.getLogger(__name__)

pedidos_api = Blueprint("pedidos_api", __name__, url_prefix="/pedidos/api")


@pedidos_api.route("/", methods=["GET"])
@jwt_required()
def obtener_pedidos():
    args = request.args
    pagina = args.get("pagina", 1, type=int)
    por_pagina = args.get("por_pagina", 10, type=int)
    buscar_estado = args.get("estado", type=str)
    buscar_clientes = args.get("cliente", type=str)

    logger.debug(
        f"Parametros recibidos: pagina={pagina}, por_pagina={por_pagina}, "
        f"buscar_estado='{buscar_estado}', buscar_clientes='{buscar_clientes}'"
    )
    result = obtener_todos(pagina, por_pagina, buscar_estado, buscar_clientes)

    return jsonify(result), result.get("status_code", 200)


@pedidos_api.route("/<int:pedido_id>", methods=["GET"])
@jwt_required()
def obtener_pedido(pedido_id):
    logger.debug(f"Obteniendo pedido con ID: {pedido_id}")
    result = obtener_por_id(pedido_id)
    return jsonify(result), result.get("status_code", 200)


@pedidos_api.route("/", methods=["POST"])
@jwt_required()
def crear_pedido_api():
    try:
        datos = request.get_json(silent=True)
        if not datos:
            result = response(
                success=False,
                message="El cuerpo de la solicitud debe ser JSON valido",
                errors={
                    "code": "invalid_input",
                    "detail": "Se esperaba un objeto JSON con los datos del pedido",
                },
                status_code=400,
            )
            return jsonify(result), 400

        cliente_id = datos.get("cliente_id")
        productos_seleccionados = datos.get("productos_seleccionados")
        fecha_entrega = datos.get("fecha_entrega")

        result = crear_pedido(cliente_id, productos_seleccionados, fecha_entrega)
        return jsonify(result), result.get("status_code", 201)
    except Exception as e:
        logger.error(f"Error en el endpoint de creacion: {e}")
        result = response(
            success=False,
            message="Error procesando la solicitud",
            errors={
                "code": "internal_server_error",
                "detail": "Error al procesar los datos del pedido",
            },
            status_code=500,
        )
        return jsonify(result), 500


@pedidos_api.route("/<int:pedido_id>", methods=["PUT"])
@jwt_required()
def actualizar_pedido_api(pedido_id):
    try:
        datos = request.get_json(silent=True)
        if not datos:
            result = response(
                success=False,
                message="El cuerpo de la solicitud debe ser JSON valido",
                errors={
                    "code": "invalid_input",
                    "detail": "Se esperaba un objeto JSON con los datos del pedido",
                },
                status_code=400,
            )
            return jsonify(result), 400

        result = actualizar_pedido(pedido_id, datos)
        return jsonify(result), result.get("status_code", 200)
    except Exception as e:
        logger.error(f"Error en el endpoint de actualizacion: {e}")
        result = response(
            success=False,
            message="Error procesando la solicitud",
            errors={
                "code": "internal_server_error",
                "detail": "Error al actualizar los datos del pedido",
            },
            status_code=500,
        )
        return jsonify(result), 500
