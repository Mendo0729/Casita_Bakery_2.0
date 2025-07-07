from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, flash, jsonify
from app.services import clientes_service
from werkzeug.exceptions import BadRequest
from sqlalchemy.exc import SQLAlchemyError
from flask_login import login_required

clientes = Blueprint('clientes', __name__, url_prefix="/clientes")

#------------------------------------------------------------------------------
# ruta para listar los clientes
# ruta para cargar dinamicamente con javascript

#renderizar el template
@clientes.route('/', methods=['GET'])
@login_required
def listar():
    return render_template('clientes/listar.html')

#ruta de los datos
@clientes.route('/api', methods=['GET'])
@login_required
def api_clientes():
    try:
        nombre = request.args.get('nombre', '').strip()
        
        if nombre:
            current_app.logger.info(f"[CLIENTES] Búsqueda por nombre: '{nombre}'")
            clientes_lista = clientes_service.buscar_por_nombre(nombre)
        else:
            current_app.logger.info("[CLIENTES] Listando todos los clientes")
            clientes_lista = clientes_service.obtener_todos()

        clientes_json = [{
            "id": cliente.id,
            "nombre": cliente.nombre,
            "fecha_registro": cliente.fecha_registro.isoformat() if cliente.fecha_registro else None
        } for cliente in clientes_lista]

        current_app.logger.info(f"[CLIENTES] Encontrados {len(clientes_json)} clientes")
        return jsonify(clientes_json)

    except Exception as e:
        current_app.logger.error(f"[CLIENTES] Error al obtener clientes: {str(e)}")
        raise BadRequest("No se pudieron obtener los clientes")

#-------------------------------------------------------------------------------

@clientes.route("/nuevo", methods=['GET', 'POST'])
@login_required
def nuevo():
    form_data = {}  # Para preservar los datos del form en caso de error
    error = None
    
    if request.method == 'POST':
        try:
            form_data = request.form
            nombre = form_data.get('nombre', '').strip()

            # Validaciones
            if not nombre:
                error = "El nombre es obligatorio"
                raise ValueError(error)
                
            if len(nombre) > 100:
                error = "El nombre no puede exceder 100 caracteres"
                raise ValueError(error)

            # Crear cliente
            cliente = clientes_service.crear_cliente({'nombre': nombre})
            current_app.logger.info(f"[CLIENTES] Cliente creado: {cliente.nombre} (ID: {cliente.id})")
            
            flash(f"Cliente {cliente.nombre} creado exitosamente", 'success')
            return redirect(url_for('clientes.listar'))

        except ValueError as e:
            current_app.logger.warning(f"Error de validación: {str(e)}")
            if not error:
                error = "Datos inválidos"
            flash(error, 'error')

        except Exception as e:
            current_app.logger.error(f"Error creando cliente: {str(e)}", exc_info=True)
            flash("Ocurrió un error al crear el cliente", 'error')
            return redirect(url_for('clientes.nuevo_cliente'))

    return render_template('clientes/nuevo.html', form_data=form_data, error=error)

#-----------------------------------------------------------------------------------------

@clientes.route("/editar/<int:id>", methods=['GET', 'POST'])
@login_required
def editar_cliente(id):
    cliente = clientes_service.obtener_cliente_por_id(id)
    if not cliente:
        flash('Cliente no encontrado', 'error')
        current_app.logger.error(f"[CLIENTES] Cliente con ID {id} no encontrado")
        return redirect(url_for('clientes.listar'))

    if request.method == 'POST':
        try:
            nombre = request.form.get('nombre', '').strip()

            if not nombre:
                flash('El nombre es requerido', 'error')
                current_app.logger.warning(f"[CLIENTES] Campo nombre vacío al editar cliente ID {id}")
                return render_template('clientes/editar.html', cliente=cliente)
            
            if len(nombre) > 100:
                flash('Máximo 100 caracteres permitidos', 'error')
                current_app.logger.warning(f"[CLIENTES] Nombre demasiado largo al editar cliente ID {id}")
                return render_template('clientes/editar.html', cliente=cliente)

            # Actualización del cliente
            cliente_actualizado = clientes_service.actualizar_cliente(id, {'nombre': nombre})
            flash(f'Cliente "{cliente_actualizado.nombre}" actualizado correctamente', 'success')
            current_app.logger.info(f"[CLIENTES] Cliente ID {id} actualizado correctamente")
            return redirect(url_for('clientes.listar'))

        except Exception as e:
            flash('Error al actualizar el cliente', 'error')
            current_app.logger.error(f"[CLIENTES] Error actualizando cliente {id}: {str(e)}")
            return render_template('clientes/editar.html', cliente=cliente)

    return render_template('clientes/editar.html', cliente=cliente)

#------------------------------------------------------------------------------------------------------

@clientes.route("/eliminar/<int:id>", methods=['POST'])
@login_required
def eliminar_cliente(id):
    try:
        current_app.logger.info(f"[CLIENTES] Iniciando eliminación del cliente ID: {id}")
        
        cliente = clientes_service.eliminar_cliente(id)
        
        if cliente:
            current_app.logger.info(
                f"[CLIENTES] Cliente eliminado exitosamente - "
                f"ID: {cliente.id}, Nombre: {cliente.nombre}, "
                f"Fecha Registro: {cliente.fecha_registro}"
            )
            return jsonify({
                'success': True,
                'message': f'Cliente {cliente.nombre} eliminado correctamente',
                'deleted_id': cliente.id
            }), 200
        else:
            current_app.logger.warning(f"[CLIENTES] Intento de eliminar cliente inexistente - ID: {id}")
            return jsonify({
                'success': False,
                'message': 'El cliente no existe'
            }), 404
            
    except ValueError as e:
        current_app.logger.error(
            f"[CLIENTES] Error de validación al eliminar cliente - "
            f"ID: {id}, Error: {str(e)}",
            exc_info=True
        )
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
            
    except SQLAlchemyError as e:
        current_app.logger.error(
            f"[CLIENTES] Error de base de datos al eliminar cliente - "
            f"ID: {id}, Error: {str(e)}",
            exc_info=True
        )
        return jsonify({
            'success': False,
            'message': 'Error en la base de datos al eliminar cliente'
        }), 500
            
    except Exception as e:
        current_app.logger.error(
            f"[CLIENTES] Error inesperado al eliminar cliente - "
            f"ID: {id}, Error: {str(e)}",
            exc_info=True
        )
        return jsonify({
            'success': False,
            'message': 'Error inesperado al eliminar cliente'
        }), 500

#---------------------------------------------------------------------------------------------------------

@clientes.route('/<int:id>')
@login_required
def detalles(id):
    try:
        cliente = clientes_service.obtener_cliente_por_id(id)
        
        if not cliente:
            current_app.logger.warning(
                f"[CLIENTES] Intento de ver detalles de cliente inexistente - ID: {id}"
            )
            flash("Cliente no encontrado", "warning")
            return redirect(url_for("clientes.listar"))
        
        current_app.logger.info(
            f"[CLIENTES] Visualizando detalles del cliente - "
            f"ID: {cliente.id}, Nombre: {cliente.nombre}"
        )
        
        return render_template(
            'clientes/detalles.html',
            cliente=cliente,
            # pedidos=pedidos
        )
        
    except Exception as e:
        current_app.logger.error(
            f"[CLIENTES] Error al mostrar detalles del cliente - "
            f"ID: {id}, Error: {str(e)}",
            exc_info=True
        )
        flash("Ocurrió un error al cargar los detalles del cliente", "error")
        return redirect(url_for("clientes.listar"))

