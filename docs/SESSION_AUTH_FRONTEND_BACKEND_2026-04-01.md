# Resumen de Cambios de la Sesion - Auth Backend y Frontend

Fecha: 2026-04-01

## Objetivo General

Durante esta sesion se implemento una base completa de autenticacion para el sistema:

- backend Django con usuarios de dominio, roles, registro, login JWT, verificacion de sesion y recuperacion manual de contrasena;
- frontend Angular con flujo de login y registro, persistencia de JWT, rutas protegidas y reorganizacion de la entrada principal de la aplicacion.

El criterio seguido fue mantener la estructura actual del repositorio, respetar la arquitectura atomica del frontend y no reemplazar el usuario interno de Django para evitar una migracion riesgosa sobre `django.contrib.auth`.

## Cambios en Backend

### 1. Nueva app de dominio `usuarios`

Se agrego una nueva app Django dedicada a usuarios administrativos del dominio.

Archivos principales incorporados:

- `backend/usuarios/apps.py`
- `backend/usuarios/models.py`
- `backend/usuarios/services.py`
- `backend/usuarios/views.py`
- `backend/usuarios/urls.py`
- `backend/usuarios/auth_service.py`
- `backend/usuarios/admin.py`

Tambien se incorporo la app en `INSTALLED_APPS` y se registraron sus rutas bajo `api/usuarios/`.

### 2. Modelado de roles y usuarios de dominio

Se agregaron los modelos:

- `Rol`
- `Usuario`

Campos relevantes del modelo `Usuario`:

- `correo_electronico`
- `contrasena`
- `fecha_creacion`
- `ultimo_ingreso`
- `esta_activo`
- `nombre`
- `apellido`
- `rol`

Decision de arquitectura:

- no se reemplazo `django.contrib.auth.User`;
- se mantuvo un usuario propio del dominio para aislar la logica de negocio y evitar un cambio estructural mas costoso.

### 3. Relacion entre usuario y consorcios

Se amplio el modelo `Consorcio` para soportar:

- `1 usuario -> N consorcios`

Esto se implemento agregando una FK opcional desde `Consorcio` hacia `usuarios.Usuario`.

Archivos impactados:

- `backend/consorcios/models.py`
- `backend/consorcios/admin.py`
- `backend/consorcios/migrations/0003_consorcio_usuario.py`

### 4. Migraciones creadas

Se generaron las siguientes migraciones:

- `backend/usuarios/migrations/0001_initial.py`
- `backend/usuarios/migrations/0002_seed_roles.py`
- `backend/usuarios/migrations/0003_usuario_fecha_creacion.py`
- `backend/consorcios/migrations/0003_consorcio_usuario.py`

Ademas se sembraron por migracion los roles iniciales:

- `superusuario`
- `administrador`

### 5. Servicio de autenticacion

Se creo `AuthService` para encapsular las operaciones de autenticacion y credenciales.

Capacidades incorporadas:

- hashing de contrasenas usando Django;
- uso de sal aleatoria de `16 bytes`;
- generacion de JWT;
- decodificacion y validacion de JWT;
- extraccion de Bearer token desde `Authorization`;
- deteccion de ventana de refresh;
- armado de respuesta estandar de autenticacion;
- generacion de contrasena temporal segura para recuperacion manual.

Configuracion por entorno soportada:

- `JWT_SECRET_KEY`
- `JWT_ALGORITHM`
- `JWT_EXPIRATION_SECONDS`
- `JWT_REFRESH_WINDOW_SECONDS`

Detalles implementados:

- algoritmo por defecto: `HS256`;
- expiracion por defecto: `1800` segundos;
- ventana de refresh por defecto: `300` segundos;
- claim `jti` aleatorio para evitar que dos refresh consecutivos produzcan el mismo token.

### 6. Servicio de usuarios

En `UsuarioService` se incorporaron operaciones para:

- registrar usuarios;
- normalizar payloads;
- resolver roles;
- autenticar usuario por correo y contrasena;
- actualizar `ultimo_ingreso` en login exitoso;
- validar sesion a partir de JWT;
- refrescar token si entra en ventana de vencimiento;
- validar que un usuario tenga rol `superusuario`;
- recuperar o resetear manualmente contrasenas.

### 7. Endpoints backend agregados

Se agregaron los siguientes endpoints:

- `POST /api/usuarios/registrar/`
- `POST /api/usuarios/login/`
- `GET /api/usuarios/autenticado/`
- `POST /api/usuarios/recuperar-contrasena/`

Comportamiento de cada uno:

