"""Migración inicial de consorcios.

Resumen:
    Crea la tabla consorcios con sus campos y restricciones.

Fecha:
    27 - 01 - 2026
"""

from decimal import Decimal

from django.db import migrations, models


class Migration(migrations.Migration):
    """Migración inicial para la app consorcios."""

    initial = True

    dependencies: list[tuple[str, str]] = []

    operations = [
        migrations.CreateModel(
            name="Consorcio",
            fields=[
                (
                    "cuit",
                    models.CharField(
                        db_column="cuit",
                        max_length=11,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "razon_social",
                    models.CharField(db_column="razon_social", max_length=100),
                ),
                ("calle", models.CharField(db_column="calle", max_length=100)),
                (
                    "numero",
                    models.PositiveIntegerField(db_column="numero"),
                ),
                (
                    "codigo_postal",
                    models.CharField(db_column="codigo_postal", max_length=10),
                ),
                ("ciudad", models.CharField(db_column="ciudad", max_length=50)),
                (
                    "interes_por_mora",
                    models.DecimalField(
                        db_column="interes_por_mora",
                        decimal_places=2,
                        max_digits=5,
                    ),
                ),
                (
                    "redondeo_aumento",
                    models.DecimalField(
                        db_column="redondeo_aumento",
                        decimal_places=2,
                        max_digits=5,
                    ),
                ),
            ],
            options={
                "db_table": "consorcios",
                "verbose_name": "Consorcio",
                "verbose_name_plural": "Consorcios",
                "constraints": [
                    models.CheckConstraint(
                        check=models.Q(numero__gt=0, numero__lt=60000),
                        name="consorcios_numero_rango",
                    ),
                    models.CheckConstraint(
                        check=models.Q(interes_por_mora__gte=Decimal("0")),
                        name="consorcios_interes_mora_gte_0",
                    ),
                    models.CheckConstraint(
                        check=models.Q(redondeo_aumento__gte=Decimal("0")),
                        name="consorcios_redondeo_aumento_gte_0",
                    ),
                    models.CheckConstraint(
                        check=models.Q(cuit__regex=r"^\d+$"),
                        name="consorcios_cuit_solo_digitos",
                    ),
                ],
            },
        )
    ]
