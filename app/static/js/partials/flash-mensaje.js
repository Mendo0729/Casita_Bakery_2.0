document.addEventListener("DOMContentLoaded", () => {
    const flashes = document.querySelectorAll(".flash-data");

    flashes.forEach(flash => {
        const tipo = flash.getAttribute("data-tipo");
        const mensaje = flash.getAttribute("data-mensaje");

        Swal.fire({
            icon: tipo === "success" ? "success" : "error",
            title: mensaje,
            showConfirmButton: false,
            timer: 2000,
        });
    });
});
