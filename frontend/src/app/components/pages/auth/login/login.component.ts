import { Component } from '@angular/core';
import { AuthService } from '../../../../services/usuarios';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
  standalone: true,
  imports: [CommonModule, FormsModule]
})
export class LoginComponent {
  username = '';
  password = '';
  errorMessage = '';

  constructor(private authService: AuthService, private router: Router) {}

  login() {
    this.authService.login(
      this.username,
      this.password,
      { username: this.username, password: this.password }
    ).subscribe({
      next: () => {
        this.router.navigate(['dashboard']);
        console.log('Login exitoso');
      },
      error: (err) => {
        this.errorMessage = err.error.message || 'Error al iniciar sesiÃ³n';
        console.log('Error al iniciar sesion');
      }
    });
  }

  ngOnInit() {
    if (this.authService.isLoggedIn()) {
      this.router.navigate(['/dashboard']);
    }
  }
}
