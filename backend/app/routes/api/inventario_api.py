import logging

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.services.inventario_service import (
    actualizar_ingrediente,
    guardar_ingrediente,
    obtener_por_id,
    obtener_todos,
)
from app.utils.create_responses import create_response as response

logger = logging.getLogger(__name__)

inventario_api = Blueprint("inventario_api", __name__, url_prefix="/inventario/api")


@inventario_api.route("/", methods=["GET"])
@jwt_required()
def obtener_ingredientes():
    pagina = request.args.get("pagina", 1, type=int)
    por_pagina = request.args.get("por_pagina", 10, type=int)
    buscar = request.args.get("buscar", None, type=str)

    result = obtener_todos(pagina=pagina, por_pagina=por_pagina, buscar=buscar)
    return jsonify(result), result.get("status_code", 200)


@inventario_api.route("/<int:ingrediente_id>", methods=["GET"])
@jwt_required()
def obtener_ingrediente_id_api(ingrediente_id):
    result = obtener_por_id(ingrediente_id=ingrediente_id)
    return jsonify(result), result.get("status_code", 200)


@inventario_api.route("/", methods=["POST"])
@jwt_required()
def guardar_ingrediente_api():
    try:
        datos = request.get_json(silent=True)

        if not datos:
            result = response(
                success=False,
                message="El cuerpo de la solicitud debe ser JSON valido",
                errors={
                    "code": "invalid_input",
                    "detail": "Se esperaba un objeto JSON con los datos del ingrediente",
                },
                status_code=400,
            )
            return jsonify(result), 400

        result = guardar_ingrediente(datos)
        return jsonify(result), result.get("status_code", 201)
    except Exception as e:
        logger.error(f"Error en endpoint de guardado: {str(e)}")
        result = response(
            success=False,
            message="Error procesando la solicitud",
            errors={
                "code": "internal_server_error",
                "detail": "Error al procesar los datos del ingrediente",
            },
            status_code=500,
        )
        return jsonify(result), 500


@inventario_api.route("/<int:ingrediente_id>", methods=["PUT"])
@jwt_required()
def actualizar_ingrediente_api(ingrediente_id):
    try:
        datos = request.get_json(silent=True)

        if not datos:
            result = response(
                success=False,
                message="El cuerpo de la solicitud debe ser JSON valido",
                errors={
                    "code": "invalid_input",
                    "detail": "Se esperaba un objeto JSON con los datos del ingrediente",
                },
                status_code=400,
            )
            return jsonify(result), 400

        result = actualizar_ingrediente(ingrediente_id, datos)
        return jsonify(result), result.get("status_code", 200)
    except Exception as e:
        logger.error(f"Error en endpoint de actualizacion: {str(e)}")
        result = response(
            success=False,
            message="Error procesando la solicitud",
            errors={
                "code": "internal_server_error",
                "detail": "Error al actualizar los datos del ingrediente",
            },
            status_code=500,
        )
        return jsonify(result), 500
