# Instrucciones para crear Templates de Expensa

## 1) Introducción: ¿Qué es un Template de Expensa?
Un **Template de Expensa** es como un **molde** o **plantilla** que define qué columnas tendrá tu hoja de expensas todos los meses. Así, podés repetir la misma estructura sin empezar de cero cada vez.

---

## 2) Guía del Formulario de Creación

### ✅ Configuración General
- **Nombre**: escribí un nombre claro que te ayude a reconocerlo, por ejemplo: **“Expensas Mensuales 2026”**.
- **Versión**: usá un número para diferenciar cambios. Por ejemplo, si mejorás la plantilla, podés pasar de **1** a **2**.

### ✅ Reglas Globales (Redondeo)
La **Estrategia de Redondeo** define cómo el sistema ajusta los importes.

Ejemplo:
- Si elegís **Hacia arriba**, entonces **$100.51 pasa a $101.00**.
- Si elegís **Sin redondeo**, el importe queda tal cual.

---

## 3) Configuración de Columnas (La parte difícil)

### ¿Qué es una “Columna”?
Es cada ítem que va a aparecer en tu hoja de expensas: **Saldo anterior**, **Interés**, **Gasto del mes**, **Total**, etc.

### Tipos de Cálculo (explicados simple)
- **Saldo anterior**: trae el saldo del mes pasado.
- **Interés**: calcula un interés sobre un saldo.
- **Prorrateo**: reparte gastos según un coeficiente (por ejemplo, superficie).
- **Concepto particular**: un monto especial para una unidad específica.
- **Monto fijo**: un valor manual que vos definís.
- **Fórmula**: un cálculo matemático combinando otras columnas.

---

## 4) Uso de Claves y Etiquetas (Endpoints Dinámicos)

### ¿Qué es la “Clave de Columna” (id)?
Es el **nombre interno** que usa el sistema para identificar cada columna. Aunque vos ves la **Etiqueta**, el sistema guarda una clave para poder usarla en cálculos.

**Ejemplo simple**:
- Etiqueta: **Saldo anterior**
- Clave interna: **saldo_anterior**

### ¿Cómo hacer fórmulas?
Usá las **llaves `{}`** para sumar o combinar columnas.

Ejemplo:
- Si querés sumar el saldo anterior y el gasto del mes, escribí:
  - **`{saldo_anterior} + {gasto_mes}`**

### ⚠️ Advertencia importante
Las claves deben escribirse **exactamente igual** (respetando mayúsculas y minúsculas). Si la clave no coincide, la fórmula no va a funcionar.

---

## 5) Preguntas Frecuentes

**¿Qué pasa si me equivoco en una fórmula?**
No te preocupes: podés corregirla y volver a guardar el template. Es recomendable probar con una previsualización antes de cerrar la liquidación.

**¿Puedo tener varios templates para el mismo edificio?**
Sí. Podés crear varios templates para un mismo consorcio y elegir el que necesites en cada periodo.