- `registrar`: crea un usuario de dominio;
- `login`: autentica contra la base y retorna JWT;
- `autenticado`: valida el token actual y lo refresca si corresponde;
- `recuperar-contrasena`: permite a un `superusuario` resetear la contrasena de otro usuario, con contrasena explicita o temporal autogenerada.

### 8. Validaciones y seguridad backend

Se cubrieron los siguientes escenarios:

- JSON invalido;
- rol inexistente;
- usuario o contrasena invalidos;
- usuario inactivo;
- token expirado o invalido;
- uso de recovery por un usuario sin permisos de `superusuario`.

### 9. Dependencias backend

Se agrego a `backend/requirements.txt`:

- `PyJWT`

## Cambios en Frontend Angular

### 1. Reorganizacion del acceso principal

La ruta raiz `/` dejo de ser el menu de consorcios y paso a ser la pantalla de autenticacion.

Nuevo flujo:

- `/` -> acceso login/register;
- `/consorcios` -> menu de consorcios autenticado;
- `/dashboard/...` -> rutas protegidas.

### 2. Capa de autenticacion frontend

Se agregaron los siguientes elementos:

- `frontend/src/models/auth.model.ts`
- `frontend/src/app/services/auth.service.ts`
- `frontend/src/app/interceptors/auth.interceptor.ts`
- `frontend/src/app/guards/auth.guard.ts`

Responsabilidades:

- tipado del contrato de auth;
- login contra backend;
- registro contra backend;
- verificacion de sesion vigente;
- persistencia de JWT en `localStorage`;
- inyeccion automatica del Bearer token en llamadas `/api/*`;
- logout;
- proteccion de rutas privadas;
- bloqueo de la pantalla de login si ya existe sesion valida.

### 3. Componentes atomicos, moleculares, organismos y template

Se agregaron nuevos componentes siguiendo la arquitectura atomica existente.

Atomos:

- `auth-input.component`
- `auth-action-button.component`

Moleculas:

- `auth-field.component`
- `auth-mode-toggle.component`
- `auth-feedback-card.component`

Organismos:

- `login-form.component`
- `register-form.component`

Template:

- `auth-access.component`

Objetivo visual:

- mantener una estetica consistente con el proyecto;
- conservar una interfaz administrativa limpia;
- generar una pantalla de entrada mas fuerte visualmente que la raiz anterior;
- sostener el flujo completo de acceso sin romper la estructura standalone existente.

### 4. Login conectado al backend

El formulario de login consume:

- `POST /api/usuarios/login/`

Y al autenticar:

- guarda el JWT;
- persiste la sesion en `localStorage`;
- redirige a `/consorcios`.

### 5. Registro conectado al backend

El formulario de registro consume:

- `POST /api/usuarios/registrar/`

Comportamiento implementado:

- registra usuarios con rol `administrador`;
- valida campos requeridos;
- valida email;
- valida longitud minima de contrasena;
- valida coincidencia entre contrasena y confirmacion;
- muestra feedback de errores de backend y confirmacion de alta exitosa.

### 6. Ajustes de shell y navegacion

Se modificaron:

- `frontend/src/app/app.config.ts`
- `frontend/src/app/app.routes.ts`
- `frontend/src/app/app.routes.server.ts`
- `frontend/src/app/app.ts`

Cambios relevantes:

- provider HTTP con interceptor de auth;
- guards para rutas privadas y de invitado;
- bootstrap de sesion al iniciar la app;
- sidebar visible solo en rutas de dashboard;
- fallback de rutas a `/`.

### 7. Ajustes de navbar y menu de consorcios

Se actualizaron:

- `frontend/src/app/components/organism/navbar-component/*`
- `frontend/src/app/components/templates/consortium-menu.component/*`

Ahora el frontend muestra:

- usuario autenticado en navbar;
- rol visible;
- boton `Salir`;
- identificacion del usuario dentro del menu de consorcios.

### 8. Ajustes de redireccion internos

Se actualizaron redirecciones que antes volvian a `/` para que ahora regresen a `/consorcios` cuando corresponde.

Archivos ajustados:

- `frontend/src/app/components/pages/consortium-form/consortium-form.ts`
- `frontend/src/app/components/pages/dashboard/dashboard.ts`

## Documentacion actualizada

Se actualizaron documentos existentes para reflejar el nuevo dominio de usuarios:

- `consorcio 360.md`
- `diagramas/diagrama relacional de la bdd.md`

Ademas, este archivo deja consolidado todo lo implementado durante la sesion.

## Pruebas y validaciones ejecutadas

### Backend

Se ejecutaron pruebas de unidad e integracion para `usuarios`.

Comando validado:

