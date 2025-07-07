document.addEventListener('DOMContentLoaded', () => {
    const clienteSelect = document.getElementById('cliente_id');
    const productosContainer = document.getElementById('productos-container');
    const btnAgregarProducto = document.getElementById('agregar-producto');
    const totalSpan = document.getElementById('total');
    const form = document.getElementById('form-crear-pedido');

    let productosDisponibles = [];

    // Cargar clientes
    fetch('/clientes/api')
        .then(res => res.json())
        .then(clientes => {
            clientes.forEach(cliente => {
                const option = document.createElement('option');
                option.value = cliente.id;
                option.textContent = cliente.nombre;
                clienteSelect.appendChild(option);
            });
        });

    // Cargar productos
    fetch('/productos/api')
        .then(res => res.json())
        .then(productos => {
            productosDisponibles = productos;
            agregarFilaProducto(); // Primera fila
        });

    btnAgregarProducto.addEventListener('click', () => {
        agregarFilaProducto();
    });

    function agregarFilaProducto() {
        const row = document.createElement('div');
        row.classList.add('producto-item');

        row.innerHTML = `
            <select name="producto_id" class="producto-select">
                <option value="">Seleccionar producto</option>
                ${productosDisponibles.map(p => `<option value="${p.id}" data-precio="${p.precio}">${p.nombre}</option>`).join('')}
            </select>
            <input type="number" name="cantidad" min="1" value="1" class="input-cantidad" required>
            <span class="subtotal">$0.00</span>
            <button type="button" class="btn-remove">Eliminar</button>
        `;

        productosContainer.appendChild(row);
        asignarEventosFila(row);
        actualizarSubtotal(row);
    }

    function asignarEventosFila(row) {
        const select = row.querySelector('.producto-select');
        const cantidadInput = row.querySelector('.input-cantidad');
        const btnEliminar = row.querySelector('.btn-remove');

        select.addEventListener('change', () => actualizarSubtotal(row));
        cantidadInput.addEventListener('input', () => actualizarSubtotal(row));
        btnEliminar.addEventListener('click', () => {
            row.remove();
            calcularTotal();
        });
    }

    function actualizarSubtotal(row) {
        const select = row.querySelector('.producto-select');
        const cantidadInput = row.querySelector('.input-cantidad');
        const subtotalSpan = row.querySelector('.subtotal');

        const precio = parseFloat(select.selectedOptions[0]?.getAttribute('data-precio') || 0);
        const cantidad = parseInt(cantidadInput.value) || 0;
        const subtotal = precio * cantidad;

        subtotalSpan.textContent = `$${subtotal.toFixed(2)}`;
        calcularTotal();
    }

    function calcularTotal() {
        let total = 0;
        document.querySelectorAll('.producto-item').forEach(row => {
            const select = row.querySelector('.producto-select');
            const cantidadInput = row.querySelector('.input-cantidad');

            const precio = parseFloat(select.selectedOptions[0]?.getAttribute('data-precio') || 0);
            const cantidad = parseInt(cantidadInput.value) || 0;
            total += precio * cantidad;
        });

        totalSpan.textContent = `$${total.toFixed(2)}`;
    }

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const cliente_id = clienteSelect.value;
        const fecha_entrega = document.getElementById('fecha_entrega').value;
        const productos = [];
        let error = false;

        document.querySelectorAll('.producto-item').forEach(row => {
            const prodId = row.querySelector('.producto-select').value;
            const cantidad = row.querySelector('.input-cantidad').value;

            if (!prodId || cantidad <= 0) {
                error = true;
                row.classList.add('error-row');
            } else {
                row.classList.remove('error-row');
                productos.push({
                    producto_id: parseInt(prodId),
                    cantidad: parseInt(cantidad)
                });
            }
        });

        if (!cliente_id || productos.length === 0 || error) {
            Swal.fire({
                icon: 'warning',
                title: 'Formulario incompleto',
                text: 'Revisa los campos requeridos y vuelve a intentar.'
            });
            return;
        }

        try {
            Swal.fire({
                title: 'Creando pedido...',
                allowOutsideClick: false,
                didOpen: () => Swal.showLoading()
            });

            const res = await fetch('/pedidos/api/crear', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ cliente_id, fecha_entrega, productos })
            });

            const data = await res.json();

            if (data.success) {
                Swal.fire({
                    icon: 'success',
                    title: 'Pedido creado',
                    text: data.message || 'El pedido se creó correctamente',
                    confirmButtonText: 'OK'
                }).then(() => {
                    window.location.href = '/pedidos';
                });
            } else {
                Swal.fire({
                    icon: 'error',
                    title: 'Error al crear pedido',
                    text: data.message || 'Ocurrió un error inesperado.'
                });
            }

        } catch (err) {
            console.error(err);
            Swal.fire({
                icon: 'error',
                title: 'Error de red',
                text: 'No se pudo crear el pedido. Intenta más tarde.'
            });
        }
    });
});
