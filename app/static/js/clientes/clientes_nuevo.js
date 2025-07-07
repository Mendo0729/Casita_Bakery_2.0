document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById('clienteForm');
    if (!form) return;

    // Configuración del loader
    const loaderConfig = {
        titulo: 'Guardando cliente...',
        mensaje: 'Por favor espere',
        successMensaje: '¡Cliente guardado exitosamente!',
        retardo: 1000
    };

    // Validación personalizada antes de mostrar el loader
    form.addEventListener('submit', function(e) {
        const nombre = document.getElementById('nombre').value.trim();
        
        // Validación que coincide con el backend
        if (!nombre) {
            e.preventDefault();
            Swal.fire('Error', 'El nombre es requerido', 'error');
            return;
        }
        
        if (nombre.length > 100 || nombre.length <= 2) {
            e.preventDefault();
            Swal.fire('Error', 'El nombre no puede tener menos de 3 caracteres o exceder los 100 caracteres', 'error');
            return;
        }
        
        // Si pasa la validación, proceder con el loader
        manejarEnvioFormularioConLoader(form, loaderConfig);
    });
});