"""Migración inicial de expensas.

Resumen:
    Crea templates, reglas y liquidaciones de expensas.

Fecha:
    14 - 02 - 2026
"""

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    """Migración inicial para la app expensas."""

    initial = True

    dependencies = [
        ("consorcios", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ExpensaTemplate",
            fields=[
                (
                    "id_expensa_template",
                    models.BigAutoField(
                        db_column="id_expensa_template",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("nombre", models.CharField(db_column="nombre", max_length=120)),
                ("version", models.PositiveIntegerField(db_column="version", default=1)),
                ("config", models.JSONField(db_column="config")),
                ("activo", models.BooleanField(db_column="activo", default=True)),
                (
                    "creado_en",
                    models.DateTimeField(auto_now_add=True, db_column="creado_en"),
                ),
                (
                    "consorcio",
                    models.ForeignKey(
                        blank=True,
                        db_column="cuit_consorcio",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="consorcios.consorcio",
                        to_field="cuit",
                    ),
                ),
            ],
            options={
                "db_table": "expensa_templates",
                "verbose_name": "Template de expensa",
                "verbose_name_plural": "Templates de expensa",
                "constraints": [
                    models.UniqueConstraint(
                        fields=("consorcio", "nombre", "version"),
                        name="expensa_template_consorcio_nombre_version_unique",
                    )
                ],
            },
        ),
        migrations.CreateModel(
            name="ExpensaRule",
            fields=[
                (
                    "id_expensa_rule",
                    models.BigAutoField(
                        db_column="id_expensa_rule",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("nombre", models.CharField(db_column="nombre", max_length=120)),
                (
                    "tipo",
                    models.CharField(
                        choices=[("Prorrateo", "Prorrateo"), ("Interes", "Interés"), ("Redondeo", "Redondeo")],
                        db_column="tipo",
                        max_length=20,
                    ),
                ),
                ("config", models.JSONField(db_column="config")),
                ("orden", models.PositiveIntegerField(db_column="orden", default=0)),
                (
                    "template",
                    models.ForeignKey(
                        db_column="id_expensa_template",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="rules",
                        to="expensas.expensatemplate",
                    ),
                ),
            ],
            options={
                "db_table": "expensa_rules",
                "verbose_name": "Regla de expensa",
                "verbose_name_plural": "Reglas de expensa",
                "constraints": [
                    models.CheckConstraint(
                        condition=models.Q(tipo__in=["Prorrateo", "Interes", "Redondeo"]),
                        name="expensa_rules_tipo_valido",
                    )
                ],
            },
        ),
        migrations.CreateModel(
            name="LiquidacionExpensa",
            fields=[
                (
                    "id_liquidacion_expensa",
                    models.BigAutoField(
                        db_column="id_liquidacion_expensa",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("periodo", models.DateField(db_column="periodo")),
                ("resultado", models.JSONField(db_column="resultado")),
                ("template_snapshot", models.JSONField(db_column="template_snapshot")),
                (
                    "creada_en",
                    models.DateTimeField(auto_now_add=True, db_column="creada_en"),
                ),
                ("cerrada", models.BooleanField(db_column="cerrada", default=False)),
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
                    "template",
                    models.ForeignKey(
                        blank=True,
                        db_column="id_expensa_template",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="expensas.expensatemplate",
                    ),
                ),
            ],
            options={
                "db_table": "liquidaciones_expensa",
                "verbose_name": "Liquidación de expensa",
                "verbose_name_plural": "Liquidaciones de expensa",
            },
        ),
    ]
