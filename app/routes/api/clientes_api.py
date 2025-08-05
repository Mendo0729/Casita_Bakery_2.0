import logging
from unittest import result

from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity)

from app.services.clientes_service import (
    obtener_todos,
    obtener_cliente_por_id,
    crear_cliente,
    actualizar_cliente,
    eliminar_cliente
)

logger = logging.getLogger(__name__)

cliente_api = Blueprint("cliente_api", __name__, url_prefix='/cliente/api')

@cliente_api.route('/', methods=['GET'])
@jwt_required()
def listar_clientes():
    pagina = request.args.get("pagina", default=1, type=int)
    por_pagina = request.args.get("por_pagina", default=10, type=int)
    buscar = request.args.get("buscar", "").strip()

    logger.debug(f"Parámetros recibidos: pagina={pagina}, por_pagina={por_pagina}, buscar='{buscar}'")

    result = obtener_todos(pagina=pagina, por_pagina=por_pagina, buscar=buscar)
    return jsonify(result), result.get("status_code", 200)


@cliente_api.route('/<int:cliente_id>', methods=['GET'])
@jwt_required()
def obtener_por_id(cliente_id):
    result = obtener_cliente_por_id(cliente_id = cliente_id)
    return jsonify(result), result.get("status_code", 200)