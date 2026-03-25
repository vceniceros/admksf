# consorcio 360
manejador de software para administracion de consorcios

## Inicio del proyecto con Docker (guía para sysadmin)

Esta guía se basa en [Dockerfile](Dockerfile) y [docker-compose.yml](docker-compose.yml). Deja el proyecto listo con **frontend**, **backend** y **base de datos** sin instalar dependencias en el host.

## 1) Requisitos mínimos en el host

- Docker Engine instalado.
- Docker Compose (plugin de Docker).
- Acceso a puertos libres `8000` y `5433` en el host.

Si el usuario no tiene permisos para usar Docker, agregarlo al grupo `docker` o ejecutar con `sudo`.

## 2) Qué servicios levanta Docker Compose

En [docker-compose.yml](docker-compose.yml) hay dos servicios:

1. **db** (PostgreSQL 15)
	- Imagen: `postgres:15-alpine`
	- Persistencia: volumen `postgres_data`.
	- Puerto host → contenedor: `5433 → 5432`.

2. **web** (Django + Angular compilado)
	- Se construye con [Dockerfile](Dockerfile).
	- Expone el puerto `8000`.
	- Corre con Gunicorn: `backend_core.wsgi:application`.

## 3) Puertos y accesos

- **Aplicación web (frontend + backend)**: http://localhost:8000
- **Base de datos PostgreSQL**: `localhost:5433`

## 4) Variables de entorno principales

Definidas en [docker-compose.yml](docker-compose.yml):
- **DB_NAME**: `admksf`
- **DB_USER**: `admin`
- **DB_PASSWORD**: `S4br1n4b0t0n4`
- **DB_HOST**: `db`
- **DB_PORT**: `5432`
- **DJANGO_SECRET_KEY**: `B0k4v4S4l1rc@mp30n`
- **DJANGO_DEBUG**: `True`

> Nota: credenciales de DB están en el compose. Para producción, moverlas a un `.env` y no commitear secretos.

## 5) Cómo se construye la imagen (resumen del Dockerfile)

El build tiene **dos etapas**:

1. **Frontend (Angular)**
	- Base: `node:22-alpine`.
	- Instala dependencias (`npm install`).
	- Compila con `npm run build -- --configuration production`.
	- Resultado: `/app/dist/frontend/browser`.

2. **Backend (Django)**
	- Base: `python:3.10-slim`.
	- Instala dependencias de sistema (`gcc`, `libpq-dev`).
	- Instala dependencias Python y `gunicorn` + `whitenoise`.
	- Copia el backend a `/app`.
	- Copia el build de Angular a:
	  - Estáticos: `/app/static_angular`
	  - Template principal: `/app/templates/index.html`
	- Ejecuta `python manage.py collectstatic --noinput`.
	- Expone `8000` y arranca Gunicorn.

## 6) Pasos de arranque (primera vez)

Ejecutar desde la raíz del proyecto.

1. **Construir y levantar en segundo plano**
	- `docker compose up -d --build`
	- Esto compila Angular + Django y levanta PostgreSQL.
	- El modo `-d` evita que el comando quede pegado a la consola, permitiendo ejecutar migraciones.

2. **Aplicar migraciones**
	- `docker compose exec web python manage.py migrate`

3. **Crear superusuario (opcional, recomendado)**
	- `docker compose exec web python manage.py createsuperuser`

4. **Abrir la app**
	- http://localhost:8000

## 7) Uso diario (comandos útiles)

- **Arrancar sin reconstruir**:
  - `docker compose up`

- **Ver logs del backend**:
  - `docker compose logs -f web`

- **Ver logs de la base**:
  - `docker compose logs -f db`

- **Entrar al contenedor del backend**:
  - `docker compose exec web bash`

- **Detener servicios**:
  - `docker compose down`

## 8) Reinicio limpio (si falla una ejecución y otra no)

Este procedimiento deja el sistema en un estado conocido y reproducible.

1. **Bajar todo y borrar volumen de DB**
	- `docker compose down -v`

2. **Levantar de cero con build**
	- `docker compose up -d --build`

3. **Aplicar migraciones**
	- `docker compose exec web python manage.py migrate`

4. **Verificar estado**
	- `docker compose ps`

5. **Abrir la app**
	- http://localhost:8000

## 9) Persistencia de base de datos

PostgreSQL usa el volumen `postgres_data` definido en el compose.
Mientras el volumen exista, los datos se conservan.

- **Eliminar todo (incluye la DB)**:
  - `docker compose down -v`

## 10) Problemas comunes y solución rápida

- **Puerto 8000 ocupado**: liberar el puerto o editar [docker-compose.yml](docker-compose.yml) y cambiar `8000:8000`.
- **Puerto 5433 ocupado**: cambiar a otro puerto en el host, por ejemplo `5434:5432`.
- **Permisos Docker**: ejecutar con `sudo` o agregar usuario al grupo `docker`.
- **Error de migraciones**: ejecutar `docker compose exec web python manage.py makemigrations` y luego `migrate`.
- **Cambios en frontend no se ven**: reconstruir la imagen con `docker compose up --build`.

## 11) Resumen rápido (checklist)

- [ ] Docker y Compose instalados.
- [ ] `docker compose up -d --build`
- [ ] `docker compose exec web python manage.py migrate`
- [ ] (opcional) `docker compose exec web python manage.py createsuperuser`
- [ ] Abrir http://localhost:8000
