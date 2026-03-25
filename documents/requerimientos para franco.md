# 📋 Requerimientos Técnicos - Demo Final Consorcio360

**De:** Valentino (Dev Lead)  
**Para:** Franco (Backend & Automation)  
**Proyecto:** Infraestructura HostSV (haizaraf.duckdns.org)

---

## 1. 🤖 Refactorización: Workflow de Gastos (n8n)
El flujo actual basado en Gmail debe convertirse en un microservicio síncrono para la App.

- [ ] **Cambio de Trigger:** Reemplazar `Gmail Trigger` por un nodo **Webhook** (`POST`).
- [ ] **Input:** El webhook debe recibir un archivo binario (Imagen/PDF de la factura).
- [ ] **Lógica:** Mantener la integración con **Gemini 2.5 Flash** para la extracción de datos.
- [ ] **HTTP Response:** Configurar el nodo de respuesta para que devuelva un **JSON** con los datos extraídos (`cuit_proveedor`, `monto`, `periodo`, etc.).
- [ ] **Objetivo:** Permitir que la App envíe la factura y reciba los datos para mostrar en pantalla antes de guardar.

## 2. 📧 Nuevo Workflow: Emisión de Recibos
Automatizar la notificación legal al propietario tras un pago.

- [ ] **Trigger:** Crear un Webhook `POST` que reciba: `dni_propietario`, `monto` y `id_unidad`.
- [ ] **Acciones:**
    1. Consultar el email en la tabla `propietarios`.
    2. Generar un PDF del recibo (puedes usar un nodo HTML a PDF).
    3. Enviar el correo con el adjunto.
- [ ] **Response:** Retornar un `HTTP 200 OK` solo si el mail se envió correctamente.

## 3. 🎨 UX & Frontend (App-Consorcio)
Ajustes visuales necesarios para la presentación de la demo.

- [ ] **Fix de Assets:** Reparar los archivos SVG de los iconos (actualmente rotos en el build).
- [ ] **Lazy Loading:** Implementar carga diferida entre rutas.
- [ ] **Estados de Carga:** Agregar *Skeleton Screens* o *Spinners* mientras se consultan los datos de los consorcios/unidades para evitar saltos visuales.
- [ ] **Build Sync:** Asegurar que los cambios se reflejen en la carpeta `/static_angular/` vinculada al volumen de producción.

---

> 🛡️ **Nota de HostSV Sentinel:** > Franco, revisá la indentación en el `docker-compose.yml` (línea 152, sección de volúmenes de Portainer), detecto un posible error que podría afectar la persistencia si reiniciamos el stack.