import logging

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.services.clientes_service import (
    actualizar_cliente,
    crear_cliente,
    eliminar_cliente,
    obtener_cliente_por_id,
    obtener_todos,
)
from app.utils.create_responses import create_response as response

logger = logging.getLogger(__name__)

cliente_api = Blueprint("cliente_api", __name__, url_prefix="/cliente/api")


@cliente_api.route("/", methods=["GET"])
@jwt_required()
def listar_clientes():
    pagina = request.args.get("pagina", default=1, type=int)
    por_pagina = request.args.get("por_pagina", default=10, type=int)
    buscar = request.args.get("buscar", "").strip()

    logger.debug(
        f"Parametros recibidos: pagina={pagina}, por_pagina={por_pagina}, buscar='{buscar}'"
    )

    result = obtener_todos(pagina=pagina, por_pagina=por_pagina, buscar=buscar)
    return jsonify(result), result.get("status_code", 200)


@cliente_api.route("/<int:cliente_id>", methods=["GET"])
@jwt_required()
def obtener_por_id(cliente_id):
    result = obtener_cliente_por_id(cliente_id=cliente_id)
    return jsonify(result), result.get("status_code", 200)


@cliente_api.route("/", methods=["POST"])
@jwt_required()
def crear_cliente_api():
    try:
        datos = request.get_json(silent=True)

        if not datos:
            result = response(
                success=False,
                message="El cuerpo de la solicitud debe ser JSON valido",
                errors={
                    "code": "invalid_input",
                    "detail": "Se esperaba un objeto JSON con los datos del cliente",
                },
                status_code=400,
            )
            return jsonify(result), 400

        result = crear_cliente(datos)
        return jsonify(result), result.get("status_code", 201)

    except Exception as e:
        logger.error(f"Error en endpoint de creacion: {str(e)}")
        result = response(
            success=False,
            message="Error procesando la solicitud",
            errors={
                "code": "internal_server_error",
                "detail": "Error al procesar los datos del cliente",
            },
            status_code=500,
        )
        return jsonify(result), 500


@cliente_api.route("/<int:cliente_id>", methods=["PUT"])
@jwt_required()
def actualizar_cliente_api(cliente_id):
    try:
        datos = request.get_json(silent=True)

        if not datos:
            result = response(
                success=False,
                message="El cuerpo de la solicitud debe ser JSON valido",
                errors={
                    "code": "invalid_input",
                    "detail": "Se esperaba un objeto JSON con los datos del cliente",
                },
                status_code=400,
            )
            return jsonify(result), 400

        result = actualizar_cliente(cliente_id=cliente_id, data=datos)
        return jsonify(result), result.get("status_code", 200)

    except Exception as e:
        logger.error(f"Error en endpoint de actualizacion: {str(e)}")
        result = response(
            success=False,
            message="Error procesando la solicitud",
            errors={
                "code": "internal_server_error",
                "detail": "Error al actualizar los datos del cliente",
            },
            status_code=500,
        )
        return jsonify(result), 500


@cliente_api.route("/<int:cliente_id>", methods=["DELETE"])
@jwt_required()
def eliminar_cliente_api(cliente_id):
    try:
        result = eliminar_cliente(cliente_id)
        return jsonify(result), result.get("status_code", 200)
    except Exception as e:
        logger.error(f"Error en endpoint de eliminar cliente {cliente_id}: {str(e)}")
        result = response(
            success=False,
            message="Error interno del servidor",
            errors={
                "code": "internal_server_error",
                "detail": "Error al eliminar el cliente",
            },
            status_code=500,
        )
        return jsonify(result), 500
