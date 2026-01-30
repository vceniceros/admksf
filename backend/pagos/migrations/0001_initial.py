"""Migración inicial de pagos.

Resumen:
    Crea la tabla pagos con relaciones y restricciones.

Fecha:
    27 - 01 - 2026
"""

from decimal import Decimal

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    """Migración inicial para la app pagos."""

    initial = True

    dependencies = [
        ("consorcios", "0001_initial"),
        ("propietarios", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Pago",
            fields=[
                (
                    "id_pago",
                    models.BigAutoField(
                        db_column="id_pago",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "numero_de_unidad_funcional",
                    models.IntegerField(db_column="numero_de_unidad_funcional"),
                ),
                (
                    "monto",
                    models.DecimalField(
                        db_column="monto",
                        decimal_places=2,
                        max_digits=10,
                    ),
                ),
                (
                    "fecha_pago",
                    models.DateTimeField(
                        db_column="fecha_pago",
                        default=django.utils.timezone.now,
                    ),
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
                (
                    "propietario",
                    models.ForeignKey(
                        db_column="dni_propietario",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="propietarios.propietario",
                        to_field="dni",
                    ),
                ),
            ],
            options={
                "db_table": "pagos",
                "verbose_name": "Pago",
                "verbose_name_plural": "Pagos",
                "constraints": [
                    models.CheckConstraint(
                        check=models.Q(monto__gt=Decimal("0")),
                        name="pagos_monto_gt_0",
                    ),
                    models.UniqueConstraint(
                        fields=["id_pago", "numero_de_unidad_funcional", "consorcio"],
                        name="pagos_id_unidad_consorcio_unique",
                    ),
                ],
            },
        )
    ]
