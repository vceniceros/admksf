"""Migración inicial de caratula.

Resumen:
    Crea la tabla caratula y su relación con consorcios.

Fecha:
    27 - 01 - 2026
"""

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    """Migración inicial para la app caratula."""

    initial = True

    dependencies = [
        ("consorcios", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Caratula",
            fields=[
                (
                    "fecha_caratula",
                    models.DateTimeField(
                        db_column="fecha_caratula",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "texto_caratula",
                    models.TextField(db_column="texto_caratula"),
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
                "db_table": "caratula",
                "verbose_name": "Carátula",
                "verbose_name_plural": "Carátulas",
            },
        )
    ]
