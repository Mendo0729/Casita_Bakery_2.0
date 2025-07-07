/**
 * Muestra un loader SweetAlert al enviar un formulario y luego lo envía con retardo opcional.
 * @param {HTMLFormElement} form - El formulario a gestionar.
 * @param {Object} options - Opciones de configuración.
 * @param {string} options.titulo - Título del loader.
 * @param {string} options.mensaje - Texto que se muestra durante el loader.
 * @param {string} options.successMensaje - Texto del mensaje de éxito.
 * @param {number} options.retardo - Milisegundos antes de enviar el formulario (opcional).
 */
function manejarEnvioFormularioConLoader(form, {
    titulo = 'Procesando...',
    mensaje = 'Por favor espere',
    successMensaje = '¡Completado!',
    retardo = 1000
} = {}) {
    if (!form) return;

    form.addEventListener('submit', function (e) {
        e.preventDefault();

        Swal.fire({
            title: titulo,
            text: mensaje,
            allowOutsideClick: false,
            allowEscapeKey: false,
            didOpen: () => {
                Swal.showLoading();
            }
        });

        setTimeout(() => {
            Swal.fire({
                icon: 'success',
                title: successMensaje,
                showConfirmButton: false,
                timer: 1500
            }).then(() => {
                e.target.submit();
            });
        }, retardo);
    });
}
