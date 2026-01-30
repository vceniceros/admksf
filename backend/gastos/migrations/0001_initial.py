"""Migración inicial de gastos.

Resumen:
    Crea la tabla gastos con relaciones y restricciones.

Fecha:
    27 - 01 - 2026
"""

from decimal import Decimal

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    """Migración inicial para la app gastos."""

    initial = True

    dependencies = [
        ("consorcios", "0001_initial"),
        ("proveedores", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Gasto",
            fields=[
                (
                    "id_gasto",
                    models.BigAutoField(
                        db_column="id_gasto",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("periodo", models.DateField(db_column="periodo")),
                (
                    "descripcion",
                    models.TextField(db_column="descripcion"),
                ),
                (
                    "monto",
                    models.DecimalField(
                        db_column="monto",
                        decimal_places=2,
                        max_digits=10,
                    ),
                ),
                (
                    "fecha_registro",
                    models.DateTimeField(
                        db_column="fecha_registro",
                        default=django.utils.timezone.now,
                    ),
                ),
                (
                    "tipo_gasto",
                    models.CharField(
                        choices=[
                            ("Mantenimiento", "Mantenimiento"),
                            ("Servicios", "Servicios"),
                            ("Limpieza", "Limpieza"),
                            ("Seguridad", "Seguridad"),
                            ("Administracion", "Administración"),
                            ("Otros", "Otros"),
                        ],
                        db_column="tipo_gasto",
                        default="Otros",
                        max_length=20,
                    ),
                ),
                (
                    "estado_pago",
                    models.CharField(
                        choices=[("Pendiente", "Pendiente"), ("Pagado", "Pagado")],
                        db_column="estado_pago",
                        default="Pendiente",
                        max_length=20,
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
                    "proveedor",
                    models.ForeignKey(
                        db_column="cuit_proveedor",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="proveedores.proveedor",
                        to_field="cuit",
                    ),
                ),
            ],
            options={
                "db_table": "gastos",
                "verbose_name": "Gasto",
                "verbose_name_plural": "Gastos",
                "constraints": [
                    models.CheckConstraint(
                        check=models.Q(monto__gt=Decimal("0")),
                        name="gastos_monto_gt_0",
                    ),
                    models.CheckConstraint(
                        check=models.Q(
                            tipo_gasto__in=[
                                "Mantenimiento",
                                "Servicios",
                                "Limpieza",
                                "Seguridad",
                                "Administracion",
                                "Otros",
                            ]
                        ),
                        name="gastos_tipo_gasto_valido",
                    ),
                    models.CheckConstraint(
                        check=models.Q(estado_pago__in=["Pendiente", "Pagado"]),
                        name="gastos_estado_pago_valido",
                    ),
                ],
            },
        )
    ]
