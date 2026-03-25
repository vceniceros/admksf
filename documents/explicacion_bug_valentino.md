# Explicación del Bug Visual — Para Valentino

## ¿Qué estaba pasando?

En todas las vistas del sistema (gastos, proveedores, propietarios, etc.) los datos 
no se mostraban al cargar la página. Solo aparecían al abrir DevTools del browser.

## ¿Por qué pasaba?

Angular usa una librería llamada **Zone.js** para detectar automáticamente cuándo 
llegaron datos nuevos y actualizar la pantalla. Sin Zone.js, Angular recibe los datos 
pero no sabe que tiene que redibujar la vista.

El proyecto tenía Zone.js comentado/eliminado (probablemente en un intento de migrar 
a "zoneless mode") pero sin completar la migración correctamente.

Al abrir DevTools, el browser generaba eventos internos que casualmente disparaban 
un ciclo de actualización de Angular — por eso los datos aparecían.

## ¿Qué se cambió?

### 1. package.json — agregar Zone.js como dependencia
```json
"zone.js": "~0.15.0"
```

### 2. angular.json — cargar Zone.js como polyfill
```json
"polyfills": ["zone.js"]
```

### 3. app.config.ts — configurar Zone.js en Angular
```typescript
import { provideZoneChangeDetection } from '@angular/core';

providers: [
  provideZoneChangeDetection({ eventCoalescing: true }),
  provideRouter(routes),
  provideHttpClient()
]
```

### 4. app.routes.server.ts — cambiar renderizado a cliente
```typescript
renderMode: RenderMode.Client  // antes era RenderMode.Server
```

### 5. dashboard.ts — corregir typo en URL
```typescript
// ANTES (roto):
`/api/caratula/consorcio/${this.consortiumId}/`

// DESPUÉS (correcto):
`/api/caratulas/consorcio/${this.consortiumId}/`
```

## ¿Por qué costó tanto encontrarlo?

El problema tuvo dos capas:

**Capa 1 — Código:** Zone.js no estaba configurado.

**Capa 2 — Infraestructura:** Los volúmenes Docker (`templates_volume`, 
`static_angular_volume`, `static_volume`) tenían versiones viejas de los archivos 
compilados. Aunque el código se corregía, los archivos viejos seguían sirviéndose.

La solución final requirió borrar los tres volúmenes y recrearlos:

```bash
docker compose down
docker volume rm n8n-infra_static_volume n8n-infra_static_angular_volume n8n-infra_templates_volume
docker compose build app-consorcio
docker compose up -d
```

## Regla para el futuro

Cada vez que modifiques el frontend y hagas rebuild, ejecutá ese comando completo 
para asegurarte de que los volúmenes se actualicen correctamente.
