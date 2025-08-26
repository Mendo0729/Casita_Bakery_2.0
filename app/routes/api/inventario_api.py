import logging

from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    jwt_required)

from app.services.inventario_service import(
    obtener_todos,
    obtener_por_id,
    guardar_ingrediente,
    actualizar_ingrediente,
)

logger = logging.getLogger(__name__)

inventario_api = Blueprint("inventario_api", __name__, url_prefix='/inventario/api')

@inventario_api.route('/', methods=['GET'])
@jwt_required()
def obtener_ingredientes():
    pagina = request.args.get('pagina', 1, type=int)
    por_pagina = request.args.get('por_pagina', 10, type=int)
    buscar = request.args.get('buscar', None, type=str)

    result = obtener_todos(pagina=pagina, por_pagina=por_pagina, buscar=buscar)
    return jsonify(result), result.get("status_code", 200)

@inventario_api.route('/<int:ingrediente_id>', methods=['GET'])
@jwt_required()
def obtener_ingrediente_id_api(ingrediente_id):
    result = obtener_por_id(ingrediente_id = ingrediente_id)
    return jsonify(result), result.get("status_code", 200)

@inventario_api.route('/', methods=['POST'])
@jwt_required()
def guardar_ingrediente_api():
    try:
        datos = request.get_json()

        if not datos:
            return jsonify({
                "success": False,
                "message": "El cuerpo de la solicitud debe ser JSON válido",
                "errors": {"request": "Body vacío o formato inválido"},
                "status_code": 400
            }), 400
        
        result = guardar_ingrediente(datos)
        return jsonify(result), result.get("status_code", 201)
    except Exception as e:
        logger.error(f"Error en endpoint de guardado: {str(e)}")
        return jsonify({
            "success": False,
            "message": "Error procesando la solicitud",
            "errors": {"request": "Error en los datos de entrada"},
            "status_code": 500
        }), 500
    
@inventario_api.route('/<int:ingrediente_id>', methods=['PUT'])
@jwt_required()
def actualizar_ingrediente_api(ingrediente_id):
    try:
        datos = request.get_json()

        if not datos:
            return jsonify({
                "success": False,
                "message": "El cuerpo de la solicitud debe ser JSON válido",
                "errors": {"request": "Body vacío o formato inválido"},
                "status_code": 400
            }), 400
        
        result = actualizar_ingrediente(ingrediente_id, datos)
        return jsonify(result), result.get("status_code", 200)
    except Exception as e:
        logger.error(f"Error en endpoint de actualizacion: {str(e)}")
        return jsonify({
            "success": False,
            "message": "Error procesando la solicitud",
            "errors": {"request": "Error en los datos de entrada"},
            "status_code": 500
        }), 500