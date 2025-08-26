import logging

from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    jwt_required)

from app.services.productos_service import(
    obtener_todos,
    obtener_por_id,
    crear_producto,
    actualizar_producto,
    eliminar
)

logger = logging.getLogger(__name__)

productos_api = Blueprint("producto_api", __name__, url_prefix='/producto/api')

@productos_api.route('/', methods=['GET'])
@jwt_required()
def listar_productos():
    pagina = request.args.get("pagina", default=1, type=int)
    por_pagina = request.args.get("por_pagina", default=10, type=int)
    buscar = request.args.get("buscar", "").strip()

    logger.debug(f"Parámetros recibidos: pagina={pagina}, por_pagina={por_pagina}, buscar='{buscar}'")

    result = obtener_todos(pagina=pagina, por_pagina=por_pagina, buscar=buscar)
    return jsonify(result), result.get("status_code", 200)

@productos_api.route('/<int:producto_id>', methods=['GET'])
@jwt_required()
def obtener_producto_id(producto_id):
    result = obtener_por_id(producto_id = producto_id)
    return jsonify(result), result.get("status_code", 200)


@productos_api.route('/', methods=['POST'])
@jwt_required()
def crear_producto_api():
    try:
        datos = request.get_json()

        if not datos:
            return jsonify({
                "success": False,
                "message": "El cuerpo de la solicitud debe ser JSON válido",
                "errors": {"request": "Body vacío o formato inválido"},
                "status_code": 400
            }), 400
        
        result = crear_producto(datos)
        return jsonify(result), result.get("status_code", 201)
    except Exception as e:
        logger.error(f"Error en endpoint de creación: {str(e)}")
        return jsonify({
            "success": False,
            "message": "Error procesando la solicitud",
            "errors": {"request": "Error en los datos de entrada"},
            "status_code": 500
        }), 500
    
@productos_api.route('/<int:producto_id>', methods=['PUT'])
@jwt_required()
def actualizar_producto_api(producto_id):
    try:
        datos = request.get_json()

        if not datos:
            return jsonify({
                "success": False,
                "message": "El cuerpo de la solicitud debe ser JSON válido",
                "errors": {"request": "Body vacío o formato inválido"},
                "status_code": 400
            }), 400
        
        result = actualizar_producto(producto_id, datos)
        return jsonify(result), result.get("status_code", 200)
    except Exception as e:
        logger.error(f"Error en endpoint de actualizacion: {str(e)}")
        return jsonify({
            "success": False,
            "message": "Error procesando la solicitud",
            "errors": {"request": "Error en los datos de entrada"},
            "status_code": 500
        }), 500
    
@productos_api.route('/<int:producto_id>', methods=['DELETE'])
@jwt_required()
def eliminar_producto_api(producto_id):
    result = eliminar(producto_id=producto_id)
    return jsonify(result), result.get("status_code", 200)