```bash
cd /home/ceni/Git/consorcio-360/backend
/home/ceni/Git/consorcio-360/.venv/bin/python manage.py test usuarios.tests.unit usuarios.tests.integration
```

Resultado final validado:

- `23` tests ejecutados;
- resultado `OK`.

Tambien se valido consistencia de migraciones con:

```bash
/home/ceni/Git/consorcio-360/.venv/bin/python manage.py makemigrations --check --dry-run
```

Resultado final:

- `No changes detected`

### Frontend

Se instalaron dependencias y se valido compilacion del frontend.

Comandos ejecutados:

```bash
cd /home/ceni/Git/consorcio-360/frontend
npm install
npm run build
```

Resultado final:

- build Angular exitosa;
- salida generada en `frontend/dist/frontend`.

Observacion:

- quedaron warnings preexistentes del repo por imports standalone no usados en componentes ajenos al flujo de autenticacion;
- no bloquearon la compilacion;
- el nuevo flujo implementado quedo compilando correctamente.

## Archivos nuevos o modificados mas relevantes

Backend:

- `backend/backend_core/settings.py`
- `backend/backend_core/urls.py`
- `backend/requirements.txt`
- `backend/consorcios/models.py`
- `backend/consorcios/admin.py`
- `backend/consorcios/migrations/0003_consorcio_usuario.py`
- `backend/usuarios/*`
- `backend/usuarios/tests/*`

Frontend:

- `frontend/src/models/auth.model.ts`
- `frontend/src/app/services/auth.service.ts`
- `frontend/src/app/interceptors/auth.interceptor.ts`
- `frontend/src/app/guards/auth.guard.ts`
- `frontend/src/app/components/atoms/auth-*`
- `frontend/src/app/components/molecules/auth-*`
- `frontend/src/app/components/organism/login-form.component/*`
- `frontend/src/app/components/organism/register-form.component/*`
- `frontend/src/app/components/templates/auth-access.component/*`
- `frontend/src/app/app.config.ts`
- `frontend/src/app/app.routes.ts`
- `frontend/src/app/app.routes.server.ts`
- `frontend/src/app/app.ts`
- `frontend/src/app/components/organism/navbar-component/*`
- `frontend/src/app/components/templates/consortium-menu.component/*`
- `frontend/src/app/components/pages/consortium-form/consortium-form.ts`
- `frontend/src/app/components/pages/dashboard/dashboard.ts`
- `frontend/package-lock.json`

Documentacion:

- `docs/SESSION_AUTH_FRONTEND_BACKEND_2026-04-01.md`
- `consorcio 360.md`
- `diagramas/diagrama relacional de la bdd.md`

## Estado al cierre de la sesion

Quedo implementado y validado:

- modelo de usuarios y roles de dominio;
- registro de usuario;
- almacenamiento de contrasena hasheada con sal;
- login con JWT;
- verificacion y refresh de sesion;
- recuperacion manual de contrasena para superusuario;
- frontend con login/register real contra backend;
- persistencia de sesion JWT en Angular;
- proteccion de rutas privadas;
- menu de consorcios detras de autenticacion.

No quedo implementado en esta sesion:

- flujo SMTP de recuperacion;
- pantalla frontend para recuperacion de contrasena;
- middleware global backend para proteger todos los endpoints por JWT;
- tests de frontend para el nuevo flujo de acceso.

## Commit Message Sugerido

```text
feat(auth): implementar usuarios de dominio, JWT backend y acceso Angular con rutas protegidas

- agregar app usuarios en Django con modelos Rol y Usuario
- relacionar Consorcio con Usuario para soportar 1 usuario a N consorcios
- crear migraciones iniciales, seed de roles y campo fecha_creacion
- incorporar AuthService backend con hashing seguro, sal de 16 bytes, JWT y password temporal
- agregar endpoints de registro, login, verificacion de autenticacion y recuperacion manual de contrasena
- cubrir flujo de usuarios con pruebas unitarias e integracion en backend
- agregar PyJWT a dependencias del backend
- crear capa de auth en Angular con modelos, AuthService, interceptor y guards
- implementar pantalla inicial de login/register respetando arquitectura atomica del frontend
- crear nuevos atomos, moleculas, organismos y template para acceso autenticado
- mover el menu de consorcios a /consorcios y proteger dashboard y rutas privadas
- persistir JWT en localStorage y adjuntarlo automaticamente a llamadas /api
- actualizar navbar y menu de consorcios para mostrar usuario autenticado y logout
- ajustar redirecciones del frontend al nuevo flujo de acceso
- actualizar documentacion funcional y relacional del proyecto
```