import logging
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from app.utils.db import db
from app.utils.logging import setup_logging


# Extensiones globales
migrate = Migrate()
jwt = JWTManager()


def create_app(config_class="config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app, origins=app.config.get("CORS_ORIGINS", ["http://localhost:4200"]))

    # Configuración de logs
    setup_logging(app)

    # Registrar blueprints
    from app.routes.api import all_blueprints
    for bp in all_blueprints:
        app.register_blueprint(bp)

    # Crear tablas en desarrollo si está habilitado
    with app.app_context():
        if app.config["DEBUG"] and app.config.get("AUTO_CREATE_DB", False):
            db.create_all()

    return app
