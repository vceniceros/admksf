# Documentación Técnica: Proyecto Consorcio 360 (ConsorcioAdmin)

## 1. Descripción General
**Consorcio 360** es una plataforma integral diseñada para la administración y gestión de consorcios, barrios cerrados y edificios. El sistema busca centralizar la comunicación, el control financiero y la automatización de procesos administrativos mediante una interfaz moderna y flujos de trabajo inteligentes.

---

## 2. Objetivos del Proyecto
* **Centralización:** Administrar múltiples consorcios desde un único panel de control.
* **Automatización de Gastos:** Integrar herramientas de IA y flujos (n8n) para procesar facturas físicas y convertirlas en registros digitales de forma automática.
* **Transparencia Financiera:** Generar reportes de expensas, seguimiento de pagos y estados de cuenta en tiempo real.
* **Escalabilidad:** Arquitectura basada en contenedores para facilitar el despliegue y crecimiento del sistema.

---

## 3. Arquitectura del Sistema
El proyecto utiliza un modelo de arquitectura desacoplada pero integrada en un mismo repositorio (monorepo), optimizada para Docker.

### Stack Tecnológico
* **Frontend:** Angular (versión 19).
* **Backend:** Django (Python 3.12).
* **Base de Datos:** PostgreSQL.
* **Servidor de Archivos:** WhiteNoise (para estáticos) e integración con Google Drive para documentos.
* **Automatización:** n8n (para el procesamiento de facturas mediante JSON).

### Flujo de Despliegue (Docker)
El `Dockerfile` utiliza una construcción multietapa (*multi-stage build*):
1.  **Etapa de construcción:** Se compila el frontend Angular.
2.  **Etapa de ejecución:** Se configura el entorno Python, se instalan las dependencias del backend y se copian los archivos compilados del frontend para que Django los sirva.

---

## 4. Estructura de Carpetas y Organización
La organización del código sigue estándares de modularidad y separación de responsabilidades:

```text
/
├── backend/                # Lógica de negocio y API (Django)
│   ├── backend_core/       # Configuración global y rutas
│   ├── templates/          # Contenedor del index.html de Angular
│   └── static/             # Archivos estáticos recolectados
├── frontend/               # Interfaz de usuario (Angular)
│   ├── src/
│   │   ├── app/
│   │   │   ├── components/ # Organizados por Atomic Design
│   │   │   │   ├── atoms/     # Componentes mínimos (botones, inputs)
│   │   │   │   ├── molecules/ # Grupos funcionales (cards, filas)
│   │   │   │   └── organisms/ # Secciones complejas (navbars, sidebars)
│   │   │   ├── pages/      # Vistas principales (Dashboard, Gastos, etc.)
│   │   │   └── services/   # Comunicación con el backend
│   │   └── models/         # Definición de interfaces de datos
├── docker-compose.yml      # Orquestación de servicios (web + db)
├── Dockerfile              # Configuración de imagen unificada
└── manager.sh              # Scripts de automatización de tareas
```

## 5. Historial de Problemas y Soluciones Técnicas

Durante el desarrollo se han enfrentado desafíos críticos de integración que fueron documentados y resueltos:

* **Servido de Single Page Application (SPA):** * *Problema:* Errores 400 Bad Request y 404 Not Found al intentar que Django sirviera los archivos estáticos de Angular.
    * *Solución:* Implementación de `WhiteNoise` para archivos estáticos y configuración de una `TemplateView` en `backend_core/urls.py` que captura todas las rutas no definidas en la API para redirigirlas al `index.html` de Angular, permitiendo que el router del frontend gestione la navegación.
* **Gestión de Errores en la API:**
    * *Problema:* Fallos silenciosos o crasheos al recibir JSONs malformados desde integraciones externas.
    * *Solución:* Se añadieron bloques `try-except` específicos para `JSONDecodeError` y `ValidationError` en las vistas de creación y actualización de consorcios, devolviendo respuestas HTTP 400 con detalles claros del error.
* **Responsividad del Layout:**
    * *Problema:* El Sidebar obstruía la vista en dispositivos móviles y no se comportaba correctamente en la pantalla de selección inicial.
    * *Solución:* Se implementó lógica de estados en Angular para ocultar el menú lateral en pantallas menores a 768px y desactivarlo por completo en rutas específicas como `/selection`.

---

## 6. Detalles de Implementación: Modelos y Base de Datos

El núcleo del sistema de información se basa en una estructura de datos robusta validada en el backend.

### Modelo: Consorcio

Representa la entidad principal del sistema. Sus campos clave son:
* **Nombre:** Identificador visual del barrio o edificio.
* **CUIT:** Clave única de identificación tributaria (incluye validador de formato).
* **Email:** Contacto administrativo.
* **Imagen URL:** Referencia a los logos o fotos del consorcio almacenados digitalmente.
* **Usuario administrador:** Relación hacia un usuario del dominio para permitir que un mismo usuario gestione múltiples consorcios.

### Modelo: Usuario y Rol

El backend incorpora un modelo de usuario administrativo propio, separado del usuario interno de Django Admin. Sus campos principales son correo electrónico, contraseña hasheada, timestamp de último ingreso, estado de activación, nombre, apellido y una relación con la tabla de roles.

Roles iniciales del dominio:
* **superusuario**
* **administrador**

### Flujo de Datos de Facturación

El sistema está preparado para recibir datos estructurados desde **n8n**. El flujo consiste en:
1.  Recepción de imagen/PDF en n8n.
2.  Procesamiento mediante IA para extraer CUIT emisor, fecha, concepto e importes.
3.  Envío de un POST JSON al backend de Django para la creación automática del registro de gasto.

---

## 7. Infraestructura y Herramientas de Desarrollo
El proyecto utiliza herramientas de automatización para garantizar la paridad entre los entornos de desarrollo y producción.

### Orquestación con Docker
* **Servicio Web:** Contenedor Python 3.12 que corre tanto el servidor Gunicorn/Runserver como el build de Angular.
* **Servicio DB:** Imagen oficial de PostgreSQL con persistencia de datos mediante volúmenes.

### Scripts de Gestión (`manager.sh`)
Se dispone de un script centralizado para agilizar tareas comunes:
* `./manager.sh build`: Construye las imágenes de Docker desde cero.
* `./manager.sh up`: Inicia los servicios en segundo plano.
* `./manager.sh migrate`: Ejecuta las migraciones de base de datos en el contenedor activo.
* `./manager.sh logs`: Permite el monitoreo en tiempo real de los errores del sistema.

---

## 8. Estado Actual y Roadmap

### Estado Actual

* ✅ Arquitectura de contenedores operativa.
* ✅ Comunicación fluida entre Angular 19 y Django.
* ✅ CRUD básico de Consorcios funcional con validaciones.
* ✅ Sistema de componentes (Atomic Design) establecido en el frontend.

### Próximos Pasos

1.  **Módulo de Liquidación:** Implementar la lógica para prorratear gastos entre unidades funcionales.
2.  **Integración de Pagos:** Conectar con pasarelas de pago para automatizar la conciliación bancaria.
3.  **Portal del Propietario:** Desarrollar la vista restringida para que los residentes puedan descargar sus expensas y ver comunicados.