
from flask import Blueprint, render_template, request, redirect, url_for
from app.services import recetas_service, productos_service, inventario_service
from flask_login import login_required

recetas = Blueprint('recetas', __name__)

@recetas.route('/recetas')
@login_required
def listar_recetas():
    print("Entrando a listar_recetas()")
    productos = productos_service.obtener_todos()
    return render_template('recetas/listar.html', productos=productos)

# Ver ingredientes (receta) de un producto específico
@recetas.route('/recetas/<int:producto_id>')
@login_required
def ver_receta(producto_id):
    receta = recetas_service.obtener_por_producto(producto_id)
    producto = productos_service.obtener_por_id(producto_id)
    ingredientes = inventario_service.obtener_todos()
    return render_template('recetas/ver.html', receta=receta, producto=producto, ingredientes=ingredientes)

# Agregar un ingrediente a la receta de un producto
@recetas.route('/recetas/<int:producto_id>/agregar', methods=['POST'])
@login_required
def agregar_ingrediente(producto_id):
    ingrediente_id = int(request.form['ingrediente_id'])
    cantidad = float(request.form['cantidad'])
    recetas_service.agregar_ingrediente_a_receta(producto_id, ingrediente_id, cantidad)
    return redirect(url_for('recetas.ver_receta', producto_id=producto_id))

# Eliminar un ingrediente de la receta
@recetas.route('/recetas/<int:producto_id>/eliminar/<int:ingrediente_id>', methods=['POST'])
@login_required
def eliminar_ingrediente(producto_id, ingrediente_id):
    recetas_service.eliminar_ingrediente_de_receta(producto_id, ingrediente_id)
    return redirect(url_for('recetas.ver_receta', producto_id=producto_id))
