# Casita Bakery Frontend

Frontend de **Casita Bakery** construido con Angular. Esta aplicacion consume la API del backend para autenticacion, clientes, productos, inventario y pedidos.

## Stack

- Angular 20
- TypeScript
- Angular Router
- Angular Forms
- HttpClient
- CSS plano

## Estado actual

El frontend ya incluye:

- login con JWT
- logout
- sesion temporal en `sessionStorage`
- interceptor para adjuntar `Authorization: Bearer <token>`
- dashboard con datos reales
- modulo de clientes conectado al backend
- modulo de productos conectado al backend
- modulo de ingredientes conectado al backend
- modulo de pedidos conectado al backend

## Estructura principal

```text
frontend/
├─ src/
│  ├─ app/
│  │  ├─ components/
│  │  │  ├─ pages/
│  │  │  └─ shared/
│  │  ├─ guards/
│  │  ├─ services/
│  │  ├─ app.config.ts
│  │  ├─ app.routes.ts
│  │  └─ auth.interceptor.ts
│  ├─ main.ts
│  └─ styles.css
├─ package.json
└─ README.md
```

## Requisitos

- Node.js instalado
- npm disponible en terminal
- backend de Casita Bakery corriendo en `http://localhost:5000`

## Instalacion

Desde la carpeta `frontend`:

```powershell
npm install
```

Si PowerShell bloquea `npm.ps1`, puedes usar cualquiera de estas opciones:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

o ejecutar:

```powershell
npm.cmd install
```

## Ejecutar en desarrollo

```powershell
npm start
```

La app queda disponible en:

```text
http://localhost:4200
```

## Scripts disponibles

Desde [package.json](/c:/Users/AbdielMendoza/Desktop/Desarrollo/Casita_Bakery_2.0/frontend/package.json):

```powershell
npm start
npm run build
npm test
```

## Rutas actuales

Configuradas en [app.routes.ts](/c:/Users/AbdielMendoza/Desktop/Desarrollo/Casita_Bakery_2.0/frontend/src/app/app.routes.ts):

- `/login`
- `/dashboard`
- `/clientes`
- `/productos`
- `/pedidos`
- `/ingredientes`

Todas las rutas excepto `/login` estan protegidas con `AuthGuard`.

## Flujo de autenticacion

El frontend consume el backend en:

```text
http://localhost:5000/auth/api
```

### Login

Pantalla:

- [login.component.ts](/c:/Users/AbdielMendoza/Desktop/Desarrollo/Casita_Bakery_2.0/frontend/src/app/components/pages/auth/login/login.component.ts)

Servicio:

- [usuarios.ts](/c:/Users/AbdielMendoza/Desktop/Desarrollo/Casita_Bakery_2.0/frontend/src/app/services/usuarios.ts)

Guard:

- [auth-guard.ts](/c:/Users/AbdielMendoza/Desktop/Desarrollo/Casita_Bakery_2.0/frontend/src/app/guards/auth-guard.ts)

Interceptor:

- [auth.interceptor.ts](/c:/Users/AbdielMendoza/Desktop/Desarrollo/Casita_Bakery_2.0/frontend/src/app/auth.interceptor.ts)

### Sesion

- el `access_token` se guarda en `sessionStorage`
- el `refresh_token` se guarda en `sessionStorage`
- el usuario autenticado se guarda en `sessionStorage`
- al cerrar sesion se limpia la sesion
- al cerrar completamente la pestaña o ventana, la sesion no persiste

## Modulos conectados

### Dashboard

- consume datos reales de pedidos y clientes
- muestra:
  - total de pedidos
  - pedidos pendientes
  - pedidos entregados
  - pedidos recientes

Archivos:

- [dashboard.component.ts](/c:/Users/AbdielMendoza/Desktop/Desarrollo/Casita_Bakery_2.0/frontend/src/app/components/pages/dashboard/dashboard.component.ts)
- [dashboard.component.html](/c:/Users/AbdielMendoza/Desktop/Desarrollo/Casita_Bakery_2.0/frontend/src/app/components/pages/dashboard/dashboard.component.html)

### Clientes

- listar
- buscar
- crear
- editar
- eliminar

Archivos:

- [clientes.ts](/c:/Users/AbdielMendoza/Desktop/Desarrollo/Casita_Bakery_2.0/frontend/src/app/services/clientes.ts)
- [clientes.component.ts](/c:/Users/AbdielMendoza/Desktop/Desarrollo/Casita_Bakery_2.0/frontend/src/app/components/pages/clientes/clientes.component.ts)

### Productos

- listar
- buscar
- crear
- editar
- eliminar

Archivos:

- [productos.ts](/c:/Users/AbdielMendoza/Desktop/Desarrollo/Casita_Bakery_2.0/frontend/src/app/services/productos.ts)
- [productos.component.ts](/c:/Users/AbdielMendoza/Desktop/Desarrollo/Casita_Bakery_2.0/frontend/src/app/components/pages/productos/productos.component.ts)

### Ingredientes

- listar
- buscar
- crear
- editar

Nota:

- no incluye eliminar porque el backend actual no expone ese endpoint

Archivos:

- [ingredientes.ts](/c:/Users/AbdielMendoza/Desktop/Desarrollo/Casita_Bakery_2.0/frontend/src/app/services/ingredientes.ts)
- [ingredientes.component.ts](/c:/Users/AbdielMendoza/Desktop/Desarrollo/Casita_Bakery_2.0/frontend/src/app/components/pages/ingredientes/ingredientes.component.ts)

### Pedidos

- listar
- filtrar por cliente y estado
- ver detalle expandible
- crear pedido
- editar pedido pendiente

Archivos:

- [pedidos.ts](/c:/Users/AbdielMendoza/Desktop/Desarrollo/Casita_Bakery_2.0/frontend/src/app/services/pedidos.ts)
- [pedidos.component.ts](/c:/Users/AbdielMendoza/Desktop/Desarrollo/Casita_Bakery_2.0/frontend/src/app/components/pages/pedidos/pedidos.component.ts)

## Convenciones visuales actuales

- sidebar unico para toda la aplicacion
- tablas con columna `#` en vez de mostrar `ID`
- modales para crear y editar
- diseño responsive base para desktop y mobile

## Como probar el proyecto completo

1. Arranca el backend:

```powershell
cd C:\Users\AbdielMendoza\Desktop\Desarrollo\Casita_Bakery_2.0\backend
.\.venv\Scripts\Activate.ps1
python run.py
```

2. Arranca el frontend:

```powershell
cd C:\Users\AbdielMendoza\Desktop\Desarrollo\Casita_Bakery_2.0\frontend
npm start
```

3. Abre:

```text
http://localhost:4200
```

4. Inicia sesion con un usuario valido del backend.

## Troubleshooting

### `npm` no se reconoce

Verifica:

```powershell
node -v
npm -v
```

Si `node` existe pero `npm` falla por politica de PowerShell:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### El login no avanza

Revisa:

- que el backend este corriendo
- que el token se guarde en `sessionStorage`
- que `AuthGuard` no este redirigiendo por sesion vacia

### `ng serve` muestra errores raros despues de muchos cambios

A veces el watcher de Angular se queda con estado viejo. En ese caso:

1. detén `ng serve`
2. cierra la terminal
3. vuelve a arrancar:

```powershell
npm start
```

## Pendientes futuros

Posibles siguientes pasos si el proyecto continua:

- pulido visual general
- paginacion real en frontend
- reportes
- roles/permisos
- manejo mas avanzado de refresh token
