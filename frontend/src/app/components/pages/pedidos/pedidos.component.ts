import { CommonModule } from '@angular/common';
import { Component, OnDestroy, OnInit, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { Cliente, ClientesService } from '../../../services/clientes';
import { Pedido, PedidosService } from '../../../services/pedidos';
import { Producto, ProductosService } from '../../../services/productos';

interface PedidoLineaForm {
  producto_id: number | null;
  cantidad: number;
}

@Component({
  selector: 'app-pedidos',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './pedidos.component.html',
  styleUrls: ['./pedidos.component.css']
})
export class PedidosComponent implements OnInit, OnDestroy {
  private pedidosService = inject(PedidosService);
  private clientesService = inject(ClientesService);
  private productosService = inject(ProductosService);

  pedidos: Pedido[] = [];
  clientes: Cliente[] = [];
  productos: Producto[] = [];

  loading = true;
  cargandoCatalogos = false;
  guardando = false;
  errorMessage = '';
  successMessage = '';
  totalPedidos = 0;
  paginaActual = 1;

  filtroCliente = '';
  filtroEstado = '';
  pedidoExpandidoId: number | null = null;

  modalAbierto = false;
  editandoPedidoId: number | null = null;
  clienteIdSeleccionado: number | null = null;
  fechaEntrega = '';
  estadoPedido: 'pendiente' | 'entregado' | 'cancelado' = 'pendiente';
  lineasPedido: PedidoLineaForm[] = [];

  private successTimeoutId: ReturnType<typeof setTimeout> | null = null;

  ngOnInit(): void {
    this.cargarCatalogos();
    this.cargarPedidos();
  }

  ngOnDestroy(): void {
    this.limpiarSuccessTimeout();
  }

  cargarPedidos(): void {
    this.loading = true;
    this.errorMessage = '';

    this.pedidosService.obtenerPedidos(1, 10, this.filtroCliente, this.filtroEstado).subscribe({
      next: (response) => {
        this.pedidos = response.data?.pedidos ?? [];
        this.totalPedidos = response.data?.total_pedidos ?? 0;
        this.paginaActual = response.data?.pagina ?? 1;
        this.loading = false;
      },
      error: (error) => {
        this.errorMessage = error?.error?.message || 'No se pudieron cargar los pedidos.';
        this.loading = false;
      }
    });
  }

  cargarCatalogos(): void {
    this.cargandoCatalogos = true;

    this.clientesService.obtenerClientes(1, 100).subscribe({
      next: (response) => {
        this.clientes = response.data?.clientes ?? [];
      }
    });

    this.productosService.obtenerProductos(1, 100).subscribe({
      next: (response) => {
        const productos = response.data?.productos ?? [];
        this.productos = productos.filter((producto) => producto.activo);
        this.cargandoCatalogos = false;
      },
      error: () => {
        this.cargandoCatalogos = false;
      }
    });
  }

  buscarPedidos(): void {
    this.successMessage = '';
    this.cargarPedidos();
  }

  toggleDetalles(pedidoId: number): void {
    this.pedidoExpandidoId = this.pedidoExpandidoId === pedidoId ? null : pedidoId;
  }

  abrirModalCrear(): void {
    this.modalAbierto = true;
    this.editandoPedidoId = null;
    this.clienteIdSeleccionado = null;
    this.fechaEntrega = '';
    this.estadoPedido = 'pendiente';
    this.lineasPedido = [{ producto_id: null, cantidad: 1 }];
    this.errorMessage = '';
    this.successMessage = '';
  }

  editarPedido(pedido: Pedido): void {
    this.modalAbierto = true;
    this.editandoPedidoId = pedido.id;
    this.clienteIdSeleccionado = pedido.cliente_id;
    this.fechaEntrega = pedido.fecha_entrega ?? '';
    this.estadoPedido = pedido.estado;
    this.lineasPedido = pedido.detalles.length
      ? pedido.detalles.map((detalle) => ({
          producto_id: detalle.producto_id,
          cantidad: detalle.cantidad
        }))
      : [{ producto_id: null, cantidad: 1 }];
    this.errorMessage = '';
    this.successMessage = '';
  }

  cerrarModal(): void {
    if (this.guardando) {
      return;
    }

    this.modalAbierto = false;
    this.editandoPedidoId = null;
    this.clienteIdSeleccionado = null;
    this.fechaEntrega = '';
    this.estadoPedido = 'pendiente';
    this.lineasPedido = [];
  }

  agregarLinea(): void {
    this.lineasPedido.push({ producto_id: null, cantidad: 1 });
  }

  eliminarLinea(index: number): void {
    if (this.lineasPedido.length === 1) {
      this.lineasPedido[0] = { producto_id: null, cantidad: 1 };
      return;
    }

    this.lineasPedido.splice(index, 1);
  }

  guardarPedido(): void {
    if (!this.clienteIdSeleccionado) {
      this.errorMessage = 'Debes seleccionar un cliente.';
      return;
    }

    const lineasValidadas = this.lineasPedido
      .map((linea) => ({
        producto_id: Number(linea.producto_id),
        cantidad: Number(linea.cantidad)
      }))
      .filter((linea) => linea.producto_id && linea.cantidad);

    if (!lineasValidadas.length || lineasValidadas.length !== this.lineasPedido.length) {
      this.errorMessage = 'Completa todos los productos y cantidades del pedido.';
      return;
    }

    if (lineasValidadas.some((linea) => !Number.isInteger(linea.cantidad) || linea.cantidad <= 0)) {
      this.errorMessage = 'Todas las cantidades deben ser enteros mayores a cero.';
      return;
    }

    this.guardando = true;
    this.errorMessage = '';
    this.successMessage = '';

    const fechaEntrega = this.fechaEntrega.trim() ? this.fechaEntrega : null;

    const request$ = this.editandoPedidoId
      ? this.pedidosService.actualizarPedido(this.editandoPedidoId, {
          fecha_entrega: fechaEntrega,
          estado: this.estadoPedido,
          productos_seleccionados: lineasValidadas
        })
      : this.pedidosService.crearPedido({
          cliente_id: this.clienteIdSeleccionado,
          fecha_entrega: fechaEntrega,
          productos_seleccionados: lineasValidadas
        });

    request$.subscribe({
      next: (response) => {
        this.mostrarSuccessMessage(response.message);
        this.guardando = false;
        this.cerrarModal();
        this.cargarPedidos();
      },
      error: (error) => {
        this.errorMessage = error?.error?.message || 'No se pudo guardar el pedido.';
        this.guardando = false;
      }
    });
  }

  cerrarSuccessMessage(): void {
    this.successMessage = '';
    this.limpiarSuccessTimeout();
  }

  obtenerNombreCliente(clienteId: number): string {
    return this.clientes.find((cliente) => cliente.id === clienteId)?.nombre ?? `Cliente #${clienteId}`;
  }

  obtenerNombreProducto(productoId: number): string {
    return this.productos.find((producto) => producto.id === productoId)?.nombre ?? `Producto #${productoId}`;
  }

  obtenerPrecioProducto(productoId: number | null): number {
    if (!productoId) {
      return 0;
    }

    return this.productos.find((producto) => producto.id === productoId)?.precio ?? 0;
  }

  calcularSubtotal(linea: PedidoLineaForm): number {
    return this.obtenerPrecioProducto(linea.producto_id) * Number(linea.cantidad || 0);
  }

  formatearMoneda(valor: number | null | undefined): string {
    return Number(valor ?? 0).toFixed(2);
  }

  formatearFecha(valor: string | null): string {
    if (!valor) {
      return 'Sin fecha';
    }

    const fecha = new Date(valor);
    return Number.isNaN(fecha.getTime()) ? valor : fecha.toLocaleDateString();
  }

  puedeEditar(pedido: Pedido): boolean {
    return pedido.estado === 'pendiente';
  }

  private mostrarSuccessMessage(message: string): void {
    this.successMessage = message;
    this.limpiarSuccessTimeout();
    this.successTimeoutId = setTimeout(() => {
      this.successMessage = '';
      this.successTimeoutId = null;
    }, 4000);
  }

  private limpiarSuccessTimeout(): void {
    if (this.successTimeoutId) {
      clearTimeout(this.successTimeoutId);
      this.successTimeoutId = null;
    }
  }
}
