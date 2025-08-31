import { Component, EventEmitter, Output } from '@angular/core';

import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';


@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.css']
})
export class SidebarComponent {
  menu = [
    { label: 'Inicio', route: '/dashboard', icon: 'assets/icons/inicio.png' },
    { label: 'Clientes', route: '/clientes', icon: 'assets/icons/clientes.png' },
    { label: 'Productos', route: '/productos', icon: 'assets/icons/productos.png' },
    { label: 'Pedidos', route: '/pedidos', icon: 'assets/icons/pedidos.png' },
    { label: 'Ingredientes', route: '/ingredientes', icon: 'assets/icons/ingredientes.png' }
  ];

  // sidebar empieza abierto
  isOpen = false;

  @Output() toggle = new EventEmitter<boolean>();

  // 🔑 Usuario logueado (simulación)
  user = {
    name: 'Abdiel Mendoza',
    avatar: 'assets/icons/user.png'
  };

  toggleMenu() {
    this.isOpen = !this.isOpen;
    this.toggle.emit(this.isOpen); // emitimos el estado
  }
}
