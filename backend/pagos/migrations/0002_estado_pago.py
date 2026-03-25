"""Agrega estado de pago.

Fecha:
    01 - 02 - 2026
"""

from django.db import migrations, models


class Migration(migrations.Migration):
    """Agregar estado_pago a pagos."""

    dependencies = [
        ("pagos", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="pago",
            name="estado_pago",
            field=models.CharField(
                choices=[
                    ("Aprobado", "Aprobado"),
                    ("Pendiente", "Pendiente"),
                    ("Parcial", "Parcial"),
                ],
                db_column="estado_pago",
                default="Pendiente",
                max_length=20,
            ),
        ),
        migrations.AddConstraint(
            model_name="pago",
            constraint=models.CheckConstraint(
                condition=models.Q(estado_pago__in=["Aprobado", "Pendiente", "Parcial"]),
                name="pagos_estado_pago_valido",
            ),
        ),
    ]
