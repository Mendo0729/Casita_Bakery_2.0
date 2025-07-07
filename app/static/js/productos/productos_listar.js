document.addEventListener('DOMContentLoaded', () => {
    const inputBuscar = document.getElementById('buscarProducto');
    const btnBuscar = document.getElementById('search-btn');
    const btnLimpiar = document.getElementById('clear-search');
    const tbody = document.getElementById('productos-tbody');

    function cargarProductos(filtro = '') {
        const url = filtro ? `/productos/api?producto=${encodeURIComponent(filtro)}` : '/productos/api';

        fetch(url)
            .then(res => res.json())
            .then(data => {
                tbody.innerHTML = '';

                if (data.length === 0) {
                    tbody.innerHTML = `<tr><td colspan="4">No se encontraron productos</td></tr>`;
                    return;
                }

                data.forEach(producto => {
                    const fila = document.createElement('tr');
                    fila.innerHTML = `
                        <td data-label="ID">${producto.id}</td>
                        <td data-label="Nombre">${producto.nombre}</td>
                        <td data-label="Precio">$${parseFloat(producto.precio).toFixed(2)}</td>
                        <td data-label="Acciones" class="actions">
                            <a href="/productos/${producto.id}" class="btn-ver" title="Ver detalles">
                                <i class="fas fa-eye"></i>
                            </a>
                            <a href="/productos/editar/${producto.id}" class="btn-edit" title="Editar">
                                <i class="fas fa-pen-to-square"></i>
                            </a>
                            <button class="btn-delete" data-id="${producto.id}" title="Eliminar">
                                <i class="fas fa-trash-alt"></i>
                            </button>
                        </td>
                    `;
                    tbody.appendChild(fila);
                });

                asignarEventosEliminar(); // <- ¡Importante!
            })
            .catch(error => {
                console.error('Error al cargar productos:', error);
                tbody.innerHTML = `<tr><td colspan="4">Error al cargar productos</td></tr>`;
            });
    }

    function asignarEventosEliminar() {
        document.querySelectorAll('.btn-delete').forEach(button => {
            button.addEventListener('click', async (e) => {
                const productoId = button.getAttribute('data-id');

                const confirm = await Swal.fire({
                    title: '¿Estás seguro?',
                    text: 'Esta acción desactivará el producto.',
                    icon: 'warning',
                    showCancelButton: true,
                    confirmButtonText: 'Sí, eliminar',
                    cancelButtonText: 'Cancelar'
                });

                if (confirm.isConfirmed) {
                    try {
                        const response = await fetch(`/productos/eliminar/${productoId}`, {
                            method: 'POST',
                            headers: {
                                'X-Requested-With': 'XMLHttpRequest'
                            }
                        });

                        const result = await response.json();

                        if (result.success) {
                            Swal.fire('Eliminado', result.message, 'success');
                            // Quitar la fila eliminada
                            const row = button.closest('tr');
                            if (row) row.remove();
                        } else {
                            Swal.fire('Error', result.message, 'error');
                        }
                    } catch (error) {
                        Swal.fire('Error', 'Error al intentar eliminar el producto.', 'error');
                        console.error(error);
                    }
                }
            });
        });
    }

    // Eventos para búsqueda
    btnBuscar.addEventListener('click', () => cargarProductos(inputBuscar.value.trim()));
    btnLimpiar.addEventListener('click', () => {
        inputBuscar.value = '';
        cargarProductos();
    });
    inputBuscar.addEventListener('keyup', e => {
        if (e.key === 'Enter') cargarProductos(inputBuscar.value.trim());
    });

    // Inicial
    cargarProductos();
});
