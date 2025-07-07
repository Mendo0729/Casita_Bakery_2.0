from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from app.services import dashboard_service

dashboard = Blueprint('dashboard', __name__, url_prefix="/dashboard")

@dashboard.route('/')
@login_required
def vista_dashboard():
    return render_template('dashboard/dashboard.html')

@dashboard.route('/api')
@login_required
def dashboard_api():
    try:
        data = dashboard_service.obtener_datos_dashboard()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
