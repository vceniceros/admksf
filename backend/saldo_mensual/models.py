"""Modelos de la app saldo_mensual.

Fecha:
    27 - 01 - 2026
"""

from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F

from shared import (
    build_model_str,
    min_value_validator,
    validate_non_negative_decimal,
)


class SaldoMensual(models.Model):
    """Representa el saldo mensual de una unidad funcional.

    Args:
        id_saldo_mensual (int): Identificador del saldo.
        numero_de_unidad_funcional (int): Número de unidad funcional.
        consorcio (Consorcio): Consorcio asociado.
        mes_anio (date): Mes y año del saldo.
        saldo_inicial (Decimal): Saldo inicial (>= 0).
        total_gastos (Decimal): Total de gastos (>= 0).
        total_pagos (Decimal): Total de pagos (>= 0).
        saldo_final (Decimal): Saldo final calculado.
        fecha_cierre (datetime | None): Fecha de cierre.
    """

    id_saldo_mensual = models.BigAutoField(primary_key=True, db_column="id_saldo_mensual")
    numero_de_unidad_funcional = models.IntegerField(db_column="numero_de_unidad_funcional")
    consorcio = models.ForeignKey(
        "consorcios.Consorcio",
        on_delete=models.CASCADE,
        db_column="cuit_consorcio",
        to_field="cuit",
    )
    mes_anio = models.DateField(db_column="mes_año")
    saldo_inicial = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        db_column="saldo_inicial",
        default=Decimal("0"),
        validators=[min_value_validator(Decimal("0"), "Saldo inicial")],
    )
    total_gastos = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        db_column="total_gastos",
        default=Decimal("0"),
        validators=[min_value_validator(Decimal("0"), "Total gastos")],
    )
    total_pagos = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        db_column="total_pagos",
        default=Decimal("0"),
        validators=[min_value_validator(Decimal("0"), "Total pagos")],
    )
    saldo_final = models.GeneratedField(
        expression=F("saldo_inicial") + F("total_gastos") - F("total_pagos"),
        output_field=models.DecimalField(max_digits=10, decimal_places=2),
        db_persist=True,
        db_column="saldo_final",
    )
    fecha_cierre = models.DateTimeField(db_column="fecha_cierre", null=True, blank=True)

    class Meta:
        db_table = "saldo_mensual"
        verbose_name = "Saldo mensual"
        verbose_name_plural = "Saldos mensuales"
        constraints = [
            models.CheckConstraint(
                check=models.Q(saldo_inicial__gte=0),
                name="saldo_mensual_saldo_inicial_gte_0",
            ),
            models.CheckConstraint(
                check=models.Q(total_gastos__gte=0),
                name="saldo_mensual_total_gastos_gte_0",
            ),
            models.CheckConstraint(
                check=models.Q(total_pagos__gte=0),
                name="saldo_mensual_total_pagos_gte_0",
            ),
            models.UniqueConstraint(
                fields=["numero_de_unidad_funcional", "consorcio", "mes_anio"],
                name="saldo_mensual_unidad_consorcio_mes_unique",
            ),
        ]

    def clean(self) -> None:
        """Valida reglas del saldo mensual.

        Raises:
            ValidationError: Si los importes son negativos.
        """

        super().clean()
        validate_non_negative_decimal(self.saldo_inicial, "Saldo inicial")
        validate_non_negative_decimal(self.total_gastos, "Total gastos")
        validate_non_negative_decimal(self.total_pagos, "Total pagos")

    def __str__(self) -> str:
        """Devuelve una representación legible del saldo mensual.

        Returns:
            str: Texto descriptivo del saldo mensual.
        """

        return build_model_str(
            "SaldoMensual",
            [
                ("id_saldo_mensual", self.id_saldo_mensual, False),
                ("numero_de_unidad_funcional", self.numero_de_unidad_funcional, False),
                ("cuit_consorcio", self.consorcio_id, True),
                ("mes_anio", self.mes_anio, False),
                ("saldo_inicial", self.saldo_inicial, False),
                ("total_gastos", self.total_gastos, False),
                ("total_pagos", self.total_pagos, False),
                ("saldo_final", self.saldo_final, False),
                ("fecha_cierre", self.fecha_cierre, False),
            ],
        )
