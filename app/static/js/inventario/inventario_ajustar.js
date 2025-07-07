document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector('form');

    manejarEnvioFormularioConLoader(form, {
        titulo: 'Guardando Ingrediente...',
        mensaje: 'Por favor espere',
        successMensaje: 'Ingrediente guardado!',
        retardo: 1000
    });
});
