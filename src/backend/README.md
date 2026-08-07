# TiroX Backend

Backend para la aplicacion **TiroX**, una plataforma para el registro y seguimiento de mediciones hormonales de usuarios. Desarrollado con **Node.js**, **Express**, **MySQL** y patron **MVC** usando **ES Modules**.

---

## Instalacion

### Requisitos previos
- Node.js (v18 o superior)
- MySQL (corriendo en localhost)

### Pasos

1. Clonar o copiar el proyecto:
   ```bash
   cd tiroX-Backend
   ```

2. Instalar dependencias:
   ```bash
   npm install
   ```

3. Configurar variables de entorno en el archivo `.env`:
   ```env
   DB_HOST=localhost
   DB_USER=root
   DB_PASS=
   DB_NAME=tirox
   JWT_SECRET=tu_secreto_aqui
   JWT_EXPIRES_IN=1d
   PORT=3000
   ```

4. Crear la base de datos en MySQL (si aun no existe):
   ```sql
   CREATE DATABASE tirox;
   USE tirox;

   CREATE TABLE users (
     id BINARY(16) NOT NULL PRIMARY KEY,
     username VARCHAR(100) NOT NULL UNIQUE,
     email VARCHAR(100) NOT NULL UNIQUE,
     password TEXT NOT NULL,
     first_name VARCHAR(100) NOT NULL,
     last_name VARCHAR(100) NOT NULL,
     age TINYINT
   );

   CREATE TABLE registers (
     id BINARY(16) NOT NULL PRIMARY KEY,
     hormone VARCHAR(50) NOT NULL,
     result DECIMAL(6,2) NOT NULL,
     user_id BINARY(16) NOT NULL,
     FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
   );
   ```

5. Iniciar el servidor:
   ```bash
   npm start
   ```

El servidor estara disponible en `http://localhost:3000`.

---

## Estructura del Proyecto (MVC)

```
tiroX-Backend/
├── src/
│   ├── config/
│   │   └── db.js               # Conexion a MySQL (pool de conexiones)
│   ├── models/
│   │   ├── User.js             # Modelo de usuario (queries a DB)
│   │   └── Record.js           # Modelo de registros (queries a DB)
│   ├── controllers/
│   │   ├── authController.js   # Logica de registro y login
│   │   └── recordsController.js # Logica CRUD de registros
│   ├── routes/
│   │   ├── auth.js             # Rutas de autenticacion
│   │   └── records.js          # Rutas de registros
│   ├── middleware/
│   │   └── auth.js             # Middleware de autenticacion JWT
│   ├── __tests__/
│   │   ├── auth.test.js        # Tests de autenticacion
│   │   ├── records.test.js     # Tests de registros
│   │   └── middleware.test.js  # Tests del middleware JWT
│   ├── app.js                  # Configuracion de Express (exportable)
│   └── server.js               # Punto de entrada (inicia el servidor)
├── .env                        # Variables de entorno
├── package.json
└── README.md
```

### Patron MVC

- **Models** (`src/models/`): Encargados de interactuar directamente con la base de datos. Contienen las queries SQL y la logica de acceso a datos.
- **Views** (API JSON): Las respuestas JSON que se envian al cliente.
- **Controllers** (`src/controllers/`): Contienen la logica de negocio. Reciben las requests, llaman a los models, y retornan las respuestas.
- **Routes** (`src/routes/`): Definen los endpoints y conectan las rutas con sus controllers.

---

## Endpoints

### Autenticacion

| Metodo | Ruta              | Descripcion              | Body Requerido                                                        |
|--------|-------------------|--------------------------|-----------------------------------------------------------------------|
| POST   | `/api/auth/register` | Registrar nuevo usuario  | `username`, `email`, `password`, `first_name`, `last_name`, `age` (opcional) |
| POST   | `/api/auth/login`    | Iniciar sesion            | `email`, `password`                                                   |

**Respuesta registro:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": "12345678-1234-1234-1234-123456789abc",
    "username": "testuser",
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User"
  }
}
```

**Respuesta login:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": "12345678-1234-1234-1234-123456789abc",
    "username": "testuser",
    "email": "test@example.com"
  }
}
```

### Registros Hormonales

> Todas las rutas requieren el header: `Authorization: Bearer <token>`

| Metodo | Ruta                  | Descripcion                  | Body Requerido              |
|--------|-----------------------|------------------------------|-----------------------------|
| POST   | `/api/records`        | Crear un registro nuevo      | `hormone`, `result`         |
| GET    | `/api/records`        | Obtener todos mis registros  | -                           |
| GET    | `/api/records/user/:userId` | Obtener registros de un usuario especifico | -          |
| GET    | `/api/records/:id`    | Obtener un registro por ID   | -                           |
| PUT    | `/api/records/:id`    | Actualizar un registro       | `hormone`, `result`         |
| DELETE | `/api/records/:id`    | Eliminar un registro         | -                           |

**Ejemplo crear registro:**
```bash
curl -X POST http://localhost:3000/api/records \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TU_TOKEN_AQUI" \
  -d '{"hormone": "TSH", "result": 4.50}'
```

**Respuesta:**
```json
{
  "id": "record-uuid-1234-5678-9abc-def012345678",
  "hormone": "TSH",
  "result": 4.50,
  "user_id": "12345678-1234-1234-1234-123456789abc"
}
```

---

## Scripts Disponibles

```bash
# Iniciar en produccion
npm start

# Iniciar en desarrollo (con nodemon, auto-reload)
npm run dev

# Ejecutar todos los tests
npm test
```

---

## Tests

Los tests estan escritos con **Jest** (modo ESM) y **Supertest**. Mockean los models para no necesitar una conexion real durante los tests.

```bash
npm test
```

### Cobertura de Tests (28 tests)

- **Auth (7):** Registro exitoso, usuario duplicado, login exitoso, credenciales invalidas, password incorrecta, errores del servidor.
- **Records (16):** Crear, obtener todos, obtener por usuario, obtener uno, actualizar, eliminar, autenticacion requerida, tokens invalidos.
- **Middleware (5):** Token valido, token ausente, token invalido, token expirado, formato incorrecto.

---

## Tecnologias

- **Runtime:** Node.js
- **Module System:** ES Modules (`import`/`export`)
- **Architecture:** MVC (Model-View-Controller)
- **Framework:** Express
- **Base de datos:** MySQL (mysql2/promise)
- **Autenticacion:** JWT (jsonwebtoken) + bcryptjs
- **UUID:** uuid v4 (para IDs de 16 bytes en binario)
- **Testing:** Jest (ESM) + Supertest
- **Desarrollo:** nodemon
