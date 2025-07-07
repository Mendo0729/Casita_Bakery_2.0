document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('nuevoProductoForm');
    const nombreInput = document.getElementById('nombre');
    const precioInput = document.getElementById('precio');

    const isEditing = document.title.toLowerCase().includes('editar');

    const validarFormulario = () => {
        const nombre = nombreInput.value.trim();
        const precio = precioInput.value.trim();

        if (!nombre) {
            nombreInput.focus();
            nombreInput.classList.add('input-error');
            Swal.fire('Error', 'El nombre es obligatorio', 'error');
            return false;
        }

        if (nombre.length < 3 || nombre.length > 100) {
            nombreInput.focus();
            nombreInput.classList.add('input-error');
            Swal.fire('Error', 'El nombre debe tener entre 3 y 100 caracteres', 'error');
            return false;
        }

        const precioDecimal = parseFloat(precio.replace(',', '.'));
        if (isNaN(precioDecimal) || precioDecimal <= 0) {
            precioInput.focus();
            precioInput.classList.add('input-error');
            Swal.fire('Error', 'El precio debe ser un número positivo', 'error');
            return false;
        }

        nombreInput.classList.remove('input-error');
        precioInput.classList.remove('input-error');
        return true;
    };

    form.addEventListener('submit', function (e) {
        e.preventDefault(); // Detiene envío inmediato

        if (!validarFormulario()) return;

        Swal.fire({
            title: isEditing ? 'Guardando cambios...' : 'Creando producto...',
            html: 'Por favor espera',
            allowOutsideClick: false,
            didOpen: () => {
                Swal.showLoading();
            }
        });

        // Espera antes de enviar realmente el form
        setTimeout(() => {
            form.submit();
        }, 1800); // 1.8 segundos de espera
    });

    // Cierre de alertas flash
    document.querySelectorAll('.close-flash').forEach(button => {
        button.addEventListener('click', (e) => {
            e.target.closest('.alert').style.display = 'none';
        });
    });
});
