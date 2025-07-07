export function createSidebar() {
    // Crear contenedor principal del sidebar
    const menuSide = document.createElement("div");
    menuSide.className = "menu__side";

    // Botón hamburguesa con imagen
    const toggleButton = document.createElement("button");
    toggleButton.className = "hamburger-btn";
    const toggleIcon = document.createElement("img");
    toggleIcon.src = "static/img/menu.png";
    toggleIcon.alt = "Menú";
    toggleIcon.className = "menu-icon";
    toggleButton.appendChild(toggleIcon);
    menuSide.appendChild(toggleButton);

    // Crear nombre de la página
    const namePage = document.createElement("div");
    namePage.className = "name__page";
    const h4 = document.createElement("h4");
    h4.textContent = "Casita Bakery";
    namePage.appendChild(h4);

    // Crear contenedor de opciones del menú
    const optionsMenu = document.createElement("div");
    optionsMenu.className = "options__menu";

    // Datos de enlaces
    const links = [
        { href: "/dashboard", text: "Inicio", icon: "/static/img/inicio.png" },
        { href: "/clientes", text: "Ver Clientes", icon: "/static/img/clientes.png" },
        { href: "/productos", text: "Ver Productos", icon: "/static/img/producto.png" },
        { href: "/recetas", text: "Ver Recetas", icon: "/static/img/recetas.png" },
        { href: "/pedidos", text: "Ver Pedidos", icon: "/static/img/pedido.png" },
        { href: "/inventario", text: "Ver Inventario", icon: "/static/img/inventario.png" },
        { href: "/logout", text: "Cerrar Sesión", icon: "/static/img/logout.png" }
    ];




    // Crear los enlaces
    links.forEach(link => {
        const a = document.createElement("a");
        a.href = link.href;

        const img = document.createElement("img");
        img.src = link.icon;
        img.alt = link.text;
        img.className = "menu-icon";

        const span = document.createElement("span");
        span.textContent = link.text;

        a.appendChild(img);
        a.appendChild(span);
        optionsMenu.appendChild(a);

        // Cerrar el menú al hacer clic (solo útil en móvil)
        a.addEventListener("click", () => {
            optionsMenu.classList.remove("active");
        });

        if (link.href === "/logout") {
            a.addEventListener("click", (e) => {
                e.preventDefault();
                Swal.fire({
                    title: "¿Cerrar sesión?",
                    text: "Tu sesión actual se cerrará.",
                    icon: "warning",
                    showCancelButton: true,
                    confirmButtonText: "Sí, salir",
                    cancelButtonText: "Cancelar",
                    confirmButtonColor: "#d4777c"
                }).then((result) => {
                    if (result.isConfirmed) {
                        window.location.href = "/logout";
                    }
                });
            });
        } else {
            // Oculta menú si es un link normal
            a.addEventListener("click", () => {
                optionsMenu.classList.remove("active");
            });
        }
    });

    // Agregar elementos al sidebar
    menuSide.appendChild(namePage);
    menuSide.appendChild(optionsMenu);

    // Toggle del menú con el botón hamburguesa
    toggleButton.addEventListener("click", () => {
        optionsMenu.classList.toggle("active");

    });

    return menuSide;
}
