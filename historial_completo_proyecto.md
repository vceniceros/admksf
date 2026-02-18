# Documentación Viva del Proyecto (Basada en Git Log)
> Generado automáticamente para análisis de IA.

## Commit: fb68522
**Fecha:** Tue Feb 17 21:56:57 2026 -0300
**Mensaje:** se agrega un menu de cargar templates de expensas, los endpoints dinamicos correspondientes usando patron strategy y builder para la creacion de las mismas

#### 📄 `backend/backend_core/settings.py`
```python
commit fb68522b36d3c2da79593d6a5f05473d934119e7
Author: Valentino <vceniceros2001@gmail.com>
Date:   Tue Feb 17 21:56:57 2026 -0300

    se agrega un menu de cargar templates de expensas, los endpoints dinamicos correspondientes usando patron strategy y builder para la creacion de las mismas

--- a/backend/backend_core/settings.py
+++ b/backend/backend_core/settings.py
@@ -50,6 +50,7 @@ INSTALLED_APPS = [
     'saldo_mensual',
     'pagos',
     'caratula',
+    'expensas',
 ]
 
 MIDDLEWARE = [
```

#### 📄 `backend/backend_core/urls.py`
```python
commit fb68522b36d3c2da79593d6a5f05473d934119e7
Author: Valentino <vceniceros2001@gmail.com>
Date:   Tue Feb 17 21:56:57 2026 -0300

    se agrega un menu de cargar templates de expensas, los endpoints dinamicos correspondientes usando patron strategy y builder para la creacion de las mismas

--- a/backend/backend_core/urls.py
+++ b/backend/backend_core/urls.py
@@ -20,6 +20,8 @@ from django.conf import settings
 from django.conf.urls.static import static
 from django.views.generic import TemplateView
 
+from expensas import views as expensas_views
+
 urlpatterns = [
     path('admin/', admin.site.urls),
     path('', TemplateView.as_view(template_name='index.html'), name='frontend'),
@@ -33,6 +35,8 @@ urlpatterns = [
     path('api/caratulas/', include('caratula.urls')),
     path('api/reparaciones-mantenimientos/', include('reparaciones_mantenimientos.urls')),
     path('api/servicios-mensuales/', include('servicios_mensuales.urls')),
+    path('api/expensas/', include('expensas.urls')),
+    path('api/liquidar/', expensas_views.liquidar_expensa),
     re_path(r'^(?!api/|admin/).*$' , TemplateView.as_view(template_name='index.html'), name='spa-fallback'),
 ]
```

#### 📄 `backend/expensas/__init__.py`
```python
commit fb68522b36d3c2da79593d6a5f05473d934119e7
Author: Valentino <vceniceros2001@gmail.com>
Date:   Tue Feb 17 21:56:57 2026 -0300

    se agrega un menu de cargar templates de expensas, los endpoints dinamicos correspondientes usando patron strategy y builder para la creacion de las mismas

new file mode 100644
--- /dev/null
+++ b/backend/expensas/__init__.py
@@ -0,0 +1,5 @@
+"""App de expensas y motor de liquidación.
+
+Fecha:
+    14 - 02 - 2026
+"""
```

#### 📄 `backend/expensas/apps.py`
```python
commit fb68522b36d3c2da79593d6a5f05473d934119e7
Author: Valentino <vceniceros2001@gmail.com>
Date:   Tue Feb 17 21:56:57 2026 -0300

    se agrega un menu de cargar templates de expensas, los endpoints dinamicos correspondientes usando patron strategy y builder para la creacion de las mismas

new file mode 100644
--- /dev/null
+++ b/backend/expensas/apps.py
@@ -0,0 +1,14 @@
+"""Configuración de la app expensas.
+
+Fecha:
+    14 - 02 - 2026
+"""
+
+from django.apps import AppConfig
+
+
+class ExpensasConfig(AppConfig):
+    """Configuración de la app expensas."""
+
+    default_auto_field = "django.db.models.BigAutoField"
+    name = "expensas"
```

#### 📄 `backend/expensas/builder.py`
```python
commit fb68522b36d3c2da79593d6a5f05473d934119e7
Author: Valentino <vceniceros2001@gmail.com>
Date:   Tue Feb 17 21:56:57 2026 -0300

    se agrega un menu de cargar templates de expensas, los endpoints dinamicos correspondientes usando patron strategy y builder para la creacion de las mismas

new file mode 100644
--- /dev/null
+++ b/backend/expensas/builder.py
@@ -0,0 +1,244 @@
+"""Builder de la liquidación de expensas.
+
+Fecha:
+    14 - 02 - 2026
+"""
+
+from __future__ import annotations
+
+from dataclasses import dataclass
+from decimal import Decimal
+from typing import Any, Dict, Iterable, List, Mapping
+
+from django.core.exceptions import ValidationError
+
+from consorcios.models import Consorcio
+from gastos.models import Gasto
+from saldo_mensual.models import SaldoMensual
+from unidades_funcionales.models import UnidadFuncional
+
+from .strategies import (
+    CompoundInterestStrategy,
+    EarlyPaymentStrategy,
+    NoRoundingStrategy,
+    RoundingStrategy,
+    SimpleInterestStrategy,
+    StepRoundingStrategy,
+    CeilingRoundingStrategy,
+    FloorRoundingStrategy,
+)
+from .utils import evaluate_expression, parse_decimal
+
+
+@dataclass
+class ColumnResult:
+    """Representa el resultado de una columna para una UF."""
+
+    column_id: str
+    value: Decimal
+
+
+class LiquidacionBuilder:
+    """Construye el resultado de una liquidación con base en metadata."""
+
+    def __init__(
+        self,
+        consorcio: Consorcio,
+        periodo,
+        template_config: Mapping[str, Any],
+        parametros: Mapping[str, Any] | None = None,
+    ) -> None:
+        self.consorcio = consorcio
+        self.periodo = periodo
+        self.template_config = template_config
+        self.parametros = parametros or {}
+        self.columns = list(self.template_config.get("columns", []))
+
+        self._conceptos_particulares = self._build_conceptos_particulares()
+        self._custom_coeficientes = self.parametros.get("coeficientes_custom", {})
+        self._rounding_strategy = self._build_rounding_strategy()
+
+    def build(self) -> Dict[str, Any]:
+        """Ejecuta el proceso de liquidación y devuelve el JSON final."""
+
+        unidades = list(
+            UnidadFuncional.objects.filter(consorcio=self.consorcio).select_related("propietario")
+        )
+        total_superficie = sum((uf.superficie for uf in unidades), Decimal("0"))
+        gastos_por_tipo, total_gastos = self._aggregate_gastos()
+
+        resultados_unidades = []
+        totales_columnas: Dict[str, Decimal] = {col["id"]: Decimal("0") for col in self.columns}
+
+        for uf in unidades:
+            coef_superficie = (
+                (uf.superficie / total_superficie) if total_superficie else Decimal("0")
+            )
+            context: Dict[str, Decimal] = {
+                "coeficiente": coef_superficie,
+                "coeficiente_superficie": coef_superficie,
+                "saldo_anterior": self._get_saldo_anterior(uf),
+            }
+            valores: Dict[str, Decimal] = {}
+
+            for column in self.columns:
+                col_id = column.get("id")
+                calc_type = column.get("calc_type") or column.get("tipo_calculo")
+                if not col_id or not calc_type:
+                    raise ValidationError("Columna inválida: falta id o tipo de cálculo.")
+                value = self._calculate_column(
+                    column,
+                    calc_type,
+                    context,
+                    gastos_por_tipo,
+                    total_gastos,
+                    uf.numero_de_unidad_funcional,
+                )
+                if column.get("apply_rounding", False):
+                    value = self._rounding_strategy.apply(value)
+                value = value.quantize(Decimal("0.01"))
+                valores[col_id] = value
+                context[col_id] = value
+                totales_columnas[col_id] += value
+
+            resultados_unidades.appe
... (truncado) ...
```

