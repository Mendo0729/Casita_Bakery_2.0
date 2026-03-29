import { CommonModule } from '@angular/common';
import { Component, OnInit, inject } from '@angular/core';
import { RouterLink } from '@angular/router';
import { forkJoin } from 'rxjs';

import { Cliente, ClientesService } from '../../../services/clientes';
import { Pedido, PedidosService } from '../../../services/pedidos';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  private pedidosService = inject(PedidosService);
  private clientesService = inject(ClientesService);

  loading = true;
  errorMessage = '';
  clientes: Cliente[] = [];
  recentOrders: Pedido[] = [];

  summary = {
    total: 0,
    pendientes: 0,
    entregados: 0
  };

  ngOnInit(): void {
    this.cargarDashboard();
  }

  cargarDashboard(): void {
    this.loading = true;
    this.errorMessage = '';

    forkJoin({
      clientes: this.clientesService.obtenerClientes(1, 100),
      pedidos: this.pedidosService.obtenerPedidos(1, 10),
      pendientes: this.pedidosService.obtenerPedidos(1, 100, '', 'pendiente'),
      entregados: this.pedidosService.obtenerPedidos(1, 100, '', 'entregado')
    }).subscribe({
      next: ({ clientes, pedidos, pendientes, entregados }) => {
        this.clientes = clientes.data?.clientes ?? [];
        this.recentOrders = pedidos.data?.pedidos ?? [];
        this.summary = {
          total: pedidos.data?.total_pedidos ?? 0,
          pendientes: pendientes.data?.total_pedidos ?? 0,
          entregados: entregados.data?.total_pedidos ?? 0
        };
        this.loading = false;
      },
      error: (error) => {
        this.errorMessage = error?.error?.message || 'No se pudieron cargar los datos del dashboard.';
        this.loading = false;
      }
    });
  }

  obtenerNombreCliente(clienteId: number): string {
    return this.clientes.find((cliente) => cliente.id === clienteId)?.nombre ?? `Cliente #${clienteId}`;
  }

  formatearFecha(valor: string | null): string {
    if (!valor) {
      return 'Sin fecha';
    }

    const fecha = new Date(valor);
    return Number.isNaN(fecha.getTime()) ? valor : fecha.toLocaleDateString();
  }
}
