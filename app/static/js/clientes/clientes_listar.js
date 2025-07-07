document.addEventListener('DOMContentLoaded', function () {
    const clientesTable = document.getElementById('clientes-tbody');
    const searchInput = document.getElementById('search-input');
    const searchBtn = document.getElementById('search-btn');
    const clearBtn = document.getElementById('clear-search');
    let isLoading = false;

    // Función para mostrar estado de carga
    function showLoading() {
        if (isLoading) return;
        isLoading = true;
        clientesTable.innerHTML = `
            <tr>
                <td colspan="4" class="loading">
                    <div class="spinner"></div>
                    Cargando clientes...
                </td>
            </tr>
        `;
    }

    // Función para cargar clientes
    function cargarClientes(nombre = '') {
        showLoading();

        let url = '/clientes/api';
        if (nombre) {
            url += `?nombre=${encodeURIComponent(nombre)}`;
        }

        fetch(url)
            .then(response => {
                if (!response.ok) throw new Error('Error en la respuesta del servidor');
                return response.json();
            })
            .then(clientes => {
                isLoading = false;
                renderClientes(clientes, nombre);
            })
            .catch(error => {
                isLoading = false;
                showError(error);
            });
    }

    // Función para renderizar clientes
    let currentPage = 1;
    let itemsPerPage = 10;
    let totalItems = 0;

    function renderClientes(clientes, searchTerm = '') {
        clientesTable.innerHTML = '';

        if (clientes.length === 0) {
            clientesTable.innerHTML = `
            <tr>
                <td colspan="4">
                    No se encontraron clientes
                    ${searchTerm ? `con el nombre "${searchTerm}"` : ''}
                </td>
            </tr>
        `;
            return;
        }

        const startNumber = (currentPage - 1) * itemsPerPage + 1;

        clientes.forEach((cliente, index) => {
            const row = document.createElement('tr');
            row.setAttribute('data-client-id', cliente.id);
            row.innerHTML = `
            <td data-label="#">${startNumber + index}</td>
            <td data-label="Nombre">${cliente.nombre}</td>
            <td data-label="Fecha de registro">${formatDate(cliente.fecha_registro)}</td>
            <td data-label="Acciones" class="actions">
                <a href="/clientes/${cliente.id}" class="btn-ver" title="Ver detalles" data-client-id="${cliente.id}">
                    <i class="fa-solid fa-eye"></i>
                </a>
                <a href="/clientes/editar/${cliente.id}" class="btn-edit" title="Editar">
                    <i class="fa-solid fa-pen-to-square"></i>
                </a>
                <button class="btn-delete" data-id="${cliente.id}" title="Eliminar">
                    <i class="fa-regular fa-trash-can"></i>
                </button>
            </td>
        `;
            clientesTable.appendChild(row);
        });

        setupDeleteButtons();
        setupViewButtons();  // Asegúrate de llamar esta función
    }

    // Configurar botones de ver detalles
    function setupViewButtons() {
        document.querySelectorAll('.btn-ver').forEach(btn => {
            btn.addEventListener('click', function (e) {
                e.preventDefault();
                const clienteId = this.getAttribute('data-client-id');
                console.log('Intentando navegar a:', `/clientes/${clienteId}`);
                window.location.href = `/clientes/${clienteId}`;
            });
        });
    }


    // Función para formatear fecha
    function formatDate(dateString) {
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        return new Date(dateString).toLocaleDateString('es-ES', options);
    }

    // Función para mostrar errores
    function showError(error) {
        console.error('Error al cargar clientes:', error);
        clientesTable.innerHTML = `
            <tr>
                <td colspan="4" class="error">
                    <i class="fa-solid fa-triangle-exclamation"></i>
                    Error al cargar los clientes. Intenta nuevamente.
                </td>
            </tr>
        `;
    }

    // Configurar botones de eliminar
    function setupDeleteButtons() {
        document.querySelectorAll('.btn-delete').forEach(btn => {
            btn.addEventListener('click', function () {
                const clienteId = this.getAttribute('data-id');
                confirmDelete(clienteId);
            });
        });
    }

    // Confirmar eliminación
    function confirmDelete(clienteId) {
        Swal.fire({
            title: '¿Eliminar cliente?',
            text: "Esta acción no se puede deshacer",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#5E2D1E',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Sí, eliminar',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.isConfirmed) {
                eliminarCliente(clienteId);
            }
        });
    }

    // Función para eliminar cliente - VERSIÓN CORREGIDA
    function eliminarCliente(id) {
        fetch(`/clientes/eliminar/${id}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        })
            .then(response => {
                console.log('Status:', response.status); // Agrega esto
                console.log('Response:', response); // Agrega esto
                if (!response.ok) throw new Error('Error al eliminar');
                return response.json();
            })
            .then(data => {
                console.log('Data:', data); // Agrega esto
                if (data.success) {
                    Swal.fire('¡Eliminado!', data.message, 'success');
                    document.querySelector(`tr[data-client-id="${id}"]`)?.remove();
                    cargarClientes(searchInput.value);
                } else {
                    throw new Error(data.message);
                }
            })
            .catch(error => {
                console.error('Error completo:', error); // Agrega esto
                Swal.fire('Error', error.message, 'error');
            });
    }

    // Event listeners
    searchBtn.addEventListener('click', () => cargarClientes(searchInput.value));
    clearBtn.addEventListener('click', () => {
        searchInput.value = '';
        cargarClientes();
    });
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') cargarClientes(searchInput.value);
    });

    // Cargar clientes al iniciar
    cargarClientes();
});