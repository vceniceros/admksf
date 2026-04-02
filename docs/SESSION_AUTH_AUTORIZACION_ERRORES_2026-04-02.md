# Resumen de Cambios de la Sesion - Autorizacion Global y Normalizacion de Errores

Fecha: 2026-04-02

## Alcance de este documento

Este documento resume exclusivamente lo avanzado despues de [SESSION_AUTH_FRONTEND_BACKEND_2026-04-01.md](/home/ceni/Git/consorcio-360/docs/SESSION_AUTH_FRONTEND_BACKEND_2026-04-01.md).

El foco de esta etapa fue:

- endurecer la seguridad de acceso sobre toda la API con JWT obligatorio;
- aplicar autorizacion por rol y por alcance de consorcios;
- simplificar la pantalla publica de acceso dejando solo login;
- normalizar los errores HTTP y el parsing de errores tanto en backend como en frontend.

## 1. Endurecimiento de autorizacion backend

### 1.1 Middleware JWT global para toda la API

Se agrego un middleware global para proteger todas las rutas bajo `/api/*`, dejando exento solamente el login.

Archivos principales:

- `backend/shared/middleware/jwt_auth.py`
- `backend/backend_core/settings.py`

Comportamiento implementado:

- exige header `Authorization: Bearer <token>` para toda llamada protegida;
- valida el JWT antes de llegar a la vista;
- inyecta en el request:
  - `request.usuario_dominio`
  - `request.jwt_token`
  - `request.jwt_refreshed_token`
- devuelve `401` consistente cuando el token falta, expiro o es invalido;
- devuelve `403` consistente cuando la vista o la capa de autorizacion detectan falta de permisos.

### 1.2 Capa compartida de autorizacion por alcance

Se incorporo una capa comun para centralizar reglas de autorizacion del dominio.

Archivo principal:

- `backend/shared/auth.py`

Helpers agregados:

- `get_request_user`
- `is_superusuario`
- `get_accessible_consorcios`
- `get_accessible_consorcio_ids`
- `ensure_consorcio_access`
- `filter_queryset_by_consorcios`
- `filter_propietarios_queryset`
- `ensure_propietario_access`
- `filter_proveedores_queryset`
- `ensure_proveedor_access`

Regla consolidada:

- `superusuario` puede ver y operar sobre todo;
- `administrador` solo puede ver y operar sobre los consorcios vinculados a su cuenta y los recursos relacionados a esos consorcios.

### 1.3 Registro de usuarios restringido a superusuario

El endpoint de registro dejo de ser publico.

Archivo principal:

- `backend/usuarios/views.py`

Nuevo comportamiento:

- `POST /api/usuarios/registrar/` ahora requiere JWT valido;
- ademas valida que el usuario autenticado tenga rol `superusuario`;
- un usuario sin token recibe `401`;
- un usuario autenticado sin permisos suficientes recibe `403`.

## 2. Restriccion de acceso por rol en modulos del dominio

Se aplico control de acceso en los principales modulos operativos para que los administradores trabajen solo dentro de su alcance.

### 2.1 Consorcios

Archivo principal:

- `backend/consorcios/views.py`

Cambios relevantes:

- listado filtrado por consorcios accesibles;
- lectura, actualizacion y borrado con chequeo explicito de acceso;
- si el usuario no es `superusuario`, la creacion y actualizacion quedan ligadas a su propio `usuario_id`;
- la subida de imagen del consorcio tambien queda protegida por autorizacion.

### 2.2 Unidades funcionales

Archivo principal:

- `backend/unidades_funcionales/views.py`

Cambios relevantes:

- CRUD protegido por acceso al consorcio asociado;
- listados generales y por filtros acotados al alcance del usuario autenticado.

### 2.3 Gastos, pagos y saldos

Archivos principales:

- `backend/gastos/views.py`
- `backend/pagos/views.py`
- `backend/saldo_mensual/views.py`

Cambios relevantes:

- validacion de acceso al consorcio antes de crear o modificar;
- filtro de listados por consorcios accesibles;
- chequeo de alcance en endpoints de archivo, carga y extraccion de gastos;
- chequeo de alcance en lectura y eliminacion.

