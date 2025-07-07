document.addEventListener("DOMContentLoaded", () => {
    // Elementos del DOM
    const abrirModalBtn = document.getElementById('abrirModal');
    const modal = document.querySelector('.modal');
    const cerrarModal = document.querySelector('.close');
    const formulario = document.getElementById('formProducto');
    const tabla = document.getElementById("tablaInventario").querySelector("tbody");
    const inputBusqueda = document.getElementById("buscarNombre");
    const btnBuscar = document.getElementById("btnBuscar");
    const btnLimpiar = document.getElementById("limpiarBusqueda");

    const URL_SCRIPT = "https://script.google.com/macros/s/AKfycbx8xRBB7i4Repi78FF4KKnS83FTwgrDduamyWOFivBLDXTh3wcQmCaCeTslSwfGGzA0/exec";
    let productosCache = [];

    // Funciones para mostrar mensajes
    function mostrarMensaje(mensaje, tipo = "exito") {
        const alerta = document.createElement("div");
        alerta.className = `alerta alerta-${tipo} mostrar`;

        // Icono según tipo de mensaje
        let icono = '';
        switch (tipo) {
            case 'exito': icono = '✓'; break;
            case 'error': icono = '✗'; break;
            default: icono = 'i';
        }

        alerta.innerHTML = `<span>${icono}</span> ${mensaje}`;
        document.body.appendChild(alerta);

        // Auto-eliminación después de 3 segundos
        setTimeout(() => {
            alerta.style.animation = 'fadeOut 0.5s forwards';
            setTimeout(() => alerta.remove(), 500);
        }, 3000);
    }

    function mostrarError(error) {
        const mensaje = error instanceof Error ? error.message : error;
        mostrarMensaje(mensaje, "error");
    }

    function mostrarCarga() {
        tabla.innerHTML = `
            <tr class="cargando-fila">
                <td colspan="6" style="text-align: center; padding: 30px;">
                    <div style="display: inline-flex; align-items: center;">
                        <div class="cargando"></div>
                        <span>Cargando inventario...</span>
                    </div>
                </td>
            </tr>
        `;
    }

    // Funciones para mostrar/ocultar modal
    function abrirModal() {
        modal.classList.add('mostrar');
        document.getElementById("nombreProducto").focus();
    }

    function cerrarModalFunc() {
        modal.classList.remove('mostrar');
        formulario.reset();
    }

    // Event listeners actualizados
    if (abrirModalBtn) abrirModalBtn.addEventListener('click', abrirModal);
    if (cerrarModal) cerrarModal.addEventListener('click', cerrarModalFunc);
    window.addEventListener('click', (e) => {
        if (e.target === modal) cerrarModalFunc();
    });

    // Delegación de eventos para la tabla
    document.addEventListener("click", async (e) => {
        const fila = e.target.closest("tr");
        if (!fila) return;

        // Editar producto
        if (e.target.closest(".btn-editar")) {
            const celdas = fila.querySelectorAll("td");
            celdas.forEach((td, i) => {
                if (i > 0 && i < 5) {
                    const valor = td.textContent;
                    td.innerHTML = `<input type="${i === 3 ? 'number' : 'text'}" value="${valor}" ${i === 3 ? 'min="1"' : ''}>`;
                }
            });
            fila.querySelector(".btn-editar").style.display = "none";
            fila.querySelector(".btn-guardar").style.display = "inline-block";
        }

        // Guardar cambios
        if (e.target.closest(".btn-guardar")) {
            await guardarCambios(fila);
        }

        // Eliminar producto
        if (e.target.closest(".btn-eliminar")) {
            await eliminarProducto(fila);
        }
    });

    // Búsqueda
    btnBuscar.addEventListener("click", () => filtrarProductos());
    btnLimpiar.addEventListener("click", () => {
        inputBusqueda.value = "";
        cargarInventario();
    });
    inputBusqueda.addEventListener("input", () => filtrarProductos());

    // Cargar inventario inicial
    cargarInventario();

    // Funciones principales
    async function cargarInventario() {
        try {
            mostrarCarga();

            const respuesta = await fetch(URL_SCRIPT);
            if (!respuesta.ok) throw new Error('Error en la respuesta del servidor');

            productosCache = await respuesta.json();
            if (!Array.isArray(productosCache)) throw new Error('Formato de datos inválido');

            renderizarTabla(productosCache);
            mostrarMensaje("Inventario cargado correctamente");
        } catch (error) {
            console.error("Error al cargar el inventario:", error);
            mostrarError(error);
        }
    }

    function renderizarTabla(productos) {
        tabla.innerHTML = "";

        if (productos.length === 0) {
            tabla.innerHTML = '<tr><td colspan="6">No se encontraron productos</td></tr>';
            return;
        }

        productos.forEach(producto => {
            const fila = document.createElement("tr");

            fila.innerHTML = `
                <td class="celda-id" data-label="ID">${producto.id}</td>
                <td class="celda-producto" data-label="Producto">${producto.producto}</td>
                <td class="celda-marca" data-label="Marca">${producto.marca}</td>
                <td class="celda-cantidad" data-label="Cantidad">${producto.cantidad}</td>
                <td class="celda-observaciones" data-label="Observaciones">${producto.observaciones || '-'}</td>
                <td class="acciones" data-label="Acciones">
                    <button class="btn-editar" type="button"><img src="img/editar.png" alt="Editar"></button>
                    <button class="btn-guardar" type="button" style="display: none;"><img src="img/guardar.png" alt="Guardar"></button>
                    <button class="btn-eliminar" type="button"><img src="img/basura.png" alt="Eliminar"></button>
                </td>
            `;

            tabla.appendChild(fila);
        });
    }

    async function guardarCambios(fila) {
        const id = fila.querySelector(".celda-id").textContent;
        const inputs = fila.querySelectorAll("input");

        const datosActualizados = {
            id,
            producto: inputs[0].value.trim(),
            marca: inputs[1].value.trim(),
            cantidad: inputs[2].value.trim(),
            observaciones: inputs[3].value.trim(),
            action: "editar"
        };

        // Validación
        if (!datosActualizados.producto || !datosActualizados.marca || !datosActualizados.cantidad) {
            mostrarMensaje("Por favor complete todos los campos obligatorios", "error");
            return;
        }

        try {
            await fetch(URL_SCRIPT, {
                method: "POST",
                mode: "no-cors",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(datosActualizados)
            });

            mostrarMensaje("Producto actualizado correctamente");
            setTimeout(cargarInventario, 500);
        } catch (error) {
            console.error("Error al guardar:", error);
            mostrarError("No se pudo guardar el producto. Intente nuevamente.");
        }
    }

    async function eliminarProducto(fila) {
        const id = fila.querySelector(".celda-id").textContent;
        const producto = fila.querySelector(".celda-producto").textContent;

        if (!confirm(`¿Estás seguro de que quieres eliminar "${producto}"?`)) {
            return;
        }

        try {
            await fetch(URL_SCRIPT, {
                method: "POST",
                mode: "no-cors",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ id, action: "eliminar" })
            });

            mostrarMensaje("Producto eliminado correctamente");
            setTimeout(cargarInventario, 500);
        } catch (error) {
            console.error("Error al eliminar:", error);
            mostrarError("No se pudo eliminar el producto. Intente nuevamente.");
        }
    }

    function filtrarProductos() {
        const termino = inputBusqueda.value.trim().toLowerCase();

        if (!termino) {
            renderizarTabla(productosCache);
            return;
        }

        const productosFiltrados = productosCache.filter(producto =>
            producto.producto.toLowerCase().includes(termino) ||
            (producto.marca && producto.marca.toLowerCase().includes(termino)) ||
            (producto.observaciones && producto.observaciones.toLowerCase().includes(termino))
        );

        renderizarTabla(productosFiltrados);
    }

    // Manejo del formulario
    formulario.addEventListener("submit", async (e) => {
        e.preventDefault();

        const producto = formulario.producto.value.trim();
        const marca = formulario.marca.value.trim();
        const cantidad = formulario.cantidad.value.trim();
        const observaciones = formulario.observaciones.value.trim();

        // Validación mejorada
        if (producto.length < 2) {
            mostrarMensaje("El nombre del producto debe tener al menos 2 caracteres", "error");
            return;
        }

        if (!marca) {
            mostrarMensaje("Por favor ingresa una marca válida", "error");
            return;
        }

        if (!cantidad || isNaN(cantidad) || Number(cantidad) <= 0) {
            mostrarMensaje("Por favor ingresa una cantidad válida (número mayor a 0)", "error");
            return;
        }

        const datos = {
            producto,
            marca,
            cantidad,
            observaciones: observaciones || null
        };

        try {
            await fetch(URL_SCRIPT, {
                method: "POST",
                mode: "no-cors",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(datos)
            });

            mostrarMensaje("Producto agregado correctamente");
            formulario.reset();
            cerrarModalFunc();
            setTimeout(cargarInventario, 500);
        } catch (error) {
            console.error("Error al enviar los datos:", error);
            mostrarError("No se pudo agregar el producto. Verifica tu conexión.");
        }
    });
});