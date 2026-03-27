import logging

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from app.utils.create_responses import create_response as response
from app.utils.db import db
from app.utils.logging import setup_logging


migrate = Migrate()
jwt = JWTManager()


def create_app(config_class="config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app, origins=app.config.get("CORS_ORIGINS", ["http://localhost:4200"]))

    setup_logging(app)

    @jwt.unauthorized_loader
    def unauthorized_callback(reason):
        result = response(
            success=False,
            message="Token de acceso requerido",
            errors={
                "code": "missing_token",
                "detail": reason,
            },
            status_code=401,
        )
        return jsonify(result), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(reason):
        result = response(
            success=False,
            message="Token invalido",
            errors={
                "code": "invalid_token",
                "detail": reason,
            },
            status_code=422,
        )
        return jsonify(result), 422

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        result = response(
            success=False,
            message="Token expirado",
            errors={
                "code": "token_expired",
                "detail": "El token ha expirado",
            },
            status_code=401,
        )
        return jsonify(result), 401

    from app.routes.api import all_blueprints

    for bp in all_blueprints:
        app.register_blueprint(bp)

    with app.app_context():
        if app.config["DEBUG"] and app.config.get("AUTO_CREATE_DB", False):
            db.create_all()

    return app