#### 📄 `backend/expensas/migrations/0001_initial.py`
```python
commit fb68522b36d3c2da79593d6a5f05473d934119e7
Author: Valentino <vceniceros2001@gmail.com>
Date:   Tue Feb 17 21:56:57 2026 -0300

    se agrega un menu de cargar templates de expensas, los endpoints dinamicos correspondientes usando patron strategy y builder para la creacion de las mismas

new file mode 100644
--- /dev/null
+++ b/backend/expensas/migrations/0001_initial.py
@@ -0,0 +1,156 @@
+"""Migración inicial de expensas.
+
+Resumen:
+    Crea templates, reglas y liquidaciones de expensas.
+
+Fecha:
+    14 - 02 - 2026
+"""
+
+from django.db import migrations, models
+import django.db.models.deletion
+
+
+class Migration(migrations.Migration):
+    """Migración inicial para la app expensas."""
+
+    initial = True
+
+    dependencies = [
+        ("consorcios", "0001_initial"),
+    ]
+
+    operations = [
+        migrations.CreateModel(
+            name="ExpensaTemplate",
+            fields=[
+                (
+                    "id_expensa_template",
+                    models.BigAutoField(
+                        db_column="id_expensa_template",
+                        primary_key=True,
+                        serialize=False,
+                    ),
+                ),
+                ("nombre", models.CharField(db_column="nombre", max_length=120)),
+                ("version", models.PositiveIntegerField(db_column="version", default=1)),
+                ("config", models.JSONField(db_column="config")),
+                ("activo", models.BooleanField(db_column="activo", default=True)),
+                (
+                    "creado_en",
+                    models.DateTimeField(auto_now_add=True, db_column="creado_en"),
+                ),
+                (
+                    "consorcio",
+                    models.ForeignKey(
+                        blank=True,
+                        db_column="cuit_consorcio",
+                        null=True,
+                        on_delete=django.db.models.deletion.CASCADE,
+                        to="consorcios.consorcio",
+                        to_field="cuit",
+                    ),
+                ),
+            ],
+            options={
+                "db_table": "expensa_templates",
+                "verbose_name": "Template de expensa",
+                "verbose_name_plural": "Templates de expensa",
+                "constraints": [
+                    models.UniqueConstraint(
+                        fields=("consorcio", "nombre", "version"),
+                        name="expensa_template_consorcio_nombre_version_unique",
+                    )
+                ],
+            },
+        ),
+        migrations.CreateModel(
+            name="ExpensaRule",
+            fields=[
+                (
+                    "id_expensa_rule",
+                    models.BigAutoField(
+                        db_column="id_expensa_rule",
+                        primary_key=True,
+                        serialize=False,
+                    ),
+                ),
+                ("nombre", models.CharField(db_column="nombre", max_length=120)),
+                (
+                    "tipo",
+                    models.CharField(
+                        choices=[("Prorrateo", "Prorrateo"), ("Interes", "Interés"), ("Redondeo", "Redondeo")],
+                        db_column="tipo",
+                        max_length=20,
+                    ),
+                ),
+                ("config", models.JSONField(db_column="config")),
+                ("orden", models.PositiveIntegerField(db_column="orden", default=0)),
+                (
+                    "template",
+                    models.ForeignKey(
+                        db_column="id_expensa_template",
+                        on_delete=django.db.models.deletion.CASCADE,
+                        related_name="rules",
+                        to="expensas.expensatemplate",
+                    ),
+                ),
+            ],
+            options={
+                "db_table": 
... (truncado) ...
```

#### 📄 `backend/expensas/migrations/__init__.py`
```python
commit fb68522b36d3c2da79593d6a5f05473d934119e7
Author: Valentino <vceniceros2001@gmail.com>
Date:   Tue Feb 17 21:56:57 2026 -0300

    se agrega un menu de cargar templates de expensas, los endpoints dinamicos correspondientes usando patron strategy y builder para la creacion de las mismas

new file mode 100644
```

#### 📄 `backend/expensas/models.py`
```python
commit fb68522b36d3c2da79593d6a5f05473d934119e7
Author: Valentino <vceniceros2001@gmail.com>
Date:   Tue Feb 17 21:56:57 2026 -0300

    se agrega un menu de cargar templates de expensas, los endpoints dinamicos correspondientes usando patron strategy y builder para la creacion de las mismas

new file mode 100644
--- /dev/null
+++ b/backend/expensas/models.py
@@ -0,0 +1,154 @@
+"""Modelos de la app expensas.
+
+Fecha:
+    14 - 02 - 2026
+"""
+
+from django.db import models
+
+from shared import build_model_str
+
+
+class RuleType(models.TextChoices):
+    """Tipos de reglas permitidas en un template de expensas."""
+
+    PRORRATEO = "Prorrateo", "Prorrateo"
+    INTERES = "Interes", "Interés"
+    REDONDEO = "Redondeo", "Redondeo"
+
+
+class ExpensaTemplate(models.Model):
+    """Representa un template de liquidación de expensas basado en metadata."""
+
+    id_expensa_template = models.BigAutoField(
+        primary_key=True,
+        db_column="id_expensa_template",
+    )
+    consorcio = models.ForeignKey(
+        "consorcios.Consorcio",
+        on_delete=models.CASCADE,
+        db_column="cuit_consorcio",
+        to_field="cuit",
+        null=True,
+        blank=True,
+    )
+    nombre = models.CharField(max_length=120, db_column="nombre")
+    version = models.PositiveIntegerField(db_column="version", default=1)
+    config = models.JSONField(db_column="config")
+    activo = models.BooleanField(db_column="activo", default=True)
+    creado_en = models.DateTimeField(db_column="creado_en", auto_now_add=True)
+
+    class Meta:
+        db_table = "expensa_templates"
+        verbose_name = "Template de expensa"
+        verbose_name_plural = "Templates de expensa"
+        constraints = [
+            models.UniqueConstraint(
+                fields=["consorcio", "nombre", "version"],
+                name="expensa_template_consorcio_nombre_version_unique",
+            )
+        ]
+
+    def __str__(self) -> str:
+        return build_model_str(
+            "ExpensaTemplate",
+            [
+                ("id_expensa_template", self.id_expensa_template, False),
+                ("cuit_consorcio", self.consorcio_id, True),
+                ("nombre", self.nombre, False),
+                ("version", self.version, False),
+                ("activo", self.activo, False),
+                ("creado_en", self.creado_en, False),
+            ],
+        )
+
+
+class ExpensaRule(models.Model):
+    """Reglas asociadas a un template de expensa."""
+
+    id_expensa_rule = models.BigAutoField(
+        primary_key=True,
+        db_column="id_expensa_rule",
+    )
+    template = models.ForeignKey(
+        ExpensaTemplate,
+        on_delete=models.CASCADE,
+        related_name="rules",
+        db_column="id_expensa_template",
+    )
+    nombre = models.CharField(max_length=120, db_column="nombre")
+    tipo = models.CharField(
+        max_length=20,
+        choices=RuleType.choices,
+        db_column="tipo",
+    )
+    config = models.JSONField(db_column="config")
+    orden = models.PositiveIntegerField(db_column="orden", default=0)
+
+    class Meta:
+        db_table = "expensa_rules"
+        verbose_name = "Regla de expensa"
+        verbose_name_plural = "Reglas de expensa"
+        constraints = [
+            models.CheckConstraint(
+                condition=models.Q(tipo__in=list(RuleType.values)),
+                name="expensa_rules_tipo_valido",
+            )
+        ]
+
+    def __str__(self) -> str:
+        return build_model_str(
+            "ExpensaRule",
+            [
+                ("id_expensa_rule", self.id_expensa_rule, False),
+                ("id_expensa_template", self.template_id, False),
+                ("nombre", self.nombre, False),
+                ("tipo", self.tipo, False),
+                ("orden", self.orden, False),
+            ],
+        )
+
+
+class LiquidacionExpensa(models.Model):
+    """Resultado inmutable de una liquidación de expensas."""
+
+    id_liqui
... (truncado) ...
```

