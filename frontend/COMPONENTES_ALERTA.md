# Componentes de Alerta y Cambio de Estado de Pago

## Átomos

### AlertComponent
Componente de alerta reutilizable que muestra un modal con título, mensaje y botones de acción.

**Ubicación:** `src/app/components/atoms/alert.component/`

**Inputs:**
- `title`: string - Título del alerta
- `message`: string - Mensaje del alerta
- `type`: AlertType - Tipo de alerta (info, warning, error, success)
- `confirmText`: string - Texto del botón confirmar (default: "Aceptar")
- `cancelText`: string - Texto del botón cancelar (default: "Cancelar")
- `isOpen`: boolean - Si el alerta está visible

**Outputs:**
- `confirm`: EventEmitter<void> - Se emite al confirmar
- `cancel`: EventEmitter<void> - Se emite al cancelar

**Uso:**
```typescript
<app-alert 
  [isOpen]="showAlert"
  title="Título"
  message="Mensaje"
  confirmText="Confirmar"
  cancelText="Cancelar"
  type="AlertType.WARNING"
  (confirm)="onConfirm()"
  (cancel)="onCancel()">
</app-alert>
```

## Moléculas

### PaymentStatusToggleComponent
Molécula que maneja el cambio de estado de pago de un gasto con confirmación por alerta.

**Ubicación:** `src/app/components/molecules/payment-status-toggle.component/`

**Inputs:**
- `spend`: Spend - Objeto del gasto a modificar

**Outputs:**
- `statusChanged`: EventEmitter<{ spend: Spend; newStatus: EstadoPago }> - Se emite cuando se confirma el cambio

**Funcionalidades:**
- Click en el badge de estado muestra un alerta de confirmación
- Alerta diferente si es cambio de Pendiente a Pagado o viceversa
- Al confirmar emite el evento con el nuevo estado
- Los estados cambian entre Pendiente y Pagado (toggle)

**Uso:**
```typescript
<app-payment-status-toggle 
  [spend]="spend"
  (statusChanged)="onStatusChanged($event)">
</app-payment-status-toggle>
```

## Servicio

### SpendsService - updateSpendStatus()
Nuevo método en el servicio de gastos para actualizar el estado de pago.

**Método:**
```typescript
updateSpendStatus(spend: Spend, newStatus: EstadoPago): Observable<Spend>
```

**Descripción:**
- Actualiza el estado de un gasto
- Por ahora funciona en memoria (localSpends)
- Preparado para llamada a backend: `POST /api/gastos/{idGasto}/status`
- Retorna Observable del gasto actualizado

**Implementación en Backend:**
```
POST /api/gastos/{idGasto}/status
Body: { estadoPago: "Pagado" | "Pendiente" }
Response: Spend (actualizado)
```

## Flujo de Interacción

1. Usuario hace clic en el badge de estado del pago en la tabla
2. Se muestra el alerta con el mensaje correspondiente
3. Usuario puede confirmar o cancelar
4. Si confirma:
   - Se llama a `updateSpendStatus()` del servicio
   - Se recibe el gasto actualizado
   - Se actualiza la tabla y se recalculan los balances
   - El toggle vuelve al estado neutral (cerrado)
5. Si cancela:
   - El alerta se cierra
   - No hay cambios

## Estilos

Los componentes incluyen:
- Animación de entrada suave para el alerta
- Hover effects interactivos
- Colores diferenciados (warning para pagos, verde para pagado, naranja para pendiente)
- Responsive design
- Accesibilidad básica

