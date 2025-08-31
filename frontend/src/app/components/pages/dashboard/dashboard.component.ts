import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SidebarComponent } from '../../shared/sidebar/sidebar.component';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, SidebarComponent],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent {
  loading = true;

  summary = {
    total: 0,
    pendientes: 0,
    entregados: 0
  };

  recentOrders = [
    { id: 1, cliente: 'Juan Pérez', estado: 'Pendiente', fecha: '2025-08-29' },
    { id: 2, cliente: 'María López', estado: 'Entregado', fecha: '2025-08-28' },
    { id: 3, cliente: 'Carlos Sánchez', estado: 'Pendiente', fecha: '2025-08-27' }
  ];

  constructor() {
    // Simulamos carga
    setTimeout(() => {
      this.summary = {
        total: 150,
        pendientes: 45,
        entregados: 105
      };
      this.loading = false;
    }, 1500);
  }
}