#### 📄 `backend/expensas/services.py`
```python
commit fb68522b36d3c2da79593d6a5f05473d934119e7
Author: Valentino <vceniceros2001@gmail.com>
Date:   Tue Feb 17 21:56:57 2026 -0300

    se agrega un menu de cargar templates de expensas, los endpoints dinamicos correspondientes usando patron strategy y builder para la creacion de las mismas

new file mode 100644
--- /dev/null
+++ b/backend/expensas/services.py
@@ -0,0 +1,56 @@
+"""Servicios para el motor de expensas.
+
+Fecha:
+    14 - 02 - 2026
+"""
+
+from __future__ import annotations
+
+from django.core.exceptions import ValidationError
+
+from consorcios.models import Consorcio
+
+from .builder import LiquidacionBuilder
+from .models import ExpensaTemplate, LiquidacionExpensa
+from .utils import parse_period
+
+
+class LiquidacionService:
+    """Servicio principal para liquidar expensas."""
+
+    @staticmethod
+    def liquidar(payload: dict) -> dict:
+        """Ejecuta la liquidación con base en un template y parámetros."""
+
+        try:
+            template_id = payload.get("template_id")
+            consorcio_cuit = payload.get("consorcio")
+            periodo_raw = payload.get("periodo")
+            cerrar = payload.get("cerrar", False)
+            parametros = payload.get("parametros", {})
+
+            if not template_id or not consorcio_cuit or not periodo_raw:
+                raise ValidationError("template_id, consorcio y periodo son obligatorios.")
+
+            template = ExpensaTemplate.objects.get(pk=template_id)
+            consorcio = Consorcio.objects.get(pk=consorcio_cuit)
+            periodo = parse_period(periodo_raw)
+
+            builder = LiquidacionBuilder(consorcio, periodo, template.config, parametros)
+            resultado = builder.build()
+            resultado["template_id"] = template_id
+
+            if cerrar:
+                LiquidacionExpensa.objects.create(
+                    consorcio=consorcio,
+                    template=template,
+                    periodo=periodo,
+                    resultado=resultado,
+                    template_snapshot=template.config,
+                    cerrada=True,
+                )
+            return resultado
+        except ExpensaTemplate.DoesNotExist as exc:
+            raise ValidationError("Template no encontrado.") from exc
+        except Consorcio.DoesNotExist as exc:
+            raise ValidationError("Consorcio no encontrado.") from exc
```

#### 📄 `backend/expensas/strategies.py`
```python
commit fb68522b36d3c2da79593d6a5f05473d934119e7
Author: Valentino <vceniceros2001@gmail.com>
Date:   Tue Feb 17 21:56:57 2026 -0300

    se agrega un menu de cargar templates de expensas, los endpoints dinamicos correspondientes usando patron strategy y builder para la creacion de las mismas

new file mode 100644
--- /dev/null
+++ b/backend/expensas/strategies.py
@@ -0,0 +1,88 @@
+"""Estrategias de cálculo para el motor de expensas.
+
+Fecha:
+    14 - 02 - 2026
+"""
+
+from __future__ import annotations
+
+from abc import ABC, abstractmethod
+from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR
+
+
+class InterestStrategy(ABC):
+    """Interfaz base para estrategias de interés."""
+
+    @abstractmethod
+    def calculate(self, base: Decimal, rate: Decimal, periods: int = 1) -> Decimal:
+        """Calcula interés sobre un capital base."""
+
+
+class SimpleInterestStrategy(InterestStrategy):
+    """Interés simple: base * tasa% * periodos."""
+
+    def calculate(self, base: Decimal, rate: Decimal, periods: int = 1) -> Decimal:
+        if base <= 0 or rate <= 0:
+            return Decimal("0")
+        return (base * rate * Decimal(periods) / Decimal("100"))
+
+
+class CompoundInterestStrategy(InterestStrategy):
+    """Interés compuesto: base * ((1 + tasa%)^periodos - 1)."""
+
+    def calculate(self, base: Decimal, rate: Decimal, periods: int = 1) -> Decimal:
+        if base <= 0 or rate <= 0:
+            return Decimal("0")
+        factor = (Decimal("1") + (rate / Decimal("100"))) ** Decimal(periods)
+        return base * (factor - Decimal("1"))
+
+
+class EarlyPaymentStrategy(InterestStrategy):
+    """Pronto pago: se aplica como descuento (interés negativo)."""
+
+    def calculate(self, base: Decimal, rate: Decimal, periods: int = 1) -> Decimal:
+        if base <= 0 or rate <= 0:
+            return Decimal("0")
+        return -(base * rate * Decimal(periods) / Decimal("100"))
+
+
+class RoundingStrategy(ABC):
+    """Interfaz base para estrategias de redondeo."""
+
+    @abstractmethod
+    def apply(self, value: Decimal) -> Decimal:
+        """Aplica redondeo al valor recibido."""
+
+
+class NoRoundingStrategy(RoundingStrategy):
+    """Sin redondeo."""
+
+    def apply(self, value: Decimal) -> Decimal:
+        return value
+
+
+class StepRoundingStrategy(RoundingStrategy):
+    """Redondea al múltiplo más cercano de un incremento."""
+
+    def __init__(self, increment: Decimal) -> None:
+        self.increment = increment
+
+    def apply(self, value: Decimal) -> Decimal:
+        if self.increment == 0:
+            return value
+        quotient = (value / self.increment).quantize(Decimal("1"))
+        return quotient * self.increment
+
+
+class CeilingRoundingStrategy(RoundingStrategy):
+    """Redondea hacia arriba a 2 decimales."""
+
+    def apply(self, value: Decimal) -> Decimal:
+        return value.quantize(Decimal("0.01"), rounding=ROUND_CEILING)
+
+
+class FloorRoundingStrategy(RoundingStrategy):
+    """Redondea hacia abajo a 2 decimales."""
+
+    def apply(self, value: Decimal) -> Decimal:
+        return value.quantize(Decimal("0.01"), rounding=ROUND_FLOOR)
```

#### 📄 `backend/expensas/tests/__init__.py`
```python
commit fb68522b36d3c2da79593d6a5f05473d934119e7
Author: Valentino <vceniceros2001@gmail.com>
Date:   Tue Feb 17 21:56:57 2026 -0300

    se agrega un menu de cargar templates de expensas, los endpoints dinamicos correspondientes usando patron strategy y builder para la creacion de las mismas

new file mode 100644
```

#### 📄 `backend/expensas/tests/integration/__init__.py`
```python
commit fb68522b36d3c2da79593d6a5f05473d934119e7
Author: Valentino <vceniceros2001@gmail.com>
Date:   Tue Feb 17 21:56:57 2026 -0300

    se agrega un menu de cargar templates de expensas, los endpoints dinamicos correspondientes usando patron strategy y builder para la creacion de las mismas

new file mode 100644
```

#### 📄 `backend/expensas/tests/integration/test_03_integration_liquidacion.py`
```python
commit fb68522b36d3c2da79593d6a5f05473d934119e7
Author: Valentino <vceniceros2001@gmail.com>
Date:   Tue Feb 17 21:56:57 2026 -0300

    se agrega un menu de cargar templates de expensas, los endpoints dinamicos correspondientes usando patron strategy y builder para la creacion de las mismas

new file mode 100644
--- /dev/null
+++ b/backend/expensas/tests/integration/test_03_integration_liquidacion.py
@@ -0,0 +1,150 @@
+import json
+from datetime import date
+from decimal import Decimal
+
+from django.test import TestCase
+
+from consorcios.models import Consorcio
+from propietarios.models import Propietario
+from proveedores.models import Proveedor, TipoProveedor
+from unidades_funcionales.models import UnidadFuncional, TipoUnidad, EstadoVivienda
+from gastos.models import Gasto, TipoGasto
+from saldo_mensual.models import SaldoMensual
+
+from expensas.models import ExpensaTemplate, LiquidacionExpensa
+
+
+class TestLiquidacionIntegration(TestCase):
+    def test_01_flujo_completo_liquidacion(self):
+        consorcio = Consorcio.objects.create(
+            cuit="20304050607",
+            razon_social="Consorcio Test",
+            calle="Av Siempre Viva",
+            numero=123,
+            codigo_postal="1000",
+            ciudad="CABA",
+            interes_por_mora=Decimal("1.50"),
+            redondeo_aumento=Decimal("0.50"),
+        )
+        propietario = Propietario.objects.create(
+            dni="12345678",
+            nombre="Juan",
+            apellido="Perez",
+        )
+        UnidadFuncional.objects.create(
+            numero_de_unidad_funcional=1,
+            consorcio=consorcio,
+            tipo_de_unidad=TipoUnidad.DEPARTAMENTO,
+            estado_de_vivienda=EstadoVivienda.PROPIETARIO,
+            superficie=Decimal("60"),
+            propietario=propietario,
+        )
+        UnidadFuncional.objects.create(
+            numero_de_unidad_funcional=2,
+            consorcio=consorcio,
+            tipo_de_unidad=TipoUnidad.DEPARTAMENTO,
+            estado_de_vivienda=EstadoVivienda.PROPIETARIO,
+            superficie=Decimal("40"),
+            propietario=propietario,
+        )
+        proveedor = Proveedor.objects.create(
+            cuit="20304050608",
+            razon_social="Proveedor Test",
+            telefono="123456",
+            email="proveedor@test.com",
+            calle="Av Test",
+            numero=10,
+            codigo_postal="1000",
+            ciudad="CABA",
+            tipo_proveedor=TipoProveedor.SERVICIOS_MENSUALES,
+        )
+        Gasto.objects.create(
+            consorcio=consorcio,
+            proveedor=proveedor,
+            periodo=date(2026, 2, 1),
+            descripcion="Mantenimiento",
+            monto=Decimal("100.00"),
+            tipo_gasto=TipoGasto.MANTENIMIENTO,
+        )
+        SaldoMensual.objects.create(
+            numero_de_unidad_funcional=1,
+            consorcio=consorcio,
+            mes_anio=date(2026, 1, 1),
+            saldo_inicial=Decimal("100.00"),
+            total_gastos=Decimal("0"),
+            total_pagos=Decimal("0"),
+        )
+        SaldoMensual.objects.create(
+            numero_de_unidad_funcional=2,
+            consorcio=consorcio,
+            mes_anio=date(2026, 1, 1),
+            saldo_inicial=Decimal("0"),
+            total_gastos=Decimal("0"),
+            total_pagos=Decimal("0"),
+        )
+        template = ExpensaTemplate.objects.create(
+            consorcio=consorcio,
+            nombre="Template Febrero",
+            version=1,
+            config={
+                "rounding": {"metodo": "none"},
+                "columns": [
+                    {
+                        "id": "saldo_anterior",
+                        "label": "Saldo Anterior",
+                        "calc_type": "saldo_anterior",
+                        "visible": True,
+                    },
+                    {
+                        "id": "interes_mora",
+                        "label
... (truncado) ...
```

