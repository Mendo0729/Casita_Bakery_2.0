import os
from app import create_app

# Detecta el entorno actual (default: development)
env = os.getenv("FLASK_ENV", "development")

# Mapea el entorno a la clase de configuración
config_map = {
    "development": "config.DevelopmentConfig",
    "production": "config.ProductionConfig",
}

# Si no encuentra el entorno, usa DevelopmentConfig por defecto
config_class = config_map.get(env, "config.DevelopmentConfig")

app = create_app(config_class)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0", 
        port=int(os.getenv("PORT", 5000)), 
        debug=(env == "development")
    )
