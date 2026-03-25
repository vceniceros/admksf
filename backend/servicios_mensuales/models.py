"""Modelos de la app servicios_mensuales.

Fecha:
    27 - 01 - 2026
"""

from django.core.exceptions import ValidationError
from django.db import models

from shared import build_model_str, validate_regex_digits


class ServicioMensual(models.Model):
    """Especialización de proveedor para servicios mensuales.

    Args:
        proveedor (Proveedor): Proveedor asociado (PK).
        numero_cuenta (str): Número de cuenta.
        numero_reclamo (str): Teléfono de reclamo.
    """

    proveedor = models.OneToOneField(
        "proveedores.Proveedor",
        on_delete=models.CASCADE,
        primary_key=True,
        db_column="cuit",
        to_field="cuit",
    )
    numero_cuenta = models.CharField(max_length=50, db_column="numero_cuenta")
    numero_reclamo = models.CharField(max_length=50, db_column="numero_reclamo")

    class Meta:
        db_table = "servicios_mensuales"
        verbose_name = "Servicio mensual"
        verbose_name_plural = "Servicios mensuales"

    def clean(self) -> None:
        """Valida reglas del servicio mensual.

        Raises:
            ValidationError: Si el CUIT no cumple el formato.
        """

        super().clean()
        validate_regex_digits(self.proveedor_id, "CUIT")

    def __str__(self) -> str:
        """Devuelve una representación legible del servicio mensual.

        Returns:
            str: Texto descriptivo del servicio mensual.
        """

        return build_model_str(
            "ServicioMensual",
            [
                ("cuit", self.proveedor_id, True),
                ("numero_cuenta", self.numero_cuenta, False),
                ("numero_reclamo", self.numero_reclamo, False),
            ],
        )