#### 📄 `backend/expensas/tests/unit/__init__.py`
```python
commit fb68522b36d3c2da79593d6a5f05473d934119e7
Author: Valentino <vceniceros2001@gmail.com>
Date:   Tue Feb 17 21:56:57 2026 -0300

    se agrega un menu de cargar templates de expensas, los endpoints dinamicos correspondientes usando patron strategy y builder para la creacion de las mismas

new file mode 100644
```

#### 📄 `backend/expensas/tests/unit/test_01_interest_strategy.py`
```python
commit fb68522b36d3c2da79593d6a5f05473d934119e7
Author: Valentino <vceniceros2001@gmail.com>
Date:   Tue Feb 17 21:56:57 2026 -0300

    se agrega un menu de cargar templates de expensas, los endpoints dinamicos correspondientes usando patron strategy y builder para la creacion de las mismas

new file mode 100644
--- /dev/null
+++ b/backend/expensas/tests/unit/test_01_interest_strategy.py
@@ -0,0 +1,26 @@
+from decimal import Decimal
+
+from django.test import TestCase
+
+from expensas.strategies import (
+    CompoundInterestStrategy,
+    EarlyPaymentStrategy,
+    SimpleInterestStrategy,
+)
+
+
+class TestInterestStrategies(TestCase):
+    def test_01_interes_simple(self):
+        estrategia = SimpleInterestStrategy()
+        resultado = estrategia.calculate(Decimal("1000"), Decimal("2"), periods=1)
+        self.assertEqual(resultado, Decimal("20"))
+
+    def test_02_interes_compuesto(self):
+        estrategia = CompoundInterestStrategy()
+        resultado = estrategia.calculate(Decimal("1000"), Decimal("2"), periods=2)
+        self.assertEqual(resultado.quantize(Decimal("0.01")), Decimal("40.40"))
+
+    def test_03_pronto_pago(self):
+        estrategia = EarlyPaymentStrategy()
+        resultado = estrategia.calculate(Decimal("1000"), Decimal("5"), periods=1)
+        self.assertEqual(resultado, Decimal("-50"))
```

#### 📄 `backend/expensas/tests/unit/test_02_prorrateo.py`
```python
commit fb68522b36d3c2da79593d6a5f05473d934119e7
Author: Valentino <vceniceros2001@gmail.com>
Date:   Tue Feb 17 21:56:57 2026 -0300

    se agrega un menu de cargar templates de expensas, los endpoints dinamicos correspondientes usando patron strategy y builder para la creacion de las mismas

new file mode 100644
--- /dev/null
+++ b/backend/expensas/tests/unit/test_02_prorrateo.py
@@ -0,0 +1,85 @@
+from decimal import Decimal
+from datetime import date
+
+from django.test import TestCase
+
+from consorcios.models import Consorcio
+from propietarios.models import Propietario
+from unidades_funcionales.models import UnidadFuncional, TipoUnidad, EstadoVivienda
+from gastos.models import Gasto, TipoGasto
+from proveedores.models import Proveedor, TipoProveedor
+
+from expensas.builder import LiquidacionBuilder
+
+
+class TestProrrateo(TestCase):
+    def test_01_prorrateo_por_superficie(self):
+        consorcio = Consorcio.objects.create(
+            cuit="20304050607",
+            razon_social="Consorcio Test",
+            calle="Av Siempre Viva",
+            numero=123,
+            codigo_postal="1000",
+            ciudad="CABA",
+            interes_por_mora=Decimal("1.50"),
+            redondeo_aumento=Decimal("0.50"),
+        )
+        propietario = Propietario.objects.create(
+            dni="12345678",
+            nombre="Juan",
+            apellido="Perez",
+        )
+        UnidadFuncional.objects.create(
+            numero_de_unidad_funcional=1,
+            consorcio=consorcio,
+            tipo_de_unidad=TipoUnidad.DEPARTAMENTO,
+            estado_de_vivienda=EstadoVivienda.PROPIETARIO,
+            superficie=Decimal("60"),
+            propietario=propietario,
+        )
+        UnidadFuncional.objects.create(
+            numero_de_unidad_funcional=2,
+            consorcio=consorcio,
+            tipo_de_unidad=TipoUnidad.DEPARTAMENTO,
+            estado_de_vivienda=EstadoVivienda.PROPIETARIO,
+            superficie=Decimal("40"),
+            propietario=propietario,
+        )
+        proveedor = Proveedor.objects.create(
+            cuit="20304050608",
+            razon_social="Proveedor Test",
+            telefono="123456",
+            email="proveedor@test.com",
+            calle="Av Test",
+            numero=10,
+            codigo_postal="1000",
+            ciudad="CABA",
+            tipo_proveedor=TipoProveedor.SERVICIOS_MENSUALES,
+        )
+        Gasto.objects.create(
+            consorcio=consorcio,
+            proveedor=proveedor,
+            periodo=date(2026, 2, 1),
+            descripcion="Limpieza",
+            monto=Decimal("100.00"),
+            tipo_gasto=TipoGasto.LIMPIEZA,
+        )
+        template_config = {
+            "columns": [
+                {
+                    "id": "gastos_ordinarios",
+                    "label": "Gastos Ordinarios",
+                    "calc_type": "prorrateo",
+                    "visible": True,
+                    "gasto_tipo": TipoGasto.LIMPIEZA,
+                }
+            ]
+        }
+        builder = LiquidacionBuilder(consorcio, date(2026, 2, 1), template_config, {})
+        resultado = builder.build()
+
+        unidades = resultado["unidades"]
+        valor_uf1 = Decimal(unidades[0]["valores"]["gastos_ordinarios"])
+        valor_uf2 = Decimal(unidades[1]["valores"]["gastos_ordinarios"])
+        self.assertEqual(valor_uf1, Decimal("60.00"))
+        self.assertEqual(valor_uf2, Decimal("40.00"))
```

