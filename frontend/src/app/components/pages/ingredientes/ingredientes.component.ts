import { CommonModule } from '@angular/common';
import { Component, OnDestroy, OnInit, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';

import {
  Ingrediente,
  IngredientePayload,
  IngredientesService
} from '../../../services/ingredientes';

@Component({
  selector: 'app-ingredientes',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './ingredientes.component.html',
  styleUrls: ['./ingredientes.component.css']
})
export class IngredientesComponent implements OnInit, OnDestroy {
  private ingredientesService = inject(IngredientesService);

  ingredientes: Ingrediente[] = [];
  loading = true;
  errorMessage = '';
  successMessage = '';
  totalIngredientes = 0;
  paginaActual = 1;

  terminoBusqueda = '';
  nombreIngrediente = '';
  cantidadIngrediente: number | null = null;
  unidadMedida = 'unidades';
  puntoReorden: number | null = null;
  editandoIngredienteId: number | null = null;
  guardando = false;
  modalAbierto = false;
  private successTimeoutId: ReturnType<typeof setTimeout> | null = null;

  ngOnInit(): void {
    this.cargarIngredientes();
  }

  ngOnDestroy(): void {
    this.limpiarSuccessTimeout();
  }

  cargarIngredientes(): void {
    this.loading = true;
    this.errorMessage = '';

    this.ingredientesService.obtenerIngredientes(1, 10, this.terminoBusqueda).subscribe({
      next: (response) => {
        this.ingredientes = response.data?.ingredientes ?? [];
        this.totalIngredientes = response.data?.total_ingredientes ?? 0;
        this.paginaActual = response.data?.pagina ?? 1;
        this.loading = false;
      },
      error: (error) => {
        this.errorMessage = error?.error?.message || 'No se pudieron cargar los ingredientes.';
        this.loading = false;
      }
    });
  }

  buscarIngredientes(): void {
    this.successMessage = '';
    this.cargarIngredientes();
  }

  abrirModalCrear(): void {
    this.modalAbierto = true;
    this.editandoIngredienteId = null;
    this.nombreIngrediente = '';
    this.cantidadIngrediente = null;
    this.unidadMedida = 'unidades';
    this.puntoReorden = null;
    this.errorMessage = '';
    this.successMessage = '';
  }

  editarIngrediente(ingrediente: Ingrediente): void {
    this.modalAbierto = true;
    this.editandoIngredienteId = ingrediente.id;
    this.nombreIngrediente = ingrediente.nombre;
    this.cantidadIngrediente = Number(ingrediente.cantidad);
    this.unidadMedida = ingrediente.unidad_medida;
    this.puntoReorden = Number(ingrediente.punto_reorden);
    this.successMessage = '';
    this.errorMessage = '';
  }

  cerrarModal(): void {
    if (this.guardando) {
      return;
    }

    this.modalAbierto = false;
    this.editandoIngredienteId = null;
    this.nombreIngrediente = '';
    this.cantidadIngrediente = null;
    this.unidadMedida = 'unidades';
    this.puntoReorden = null;
  }

  cerrarSuccessMessage(): void {
    this.successMessage = '';
    this.limpiarSuccessTimeout();
  }

  guardarIngrediente(): void {
    const nombre = this.nombreIngrediente.trim();
    const unidad_medida = this.unidadMedida.trim() || 'unidades';

    if (!nombre) {
      this.errorMessage = 'El nombre del ingrediente es requerido.';
      return;
    }

    if (this.cantidadIngrediente === null || Number.isNaN(this.cantidadIngrediente) || this.cantidadIngrediente < 0) {
      this.errorMessage = 'La cantidad debe ser mayor o igual a cero.';
      return;
    }

    if (this.puntoReorden === null || Number.isNaN(this.puntoReorden) || this.puntoReorden < 0) {
      this.errorMessage = 'El punto de reorden debe ser mayor o igual a cero.';
      return;
    }

    this.guardando = true;
    this.errorMessage = '';
    this.successMessage = '';

    const payload: IngredientePayload = {
      nombre,
      cantidad: this.cantidadIngrediente,
      unidad_medida,
      punto_reorden: this.puntoReorden
    };

    const request$ = this.editandoIngredienteId
      ? this.ingredientesService.actualizarIngrediente(this.editandoIngredienteId, payload)
      : this.ingredientesService.crearIngrediente(payload);

    request$.subscribe({
      next: (response) => {
        this.mostrarSuccessMessage(response.message);
        this.guardando = false;
        this.modalAbierto = false;
        this.editandoIngredienteId = null;
        this.nombreIngrediente = '';
        this.cantidadIngrediente = null;
        this.unidadMedida = 'unidades';
        this.puntoReorden = null;
        this.cargarIngredientes();
      },
      error: (error) => {
        this.errorMessage = error?.error?.message || 'No se pudo guardar el ingrediente.';
        this.guardando = false;
      }
    });
  }

  formatearNumero(valor: number): string {
    return Number(valor).toFixed(2);
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
