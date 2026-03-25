"""Migración inicial de reparaciones_mantenimientos.

Resumen:
    Crea la tabla reparaciones_mantenimientos y su relación con proveedores.

Fecha:
    27 - 01 - 2026
"""

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    """Migración inicial para la app reparaciones_mantenimientos."""

    initial = True

    dependencies = [
        ("proveedores", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ReparacionMantenimiento",
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
                    "numero_reclamo",
                    models.CharField(db_column="numero_reclamo", max_length=50),
                ),
            ],
            options={
                "db_table": "reparaciones_mantenimientos",
                "verbose_name": "Reparación y mantenimiento",
                "verbose_name_plural": "Reparaciones y mantenimientos",
            },
        )
    ]
