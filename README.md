# Casita Bakery 2.0

Sistema web para la gestion operativa de **Casita Bakery**, con backend en Flask y frontend en Angular.

El proyecto permite administrar:

- clientes
- productos
- ingredientes
- pedidos
- autenticacion con JWT

## Arquitectura general

```text
Casita_Bakery_2.0/
├─ backend/
└─ frontend/
```

### Backend

API REST construida con Flask + MySQL.

Responsabilidades:

- autenticacion
- logica de negocio
- acceso a base de datos
- validaciones del servidor

Documentacion completa:

- [README del backend](/c:/Users/AbdielMendoza/Desktop/Desarrollo/Casita_Bakery_2.0/backend/README.md)

### Frontend

Aplicacion Angular que consume la API del backend.

Responsabilidades:

- login
- dashboard
- CRUD visual de modulos
- sesion y navegacion

Documentacion completa:

- [README del frontend](/c:/Users/AbdielMendoza/Desktop/Desarrollo/Casita_Bakery_2.0/frontend/README.md)

## Stack

### Backend

- Python
- Flask
- Flask-SQLAlchemy
- Flask-JWT-Extended
- MySQL

### Frontend

- Angular 20
- TypeScript
- Angular Router
- Angular Forms
- HttpClient

## Estado actual del proyecto

Actualmente el sistema ya tiene funcionales:

- login con JWT
- logout
- dashboard con datos reales
- modulo de clientes
- modulo de productos
- modulo de ingredientes
- modulo de pedidos
- seeds de datos demo

Pendientes que pueden venir despues:

- reportes
- roles y permisos mas avanzados
- consumo automatico de inventario por recetas
- mejoras visuales adicionales

## Requisitos

Para trabajar el proyecto completo necesitas:

- Python 3.11+
- Node.js
- npm
- MySQL Server

## Arranque rapido

### 1. Backend

```powershell
cd C:\Users\AbdielMendoza\Desktop\Desarrollo\Casita_Bakery_2.0\backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py
```

Backend disponible en:

```text
http://127.0.0.1:5000
```

### 2. Frontend

```powershell
cd C:\Users\AbdielMendoza\Desktop\Desarrollo\Casita_Bakery_2.0\frontend
npm install
npm start
```

Frontend disponible en:

```text
http://localhost:4200
```

## Base de datos y datos demo

El backend incluye:

- [Script_db_Casita_Bakery.sql](/c:/Users/AbdielMendoza/Desktop/Desarrollo/Casita_Bakery_2.0/backend/Script_db_Casita_Bakery.sql)
- [seed_data.sql](/c:/Users/AbdielMendoza/Desktop/Desarrollo/Casita_Bakery_2.0/backend/seed_data.sql)
- [reset_seed.sql](/c:/Users/AbdielMendoza/Desktop/Desarrollo/Casita_Bakery_2.0/backend/reset_seed.sql)

Uso recomendado:

- `Script_db_Casita_Bakery.sql` para crear el esquema
- `seed_data.sql` para cargar datos demo
- `reset_seed.sql` para limpiar y volver a sembrar

## Flujo funcional actual

1. El usuario inicia sesion desde el frontend.
2. El backend valida credenciales y entrega tokens JWT.
3. El frontend guarda la sesion en `sessionStorage`.
4. El interceptor adjunta el token a las rutas protegidas.
5. El usuario puede administrar clientes, productos, ingredientes y pedidos.

## Modulos implementados

### Dashboard

- resumen de pedidos reales
- pedidos pendientes
- pedidos entregados
- tabla de pedidos recientes

### Clientes

- listar
- buscar
- crear
- editar
- eliminar

### Productos

- listar
- buscar
- crear
- editar
- eliminar

### Ingredientes

- listar
- buscar
- crear
- editar

### Pedidos

- listar
- filtrar
- ver detalle
- crear
- editar pendientes

## Variables de entorno

El backend usa `.env` y ya incluye una plantilla:

- [backend/.env.example](/c:/Users/AbdielMendoza/Desktop/Desarrollo/Casita_Bakery_2.0/backend/.env.example)

## Recomendaciones

- mantén el backend y el frontend levantados en terminales separadas
- usa `reset_seed.sql` cuando quieras volver a un estado limpio de pruebas
- reinicia `ng serve` si Angular se queda con errores de watcher
- mantén `.env` fuera del repositorio

## Troubleshooting rapido

### `npm` no funciona en PowerShell

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### Login falla por dependencia de MySQL

Verifica que el backend tenga instaladas todas las dependencias:

```powershell
pip install -r backend/requirements.txt
```

### Angular queda con errores fantasma

Deten `ng serve` y vuelvelo a iniciar.

## Documentacion por modulo

- [Backend README](/c:/Users/AbdielMendoza/Desktop/Desarrollo/Casita_Bakery_2.0/backend/README.md)
- [Frontend README](/c:/Users/AbdielMendoza/Desktop/Desarrollo/Casita_Bakery_2.0/frontend/README.md)
