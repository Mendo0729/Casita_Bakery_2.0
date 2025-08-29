import os
from datetime import timedelta

class Config:
    # ---------------------- Flask ----------------------
    SECRET_KEY = os.getenv("APP_SECRET_KEY", "dev-secret-key-change-in-production")
    ENV = os.getenv("FLASK_ENV", "production")
    DEBUG = ENV == "development"

    # ---------------------- DB -------------------------
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('DB_USER', 'root')}:{os.getenv('DB_PASSWORD', '')}"
        f"@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '3306')}/{os.getenv('DB_NAME', 'casita_bakery')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 3600,
        "pool_pre_ping": True,
        "pool_size": 10,
        "max_overflow": 20,
    }

    # ---------------------- JWT ------------------------
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret-key-change-in-production")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_HEADER_NAME = "Authorization"
    JWT_HEADER_TYPE = "Bearer"

    # ---------------------- CORS -----------------------
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:4200").split(",")

    # ---------------------- LOGGING --------------------
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # ---------------------- DB auto-create (solo dev) ---
    AUTO_CREATE_DB = os.getenv("AUTO_CREATE_DB", "False").lower() in ("true", "1", "yes")


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = "development"


class ProductionConfig(Config):
    DEBUG = False
    ENV = "production"
    SESSION_COOKIE_SECURE = True  # solo en prod
