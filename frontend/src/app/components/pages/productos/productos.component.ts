import { CommonModule } from '@angular/common';
import { Component, OnDestroy, OnInit, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { Producto, ProductoPayload, ProductosService } from '../../../services/productos';

@Component({
  selector: 'app-productos',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './productos.component.html',
  styleUrls: ['./productos.component.css']
})
export class ProductosComponent implements OnInit, OnDestroy {
  private productosService = inject(ProductosService);

  productos: Producto[] = [];
  loading = true;
  errorMessage = '';
  successMessage = '';
  totalProductos = 0;
  paginaActual = 1;

  terminoBusqueda = '';
  nombreProducto = '';
  precioProducto: number | null = null;
  descripcionProducto = '';
  productoActivo = true;
  editandoProductoId: number | null = null;
  guardando = false;
  eliminandoId: number | null = null;
  modalAbierto = false;
  private successTimeoutId: ReturnType<typeof setTimeout> | null = null;

  ngOnInit(): void {
    this.cargarProductos();
  }

  ngOnDestroy(): void {
    this.limpiarSuccessTimeout();
  }

  cargarProductos(): void {
    this.loading = true;
    this.errorMessage = '';

    this.productosService.obtenerProductos(1, 10, this.terminoBusqueda).subscribe({
      next: (response) => {
        this.productos = response.data?.productos ?? [];
        this.totalProductos = response.data?.total_productos ?? 0;
        this.paginaActual = response.data?.pagina ?? 1;
        this.loading = false;
      },
      error: (error) => {
        this.errorMessage = error?.error?.message || 'No se pudieron cargar los productos.';
        this.loading = false;
      }
    });
  }

  buscarProductos(): void {
    this.successMessage = '';
    this.cargarProductos();
  }

  abrirModalCrear(): void {
    this.modalAbierto = true;
    this.editandoProductoId = null;
    this.nombreProducto = '';
    this.precioProducto = null;
    this.descripcionProducto = '';
    this.productoActivo = true;
    this.errorMessage = '';
    this.successMessage = '';
  }

  editarProducto(producto: Producto): void {
    this.modalAbierto = true;
    this.editandoProductoId = producto.id;
    this.nombreProducto = producto.nombre;
    this.precioProducto = Number(producto.precio);
    this.descripcionProducto = producto.descripcion ?? '';
    this.productoActivo = producto.activo;
    this.successMessage = '';
    this.errorMessage = '';
  }

  cerrarModal(): void {
    if (this.guardando) {
      return;
    }

    this.modalAbierto = false;
    this.editandoProductoId = null;
    this.nombreProducto = '';
    this.precioProducto = null;
    this.descripcionProducto = '';
    this.productoActivo = true;
  }

  cerrarSuccessMessage(): void {
    this.successMessage = '';
    this.limpiarSuccessTimeout();
  }

  guardarProducto(): void {
    const nombre = this.nombreProducto.trim();
    const descripcion = this.descripcionProducto.trim();

    if (!nombre) {
      this.errorMessage = 'El nombre del producto es requerido.';
      return;
    }

    if (this.precioProducto === null || Number.isNaN(this.precioProducto) || this.precioProducto <= 0) {
      this.errorMessage = 'El precio debe ser mayor a cero.';
      return;
    }

    this.guardando = true;
    this.errorMessage = '';
    this.successMessage = '';

    const payload: ProductoPayload = {
      nombre,
      precio: this.precioProducto,
      descripcion
    };

    if (this.editandoProductoId) {
      payload.activo = this.productoActivo;
    }

    const request$ = this.editandoProductoId
      ? this.productosService.actualizarProducto(this.editandoProductoId, payload)
      : this.productosService.crearProducto(payload);

    request$.subscribe({
      next: (response) => {
        this.mostrarSuccessMessage(response.message);
        this.guardando = false;
        this.modalAbierto = false;
        this.editandoProductoId = null;
        this.nombreProducto = '';
        this.precioProducto = null;
        this.descripcionProducto = '';
        this.productoActivo = true;
        this.cargarProductos();
      },
      error: (error) => {
        this.errorMessage = error?.error?.message || 'No se pudo guardar el producto.';
        this.guardando = false;
      }
    });
  }

  eliminarProducto(producto: Producto): void {
    const confirmar = window.confirm(`Deseas eliminar el producto "${producto.nombre}"?`);
    if (!confirmar) {
      return;
    }

    this.eliminandoId = producto.id;
    this.errorMessage = '';
    this.successMessage = '';

    this.productosService.eliminarProducto(producto.id).subscribe({
      next: (response) => {
        this.mostrarSuccessMessage(response.message);
        if (this.editandoProductoId === producto.id) {
          this.cerrarModal();
        }
        this.eliminandoId = null;
        this.cargarProductos();
      },
      error: (error) => {
        this.errorMessage = error?.error?.message || 'No se pudo eliminar el producto.';
        this.eliminandoId = null;
      }
    });
  }

  formatearPrecio(precio: number): string {
    return Number(precio).toFixed(2);
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
