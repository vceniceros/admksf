"""Actualiza restricción de tipo de unidad para incluir PH.

Fecha:
    14 - 02 - 2026
"""

from django.db import migrations, models


class Migration(migrations.Migration):
    """Actualiza la restricción de tipo_de_unidad."""

    dependencies = [
        ("unidades_funcionales", "0002_tipo_unidad_check"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="unidadfuncional",
            name="unidades_funcionales_tipo_valido",
        ),
        migrations.AddConstraint(
            model_name="unidadfuncional",
            constraint=models.CheckConstraint(
                condition=models.Q(tipo_de_unidad__in=["Departamento", "Lote", "PH"]),
                name="unidades_funcionales_tipo_valido",
            ),
        ),
    ]
