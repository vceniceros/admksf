# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Consorcio 360** — A full-stack platform for managing residential buildings and gated communities (consorcios). Handles expense liquidation, payment tracking, unit/owner management, and supplier records.

- **Backend:** Django 5.2 + Python 3.10 + PostgreSQL 16
- **Frontend:** Angular 21 standalone components + Tailwind CSS + Zone.js ~0.15.0
- **Deployment:** Docker + Caddy reverse proxy at `haizaraf.duckdns.org`

---

## Development Commands

### Local Development (Docker)

```bash
docker compose up -d --build    # Build and start all services
docker compose logs -f web      # Stream backend logs
docker compose exec web bash    # Enter backend container shell
docker compose down             # Stop all services
docker compose down -v          # Stop services and delete database volume
```

Or use the interactive CLI:
```bash
./manager.sh
```

### Database Migrations

```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py createsuperuser
```

### Frontend (from `frontend/`)

```bash
npm install
npm run build     # Production build → dist/frontend/browser
npm start         # Dev server on http://localhost:4200
npm test          # Run Vitest unit tests
```

### Backend (from `backend/`)

```bash
python manage.py migrate
python manage.py runserver
python manage.py test
```

### Seeding Data

```bash
python scripts/seed_barrio_los_pinos.py   # Development data
python scripts/seed_staging.py            # Staging data
```

---

## Production Deployment

**Frontend changes require deleting Docker volumes** — without this, Angular assets won't update:

```bash
cd ~/n8n-infra
docker compose down
docker volume rm n8n-infra_static_volume n8n-infra_static_angular_volume n8n-infra_templates_volume
docker compose build app-consorcio
docker compose up -d
```

- Production URL: `https://haizaraf.duckdns.org`
- Internal API port: `127.0.0.1:8001 → 8000`
- Webhook n8n: `https://n8n-haizaraf.duckdns.org/webhook/gastos-app`
- Test consorcio CUIT: `20123456789` (Edificio Central), template ID: `3`

---

## Architecture

### Multi-Stage Docker Build

`Dockerfile` compiles Angular first (Node 22-alpine), then copies built assets into the Django image (Python 3.10-slim). Angular's `dist/frontend/browser/` is served by WhiteNoise as static files.

### SPA Fallback Pattern

Django routes:
- `/api/*` → Django REST views
- `/admin/*` → Django admin
- Everything else → `templates/index.html` (Angular router takes over)

See `backend/backend_core/urls.py` for the `re_path` SPA fallback.

### Backend Module Structure

Each Django app is self-contained (`models.py`, `views.py`, `services.py`, `urls.py`, `migrations/`):

- `consorcios/` — Building/community entities
- `expensas/` — **Core expense liquidation engine** (Builder + Strategy pattern)
- `gastos/` — Individual expense records
- `pagos/` — Payment transactions
- `propietarios/` — Owners/residents
- `unidades_funcionales/` — Individual apartments/units
- `proveedores/` — Service providers/vendors
- `saldo_mensual/` — Monthly balance snapshots
- `caratula/` — Invoice/statement generation
- `servicios_mensuales/` — Monthly recurring services
- `reparaciones_mantenimientos/` — Repairs & maintenance
- `shared/middleware/webhook_auth.py` — Token auth for n8n webhooks

### Expense Liquidation Engine (`backend/expensas/`)

The most complex module. Uses **Builder + Strategy patterns**:

- `builder.py` — `LiquidacionBuilder` orchestrates the calculation pipeline
- `strategies.py` — Pluggable interest strategies (`SimpleInterest`, `CompoundInterest`, `EarlyPayment`) and rounding strategies (`NoRounding`, `StepRounding`, `Ceiling`, `Floor`)
- `utils.py` — `SafeExpressionEvaluator` safely evaluates user-defined formulas

Flow: `ExpensaTemplate.config` → `LiquidacionBuilder` → iterate `UnidadFuncional` → apply strategies → accumulate totals → JSON response via `POST /api/liquidar/`

### Frontend Component Architecture

Follows **Atomic Design**:
- `atoms/` — Buttons, inputs, labels, icons
- `molecules/` — Cards, buttons-with-icons
- `organism/` — Navbar, sidebar, footer
- `pages/` — Full-page views
- `templates/` — Layout wrappers

All components are **standalone** (no NgModules) — each declares its own `imports: [...]`.

---

## Critical Rules

### TypeScript Types

```typescript
// CUIT always as string — 11 digits exceeds Number.MAX_SAFE_INTEGER
CUIT: string  // NEVER number
DNI: string   // NEVER number

// Payment status literals
PaymentStatus: 'Aprobado' | 'Pendiente' | 'Parcial'
EstadoPago = { APROBADO: 'Aprobado', PENDIENTE: 'Pendiente', PARCIAL: 'Parcial' }
```

### Angular Pipe Injection (Known Gotchas)

```typescript
// NEVER — causes errors in standalone pipes:
inject(CurrencyPipe)
inject(DatePipe)
inject(DecimalPipe)

// ALWAYS use instead:
import { formatCurrency, formatDate, formatNumber } from '@angular/common'
// + inject(LOCALE_ID) where needed
```

Before changing a field type in a shared model, run:
```bash
grep -rn "fieldName" frontend/src --include="*.ts" --include="*.html"
```

### General

- Read relevant files before proposing changes.
- When debugging: check logs first, never guess.
- Never modify production data directly.

---

## 9 Directivas de Trabajo

1. Planificar antes de escribir código: si la tarea tiene varios pasos, usar /plan para explorar escenarios y definir el enfoque.
2. Si algo empieza a salir mal, parar y replantear: seguir pusheando cambios sobre algo mal diseñado casi siempre empeora el resultado.
3. Usar subagentes para investigación: leer código, explorar el repo o revisar docs en paralelo mantiene limpio el contexto principal.
4. Una ejecución = un objetivo claro: si mezclás muchas cosas en la misma tarea, el agente pierde foco.
5. No cerrar algo sin probarlo: correr tests, mirar logs y revisar el diff antes de decir que terminó.
6. Si corregís algo, guardalo: documentarlo evita que el agente repita el mismo error en el repo.
7. Cuando aparece un error: empezar por logs y stack trace. Muchas veces ahí está el archivo y la línea exacta.
8. Hacer cambios chicos y localizados: tocar solo lo necesario reduce efectos secundarios en el repo.
9. Generar una nueva skill al detectar nuevo conocimiento o patrones recurrentes.

---

## Runbook operativo
Ver `docs/RUNBOOK.md` para procedimientos completos de deploy, backups, staging y troubleshooting.
