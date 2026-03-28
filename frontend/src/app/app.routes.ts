import { Routes } from '@angular/router';
import { LoginComponent } from './components/pages/auth/login/login.component';
import { DashboardComponent } from './components/pages/dashboard/dashboard.component';
import { ClientesComponent } from './components/pages/clientes/clientes.component';
import { ProductosComponent } from './components/pages/productos/productos.component';
import { PedidosComponent } from './components/pages/pedidos/pedidos.component';
import { IngredientesComponent } from './components/pages/ingredientes/ingredientes.component';
import { AuthGuard } from './guards/auth-guard';

export const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  { path: 'dashboard', component: DashboardComponent, canActivate: [AuthGuard] },
  { path: 'clientes', component: ClientesComponent, canActivate: [AuthGuard] },
  { path: 'productos', component: ProductosComponent, canActivate: [AuthGuard] },
  { path: 'pedidos', component: PedidosComponent, canActivate: [AuthGuard] },
  { path: 'ingredientes', component: IngredientesComponent, canActivate: [AuthGuard] },
  { path: '**', redirectTo: 'dashboard' }
];
