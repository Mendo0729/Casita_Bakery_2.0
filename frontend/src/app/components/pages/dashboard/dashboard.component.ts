import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
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
    { id: 1, cliente: 'Juan Perez', estado: 'Pendiente', fecha: '2025-08-29' },
    { id: 2, cliente: 'Maria Lopez', estado: 'Entregado', fecha: '2025-08-28' },
    { id: 3, cliente: 'Carlos Sanchez', estado: 'Pendiente', fecha: '2025-08-27' }
  ];

  constructor() {
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
