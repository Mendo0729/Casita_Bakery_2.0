from flask import Flask, render_template
from flask_login import LoginManager  # Corrección aquí
from .utils.db import db
from .models import Usuario
from flask_migrate import Migrate
from config import Config


import logging
from logging.handlers import RotatingFileHandler
import os

login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message_category = "warning"

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

def configurar_logs(app):
    if not os.path.exists('logs'):
        os.makedirs('logs')

    log_handler = RotatingFileHandler('logs/casita.log', maxBytes=100000, backupCount=3)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
    log_handler.setFormatter(formatter)
    log_handler.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    app.logger.addHandler(log_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Aplicación Casita Bakery iniciada')

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    configurar_logs(app)
    # migrate = Migrate(app, db)  # opcional, si usas Flask-Migrate

    login_manager.init_app(app)

    # Blueprints

    return app
