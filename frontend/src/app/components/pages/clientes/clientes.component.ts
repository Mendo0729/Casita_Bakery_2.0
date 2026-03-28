import { CommonModule } from '@angular/common';
import { Component, OnDestroy, OnInit, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { Cliente, ClientesService } from '../../../services/clientes';

@Component({
  selector: 'app-clientes',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './clientes.component.html',
  styleUrls: ['./clientes.component.css']
})
export class ClientesComponent implements OnInit, OnDestroy {
  private clientesService = inject(ClientesService);

  clientes: Cliente[] = [];
  loading = true;
  errorMessage = '';
  successMessage = '';
  totalClientes = 0;
  paginaActual = 1;

  terminoBusqueda = '';
  nombreCliente = '';
  editandoClienteId: number | null = null;
  guardando = false;
  eliminandoId: number | null = null;
  modalAbierto = false;
  private successTimeoutId: ReturnType<typeof setTimeout> | null = null;

  ngOnInit(): void {
    this.cargarClientes();
  }

  ngOnDestroy(): void {
    this.limpiarSuccessTimeout();
  }

  cargarClientes(): void {
    this.loading = true;
    this.errorMessage = '';

    this.clientesService.obtenerClientes(1, 10, this.terminoBusqueda).subscribe({
      next: (response) => {
        this.clientes = response.data?.clientes ?? [];
        this.totalClientes = response.data?.total_clientes ?? 0;
        this.paginaActual = response.data?.pagina ?? 1;
        this.loading = false;
      },
      error: (error) => {
        this.errorMessage = error?.error?.message || 'No se pudieron cargar los clientes.';
        this.loading = false;
      }
    });
  }

  buscarClientes(): void {
    this.successMessage = '';
    this.cargarClientes();
  }

  abrirModalCrear(): void {
    this.modalAbierto = true;
    this.editandoClienteId = null;
    this.nombreCliente = '';
    this.errorMessage = '';
    this.successMessage = '';
  }

  editarCliente(cliente: Cliente): void {
    this.modalAbierto = true;
    this.editandoClienteId = cliente.id;
    this.nombreCliente = cliente.nombre;
    this.successMessage = '';
    this.errorMessage = '';
  }

  cerrarModal(): void {
    if (this.guardando) {
      return;
    }

    this.modalAbierto = false;
    this.editandoClienteId = null;
    this.nombreCliente = '';
  }

  cerrarSuccessMessage(): void {
    this.successMessage = '';
    this.limpiarSuccessTimeout();
  }

  guardarCliente(): void {
    const nombre = this.nombreCliente.trim();

    if (!nombre) {
      this.errorMessage = 'El nombre del cliente es requerido.';
      return;
    }

    this.guardando = true;
    this.errorMessage = '';
    this.successMessage = '';

    const request$ = this.editandoClienteId
      ? this.clientesService.actualizarCliente(this.editandoClienteId, nombre)
      : this.clientesService.crearCliente(nombre);

    request$.subscribe({
      next: (response) => {
        this.mostrarSuccessMessage(response.message);
        this.nombreCliente = '';
        this.editandoClienteId = null;
        this.guardando = false;
        this.modalAbierto = false;
        this.cargarClientes();
      },
      error: (error) => {
        this.errorMessage = error?.error?.message || 'No se pudo guardar el cliente.';
        this.guardando = false;
      }
    });
  }

  eliminarCliente(cliente: Cliente): void {
    const confirmar = window.confirm(`Deseas eliminar a "${cliente.nombre}"?`);
    if (!confirmar) {
      return;
    }

    this.eliminandoId = cliente.id;
    this.errorMessage = '';
    this.successMessage = '';

    this.clientesService.eliminarCliente(cliente.id).subscribe({
      next: (response) => {
        this.mostrarSuccessMessage(response.message);
        if (this.editandoClienteId === cliente.id) {
          this.cerrarModal();
        }
        this.eliminandoId = null;
        this.cargarClientes();
      },
      error: (error) => {
        this.errorMessage = error?.error?.message || 'No se pudo eliminar el cliente.';
        this.eliminandoId = null;
      }
    });
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
