"""Modelos de la app consorcios.

Fecha:
    27 - 01 - 2026
"""

from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models

from shared import (
    build_model_str,
    digits_only_validator,
    max_value_validator,
    min_value_validator,
    validate_non_negative_decimal,
    validate_range,
    validate_regex_digits,
)


class Consorcio(models.Model):
    """Representa un consorcio y sus parámetros financieros.

    Args:
        cuit (str): CUIT del consorcio. Solo dígitos.
        razon_social (str): Razón social del consorcio.
        calle (str): Calle del domicilio.
        numero (int): Número de calle.
        codigo_postal (str): Código postal.
        ciudad (str): Ciudad.
        interes_por_mora (Decimal): Interés por mora (>= 0).
        redondeo_aumento (Decimal): Redondeo de aumento (>= 0).
    """

    cuit = models.CharField(
        max_length=11,
        primary_key=True,
        db_column="cuit",
        validators=[digits_only_validator("CUIT")],
    )
    razon_social = models.CharField(max_length=100, db_column="razon_social")
    calle = models.CharField(max_length=100, db_column="calle")
    numero = models.PositiveIntegerField(
        db_column="numero",
        validators=[
            min_value_validator(1, "Número"),
            max_value_validator(59999, "Número"),
        ],
    )
    codigo_postal = models.CharField(max_length=10, db_column="codigo_postal")
    ciudad = models.CharField(max_length=50, db_column="ciudad")
    interes_por_mora = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        db_column="interes_por_mora",
        validators=[min_value_validator(Decimal("0"), "Interés por mora")],
    )
    redondeo_aumento = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        db_column="redondeo_aumento",
        validators=[min_value_validator(Decimal("0"), "Redondeo de aumento")],
    )

    class Meta:
        db_table = "consorcios"
        verbose_name = "Consorcio"
        verbose_name_plural = "Consorcios"
        constraints = [
            models.CheckConstraint(
                check=models.Q(numero__gt=0, numero__lt=60000),
                name="consorcios_numero_rango",
            ),
            models.CheckConstraint(
                check=models.Q(interes_por_mora__gte=0),
                name="consorcios_interes_mora_gte_0",
            ),
            models.CheckConstraint(
                check=models.Q(redondeo_aumento__gte=0),
                name="consorcios_redondeo_aumento_gte_0",
            ),
            models.CheckConstraint(
                check=models.Q(cuit__regex=r"^\d+$"),
                name="consorcios_cuit_solo_digitos",
            ),
        ]

    def clean(self) -> None:
        """Valida reglas de negocio adicionales del consorcio.

        Raises:
            ValidationError: Si alguna regla no se cumple.
        """

        super().clean()
        validate_range(self.numero, 1, 59999, "Número")
        validate_non_negative_decimal(self.interes_por_mora, "Interés por mora")
        validate_non_negative_decimal(self.redondeo_aumento, "Redondeo de aumento")
        validate_regex_digits(self.cuit, "CUIT")

    def __str__(self) -> str:
        """Devuelve una representación legible del consorcio.

        Returns:
            str: Texto descriptivo del consorcio.
        """

        return build_model_str(
            "Consorcio",
            [
                ("cuit", self.cuit, True),
                ("razon_social", self.razon_social, False),
                ("calle", self.calle, False),
                ("numero", self.numero, False),
                ("codigo_postal", self.codigo_postal, False),
                ("ciudad", self.ciudad, False),
                ("interes_por_mora", self.interes_por_mora, False),
                ("redondeo_aumento", self.redondeo_aumento, False),
            ],
        )
