from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.utils.db import db
import logging
from logging.handlers import RotatingFileHandler
import os
import socket
import json

# Extensiones globales
migrate = Migrate()
jwt = JWTManager()

# Logger en formato JSON
class JSONFormatter(logging.Formatter):
    def __init__(self):
        super().__init__()
        self.host_ip = socket.gethostbyname(socket.gethostname())

    def format(self, record):
        log_data = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "module": record.module,
            "message": record.getMessage(),
            "ip": self.host_ip
        }
        return json.dumps(log_data)

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:4200"}})

    # Crear carpeta logs si no existe
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # Limpiar handlers previos para evitar duplicados
    if app.logger.hasHandlers():
        app.logger.handlers.clear()

    # Handler archivo
    file_handler = RotatingFileHandler("logs/api.log", maxBytes=1024 * 1024, backupCount=5)
    file_handler.setFormatter(JSONFormatter())
    file_handler.setLevel(logging.DEBUG)

    # Handler consola
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.DEBUG)

    # Añadir handlers
    app.logger.setLevel(logging.DEBUG)
    app.logger.addHandler(file_handler)
    if app.config["DEBUG"]:
        app.logger.addHandler(console_handler)

    # Igual limpiar y agregar handlers para werkzeug logger si lo usas
    werkzeug_logger = logging.getLogger('werkzeug')
    if werkzeug_logger.hasHandlers():
        werkzeug_logger.handlers.clear()
    werkzeug_logger.setLevel(logging.INFO)
    werkzeug_logger.addHandler(file_handler)
    if app.config["DEBUG"]:
        werkzeug_logger.addHandler(console_handler)

    # Registrar blueprints solo API
    from app.routes.api.auth_api import auth_api
    from app.routes.api.clientes_api import cliente_api

    app.register_blueprint(auth_api)
    app.register_blueprint(cliente_api)

    # Crear tablas solo si estás en desarrollo
    with app.app_context():
        if app.config["DEBUG"]:
            db.create_all()

    return app

