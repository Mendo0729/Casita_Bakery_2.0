// ==================== CONFIGURACIÓN GLOBAL ====================
const URL_SHEET = 'https://script.google.com/macros/s/AKfycbzNhM_JqQDj8y94UEDKhIFqfTGbpSGkraEUJq1lxZbs9-jD9ABop60oZDzcxDrFSNML/exec';
const productosSeleccionados = [];
let datosPedidos = [];

// ==================== FUNCIONES DE MENSAJES ====================
function mostrarMensaje(mensaje, tipo = "exito") {
    const alerta = document.createElement("div");
    alerta.className = `alerta alerta-${tipo} mostrar`;

    let icono = '';
    switch (tipo) {
        case 'exito': icono = '✓'; break;
        case 'error': icono = '✗'; break;
        default: icono = 'i';
    }

    alerta.innerHTML = `<span>${icono}</span> ${mensaje}`;
    document.body.appendChild(alerta);

    setTimeout(() => {
        alerta.style.animation = 'fadeOut 0.5s forwards';
        setTimeout(() => alerta.remove(), 500);
    }, 3000);
}

function mostrarError(error) {
    const mensaje = error instanceof Error ? error.message : error;
    mostrarMensaje(mensaje, "error");
}

function mostrarCargaPedidos() {
    const tbody = document.querySelector('#tablaPedidos tbody');
    if (!tbody) return;
    tbody.innerHTML = `
        <tr class="cargando-fila">
            <td colspan="6" style="text-align: center; padding: 30px;">
                <div style="display: inline-flex; align-items: center;">
                    <div class="cargando"></div>
                    <span>Cargando pedidos...</span>
                </div>
            </td>
        </tr>
    `;
}

