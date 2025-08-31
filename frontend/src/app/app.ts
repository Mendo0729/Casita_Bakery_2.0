import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { SidebarComponent } from './components/shared/sidebar/sidebar.component';
import { AuthService } from './services/usuarios';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, SidebarComponent],
  templateUrl: './app.html',
  styleUrls: ['./app.css']
})
export class App {
  isSidebarOpen = false;

  constructor(public authService: AuthService) {}

  onSidebarToggle(open: boolean) {
    this.isSidebarOpen = open;
  }
}