### 2.4 Caratula y expensas

Archivos principales:

- `backend/caratula/views.py`
- `backend/expensas/views.py`

Cambios relevantes:

- autorizacion sobre el consorcio antes de crear, listar, actualizar o eliminar;
- proteccion adicional sobre templates de expensas asociados a consorcios;
- validacion para evitar liquidar con un template perteneciente a otro consorcio.

### 2.5 Propietarios y proveedores

Archivos principales:

- `backend/propietarios/views.py`
- `backend/proveedores/views.py`

Cambios relevantes:

- los propietarios se filtran por las unidades funcionales y consorcios accesibles;
- los proveedores se filtran por gastos vinculados a consorcios accesibles;
- lectura, actualizacion y borrado quedan sujetos a control de alcance.

### 2.6 Servicios mensuales y reparaciones/mantenimientos

Archivos principales:

- `backend/servicios_mensuales/views.py`
- `backend/reparaciones_mantenimientos/views.py`

Cambios relevantes:

- se extendio la misma logica de alcance aplicada a proveedores;
- los registros asociados a proveedores quedan visibles y editables solo si el usuario tiene acceso al consorcio relacionado.

## 3. Ajuste del acceso publico en Angular

Se simplifico la experiencia publica de autenticacion para dejar visible unicamente el login.

Archivos principales:

- `frontend/src/app/components/organism/login-form.component/login-form.component.html`
- `frontend/src/app/components/organism/login-form.component/login-form.component.ts`
- `frontend/src/app/components/templates/auth-access.component/auth-access.component.html`
- `frontend/src/app/components/templates/auth-access.component/auth-access.component.ts`

Cambios implementados:

- se elimino del acceso publico el toggle entre login y registro;
- se saco el CTA para crear cuenta desde la pantalla publica;
- se mantuvieron en el repo los componentes, templates, forms y servicios de registro para reutilizarlos luego en un panel administrativo;
- se actualizo el copy principal de la hero para presentar mejor el producto.

Copy activo en la pantalla publica:

> Centraliza las liquidaciones de expensas, automatiza el pago a proveedores y lleva el control financiero de todos tus edificios desde una unica plataforma en la nube.

## 4. Normalizacion de respuestas y errores en backend

### 4.1 Nueva capa compartida de respuestas API

Se agrego un modulo comun para estandarizar envelopes JSON y mapping de excepciones.

Archivo principal:

- `backend/shared/api_responses.py`

Helpers agregados:

- `success_response`
- `error_response`
- `extract_validation_errors`
- `invalid_json_response`
- `validation_error_response`
- `exception_response`

Objetivo:

- evitar que cada vista improvise su propio formato;
- reducir respuestas inconsistentes entre modulos;
- mapear mejor `400`, `401`, `403`, `404` y `500`.

### 4.2 Criterio de mapping aplicado

`exception_response` ahora resuelve de forma uniforme:

- `JSONDecodeError` -> `400`
- `ValidationError` -> `400`
- `PermissionDenied` -> `403`
- `ObjectDoesNotExist` -> `404`
- cualquier excepcion inesperada -> `500`

Formato estandar de exito:

```json
{
  "status": "success",
  "message": "...",
  "data": {}
}
```

Formato estandar de error:

```json
{
  "status": "error",
  "message": "...",
  "errors": {}
}
```

### 4.3 Vistas migradas al esquema comun

Se migraron a este esquema las vistas de:

- `usuarios`
- `consorcios`
- `unidades_funcionales`
- `gastos`
- `pagos`
- `saldo_mensual`
- `caratula`
- `expensas`
- `propietarios`
- `proveedores`
- `servicios_mensuales`
- `reparaciones_mantenimientos`

Resultado:

- se eliminaron muchos `except Exception` que devolvian estados incorrectos;
- se redujo el riesgo de devolver `404` cuando en realidad correspondia `403` o `400`;
- todas las vistas criticas quedaron alineadas con el mismo contrato de respuesta.

## 5. Normalizacion de manejo de errores en frontend

### 5.1 Servicio compartido de parsing de errores

Se incorporo una capa comun para interpretar respuestas HTTP del backend.

Archivo principal:

