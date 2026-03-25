"""Migración inicial de servicios_mensuales.

Resumen:
    Crea la tabla servicios_mensuales y su relación con proveedores.

Fecha:
    27 - 01 - 2026
"""

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    """Migración inicial para la app servicios_mensuales."""

    initial = True

    dependencies = [
        ("proveedores", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ServicioMensual",
            fields=[
                (
                    "proveedor",
                    models.OneToOneField(
                        db_column="cuit",
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="proveedores.proveedor",
                        to_field="cuit",
                    ),
                ),
                (
                    "numero_cuenta",
                    models.CharField(db_column="numero_cuenta", max_length=50),
                ),
                (
                    "numero_reclamo",
                    models.CharField(db_column="numero_reclamo", max_length=50),
                ),
            ],
            options={
                "db_table": "servicios_mensuales",
                "verbose_name": "Servicio mensual",
                "verbose_name_plural": "Servicios mensuales",
            },
        )
    ]
