import logging
import os
from logging.handlers import RotatingFileHandler

from app.utils.json_logger import JSONFormatter


def setup_logging(app):
    """Configura los logs para la aplicación Flask"""
    # Crear carpeta logs si no existe
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # Limpiar handlers previos para evitar duplicados
    if app.logger.hasHandlers():
        app.logger.handlers.clear()

    # Handler archivo con formato JSON
    file_handler = RotatingFileHandler(
        "logs/api.log", maxBytes=1024 * 1024, backupCount=5
    )
    file_handler.setFormatter(JSONFormatter())
    file_handler.setLevel(logging.DEBUG)

    # Handler consola (formato legible)
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    )
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.DEBUG)

    # Configuración del logger principal
    app.logger.setLevel(app.config.get("LOG_LEVEL", logging.INFO))
    app.logger.addHandler(file_handler)
    if app.config["DEBUG"]:
        app.logger.addHandler(console_handler)

    # Configurar werkzeug logger (requests)
    werkzeug_logger = logging.getLogger("werkzeug")
    if werkzeug_logger.hasHandlers():
        werkzeug_logger.handlers.clear()
    werkzeug_logger.setLevel(logging.INFO)
    werkzeug_logger.addHandler(file_handler)
    if app.config["DEBUG"]:
        werkzeug_logger.addHandler(console_handler)

    app.logger.info("✅ Logging inicializado correctamente")