#### 📄 `backend/expensas/urls.py`
```python
commit fb68522b36d3c2da79593d6a5f05473d934119e7
Author: Valentino <vceniceros2001@gmail.com>
Date:   Tue Feb 17 21:56:57 2026 -0300

    se agrega un menu de cargar templates de expensas, los endpoints dinamicos correspondientes usando patron strategy y builder para la creacion de las mismas

new file mode 100644
--- /dev/null
+++ b/backend/expensas/urls.py
@@ -0,0 +1,31 @@
+"""Rutas para la app expensas.
+
+Fecha:
+    14 - 02 - 2026
+"""
+
+from django.urls import path
+
+from . import views
+
+urlpatterns = [
+    path("liquidar/", views.liquidar_expensa, name="liquidar-expensa"),
+    path("templates/", views.listar_templates, name="listar-templates"),
+    path(
+        "templates/consorcio/<str:cuit_consorcio>/",
+        views.listar_templates_por_consorcio,
+        name="listar-templates-por-consorcio",
+    ),
+    path("templates/crear/", views.crear_template, name="crear-template"),
+    path("templates/<int:template_id>/", views.obtener_template, name="obtener-template"),
+    path(
+        "templates/<int:template_id>/actualizar/",
+        views.actualizar_template,
+        name="actualizar-template",
+    ),
+    path(
+        "templates/<int:template_id>/eliminar/",
+        views.eliminar_template,
+        name="eliminar-template",
+    ),
+]
```

#### 📄 `backend/expensas/utils.py`
```python
commit fb68522b36d3c2da79593d6a5f05473d934119e7
Author: Valentino <vceniceros2001@gmail.com>
Date:   Tue Feb 17 21:56:57 2026 -0300

    se agrega un menu de cargar templates de expensas, los endpoints dinamicos correspondientes usando patron strategy y builder para la creacion de las mismas

new file mode 100644
--- /dev/null
+++ b/backend/expensas/utils.py
@@ -0,0 +1,88 @@
+"""Utilidades para el motor de expensas.
+
+Fecha:
+    14 - 02 - 2026
+"""
+
+from __future__ import annotations
+
+import ast
+from datetime import date
+from decimal import Decimal
+from typing import Any, Mapping
+
+from django.core.exceptions import ValidationError
+
+
+def parse_decimal(value: Any, label: str = "valor") -> Decimal:
+    """Convierte un valor a Decimal con mensaje controlado."""
+
+    if isinstance(value, Decimal):
+        return value
+    if value is None:
+        return Decimal("0")
+    try:
+        return Decimal(str(value))
+    except Exception as exc:
+        raise ValidationError(f"{label} inválido: {value}") from exc
+
+
+def parse_period(value: str) -> date:
+    """Convierte un string YYYY-MM o YYYY-MM-DD en date del primer día del mes."""
+
+    try:
+        if len(value) == 7:
+            return date.fromisoformat(f"{value}-01")
+        return date.fromisoformat(value)
+    except Exception as exc:
+        raise ValidationError(f"Periodo inválido: {value}") from exc
+
+
+class SafeExpressionEvaluator(ast.NodeVisitor):
+    """Evalúa expresiones aritméticas simples usando un contexto de variables."""
+
+    ALLOWED_BINOPS = (ast.Add, ast.Sub, ast.Mult, ast.Div)
+    ALLOWED_UNARYOPS = (ast.UAdd, ast.USub)
+
+    def __init__(self, context: Mapping[str, Decimal]) -> None:
+        self.context = context
+
+    def visit(self, node: ast.AST) -> Decimal:
+        if isinstance(node, ast.Expression):
+            return self.visit(node.body)
+        if isinstance(node, ast.BinOp) and isinstance(node.op, self.ALLOWED_BINOPS):
+            left = self.visit(node.left)
+            right = self.visit(node.right)
+            if isinstance(node.op, ast.Add):
+                return left + right
+            if isinstance(node.op, ast.Sub):
+                return left - right
+            if isinstance(node.op, ast.Mult):
+                return left * right
+            if isinstance(node.op, ast.Div):
+                return left / right
+        if isinstance(node, ast.UnaryOp) and isinstance(node.op, self.ALLOWED_UNARYOPS):
+            operand = self.visit(node.operand)
+            if isinstance(node.op, ast.UAdd):
+                return operand
+            return -operand
+        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float, str)):
+            return parse_decimal(node.value)
+        if isinstance(node, ast.Name):
+            if node.id not in self.context:
+                raise ValidationError(f"Variable no definida: {node.id}")
+            return self.context[node.id]
+        raise ValidationError("Expresión no permitida.")
+
+
+def evaluate_expression(expression: str, context: Mapping[str, Decimal]) -> Decimal:
+    """Evalúa una expresión aritmética segura."""
+
+    try:
+        tree = ast.parse(expression, mode="eval")
+        evaluator = SafeExpressionEvaluator(context)
+        return evaluator.visit(tree)
+    except ValidationError:
+        raise
+    except Exception as exc:
+        raise ValidationError(f"Expresión inválida: {expression}") from exc
```

#### 📄 `backend/expensas/views.py`
```python
commit fb68522b36d3c2da79593d6a5f05473d934119e7
Author: Valentino <vceniceros2001@gmail.com>
Date:   Tue Feb 17 21:56:57 2026 -0300

    se agrega un menu de cargar templates de expensas, los endpoints dinamicos correspondientes usando patron strategy y builder para la creacion de las mismas

new file mode 100644
--- /dev/null
+++ b/backend/expensas/views.py
@@ -0,0 +1,200 @@
+"""Views para la app expensas.
+
+Fecha:
+    14 - 02 - 2026
+"""
+
+import json
+
+from django.core.exceptions import ValidationError
+from django.http import JsonResponse
+from django.views.decorators.csrf import csrf_exempt
+from django.views.decorators.http import require_http_methods
+
+from .services import LiquidacionService
+from .models import ExpensaTemplate
+
+
+@csrf_exempt
+@require_http_methods(["POST"])
+def liquidar_expensa(request):
+    """Genera una liquidación en base a un template.
+
+    POST: {
+        "template_id": 1,
+        "consorcio": "20304050607",
+        "periodo": "2026-02",
+        "cerrar": true,
+        "parametros": {
+            "conceptos_particulares": [
+                {"unidad": 1, "column_id": "reparaciones", "monto": "1200.00"}
+            ],
+            "coeficientes_custom": {"1": "0.6", "2": "0.4"}
+        }
+    }
+    """
+
+    try:
+        payload = json.loads(request.body)
+        resultado = LiquidacionService.liquidar(payload)
+        status_code = 201 if payload.get("cerrar") else 200
+        return JsonResponse({"status": "success", "data": resultado}, status=status_code)
+    except ValidationError as exc:
+        return JsonResponse({"status": "error", "message": str(exc)}, status=400)
+    except Exception as exc:
+        return JsonResponse({"status": "error", "message": str(exc)}, status=500)
+
+
+@csrf_exempt
+@require_http_methods(["GET"])
+def listar_templates(request):
+    """Lista templates de expensa.
+
+    GET: /api/expensas/templates/?consorcio=<cuit>
+    """
+
+    try:
+        consorcio = request.GET.get("consorcio")
+        queryset = ExpensaTemplate.objects.all()
+        if consorcio:
+            queryset = queryset.filter(consorcio_id=consorcio)
+        templates = [
+            {
+                "id": template.id_expensa_template,
+                "consorcio": template.consorcio_id,
+                "nombre": template.nombre,
+                "version": template.version,
+                "activo": template.activo,
+            }
+            for template in queryset.order_by("-creado_en")
+        ]
+        return JsonResponse({"status": "success", "data": templates})
+    except Exception as exc:
+        return JsonResponse({"status": "error", "message": str(exc)}, status=500)
+
+
+@csrf_exempt
+@require_http_methods(["GET"])
+def listar_templates_por_consorcio(request, cuit_consorcio):
+    """Lista templates de expensa por consorcio."""
+    try:
+        queryset = ExpensaTemplate.objects.filter(consorcio_id=cuit_consorcio)
+        templates = [
+            {
+                "id": template.id_expensa_template,
+                "consorcio": template.consorcio_id,
+                "nombre": template.nombre,
+                "version": template.version,
+                "activo": template.activo,
+            }
+            for template in queryset.order_by("-creado_en")
+        ]
+        return JsonResponse({"status": "success", "data": templates})
+    except Exception as exc:
+        return JsonResponse({"status": "error", "message": str(exc)}, status=500)
+
+
+@csrf_exempt
+@require_http_methods(["POST"])
+def crear_template(request):
+    """Crea un template de expensa."""
+
+    try:
+        payload = json.loads(request.body)
+        template = ExpensaTemplate.objects.create(
+            consorcio_id=payload.get("consorcio"),
+            nombre=payload.get("nombre"),
+            version=payload.get("version", 1),
+            config=payload.get("config", {}),
+            activo=payload.get("activo", True),
+        )
+        return J
... (truncado) ...
```

