import os
from datetime import timedelta

class Config:
    # ---------------------------- FLASK ---------------------------
    ENV = os.getenv("FLASK_ENV", "production")
    DEBUG = ENV == "development"
    SECRET_KEY = os.getenv("APP_SECRET_KEY", "dev-secret-key-change-in-production")

    # Configuración importante para sesiones
    SESSION_COOKIE_SECURE = ENV == "production"  # True en producción con HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    # ---------------------------- MySQL ---------------------------
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('DB_USER', 'root')}:{os.getenv('DB_PASSWORD', '')}"
        f"@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '3306')}/{os.getenv('DB_NAME', 'casita_bakery')}"
    )
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 3600,
        'pool_pre_ping': True,
        'pool_size': 10,
        'max_overflow': 20
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ---------------------------- JWT ---------------------------
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret-key-change-in-production")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", "3600")))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES", "2592000")))  # 30 días
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_HEADER_NAME = "Authorization"
    JWT_HEADER_TYPE = "Bearer"
    
    # Cookies (si decides usarlas en el futuro)
    JWT_COOKIE_SECURE = ENV == "production"  # True si usas HTTPS
    JWT_COOKIE_CSRF_PROTECT = ENV == "production"  # Protección CSRF solo en producción
