from flask import Blueprint, render_template, request, redirect, url_for
from app.services import inventario_service
from flask_login import login_required

inventario = Blueprint('inventario', __name__)

@inventario.route('/inventario')
@login_required
def listar_ingredientes():
    nombre = request.args.get('nombre', '').strip()
    if nombre:
        lista = inventario_service.obtener_por_nombre(nombre)
    else:
        lista = inventario_service.obtener_todos()
    return render_template('inventario/listar.html', inventario=lista)

@inventario.route('/inventario/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_ingrediente():
    if request.method == 'POST':
        data = {
            'nombre': request.form['nombre'],
            'cantidad': request.form['cantidad'],
            'unidad_medida': request.form.get('unidad_medida', 'unidades'),
            'punto_reorden': request.form.get('punto_reorden', '5.00')
        }
        inventario_service.crear(data)
        return redirect(url_for('inventario.listar_ingredientes'))
    return render_template('inventario/ajustar.html')

@inventario.route('/inventario/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_ingrediente(id):
    ingrediente = inventario_service.obtener_por_id(id)
    if request.method == 'POST':
        data = {
            'nombre': request.form['nombre'],
            'cantidad': request.form['cantidad'],
            'unidad_medida': request.form.get('unidad_medida', ingrediente.unidad_medida),
            'punto_reorden': request.form.get('punto_reorden', ingrediente.punto_reorden)
        }
        inventario_service.actualizar(id, data)
        return redirect(url_for('inventario.listar_ingredientes'))
    return render_template('inventario/ajustar.html', ingrediente=ingrediente)

@inventario.route('/inventario/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_ingrediente(id):
    inventario_service.eliminar(id)
    return redirect(url_for('inventario.listar_ingredientes'))
