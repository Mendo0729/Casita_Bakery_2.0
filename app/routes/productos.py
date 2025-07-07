from flask import Blueprint, render_template, request, redirect, url_for, current_app, flash, jsonify
from app.services import productos_service
from werkzeug.exceptions import BadRequest
from decimal import Decimal
from sqlalchemy.exc import SQLAlchemyError
from flask_login import login_required

productos = Blueprint('productos', __name__, url_prefix="/productos")

#----------------------------------------------------------------------------
# ruta para listar los productos
# ruta para cargar dinamicamente con javascript

@productos.route('/', methods=['GET'])
@login_required
def listar():
    return render_template('productos/listar.html')

#ruta de los datos
@productos.route('/api', methods=['GET'])
@login_required
def api_productos():
    try:
        producto = request.args.get('producto', '').strip()
        if producto:
            current_app.logger.info(f"[PRODUCTOS] Búsqueda por nombre: '{producto}'")
            lista = productos_service.obtener_por_nombre(producto)
        else:
            current_app.logger.info("[PRODUCTOS] Listando todos los productos")
            lista = productos_service.obtener_todos()

        productos_json = [{
            "id": p.id,
            "nombre": p.nombre,
            "precio": p.precio
        } for p in lista]

        current_app.logger.info(f"[PRODUCTOS] Encontrados {len(productos_json)} productos")
        return jsonify(productos_json)

    except Exception as e:
        current_app.logger.error(f"[PRODUCTOS] Error al obtener productos: {str(e)}")
        raise BadRequest("No se pudieron obtener los productos")

#-------------------------------------------------------------------------------------------------

@productos.route('/productos/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_producto():
    form_data = {} 
    error = None

    if request.method == 'POST':
        try:
            form_data = request.form
            nombre = form_data.get('nombre', '').strip()
            precio = form_data.get('precio', '').strip()
            descripcion = form_data.get('descripcion', '').strip()

            if not nombre:
                error = "El nombre es obligatorio"
                raise ValueError(error)
                
            if len(nombre) > 100:
                error = "El nombre no puede exceder 100 caracteres"
                raise ValueError(error)
            
            try:
                precio_val = Decimal(precio)
                if precio_val <= 0:
                    raise ValueError
            except:
                error = "El precio debe ser un número positivo"
                raise ValueError(error)
            
            producto = productos_service.crear({
                'nombre': nombre,
                'precio': precio,
                'descripcion': descripcion
            })

            flash(f"Producto '{producto.nombre}' creado exitosamente", "success")
            return redirect(url_for('productos.listar'))

        except ValueError as e:
            current_app.logger.warning(f"Error de validación: {str(e)}")
            flash(error or "Datos inválidos", "error")

        except Exception as e:
            current_app.logger.error(f"Error creando el Producto: {str(e)}", exc_info=True)
            flash("Ocurrió un error al crear el producto", 'error')
            return redirect(url_for('clientes.nuevo_producto'))
            
        
    return render_template('productos/nuevo.html', form_data=form_data, error=error)

#------------------------------------------------------------------------------------------------------

@productos.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_producto(id):
    producto = productos_service.obtener_por_id(id)
    if not producto:
        flash("Producto no encontrado", "error")
        return redirect(url_for('productos.listar'))

    error = None
    form_data = {
        "nombre": producto.nombre,
        "precio": producto.precio,
        "descripcion": producto.descripcion or ""
    }

    if request.method == 'POST':
        try:
            form_data = request.form
            nombre = form_data.get('nombre', '').strip()
            precio = form_data.get('precio', '').strip()
            descripcion = form_data.get('descripcion', '').strip()

            if not nombre:
                error = "El nombre es obligatorio"
                raise ValueError(error)

            if len(nombre) > 100:
                error = "El nombre no puede exceder 100 caracteres"
                raise ValueError(error)

            try:
                precio_val = Decimal(precio)
                if precio_val <= 0:
                    raise ValueError
            except:
                error = "El precio debe ser un número positivo"
                raise ValueError(error)
            
            producto = productos_service.actualizar(id, {
                'nombre': nombre,
                'precio': precio_val,
                'descripcion': descripcion
            })

            flash(f"Producto '{producto.nombre}' actualizado correctamente", "success")
            return redirect(url_for('productos.listar'))

        except ValueError as e:
            current_app.logger.warning(f"[PRODUCTO] Validación fallida: {str(e)}")
            flash(error or "Datos inválidos", "error")

        except Exception as e:
            current_app.logger.error(f"[PRODUCTO] Error editando producto {id}: {str(e)}", exc_info=True)
            flash("Ocurrió un error al editar el producto", 'error')

    return render_template('productos/editar.html', form_data=form_data, error=error, producto=producto)

#------------------------------------------------------------------------------------------------------------

@productos.route('/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_producto(id):
    try:
        current_app.logger.info(f"[PRODUCTOS] Iniciando eliminación del Producto ID: {id}")

        producto = productos_service.eliminar(id)

        if producto:
            current_app.logger.info(
                f"[PRODUCTOS] Producto desactivado exitosamente - "
                f"ID: {producto.id}, Nombre: {producto.nombre}"
            )
            return jsonify({
                'success': True,
                'message': f'Producto {producto.nombre} desactivado correctamente',
                'desactivate_id': producto.id
            }), 200

        current_app.logger.warning(f"[PRODUCTOS] Intento de desactivar producto inexistente - ID: {id}")
        return jsonify({
            'success': False,
            'message': 'El producto no existe'
        }), 404

    except ValueError as e:
        current_app.logger.error(f"[PRODUCTOS] Error de validación - ID: {id} - {str(e)}", exc_info=True)
        return jsonify({'success': False, 'message': str(e)}), 400

    except SQLAlchemyError as e:
        current_app.logger.error(f"[PRODUCTOS] Error de DB - ID: {id} - {str(e)}", exc_info=True)
        return jsonify({'success': False, 'message': 'Error en la base de datos'}), 500

    except Exception as e:
        current_app.logger.error(f"[PRODUCTOS] Error inesperado - ID: {id} - {str(e)}", exc_info=True)
        return jsonify({'success': False, 'message': 'Error inesperado al desactivar el producto'}), 500

#----------------------------------------------------------------------------------------------------------------------------------------------


@productos.route('/<int:id>')
@login_required
def detalle_producto(id):
    try:
        producto = productos_service.obtener_por_id(id)
        
        if not producto:
            current_app.logger.warning(
                f"[PRODUCTOS] Intento de ver detalles de un Producto inexistente - ID: {id}"
            )
            flash("Producto no encontrado", "warning")
            return redirect(url_for("productos.listar"))
        
        current_app.logger.info(
            f"[PRODUCTO] Visualizando detalles del Producto - "
            f"ID: {producto.id}, Nombre: {producto.nombre}"
        )
        
        return render_template(
            'productos/detalles.html',
            producto=producto,
        )
        
    except Exception as e:
        current_app.logger.error(
            f"[PRODUCTOS] Error al mostrar detalles del Producto - "
            f"ID: {id}, Error: {str(e)}",
            exc_info=True
        )
        flash("Ocurrió un error al cargar los detalles del Producto", "error")
        return redirect(url_for("productos.listar"))
