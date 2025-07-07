// Control del modal
document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('modalAgregar');
    const btnAbrir = document.getElementById('abrirModal');
    const btnCerrar = document.getElementById('cerrarModal');

    btnAbrir.addEventListener('click', function () {
        modal.style.display = 'block';
    });

    btnCerrar.addEventListener('click', function () {
        modal.style.display = 'none';
    });

    // Cerrar al hacer click fuera del modal
    window.addEventListener('click', function (event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    });
});