#### 📄 `backend/unidades_funcionales/migrations/0003_update_tipo_unidad_check.py`
```python
commit fb68522b36d3c2da79593d6a5f05473d934119e7
Author: Valentino <vceniceros2001@gmail.com>
Date:   Tue Feb 17 21:56:57 2026 -0300

    se agrega un menu de cargar templates de expensas, los endpoints dinamicos correspondientes usando patron strategy y builder para la creacion de las mismas

new file mode 100644
--- /dev/null
+++ b/backend/unidades_funcionales/migrations/0003_update_tipo_unidad_check.py
@@ -0,0 +1,29 @@
+"""Actualiza restricción de tipo de unidad para incluir PH.
+
+Fecha:
+    14 - 02 - 2026
+"""
+
+from django.db import migrations, models
+
+
+class Migration(migrations.Migration):
+    """Actualiza la restricción de tipo_de_unidad."""
+
+    dependencies = [
+        ("unidades_funcionales", "0002_tipo_unidad_check"),
+    ]
+
+    operations = [
+        migrations.RemoveConstraint(
+            model_name="unidadfuncional",
+            name="unidades_funcionales_tipo_valido",
+        ),
+        migrations.AddConstraint(
+            model_name="unidadfuncional",
+            constraint=models.CheckConstraint(
+                condition=models.Q(tipo_de_unidad__in=["Departamento", "Lote", "PH"]),
+                name="unidades_funcionales_tipo_valido",
+            ),
+        ),
+    ]
```

#### 📄 `backend/unidades_funcionales/models.py`
```python
commit fb68522b36d3c2da79593d6a5f05473d934119e7
Author: Valentino <vceniceros2001@gmail.com>
Date:   Tue Feb 17 21:56:57 2026 -0300

    se agrega un menu de cargar templates de expensas, los endpoints dinamicos correspondientes usando patron strategy y builder para la creacion de las mismas

--- a/backend/unidades_funcionales/models.py
+++ b/backend/unidades_funcionales/models.py
@@ -29,6 +29,7 @@ class TipoUnidad(models.TextChoices):
 
     DEPARTAMENTO = "Departamento", "Departamento"
     LOTE = "Lote", "Lote"
+    PH = "PH", "PH"
 
 
 class UnidadFuncional(models.Model):
```

#### 📄 `frontend/postcss.config.js`
```python
commit fb68522b36d3c2da79593d6a5f05473d934119e7
Author: Valentino <vceniceros2001@gmail.com>
Date:   Tue Feb 17 21:56:57 2026 -0300

    se agrega un menu de cargar templates de expensas, los endpoints dinamicos correspondientes usando patron strategy y builder para la creacion de las mismas

new file mode 100644
--- /dev/null
+++ b/frontend/postcss.config.js
@@ -0,0 +1,6 @@
+module.exports = {
+  plugins: {
+    tailwindcss: {},
+    autoprefixer: {}
+  }
+};
```

#### 📄 `frontend/src/app/app.routes.ts`
```python
commit fb68522b36d3c2da79593d6a5f05473d934119e7
Author: Valentino <vceniceros2001@gmail.com>
Date:   Tue Feb 17 21:56:57 2026 -0300

    se agrega un menu de cargar templates de expensas, los endpoints dinamicos correspondientes usando patron strategy y builder para la creacion de las mismas

--- a/frontend/src/app/app.routes.ts
+++ b/frontend/src/app/app.routes.ts
@@ -49,6 +49,10 @@ export const routes: Routes = [
     path: 'dashboard/:consortiumName/pagos/:idPago/editar',
     loadComponent: () => import('./components/pages/payment-upload/payment-upload').then(m => m.PaymentUpload)
   },
+  {
+    path: 'dashboard/:consortiumName/expensas',
+    loadComponent: () => import('./components/pages/settlement/settlement').then(m => m.SettlementComponent)
+  },
   {
     path: 'dashboard/:consortiumName/gastos/carga-de-gasto',
     loadComponent: () => import('./components/pages/expense-upload/expense-upload').then(m => m.ExpenseUpload)
```

#### 📄 `frontend/src/app/components/organism/sidebar.component/sidebar.component.css`
```python
commit fb68522b36d3c2da79593d6a5f05473d934119e7
Author: Valentino <vceniceros2001@gmail.com>
Date:   Tue Feb 17 21:56:57 2026 -0300

    se agrega un menu de cargar templates de expensas, los endpoints dinamicos correspondientes usando patron strategy y builder para la creacion de las mismas

--- a/frontend/src/app/components/organism/sidebar.component/sidebar.component.css
+++ b/frontend/src/app/components/organism/sidebar.component/sidebar.component.css
@@ -7,6 +7,9 @@
   padding: 16px 8px;
   box-shadow: 2px 0 4px rgba(0, 0, 0, 0.05);
   align-self: stretch;
+  overflow-y: auto;
+  overflow-x: hidden;
+  scrollbar-gutter: stable;
 }
 
 /* En mobile: fixed positioning y control de visibilidad */
```

#### 📄 `frontend/src/app/components/organism/sidebar.component/sidebar.component.html`
```python
commit fb68522b36d3c2da79593d6a5f05473d934119e7
Author: Valentino <vceniceros2001@gmail.com>
Date:   Tue Feb 17 21:56:57 2026 -0300

    se agrega un menu de cargar templates de expensas, los endpoints dinamicos correspondientes usando patron strategy y builder para la creacion de las mismas

--- a/frontend/src/app/components/organism/sidebar.component/sidebar.component.html
+++ b/frontend/src/app/components/organism/sidebar.component/sidebar.component.html
@@ -65,4 +65,13 @@
     [routerLink]="expensesRoute"
     [isActive]="false">
   </app-navbar-item>
+
+  <app-navbar-item 
+    iconHref="assets/img/sprites.svg#expenses" 
+    label="Expensas" 
+    size="24" 
+    iconColor="#000000" 
+    [routerLink]="settlementRoute"
+    [isActive]="false">
+  </app-navbar-item>
 </nav>
\ No newline at end of file
```

#### 📄 `frontend/src/app/components/organism/sidebar.component/sidebar.component.ts`
```python
commit fb68522b36d3c2da79593d6a5f05473d934119e7
Author: Valentino <vceniceros2001@gmail.com>
Date:   Tue Feb 17 21:56:57 2026 -0300

    se agrega un menu de cargar templates de expensas, los endpoints dinamicos correspondientes usando patron strategy y builder para la creacion de las mismas

--- a/frontend/src/app/components/organism/sidebar.component/sidebar.component.ts
+++ b/frontend/src/app/components/organism/sidebar.component/sidebar.component.ts
@@ -22,6 +22,7 @@ export class SidebarComponent implements OnInit {
   paymentsRoute: string = '';
   monthlyBalanceRoute: string = '';
   expensesRoute: string = '';
+  settlementRoute: string = '';
 
   constructor(
     private route: ActivatedRoute,
@@ -53,6 +54,7 @@ export class SidebarComponent implements OnInit {
       this.paymentsRoute = `/dashboard/${this.consortiumName}/pagos`;
       this.monthlyBalanceRoute = `/dashboard/${this.consortiumName}/saldos-mensuales`;
       this.expensesRoute = `/dashboard/${this.consortiumName}/gastos`;
+      this.settlementRoute = `/dashboard/${this.consortiumName}/expensas`;
     }
   }
 }
\ No newline at end of file
```

#### 📄 `frontend/src/app/components/pages/settlement/settlement.css`
```python
commit fb68522b36d3c2da79593d6a5f05473d934119e7
Author: Valentino <vceniceros2001@gmail.com>
Date:   Tue Feb 17 21:56:57 2026 -0300

    se agrega un menu de cargar templates de expensas, los endpoints dinamicos correspondientes usando patron strategy y builder para la creacion de las mismas

new file mode 100644
```

