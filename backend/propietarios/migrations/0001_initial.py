"""Migración inicial de propietarios.

Resumen:
    Crea la tabla propietarios con sus campos y restricciones.

Fecha:
    27 - 01 - 2026
"""

from django.db import migrations, models


class Migration(migrations.Migration):
    """Migración inicial para la app propietarios."""

    initial = True

    dependencies: list[tuple[str, str]] = []

    operations = [
        migrations.CreateModel(
            name="Propietario",
            fields=[
                (
                    "dni",
                    models.CharField(
                        db_column="dni",
                        max_length=15,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("nombre", models.CharField(db_column="nombre", max_length=50)),
                ("apellido", models.CharField(db_column="apellido", max_length=50)),
                (
                    "telefono",
                    models.CharField(blank=True, db_column="telefono", max_length=20, null=True),
                ),
                (
                    "email",
                    models.EmailField(blank=True, db_column="email", max_length=100, null=True),
                ),
            ],
            options={
                "db_table": "propietarios",
                "verbose_name": "Propietario",
                "verbose_name_plural": "Propietarios",
                "constraints": [
                    models.CheckConstraint(
                        check=models.Q(dni__regex=r"^\d+$"),
                        name="propietarios_dni_solo_digitos",
                    )
                ],
            },
        )
    ]
