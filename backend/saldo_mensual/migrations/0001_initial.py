"""Migración inicial de saldo_mensual.

Resumen:
    Crea la tabla saldo_mensual con saldo_final generado.

Fecha:
    27 - 01 - 2026
"""

from decimal import Decimal

from django.db import migrations, models
from django.db.models import F
import django.db.models.deletion


class Migration(migrations.Migration):
    """Migración inicial para la app saldo_mensual."""

    initial = True

    dependencies = [
        ("consorcios", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="SaldoMensual",
            fields=[
                (
                    "id_saldo_mensual",
                    models.BigAutoField(
                        db_column="id_saldo_mensual",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "numero_de_unidad_funcional",
                    models.IntegerField(db_column="numero_de_unidad_funcional"),
                ),
                ("mes_anio", models.DateField(db_column="mes_año")),
                (
                    "saldo_inicial",
                    models.DecimalField(
                        db_column="saldo_inicial",
                        decimal_places=2,
                        default=Decimal("0"),
                        max_digits=10,
                    ),
                ),
                (
                    "total_gastos",
                    models.DecimalField(
                        db_column="total_gastos",
                        decimal_places=2,
                        default=Decimal("0"),
                        max_digits=10,
                    ),
                ),
                (
                    "total_pagos",
                    models.DecimalField(
                        db_column="total_pagos",
                        decimal_places=2,
                        default=Decimal("0"),
                        max_digits=10,
                    ),
                ),
                (
                    "saldo_final",
                    models.GeneratedField(
                        db_column="saldo_final",
                        db_persist=True,
                        expression=F("saldo_inicial") + F("total_gastos") - F("total_pagos"),
                        output_field=models.DecimalField(decimal_places=2, max_digits=10),
                    ),
                ),
                (
                    "fecha_cierre",
                    models.DateTimeField(blank=True, db_column="fecha_cierre", null=True),
                ),
                (
                    "consorcio",
                    models.ForeignKey(
                        db_column="cuit_consorcio",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="consorcios.consorcio",
                        to_field="cuit",
                    ),
                ),
            ],
            options={
                "db_table": "saldo_mensual",
                "verbose_name": "Saldo mensual",
                "verbose_name_plural": "Saldos mensuales",
                "constraints": [
                    models.CheckConstraint(
                        check=models.Q(saldo_inicial__gte=Decimal("0")),
                        name="saldo_mensual_saldo_inicial_gte_0",
                    ),
                    models.CheckConstraint(
                        check=models.Q(total_gastos__gte=Decimal("0")),
                        name="saldo_mensual_total_gastos_gte_0",
                    ),
                    models.CheckConstraint(
                        check=models.Q(total_pagos__gte=Decimal("0")),
                        name="saldo_mensual_total_pagos_gte_0",
                    ),
                    models.UniqueConstraint(
                        fields=["numero_de_unidad_funcional", "consorcio", "mes_anio"],
                        name="saldo_mensual_unidad_consorcio_mes_unique",
                    ),
                ],
            },
        )
    ]
