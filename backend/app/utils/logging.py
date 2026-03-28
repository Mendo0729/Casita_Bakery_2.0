import logging
import os
import re
from logging.handlers import RotatingFileHandler

from app.utils.json_logger import JSONFormatter


ANSI_ESCAPE_RE = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")


class StripAnsiFilter(logging.Filter):
    def filter(self, record):
        if isinstance(record.msg, str):
            record.msg = ANSI_ESCAPE_RE.sub("", record.msg)
        return True


def setup_logging(app):
    """Configura los logs para la aplicacion Flask."""
    log_level = getattr(
        logging,
        str(app.config.get("LOG_LEVEL", "INFO")).upper(),
        logging.INFO,
    )

    if not os.path.exists("logs"):
        os.makedirs("logs")

    if app.logger.hasHandlers():
        app.logger.handlers.clear()

    file_handler = RotatingFileHandler(
        "logs/api.log", maxBytes=1024 * 1024, backupCount=5
    )
    file_handler.setFormatter(JSONFormatter())
    file_handler.setLevel(log_level)
    file_handler.addFilter(StripAnsiFilter())

    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    )
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(log_level)
    console_handler.addFilter(StripAnsiFilter())

    app.logger.setLevel(log_level)
    app.logger.addHandler(file_handler)
    if app.config["DEBUG"]:
        app.logger.addHandler(console_handler)

    werkzeug_logger = logging.getLogger("werkzeug")
    if werkzeug_logger.hasHandlers():
        werkzeug_logger.handlers.clear()
    werkzeug_logger.setLevel(log_level)
    werkzeug_logger.addHandler(file_handler)
    if app.config["DEBUG"]:
        werkzeug_logger.addHandler(console_handler)

    app.logger.info("Logging inicializado correctamente")
