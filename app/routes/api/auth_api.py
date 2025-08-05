from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token
)

from app.services.auth_service import validacion_usuario

auth_api = Blueprint('auth_api', __name__, url_prefix='/auth/api')

@auth_api.route('/login', methods=['POST'])
def api_login():
    data = request.get_json()

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