function formatearFecha(fechaString) {
    const fecha = new Date(fechaString);
    return fecha.toLocaleString('es-ES', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}
// Ejemplo: "31/05/2023, 14:30"

// ==================== INICIALIZACIÓN ====================
document.addEventListener('DOMContentLoaded', () => {
    const abrirModalBtn = document.getElementById('abrirModal');
    const modal = document.querySelector('.modal');
    const cerrarModal = document.querySelector('.close');
    const selectProducto = document.getElementById('producto');
    const formulario = document.getElementById('pedidoForm');

    if (abrirModalBtn) abrirModalBtn.addEventListener('click', () => modal.style.display = 'block');
    if (cerrarModal) cerrarModal.addEventListener('click', cerrarModalHandler);
    window.addEventListener('click', e => { if (e.target === modal) cerrarModalHandler(); });
    if (selectProducto) selectProducto.addEventListener('change', mostrarOpciones);
    if (formulario) formulario.addEventListener('submit', enviarPedido);

    if (document.getElementById('tablaPedidos')) cargarPedidos();

    const formBusqueda = document.getElementById('busquedaForm');
    const inputNombre = document.getElementById('buscarNombre');
    const inputFecha = document.getElementById('buscarFecha');
    const btnLimpiar = document.getElementById('limpiarBusqueda');

    // Función para buscar pedidos por nombre
    function buscarPedidosPorNombre(nombreBusqueda) {
        const nombreLower = nombreBusqueda.trim().toLowerCase();
        if (!nombreLower) return datosPedidos; // Si no hay texto, devuelve todos
        return datosPedidos.filter(pedido =>
            pedido.nombre.toLowerCase().includes(nombreLower)
        );
    }

    // Dentro de tu inicialización DOMContentLoaded, cambia el listener del formulario búsqueda por este:
    if (formBusqueda) {
        formBusqueda.addEventListener('submit', (e) => {
            e.preventDefault();
            const nombre = inputNombre.value.trim();
            const fecha = inputFecha.value;

            // Usa la función para buscar por nombre
            let resultados = buscarPedidosPorNombre(nombre);

            // Si hay fecha, filtra también por fecha
            if (fecha) {
                resultados = resultados.filter(p => p.fecha === fecha);
            }

            mostrarPedidos(resultados);
        });
    }

    if (btnLimpiar) {
        btnLimpiar.addEventListener('click', () => {
            inputNombre.value = '';
            inputFecha.value = '';
            mostrarPedidos(datosPedidos);
        });
    }
});

function cerrarModalHandler() {
    document.querySelector('.modal').style.display = 'none';
    document.getElementById('pedidoForm').reset();
    productosSeleccionados.length = 0;
    actualizarLista();
    document.getElementById('opcionesCantidad').style.display = 'none';
    document.getElementById('opcionesCheckboxes').innerHTML = '';
}

// ==================== UI ====================
function mostrarOpciones() {
    const producto = document.getElementById('producto').value;
    const opcionesDiv = document.getElementById('opcionesCantidad');
    const checkboxesDiv = document.getElementById('opcionesCheckboxes');
    checkboxesDiv.innerHTML = '';

    if (!producto) {
        opcionesDiv.style.display = 'none';
        return;
    }

    opcionesDiv.style.display = 'block';

    const opciones = producto === 'Cheesecake'
        ? ['Pedazo', 'Completo']
        : ['Individual', 'Caja de 3'];

    opciones.forEach(opcion => {
        checkboxesDiv.innerHTML += `
            <label><input type="checkbox" name="tipoPedido" value="${opcion}"> ${opcion}</label>
        `;
    });

    checkboxesDiv.innerHTML += `
        <label for="cantidad">Cantidad:</label>
        <input type="number" id="cantidad" name="cantidad" min="1" value="1">
    `;
}

function actualizarLista() {
    const lista = document.getElementById('productosSeleccionados');
    lista.innerHTML = '';
    productosSeleccionados.forEach((prod, i) => {
        const li = document.createElement('li');
        li.textContent = `${prod.nombre} - ${prod.tipo} x${prod.cantidad}`;
        const btn = document.createElement('button');
        btn.textContent = '❌';
        btn.onclick = () => eliminarProducto(i);
        btn.style.marginLeft = '10px';
        li.appendChild(btn);
        lista.appendChild(li);
    });
}

function eliminarProducto(index) {
    productosSeleccionados.splice(index, 1);
    actualizarLista();
}

// ==================== LÓGICA DE PRODUCTOS ====================
function agregarProducto() {
    const producto = document.getElementById('producto').value;
    const cantidad = parseInt(document.getElementById('cantidad')?.value || '1');
    const tipoSeleccionado = Array.from(document.querySelectorAll('#opcionesCheckboxes input[type="checkbox"]'))
        .filter(cb => cb.checked)
        .map(cb => cb.value)
        .join(', ');

    if (!producto || !tipoSeleccionado || cantidad < 1) {
        mostrarMensaje("Completa el producto, tipo y cantidad.", "error");
        return;
    }

    productosSeleccionados.push({ nombre: producto, tipo: tipoSeleccionado, cantidad });
    actualizarLista();
    document.getElementById('producto').value = '';
    document.getElementById('opcionesCantidad').style.display = 'none';
    document.getElementById('opcionesCheckboxes').innerHTML = '';
}

// ==================== ENVÍO ====================
function enviarPedido(e) {
    e.preventDefault();
    const nombre = document.getElementById('nombre').value.trim();
    const fechaInput = document.getElementById('fecha').value;

    if (!nombre || !fechaInput || productosSeleccionados.length === 0) {
        mostrarMensaje('Completa todos los campos y agrega productos.', 'error');
        return;
    }

    const fechaObj = new Date(fechaInput);
    if(isNaN(fechaObj.getTime())){
        mostrarMensaje('La fecha ingresada no es valida', 'error');
        return;
    }

    const pedidoTexto = productosSeleccionados.map(p => `${p.nombre} (${p.tipo} x${p.cantidad})`).join(', ');

    const data = {
        accion: 'agregar',
        nombre,
        pedido: pedidoTexto,
        fecha: fechaInput,
        estado: 'Pendiente',
        timestamp: new Date().toISOString()
    };

    fetch(URL_SHEET, {
        method: 'POST',
        mode: 'no-cors',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    }).then(() => {
        mostrarMensaje('Pedido enviado correctamente.');
        e.target.reset();
        productosSeleccionados.length = 0;
        actualizarLista();
        document.getElementById('opcionesCantidad').style.display = 'none';
        document.getElementById('opcionesCheckboxes').innerHTML = '';
        cargarPedidos();
        cerrarModalHandler();
    }).catch(err => {
        console.error(err);
        mostrarError('Error al guardar el pedido.');
    });
}

// ==================== GESTIÓN DE PEDIDOS ====================
function cargarPedidos() {
    mostrarCargaPedidos();

    fetch(URL_SHEET)
        .then(res => {
            if (!res.ok) throw new Error('Error en la respuesta del servidor');
            return res.json();
        })
        .then(data => {
            datosPedidos = data.filter(p => p.estado === 'Pendiente');
            mostrarPedidos(datosPedidos);
            mostrarMensaje("Pedidos cargados correctamente");
        })
        .catch(err => {
            console.error(err);
            mostrarError('Error al cargar pedidos.');
        });
}

function mostrarPedidos(pedidos) {
    const tbody = document.querySelector('#tablaPedidos tbody');
    if (!tbody) return;
    tbody.innerHTML = '';

    if (pedidos.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6">No hay pedidos.</td></tr>`;
        return;
    }

    pedidos.forEach(p => {
        const fila = document.createElement('tr');
        fila.innerHTML = `
            <td data-label="Fecha-Entrada">${formatearFecha(p.timestamp)}</td>
            <td data-label="Cliente" contenteditable="false">${p.nombre}</td>
            <td data-label="Pedido" contenteditable="false">${p.pedido}</td>
            <td data-label="Fecha-Entrega" contenteditable="false">${formatearFecha(p.fecha)}</td>
            <td data-label="Estado">
                <select class="estado-select" disabled>
                    <option value="Pendiente" ${p.estado === 'Pendiente' ? 'selected' : ''}>Pendiente</option>
                    <option value="Completado" ${p.estado === 'Completado' ? 'selected' : ''}>Completado</option>
                </select>
            </td>
            <td class="acciones" data-label="Acciones">
                    <button class="btn-editar" type="button"><img src="img/editar.png" alt="Editar"></button>
                    <button class="btn-guardar" type="button" style="display: none;"><img src="img/guardar.png" alt="Guardar"></button>
                    <button class="btn-eliminar" type="button"><img src="img/basura.png" alt="Eliminar"></button>
                    <button class="btn-cancelar" style="display:none;"><img src="img/cancelar.png" alt="Cancelar"></button>
                </td>
        `;

        tbody.appendChild(fila);

        const btnEditar = fila.querySelector('.btn-editar');
        const btnEliminar = fila.querySelector('.btn-eliminar');
        const btnGuardar = fila.querySelector('.btn-guardar');
        const btnCancelar = fila.querySelector('.btn-cancelar');
        const celdasEditables = fila.querySelectorAll('td[contenteditable]');
        const selectEstado = fila.querySelector('.estado-select');

        btnEditar.onclick = () => {
            celdasEditables.forEach(td => td.contentEditable = 'true');
            selectEstado.disabled = false;
            btnEditar.style.display = 'none';
            btnEliminar.style.display = 'none';
            btnGuardar.style.display = 'inline-block';
            btnCancelar.style.display = 'inline-block';
        };

        btnCancelar.onclick = () => {
            // Recargar datos originales para esta fila
            const original = datosPedidos.find(d => d.timestamp === p.timestamp);
            if (original) {
                fila.cells[1].textContent = original.nombre;
                fila.cells[2].textContent = original.pedido;
                fila.cells[3].textContent = original.fecha;
                selectEstado.value = original.estado;
            }
            celdasEditables.forEach(td => td.contentEditable = 'false');
            selectEstado.disabled = true;
            btnEditar.style.display = 'inline-block';
            btnEliminar.style.display = 'inline-block';
            btnGuardar.style.display = 'none';
            btnCancelar.style.display = 'none';
        };

        btnGuardar.onclick = () => {
            const nuevoNombre = fila.cells[1].textContent.trim();
            const nuevoPedido = fila.cells[2].textContent.trim();
            const nuevaFecha = fila.cells[3].textContent.trim();
            const nuevoEstado = selectEstado.value;

            if (!nuevoNombre || !nuevoPedido || !nuevaFecha) {
                mostrarMensaje('Todos los campos deben estar completos.', 'error');
                return;
            }

            const data = {
                accion: 'actualizar',
                timestamp: p.timestamp,
                nombre: nuevoNombre,
                pedido: nuevoPedido,
                fecha: nuevaFecha,
                estado: nuevoEstado
            };

            fetch(URL_SHEET, {
                method: 'POST',
                mode: 'no-cors',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            }).then(() => {
                mostrarMensaje('Pedido actualizado correctamente.');
                cargarPedidos();
            }).catch(err => {
                console.error(err);
                mostrarError('Error al actualizar el pedido.');
            });
        };

        btnEliminar.onclick = () => {
            if (!confirm('¿Seguro que quieres eliminar este pedido?')) return;
            const data = {
                accion: 'eliminar',
                timestamp: p.timestamp
            };

            fetch(URL_SHEET, {
                method: 'POST',
                mode: 'no-cors',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            }).then(() => {
                mostrarMensaje('Pedido eliminado correctamente.');
                cargarPedidos();
            }).catch(err => {
                console.error(err);
                mostrarError('Error al eliminar el pedido.');
            });
        };
    });
}