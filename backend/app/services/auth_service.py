import logging
import time

from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import check_password_hash

from app.models import Usuario
from app.utils.create_responses import create_response as response
from app.utils.db import db

logger = logging.getLogger(__name__)

def validacion_usuario(username, password):

    try:

        # Agregar validaciones de tipo y longitud
        if not isinstance(username, str) or not isinstance(password, str):
            return response(
                success=False,
                message="Datos de entrada inválidos",
                errors={
                    "code": "invalid_input",
                    "detail": "Los campos deben ser texto"
                    },
                status_code=400
            )

        username = username.strip()
        password = password.strip()

        if not username or not password:
            return response(
                success=False,
                message="Los campos no pueden estar vacíos",
                errors={
                    "code": "empty_fields",
                    "detail": "Los campos son requeridos"
                },
                status_code=400
            )
        user = Usuario.query.filter_by(usuario=username).first()
        if not user or not user.check_password(password):
            time.sleep(0.5)  # Protección contra ataques de fuerza bruta
            logger.warning(f"Intento de login fallido para usuario: {username}")
            return response(
                success=False,
                message="Nombre de usuario o contraseña incorrectos",
                errors={
                    "code": "invalid_credentials",
                    "detail": "Nombre de usuario o contraseña incorrectos"
                    },
                status_code=401
            )
        logger.info(f"Usuario autenticado exitosamente: {username}")
        return response(
            success=True,
            data=user.to_dict(),
            message="Usuario autenticado exitosamente",
            status_code=200
        )

    except SQLAlchemyError as e:
        logger.error(f"Error al validar el usuario {username}: {str(e)}")
        return response(
            success=False,
            message="Error al validar el usuario",
            errors={
                "code": "database_error",
                "detail": str(e)},
            status_code=500
        )
    except Exception as e:
        logger.error(f"Error inesperado al obtener las tarea: {str(e)}")
        return response(
            success=False,
            message="Error interno al validar el usuario",
            errors={
                "code": "internal_server_error",
                "detail": "Error interno del servidor"
                },
            status_code=500
        ) 

"""def cerrar_sesion():
    session.clear()"""
