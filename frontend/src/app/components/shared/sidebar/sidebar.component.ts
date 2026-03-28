import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Output } from '@angular/core';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../../services/usuarios';

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

  isOpen = false;

  @Output() toggle = new EventEmitter<boolean>();

  user = {
    avatar: 'assets/icons/user.png'
  };

  constructor(private authService: AuthService, private router: Router) {}

  get userName(): string {
    const user = this.authService.getUser();
    return user?.nombre || user?.username || user?.name || 'Usuario';
  }

  toggleMenu() {
    this.isOpen = !this.isOpen;
    this.toggle.emit(this.isOpen);
  }

  logout() {
    this.authService.logout();
    this.isOpen = false;
    this.toggle.emit(false);
    this.router.navigate(['/login']);
  }
}