- `frontend/src/app/services/api-error.service.ts`

Capacidades agregadas:

- `extractMessage`
- `extractDetailedMessage`
- `toAppError`
- clase `AppHttpError`

Objetivo:

- evitar parsing manual repetido en componentes;
- aprovechar el envelope comun del backend;
- mostrar mensajes mas utiles al usuario.

### 5.2 Interceptor de autenticacion reforzado

Archivo principal:

- `frontend/src/app/interceptors/auth.interceptor.ts`

Cambios implementados:

- ante `401`, limpia la sesion;
- si la llamada no es de login, redirige automaticamente a `/`;
- convierte el error HTTP crudo a `AppHttpError` para el resto de la app.

### 5.3 Servicios y pantallas migradas

Archivos principales:

- `frontend/src/app/services/auth.service.ts`
- `frontend/src/app/components/pages/consortium-form/consortium-form.ts`
- `frontend/src/app/components/organism/consortium-grid.component/consortium-grid.component.ts`
- `frontend/src/app/components/pages/units/units.ts`
- `frontend/src/app/components/pages/providers/providers.ts`
- `frontend/src/app/components/pages/owners/owners.ts`

Cambios relevantes:

- se reemplazo el parsing manual de `error?.error?.message`;
- se unificaron mensajes enriquecidos con detalles de validacion cuando existen `errors` por campo;
- se mantuvo la UX actual basada en `alert(...)`, pero con mensajes mucho mas fiables y coherentes con el backend.

## 6. Ajustes de pruebas

Se reforzaron pruebas de integracion para asegurar el nuevo contrato de seguridad.

Archivos principales:

- `backend/usuarios/tests/integration/test_03_integration_registro_usuario.py`
- `backend/consorcios/tests/integration/test_03_integration_consorcio_crud.py`

Cobertura agregada o actualizada:

- registro de usuario con JWT de superusuario;
- rechazo con `401` cuando se intenta registrar sin autenticacion;
- CRUD de consorcios usando JWT valido;
- rechazo con `401` cuando se intenta acceder a consorcios sin autenticacion.

## 7. Validaciones ejecutadas

Validaciones confirmadas durante esta etapa:

- backend:
  - `python manage.py test usuarios.tests consorcios.tests`
- frontend:
  - `npm run build`

Resultado:

- tests backend: OK, 29 pruebas pasando;
- build Angular: OK.

## 8. Estado funcional al cierre

Al cierre de esta iteracion:

- toda la API de negocio relevante exige autenticacion JWT;
- el alcance del usuario ya no depende de la UI, sino de validaciones reales en backend;
- el rol del usuario sigue viajando dentro del JWT y se usa para determinar alcance operativo;
- el acceso publico del frontend queda reducido a login;
- los errores HTTP son mucho mas consistentes en codigo de estado y formato JSON;
- varias pantallas Angular ya consumen una capa centralizada de parsing de errores.

## 9. Pendientes naturales para la siguiente iteracion

Quedan como pasos logicos posteriores:

- migrar las pantallas Angular restantes que todavia usen parsing manual o `alert(...)` directo;
- ampliar pruebas especificas de contratos `403` por alcance para modulos adicionales;
- eventualmente mover el alta de usuarios al futuro panel administrativo de superusuario usando el flujo de registro ya preservado.

## Commit message sugerido

```text
feat(auth): enforce global JWT scope and normalize API/frontend errors

- add global JWT middleware for /api routes and attach domain user to requests
- centralize backend authorization helpers for consorcio, propietario and proveedor scope
- restrict user registration to authenticated superusers
- enforce role-based access across consorcios, unidades, gastos, pagos, saldos, caratula, expensas, propietarios, proveedores and related modules
- simplify public auth screen to login-only while preserving register artifacts for future admin UI
- add shared backend API response helpers with reliable 400/403/404/500 mapping
- normalize auth and domain views to use common success/error envelopes
- add shared frontend ApiErrorService and typed AppHttpError handling
- update auth interceptor to clear session and redirect on unauthorized protected requests
- refactor key Angular pages to use centralized detailed error parsing
- update integration tests for authenticated registration and protected consorcio endpoints
```