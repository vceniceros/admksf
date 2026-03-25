"""Agrega restricción de tipo de unidad.

Fecha:
    01 - 02 - 2026
"""

from django.db import migrations, models


class Migration(migrations.Migration):
    """Restricción para tipo_de_unidad."""

    dependencies = [
        ("unidades_funcionales", "0001_initial"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="unidadfuncional",
            constraint=models.CheckConstraint(
                condition=models.Q(tipo_de_unidad__in=["Departamento", "Lote"]),
                name="unidades_funcionales_tipo_valido",
            ),
        ),
    ]
