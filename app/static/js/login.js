document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    const usuarioInput = document.getElementById("usuario");
    const passwordInput = document.getElementById("password");

    // Validación de campos vacíos antes de enviar
    form.addEventListener("submit", function (e) {
        const usuario = usuarioInput.value.trim();
        const password = passwordInput.value.trim();

        if (!usuario || !password) {
            e.preventDefault(); // Detiene el envío del formulario
            Swal.fire({
                icon: "warning",
                title: "Campos obligatorios",
                text: "Por favor, completa todos los campos.",
                confirmButtonColor: "#d4777c",
            });
        }
    });

    // Mostrar mensajes flash del servidor (por ejemplo, login incorrecto)
    const flashMessages = document.querySelectorAll("[data-flash-message]");
    flashMessages.forEach((el) => {
        const tipo = el.dataset.flashCategory || "info";
        const mensaje = el.dataset.flashMessage;

        Swal.fire({
            icon: {
                success: "success",
                danger: "error",
                warning: "warning",
                info: "info",
            }[tipo] || "info",
            title: mensaje,
            confirmButtonColor: "#d4777c",
        });
    });
});
