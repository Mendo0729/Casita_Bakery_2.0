document.addEventListener('DOMContentLoaded', () => {
    fetch('/dashboard/api')
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                console.error('Error del servidor:', data.error);
                return;
            }

            // Actualizar tarjetas
            document.getElementById('total-clientes').textContent = data.total_clientes || 0;
            document.getElementById('total-pedidos').textContent = data.total_pedidos || 0;
            document.getElementById('total-ingresos').textContent = `$${parseFloat(data.total_ingresos || 0).toFixed(2)}`;
            document.getElementById('total-productos').textContent = data.total_productos || 0;

            // Pedidos por estado
            const estados = [
                { estado: 'Pendientes', cantidad: data.pendientes || 0 },
                { estado: 'Entregados', cantidad: data.entregados || 0 },
                { estado: 'Cancelados', cantidad: data.cancelados || 0 }
            ];

            const ctxEstado = document.getElementById('grafico-estados').getContext('2d');
            new Chart(ctxEstado, {
                type: 'doughnut',
                data: {
                    labels: estados.map(e => e.estado),
                    datasets: [{
                        label: 'Cantidad',
                        data: estados.map(e => e.cantidad),
                        backgroundColor: ['#D4777C', '#5E2D1E', '#B6704F'],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { position: 'bottom' }
                    }
                }
            });

            // Ingresos últimos 7 días
            const ingresos = Array.isArray(data.ingresos_7_dias) ? data.ingresos_7_dias : [];
            const ingresosTotales = ingresos.reduce((acc, curr) => acc + curr.total, 0);
            document.getElementById('total-ingresos').textContent = `$${ingresosTotales.toFixed(2)}`;

            const ctxIngresos = document.getElementById('grafico-ingresos').getContext('2d');
            new Chart(ctxIngresos, {
                type: 'bar',
                data: {
                    labels: ingresos.map(e => e.fecha),
                    datasets: [{
                        label: 'Ingresos ($)',
                        data: ingresos.map(e => e.total),
                        backgroundColor: '#5E2D1E'
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: { beginAtZero: true }
                    }
                }
            });


            // Top productos
            const topProductos = Array.isArray(data.top_productos) ? data.top_productos : [];
            const listaTop = document.getElementById('lista-top-productos');
            listaTop.innerHTML = '';

            if (topProductos.length === 0) {
                listaTop.innerHTML = '<li>No hay datos disponibles.</li>';
            } else {
                topProductos.forEach((producto, i) => {
                    const li = document.createElement('li');
                    li.innerHTML = `<strong>${i + 1}. ${producto.nombre}</strong> - ${producto.total_vendido} vendidos`;
                    listaTop.appendChild(li);
                });
            }

            // Pedidos pendientes últimos 7 días (lista)
            const pedidosPendientes = Array.isArray(data.pedidos_proximos_7_dias) ? data.pedidos_proximos_7_dias : [];
            const contenedorPendientes = document.querySelector('.pedidos-pendientes-container');

            // Limpiar contenido anterior excepto el título
            contenedorPendientes.querySelectorAll('ul, table, p').forEach(el => el.remove());

            if (pedidosPendientes.length === 0) {
                const p = document.createElement('p');
                p.textContent = "No hay pedidos pendientes para los proximos 7 días.";
                contenedorPendientes.appendChild(p);
            } else {
                const tabla = document.createElement('table');
                tabla.style.width = '100%';
                tabla.style.borderCollapse = 'collapse';

                tabla.innerHTML = `
                    <thead>
                        <tr>
                            <th style="border-bottom:1px solid #ccc; padding:8px; text-align:left;">ID Pedido</th>
                            <th style="border-bottom:1px solid #ccc; padding:8px; text-align:left;">Fecha</th>
                            <th style="border-bottom:1px solid #ccc; padding:8px; text-align:left;">Cliente</th>
                            <th style="border-bottom:1px solid #ccc; padding:8px; text-align:right;">Total ($)</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${pedidosPendientes.map(pedido => `
                            <tr>
                                <td style="padding:8px; border-bottom:1px solid #eee;">${pedido.id}</td>
                                <td style="padding:8px; border-bottom:1px solid #eee;">${pedido.fecha_entrega}</td>
                                <td style="padding:8px; border-bottom:1px solid #eee;">${pedido.cliente}</td>
                                <td style="padding:8px; border-bottom:1px solid #eee; text-align:right;">${pedido.total.toFixed(2)}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                `;

                contenedorPendientes.appendChild(tabla);
            }

        })
        .catch(err => {
            console.error('Error al cargar datos del dashboard:', err);
        });
});
