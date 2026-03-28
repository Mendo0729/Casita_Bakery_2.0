from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required
)

from app.services.auth_service import validacion_usuario
from app.utils.create_responses import create_response as response

auth_api = Blueprint('auth_api', __name__, url_prefix='/auth/api')


@auth_api.route('/login', methods=['POST'])
def api_login():
    data = request.get_json(silent=True)

    if not data or not isinstance(data, dict):
        result = response(
            success=False,
            message="El cuerpo de la solicitud debe ser JSON valido",
            errors={
                "code": "invalid_input",
                "detail": "Se esperaba un objeto JSON con username y password"
            },
            status_code=400
        )
        return jsonify(result), 400

    username = data.get('username')
    password = data.get('password')

    result = validacion_usuario(username, password)

    if result["success"]:
        user_data = result["data"]
        access_token = create_access_token(identity=str(user_data["id"]))
        refresh_token = create_refresh_token(identity=str(user_data["id"]))

        result["tokens"] = {
            "access": access_token,
            "refresh": refresh_token
        }

    return jsonify(result), result.get("status_code", 200)


@auth_api.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def api_refresh():
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=user_id)

    result = response(
        success=True,
        message="Token renovado correctamente",
        data={
            "access": access_token
        },
        status_code=200
    )
    return jsonify(result), 200
