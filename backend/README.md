# Casita Bakery Backend

Backend REST para la gestion de clientes, productos, inventario y pedidos de **Casita Bakery**.

Esta API esta construida con Flask y MySQL, usa JWT para autenticacion y ya incluye scripts para crear el esquema y cargar datos de prueba.

## Stack

- Python 3.11+
- Flask
- Flask-SQLAlchemy
- Flask-JWT-Extended
- Flask-CORS
- MySQL
- PyMySQL

## Funcionalidades actuales

- Login con JWT
- Refresh token
- CRUD de clientes
- CRUD de productos
- CRUD de inventario
- Gestion de pedidos con detalles
- Logging en archivo y consola
- Seeds de datos demo

## Estructura

```text
backend/
├─ app/
│  ├─ models/
│  ├─ routes/
│  ├─ services/
│  └─ utils/
├─ logs/
├─ .env.example
├─ config.py
├─ create_user.py
├─ requirements.txt
├─ run.py
├─ Script_db_Casita_Bakery.sql
├─ seed_data.sql
└─ reset_seed.sql
```

## Requisitos

- Python instalado
- MySQL Server disponible
- Una base de datos llamada `Casita_Bakery`

## Instalacion

Desde la carpeta `backend`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Si PowerShell bloquea la activacion del entorno virtual:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## Variables de entorno

Crea un archivo `.env` a partir de [.env.example](/c:/Users/AbdielMendoza/Desktop/Desarrollo/Casita_Bakery_2.0/backend/.env.example).

Variables principales:

```env
FLASK_ENV=development
PORT=5000

DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=Casita_Bakery

APP_SECRET_KEY=replace_with_app_secret
JWT_SECRET_KEY=replace_with_jwt_secret

CORS_ORIGINS=http://localhost:4200
LOG_LEVEL=INFO
AUTO_CREATE_DB=False
```

## Crear la base de datos

Si aun no has creado el esquema, ejecuta:

```sql
SOURCE Script_db_Casita_Bakery.sql;
```

O abre [Script_db_Casita_Bakery.sql](/c:/Users/AbdielMendoza/Desktop/Desarrollo/Casita_Bakery_2.0/backend/Script_db_Casita_Bakery.sql) en MySQL Workbench y ejecutalo completo.

## Cargar datos demo

Para insertar datos de prueba sobre una base vacia:

```sql
SOURCE seed_data.sql;
```

Para limpiar y volver a sembrar todo:

```sql
SOURCE reset_seed.sql;
```

Conteos esperados despues de `reset_seed.sql`:

- `Clientes`: 5
- `Productos`: 5
- `Ingredientes`: 9
- `Pedidos`: 3
- `Detalles_pedido`: 7
- `Recetas`: 20

## Crear usuario de acceso

Puedes crear usuarios manualmente con:

```powershell
python create_user.py <username> <password>
```

Ejemplo:

```powershell
python create_user.py admin 123456
```

## Ejecutar el backend

Con el entorno virtual activo:

```powershell
python run.py
```

La API queda disponible normalmente en:

```text
http://127.0.0.1:5000
```

## Autenticacion

### Login

Endpoint:

```http
POST /auth/api/login
```

Body:

```json
{
  "username": "admin",
  "password": "123456"
}
```

Respuesta exitosa:

```json
{
  "success": true,
  "message": "Login exitoso",
  "data": {
    "access_token": "...",
    "refresh_token": "...",
    "user": {
      "id": 1,
      "usuario": "admin"
    }
  }
}
```

### Refresh

Endpoint:

```http
POST /auth/api/refresh
```

Header:

```http
Authorization: Bearer <refresh_token>
```

## Endpoints principales

### Auth

- `POST /auth/api/login`
- `POST /auth/api/refresh`

### Clientes

- `GET /cliente/api/`
- `GET /cliente/api/<id>`
- `POST /cliente/api/`
- `PUT /cliente/api/<id>`
- `DELETE /cliente/api/<id>`

### Productos

- `GET /producto/api/`
- `GET /producto/api/<id>`
- `POST /producto/api/`
- `PUT /producto/api/<id>`
- `DELETE /producto/api/<id>`

### Inventario

- `GET /inventario/api/`
- `GET /inventario/api/<id>`
- `POST /inventario/api/`
- `PUT /inventario/api/<id>`

### Pedidos

- `GET /pedidos/api/`
- `GET /pedidos/api/<id>`
- `POST /pedidos/api/`
- `PUT /pedidos/api/<id>`

## Formato de respuesta

La API usa un formato uniforme como base:

```json
{
  "success": true,
  "message": "Operacion realizada correctamente",
  "data": {},
  "errors": null,
  "status_code": 200,
  "timestamp": "2026-03-28T12:00:00"
}
```

## Logs

Los logs se escriben en:

- [logs/api.log](/c:/Users/AbdielMendoza/Desktop/Desarrollo/Casita_Bakery_2.0/backend/logs/api.log)

El nivel de logs se controla con:

```env
LOG_LEVEL=INFO
```

## Estado actual del proyecto

El backend esta preparado para trabajar con el frontend actual y ya cubre:

- autenticacion
- clientes
- productos
- ingredientes
- pedidos

Cosas que **todavia no estan implementadas como flujo operativo completo**:

- consumo automatico de inventario a partir de recetas
- modulo de reportes
- sistema de roles/permisos avanzado

## Recomendaciones de uso

- Usa `reset_seed.sql` cuando quieras volver a un estado limpio de pruebas.
- Mantén `.env` fuera del repositorio.
- Reinicia `run.py` despues de cambiar dependencias o configuracion sensible.

## Troubleshooting

### Error con `npm` o CORS

Verifica que el frontend corra en:

```text
http://localhost:4200
```

y que `CORS_ORIGINS` lo incluya.

### Error de login por `cryptography`

Si MySQL usa metodos modernos de autenticacion, asegúrate de tener instalada esta dependencia:

```powershell
pip install -r requirements.txt
```

El archivo [requirements.txt](/c:/Users/AbdielMendoza/Desktop/Desarrollo/Casita_Bakery_2.0/backend/requirements.txt) ya incluye `cryptography`.