#### 📄 `frontend/src/app/components/pages/settlement/settlement.html`
```python
commit fb68522b36d3c2da79593d6a5f05473d934119e7
Author: Valentino <vceniceros2001@gmail.com>
Date:   Tue Feb 17 21:56:57 2026 -0300

    se agrega un menu de cargar templates de expensas, los endpoints dinamicos correspondientes usando patron strategy y builder para la creacion de las mismas

new file mode 100644
--- /dev/null
+++ b/frontend/src/app/components/pages/settlement/settlement.html
@@ -0,0 +1,386 @@
+<div class="mx-auto max-w-7xl p-6">
+      <div class="mt-4">
+    <h1 class="text-2xl font-semibold text-slate-800">Liquidación de Expensas</h1>
+    <p class="text-sm text-slate-500">Seleccioná el periodo y el template para previsualizar la liquidación.</p>
+  </div>
+
+  <div class="grid grid-cols-1 gap-4 rounded-xl border border-slate-200 bg-white p-4 shadow-sm md:grid-cols-3">
+    <div class="flex flex-col gap-2">
+      <label class="text-xs font-semibold text-slate-500">Periodo (Mes/Año)</label>
+
+      <p *ngIf="columnError" class="mt-3 text-xs font-semibold text-red-600">{{ columnError }}</p>
+      <input
+        type="month"
+        class="h-10 rounded-lg border border-slate-300 px-3 text-sm text-slate-700 focus:border-slate-400 focus:outline-none"
+        [(ngModel)]="period"
+      />
+    </div>
+
+    <div class="flex flex-col gap-2">
+      <label class="text-xs font-semibold text-slate-500">Template</label>
+      <select
+        class="h-10 rounded-lg border border-slate-300 bg-white px-3 text-sm text-slate-700 focus:border-slate-400 focus:outline-none"
+        [(ngModel)]="selectedTemplateId"
+      >
+        <option value="">Seleccionar template</option>
+        <option *ngFor="let template of (templates$ | async)" [value]="template.id">
+          {{ template.nombre }} (v{{ template.version }})
+        </option>
+      </select>
+    </div>
+
+    <div class="flex items-end gap-3">
+      <button
+        class="h-10 rounded-lg bg-slate-900 px-4 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:bg-slate-300"
+        (click)="preview()"
+        [disabled]="isPreviewLoading || !selectedTemplateId"
+      >
+        {{ isPreviewLoading ? 'Procesando...' : 'Previsualizar' }}
+      </button>
+
+      <button
+        class="h-10 rounded-lg border border-slate-300 px-4 text-sm font-semibold text-slate-700 transition hover:border-slate-400 disabled:cursor-not-allowed disabled:text-slate-400"
+        (click)="closeSettlement()"
+        [disabled]="isClosing || !selectedTemplateId"
+      >
+        {{ isClosing ? 'Cerrando...' : 'Cerrar Liquidación' }}
+      </button>
+    </div>
+  </div>
+
+  <div class="mt-6 rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
+    <div class="flex items-center justify-between">
+      <div>
+        <h2 class="text-base font-semibold text-slate-800">Templates de Expensa</h2>
+        <p class="text-xs text-slate-500">Creá, editá o eliminá templates del consorcio.</p>
+      </div>
+      <button
+        class="h-9 rounded-lg bg-slate-900 px-3 text-xs font-semibold text-white transition hover:bg-slate-800"
+        (click)="openTemplateForm()"
+      >
+        Nuevo Template
+      </button>
+    </div>
+
+    <div class="mt-4 overflow-x-auto">
+      <table class="min-w-full text-left text-sm">
+        <thead class="border-b border-slate-200 text-xs uppercase text-slate-500">
+          <tr>
+            <th class="px-3 py-2">Nombre</th>
+            <th class="px-3 py-2">Versión</th>
+            <th class="px-3 py-2">Activo</th>
+            <th class="px-3 py-2 text-right">Acciones</th>
+          </tr>
+        </thead>
+        <tbody class="divide-y divide-slate-100">
+          <tr *ngFor="let template of templates">
+            <td class="px-3 py-2 text-slate-700">{{ template.nombre }}</td>
+            <td class="px-3 py-2 text-slate-700">v{{ template.version }}</td>
+            <td class="px-3 py-2">
+              <span
+                class="rounded-full px-2 py-1 text-xs"
+      
... (truncado) ...
```

#### 📄 `frontend/src/app/components/pages/settlement/settlement.ts`
```python
commit fb68522b36d3c2da79593d6a5f05473d934119e7
Author: Valentino <vceniceros2001@gmail.com>
Date:   Tue Feb 17 21:56:57 2026 -0300

    se agrega un menu de cargar templates de expensas, los endpoints dinamicos correspondientes usando patron strategy y builder para la creacion de las mismas

new file mode 100644
--- /dev/null
+++ b/frontend/src/app/components/pages/settlement/settlement.ts
@@ -0,0 +1,397 @@
+import { ChangeDetectionStrategy, Component, OnInit } from '@angular/core';
+import { CommonModule, CurrencyPipe } from '@angular/common';
+import { ActivatedRoute } from '@angular/router';
+import { FormsModule } from '@angular/forms';
+import { BehaviorSubject, Observable, map } from 'rxjs';
+
+import { ConsortiumService } from '../../../services/consortium.service';
+import { SettlementService } from '../../../services/settlement.service';
+import {
+  SettlementResponse,
+  SettlementTableRow,
+  SettlementTableState,
+  SettlementTemplate
+} from '../../../../models/settlement.model';
+import { SettlementValuePipe } from '../../../shared/pipes/settlement-value.pipe';
+
+@Component({
+  selector: 'app-settlement',
+  imports: [CommonModule, FormsModule, CurrencyPipe, SettlementValuePipe],
+  templateUrl: './settlement.html',
+  styleUrl: './settlement.css',
+  standalone: true,
+  changeDetection: ChangeDetectionStrategy.OnPush
+})
+export class SettlementComponent implements OnInit {
+  consortiumName: string = '';
+  consortiumId: string = '';
+
+  period: string = this.defaultPeriod();
+  selectedTemplateId: string = '';
+
+  templates$!: Observable<SettlementTemplate[]>;
+  templates: SettlementTemplate[] = [];
+
+  private settlementSubject = new BehaviorSubject<SettlementResponse | null>(null);
+  settlement$ = this.settlementSubject.asObservable().pipe(
+    map(response => (response ? this.mapToTableState(response) : null))
+  );
+
+  isPreviewLoading = false;
+  isClosing = false;
+  showTemplateForm = false;
+  isEditTemplate = false;
+  showDeleteConfirm = false;
+  templateToDelete: SettlementTemplate | null = null;
+  formError = '';
+  columnError = '';
+  templateForm = {
+    id: 0,
+    nombre: '',
+    version: 1,
+    activo: true,
+    roundingMetodo: 'none',
+    roundingIncrement: '0.50',
+    columns: [] as any[]
+  };
+  columnDraft = this.createEmptyColumn();
+  editingColumnIndex: number | null = null;
+
+  constructor(
+    private route: ActivatedRoute,
+    private consortiumService: ConsortiumService,
+    private settlementService: SettlementService
+  ) {}
+
+  ngOnInit(): void {
+    this.route.params.subscribe(params => {
+      this.consortiumName = params['consortiumName'];
+      this.loadConsortiumData();
+    });
+  }
+
+  loadConsortiumData(): void {
+    this.consortiumService.getAllConsortiums().subscribe({
+      next: (consortia) => {
+        const decodedName = decodeURIComponent(this.consortiumName.replace(/-/g, ' '));
+        const found = consortia.find(c => c.name.toLowerCase() === decodedName.toLowerCase());
+        if (found) {
+          this.consortiumId = String(found.id);
+          this.templates$ = this.settlementService.getTemplatesByConsortium(this.consortiumId);
+          this.templates$.subscribe({
+            next: (items) => {
+              this.templates = items;
+            }
+          });
+        }
+      }
+    });
+  }
+
+  preview(): void {
+    if (!this.canSubmit()) {
+      return;
+    }
+    this.isPreviewLoading = true;
+    const payload = this.buildPayload(false);
+    this.settlementService.preview(payload).subscribe({
+      next: (response) => {
+        this.settlementSubject.next(response);
+        this.isPreviewLoading = false;
+      },
+      error: () => {
+        this.isPreviewLoading = false;
+      }
+    });
+  }
+
+  closeSettlement(): void {
+    if (!this.canSubmit()) {
+      return;
+    }
+    this.isClosing = true;
+    const payload = this.buildPayload(true);
+    this.settlementService.closeSettlement(payload)
... (truncado) ...
```

