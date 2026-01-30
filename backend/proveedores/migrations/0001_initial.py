"""Migración inicial de proveedores.

Resumen:
    Crea la tabla proveedores con sus campos y restricciones.

Fecha:
    27 - 01 - 2026
"""

from django.db import migrations, models


class Migration(migrations.Migration):
    """Migración inicial para la app proveedores."""

    initial = True

    dependencies: list[tuple[str, str]] = []

    operations = [
        migrations.CreateModel(
            name="Proveedor",
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
                (
                    "telefono",
                    models.CharField(blank=True, db_column="telefono", max_length=20, null=True),
                ),
                (
                    "email",
                    models.EmailField(blank=True, db_column="email", max_length=100, null=True),
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
                    "tipo_proveedor",
                    models.CharField(
                        choices=[
                            ("servicios_mensuales", "Servicios mensuales"),
                            ("reparaciones_mantenimientos", "Reparaciones y mantenimientos"),
                        ],
                        db_column="tipo_proveedor",
                        max_length=30,
                    ),
                ),
            ],
            options={
                "db_table": "proveedores",
                "verbose_name": "Proveedor",
                "verbose_name_plural": "Proveedores",
                "constraints": [
                    models.CheckConstraint(
                        check=models.Q(numero__gt=0, numero__lt=60000),
                        name="proveedores_numero_rango",
                    ),
                    models.CheckConstraint(
                        check=models.Q(cuit__regex=r"^\d+$"),
                        name="proveedores_cuit_solo_digitos",
                    ),
                    models.CheckConstraint(
                        check=models.Q(
                            tipo_proveedor__in=[
                                "servicios_mensuales",
                                "reparaciones_mantenimientos",
                            ]
                        ),
                        name="proveedores_tipo_proveedor_valido",
                    ),
                ],
            },
        )
    ]
