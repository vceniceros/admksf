"""Modelos de la app proveedores.

Fecha:
    27 - 01 - 2026
"""

from django.core.exceptions import ValidationError
from django.db import models

from shared import (
    build_model_str,
    digits_only_validator,
    max_value_validator,
    min_value_validator,
    validate_range,
    validate_regex_digits,
)


class TipoProveedor(models.TextChoices):
    """Tipos de proveedor permitidos."""

    SERVICIOS_MENSUALES = "servicios_mensuales", "Servicios mensuales"
    REPARACIONES_MANTENIMIENTOS = (
        "reparaciones_mantenimientos",
        "Reparaciones y mantenimientos",
    )


class Proveedor(models.Model):
    """Representa un proveedor de servicios o reparaciones.

    Args:
        cuit (str): CUIT del proveedor. Solo dígitos.
        razon_social (str): Razón social.
        telefono (str | None): Teléfono de contacto.
        email (str | None): Email de contacto.
        calle (str): Calle del domicilio.
        numero (int): Número de calle.
        codigo_postal (str): Código postal.
        ciudad (str): Ciudad.
        tipo_proveedor (str): Tipo de proveedor.
    """

    cuit = models.CharField(
        max_length=11,
        primary_key=True,
        db_column="cuit",
        validators=[digits_only_validator("CUIT")],
    )
    razon_social = models.CharField(max_length=100, db_column="razon_social")
    telefono = models.CharField(max_length=20, db_column="telefono", null=True, blank=True)
    email = models.EmailField(max_length=100, db_column="email", null=True, blank=True)
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
    tipo_proveedor = models.CharField(
        max_length=30,
        db_column="tipo_proveedor",
        choices=TipoProveedor.choices,
    )

    class Meta:
        db_table = "proveedores"
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        constraints = [
            models.CheckConstraint(
                check=models.Q(numero__gt=0, numero__lt=60000),
                name="proveedores_numero_rango",
            ),
            models.CheckConstraint(
                check=models.Q(cuit__regex=r"^\d+$"),
                name="proveedores_cuit_solo_digitos",
            ),
            models.CheckConstraint(
                check=models.Q(
                    tipo_proveedor__in=[
                        TipoProveedor.SERVICIOS_MENSUALES,
                        TipoProveedor.REPARACIONES_MANTENIMIENTOS,
                    ]
                ),
                name="proveedores_tipo_proveedor_valido",
            ),
        ]

    def clean(self) -> None:
        """Valida reglas del proveedor.

        Raises:
            ValidationError: Si alguna regla no se cumple.
        """

        super().clean()
        validate_range(self.numero, 1, 59999, "Número")
        validate_regex_digits(self.cuit, "CUIT")

    def __str__(self) -> str:
        """Devuelve una representación legible del proveedor.

        Returns:
            str: Texto descriptivo del proveedor.
        """

        return build_model_str(
            "Proveedor",
            [
                ("cuit", self.cuit, True),
                ("razon_social", self.razon_social, False),
                ("telefono", self.telefono, True),
                ("email", self.email, True),
                ("calle", self.calle, False),
                ("numero", self.numero, False),
                ("codigo_postal", self.codigo_postal, False),
                ("ciudad", self.ciudad, False),
                ("tipo_proveedor", self.tipo_proveedor, False),
            ],
        )