#### 📄 `frontend/src/app/services/settlement.service.ts`
```python
commit fb68522b36d3c2da79593d6a5f05473d934119e7
Author: Valentino <vceniceros2001@gmail.com>
Date:   Tue Feb 17 21:56:57 2026 -0300

    se agrega un menu de cargar templates de expensas, los endpoints dinamicos correspondientes usando patron strategy y builder para la creacion de las mismas

new file mode 100644
--- /dev/null
+++ b/frontend/src/app/services/settlement.service.ts
@@ -0,0 +1,68 @@
+import { Injectable } from '@angular/core';
+import { HttpClient } from '@angular/common/http';
+import { Observable, map } from 'rxjs';
+import { SettlementResponse, SettlementTemplate } from '../../models/settlement.model';
+
+@Injectable({
+  providedIn: 'root'
+})
+export class SettlementService {
+  private templatesUrl = '/api/expensas/templates/';
+  private liquidarUrl = '/api/liquidar/';
+
+  constructor(private http: HttpClient) {}
+
+  getTemplates(): Observable<SettlementTemplate[]> {
+    return this.http.get<{ status: string; data: any[] }>(this.templatesUrl).pipe(
+      map(response => (response.data || []).map(item => this.mapTemplate(item)))
+    );
+  }
+
+  getTemplatesByConsortium(cuitConsorcio: string): Observable<SettlementTemplate[]> {
+    return this.http
+      .get<{ status: string; data: any[] }>(`${this.templatesUrl}consorcio/${cuitConsorcio}/`)
+      .pipe(map(response => (response.data || []).map(item => this.mapTemplate(item))));
+  }
+
+  getTemplateById(templateId: number): Observable<SettlementTemplate | undefined> {
+    return this.http
+      .get<{ status: string; data: any }>(`${this.templatesUrl}${templateId}/`)
+      .pipe(map(response => (response?.data ? this.mapTemplate(response.data) : undefined)));
+  }
+
+  createTemplate(payload: any): Observable<any> {
+    return this.http.post(`${this.templatesUrl}crear/`, payload);
+  }
+
+  updateTemplate(templateId: number, payload: any): Observable<any> {
+    return this.http.put(`${this.templatesUrl}${templateId}/actualizar/`, payload);
+  }
+
+  deleteTemplate(templateId: number): Observable<any> {
+    return this.http.delete(`${this.templatesUrl}${templateId}/eliminar/`);
+  }
+
+  preview(payload: any): Observable<SettlementResponse> {
+    return this.http.post<{ status: string; data: SettlementResponse }>(this.liquidarUrl, payload).pipe(
+      map(response => response.data)
+    );
+  }
+
+  closeSettlement(payload: any): Observable<SettlementResponse> {
+    return this.http.post<{ status: string; data: SettlementResponse }>(this.liquidarUrl, {
+      ...payload,
+      cerrar: true
+    }).pipe(map(response => response.data));
+  }
+
+  private mapTemplate(item: any): SettlementTemplate {
+    return {
+      id: Number(item.id ?? item.id_expensa_template ?? 0),
+      consorcio: item.consorcio ?? item.cuit_consorcio ?? null,
+      nombre: item.nombre ?? 'Template',
+      version: Number(item.version ?? 1),
+      activo: Boolean(item.activo ?? true),
+      config: item.config ?? undefined
+    } as SettlementTemplate;
+  }
+}
```

#### 📄 `frontend/src/app/shared/pipes/settlement-value.pipe.ts`
```python
commit fb68522b36d3c2da79593d6a5f05473d934119e7
Author: Valentino <vceniceros2001@gmail.com>
Date:   Tue Feb 17 21:56:57 2026 -0300

    se agrega un menu de cargar templates de expensas, los endpoints dinamicos correspondientes usando patron strategy y builder para la creacion de las mismas

new file mode 100644
--- /dev/null
+++ b/frontend/src/app/shared/pipes/settlement-value.pipe.ts
@@ -0,0 +1,49 @@
+import { CurrencyPipe } from '@angular/common';
+import { Pipe, PipeTransform, inject } from '@angular/core';
+import { SettlementColumn } from '../../../models/settlement.model';
+
+@Pipe({
+  name: 'settlementValue',
+  standalone: true
+})
+export class SettlementValuePipe implements PipeTransform {
+  private currencyPipe = inject(CurrencyPipe);
+
+  transform(value: string | number | null | undefined, column?: SettlementColumn): string {
+    if (value === null || value === undefined || value === '') {
+      return '-';
+    }
+
+    const numericValue = Number(value);
+    const shouldFormat = this.isMonetaryColumn(column);
+
+    if (shouldFormat && !Number.isNaN(numericValue)) {
+      return (
+        this.currencyPipe.transform(numericValue, 'ARS', 'symbol', '1.2-2', 'es-AR') ??
+        numericValue.toFixed(2)
+      );
+    }
+
+    return String(value);
+  }
+
+  private isMonetaryColumn(column?: SettlementColumn): boolean {
+    if (!column) {
+      return false;
+    }
+    const calcType = (column.calc_type || '').toLowerCase();
+    if ([
+      'saldo_anterior',
+      'interes',
+      'prorrateo',
+      'concepto_particular',
+      'fijo',
+      'formula'
+    ].includes(calcType)) {
+      return true;
+    }
+
+    const label = `${column.label ?? ''} ${column.id ?? ''}`.toLowerCase();
+    return /monto|total|saldo|inter[eé]s|gasto|expensa|mora|repar|multa/.test(label);
+  }
+}
```

#### 📄 `frontend/src/models/settlement.model.ts`
```python
commit fb68522b36d3c2da79593d6a5f05473d934119e7
Author: Valentino <vceniceros2001@gmail.com>
Date:   Tue Feb 17 21:56:57 2026 -0300

    se agrega un menu de cargar templates de expensas, los endpoints dinamicos correspondientes usando patron strategy y builder para la creacion de las mismas

new file mode 100644
--- /dev/null
+++ b/frontend/src/models/settlement.model.ts
@@ -0,0 +1,47 @@
+export interface SettlementTemplate {
+  id: number;
+  consorcio?: string | null;
+  nombre: string;
+  version: number;
+  activo: boolean;
+  config?: any;
+}
+
+export interface SettlementColumn {
+  id: string;
+  label: string;
+  visible: boolean;
+  calc_type: string;
+  help_text?: string;
+}
+
+export interface SettlementUnitRow {
+  numero_unidad_funcional: number;
+  propietario: string;
+  apellido: string;
+  valores: Record<string, string>;
+}
+
+export interface SettlementResponse {
+  consorcio: string;
+  periodo: string;
+  template_id: number;
+  columns: SettlementColumn[];
+  unidades: SettlementUnitRow[];
+  totales: Record<string, string>;
+}
+
+export interface SettlementTableRow {
+  unidad_funcional: string;
+  propietario: string;
+  apellido: string;
+  [key: string]: string;
+}
+
+export interface SettlementTableState {
+  columns: SettlementColumn[];
+  rows: SettlementTableRow[];
+  totales: Record<string, string>;
+  templateId: number;
+  periodo: string;
+}
```

#### 📄 `frontend/src/styles.css`
```python
commit fb68522b36d3c2da79593d6a5f05473d934119e7
Author: Valentino <vceniceros2001@gmail.com>
Date:   Tue Feb 17 21:56:57 2026 -0300

    se agrega un menu de cargar templates de expensas, los endpoints dinamicos correspondientes usando patron strategy y builder para la creacion de las mismas

--- a/frontend/src/styles.css
+++ b/frontend/src/styles.css
@@ -1,9 +1,3 @@
-/* You can add global styles to this file, and also import other style files */
-
-* {
-  font-family: serif;
-}
-
-body {
-  font-family: serif;
-}
+@tailwind base;
+@tailwind components;
+@tailwind utilities;
```

#### 📄 `frontend/tailwind.config.js`
```python
commit fb68522b36d3c2da79593d6a5f05473d934119e7
Author: Valentino <vceniceros2001@gmail.com>
Date:   Tue Feb 17 21:56:57 2026 -0300

    se agrega un menu de cargar templates de expensas, los endpoints dinamicos correspondientes usando patron strategy y builder para la creacion de las mismas

new file mode 100644
--- /dev/null
+++ b/frontend/tailwind.config.js
@@ -0,0 +1,8 @@
+/** @type {import('tailwindcss').Config} */
+module.exports = {
+  content: ['./src/**/*.{html,ts}'],
+  theme: {
+    extend: {}
+  },
+  plugins: []
+};
```

---
