# app/routes/main.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app.models import Usuario

main = Blueprint("main", __name__)

@main.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        password = request.form.get('password')

        user = Usuario.query.filter_by(usuario=usuario).first()
        if user and user.check_password(password):
            login_user(user)  # <-- Flask-Login maneja la sesión
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('dashboard.vista_dashboard'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')

    return render_template('index.html')


@main.route('/logout')
@login_required
def logout():
    logout_user()  # <-- Cierra sesión con Flask-Login
    flash("Has cerrado sesión correctamente", "info")
    return redirect(url_for('main.login'))
