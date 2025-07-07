document.addEventListener('DOMContentLoaded', () => {
    const inputBuscar = document.getElementById('buscarCliente');
    const filtroEstado = document.getElementById('filtrarEstado');
    const btnBuscar = document.getElementById('search-btn');
    const btnLimpiar = document.getElementById('clear-search');
    const tbody = document.getElementById('pedidos-tbody');

    function cargarPedidos(cliente = '', estado = '') {
        let url = '/pedidos/api';
        const params = [];

        if (cliente) params.push(`cliente=${encodeURIComponent(cliente)}`);
        if (estado) params.push(`estado=${encodeURIComponent(estado)}`);
        if (params.length > 0) url += `?${params.join('&')}`;

        fetch(url)
            .then(res => {
                if (!res.ok) throw new Error('Respuesta no válida del servidor');
                return res.json();
            })
            .then(data => {
                tbody.innerHTML = '';

                if (data.length === 0) {
                    tbody.innerHTML = `<tr><td colspan="7">No se encontraron pedidos</td></tr>`;
                    return;
                }

                data.forEach(pedido => {
                    const fila = document.createElement('tr');
                    const acciones = [];

                    // Botón de ver
                    acciones.push(`
                        <a href="/pedidos/${pedido.id}" class="btn-ver" title="Ver Detalles">
                            <i class="fas fa-eye"></i>
                        </a>
                    `);

                    // Si está pendiente, mostrar botones de cambio de estado
                    if (pedido.estado === 'pendiente') {
                        acciones.push(`
                            <button class="btn-edit cambiar-estado" data-id="${pedido.id}" data-estado="entregado" title="Marcar como Entregado">
                                <i class="fas fa-check"></i>
                            </button>
                            <button class="btn-delete cambiar-estado" data-id="${pedido.id}" data-estado="cancelado" title="Cancelar Pedido">
                                <i class="fas fa-times"></i>
                            </button>
                        `);
                    }

                    fila.innerHTML = `
                        <td data-label="#">${pedido.id}</td>
                        <td data-label="Cliente">${pedido.cliente}</td>
                        <td data-label="Estado">${pedido.estado}</td>
                        <td data-label="Fecha Pedido">${pedido.fecha_pedido}</td>
                        <td data-label="Fecha Entrega">${pedido.fecha_entrega}</td>
                        <td data-label="Total">$${pedido.total.toFixed(2)}</td>
                        <td data-label="Acciones" class="actions">
                            ${acciones.join('')}
                        </td>
                    `;
                    tbody.appendChild(fila);
                });

                // Después de renderizar filas, asignar eventos
                asignarEventosCambioEstado();
            })
            .catch(error => {
                console.error('Error al cargar pedidos:', error);
                tbody.innerHTML = `<tr><td colspan="7">Error al cargar los pedidos</td></tr>`;
            });
    }

    function asignarEventosCambioEstado() {
        document.querySelectorAll('.cambiar-estado').forEach(btn => {
            btn.addEventListener('click', () => {
                const pedidoId = btn.getAttribute('data-id');
                const nuevoEstado = btn.getAttribute('data-estado');

                Swal.fire({
                    title: `¿Confirmar cambio a "${nuevoEstado}"?`,
                    icon: 'warning',
                    showCancelButton: true,
                    confirmButtonText: 'Sí, confirmar',
                    cancelButtonText: 'Cancelar'
                }).then(result => {
                    if (result.isConfirmed) {
                        fetch(`/pedidos/api/${pedidoId}/estado`, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({ estado: nuevoEstado })
                        })
                        .then(res => res.json())
                        .then(data => {
                            if (data.success) {
                                Swal.fire('Éxito', data.message, 'success').then(() => {
                                    cargarPedidos(inputBuscar.value.trim(), filtroEstado.value);
                                });
                            } else {
                                Swal.fire('Error', data.message, 'error');
                            }
                        })
                        .catch(err => {
                            console.error(err);
                            Swal.fire('Error', 'No se pudo cambiar el estado', 'error');
                        });
                    }
                });
            });
        });
    }

    // Eventos
    btnBuscar.addEventListener('click', () => {
        cargarPedidos(inputBuscar.value.trim(), filtroEstado.value);
    });

    btnLimpiar.addEventListener('click', () => {
        inputBuscar.value = '';
        filtroEstado.value = '';
        cargarPedidos();
    });

    inputBuscar.addEventListener('keyup', e => {
        if (e.key === 'Enter') {
            cargarPedidos(inputBuscar.value.trim(), filtroEstado.value);
        }
    });

    filtroEstado.addEventListener('change', () => {
        cargarPedidos(inputBuscar.value.trim(), filtroEstado.value);
    });

    // Cargar todos al iniciar
    cargarPedidos();
});
