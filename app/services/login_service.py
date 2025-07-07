from app.models import Usuario
from flask import session
from werkzeug.security import check_password_hash

def autenticar_usuario(usuario, password):
    user = Usuario.query.filter_by(usuario=usuario).first()
    if user and user.check_password(password):
        session['usuario_id'] = user.id
        session['usuario'] = user.usuario
        return True
    return False

def cerrar_sesion():
    session.clear()
