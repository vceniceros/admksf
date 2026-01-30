"""Migración inicial de unidades_funcionales.

Resumen:
    Crea la tabla unidades_funcionales con relaciones y restricciones.

Fecha:
    27 - 01 - 2026
"""

from decimal import Decimal

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    """Migración inicial para la app unidades_funcionales."""

    initial = True

    dependencies = [
        ("consorcios", "0001_initial"),
        ("propietarios", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="UnidadFuncional",
            fields=[
                (
                    "numero_de_unidad_funcional",
                    models.IntegerField(
                        db_column="numero_de_unidad_funcional",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "tipo_de_unidad",
                    models.CharField(db_column="tipo_de_unidad", max_length=50),
                ),
                (
                    "estado_de_vivienda",
                    models.CharField(
                        choices=[
                            ("Propietario", "Propietario"),
                            ("Inquilino", "Inquilino"),
                            ("Vacio", "Vacío"),
                        ],
                        db_column="estado_de_vivienda",
                        max_length=50,
                    ),
                ),
                (
                    "superficie",
                    models.DecimalField(
                        db_column="superficie",
                        decimal_places=2,
                        max_digits=7,
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
                "db_table": "unidades_funcionales",
                "verbose_name": "Unidad funcional",
                "verbose_name_plural": "Unidades funcionales",
                "constraints": [
                    models.CheckConstraint(
                        check=models.Q(
                            estado_de_vivienda__in=["Propietario", "Inquilino", "Vacio"]
                        ),
                        name="unidades_funcionales_estado_valido",
                    ),
                    models.CheckConstraint(
                        check=models.Q(superficie__gt=Decimal("0")),
                        name="unidades_funcionales_superficie_gt_0",
                    ),
                    models.UniqueConstraint(
                        fields=["numero_de_unidad_funcional", "consorcio"],
                        name="unidades_funcionales_numero_consorcio_unique",
                    ),
                ],
            },
        )
    ]
