# ==========================================
# ETAPA 1: Construccion del Frontend (Angular)
# ==========================================
FROM node:22-alpine as build-step

WORKDIR /app

# Copiamos package.json e instalamos dependencias
COPY ./frontend/package.json ./frontend/package-lock.json ./
RUN npm install

# Copiamos el codigo fuente de Angular y construimos
COPY ./frontend ./
RUN npm run build -- --configuration production

# ==========================================
# ETAPA 2: Construcción del Backend (Django)
# ==========================================
FROM python:3.10-slim

WORKDIR /app

# Variables de entorno para Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instalar dependencias del sistema si son necesarias (opcional)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python
COPY ./backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn whitenoise

# Copiar el codigo de Django
COPY ./backend ./

# Copiamos los archivos compilados de Angular (desde la etapa 1) a Django

# 1. Copiamos los estaticos (JS, CSS) 
COPY --from=build-step /app/dist/frontend/browser /app/static_angular

# 2. Movemos el index.html a la carpeta de templates de Django
# (Asegúrate de tener una carpeta 'templates' creada en tu proyecto Django o créala aquí)
RUN mkdir -p /app/templates
RUN mv /app/static_angular/index.html /app/templates/index.html

# Recolectar estaticos (WhiteNoise los servirá)
RUN python manage.py collectstatic --noinput

# Exponer el puerto
EXPOSE 8000

# Comando para correr la app (usando Gunicorn para producción)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "backend_core.wsgi:application"]
