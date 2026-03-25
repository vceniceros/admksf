"""Modelos de la app reparaciones_mantenimientos.

Fecha:
    27 - 01 - 2026
"""

from django.core.exceptions import ValidationError
from django.db import models

from shared import build_model_str, validate_regex_digits


class ReparacionMantenimiento(models.Model):
    """Especialización de proveedor para reparaciones y mantenimientos.

    Args:
        proveedor (Proveedor): Proveedor asociado (PK).
        numero_reclamo (str): Teléfono de reclamo.
    """

    proveedor = models.OneToOneField(
        "proveedores.Proveedor",
        on_delete=models.CASCADE,
        primary_key=True,
        db_column="cuit",
        to_field="cuit",
    )
    numero_reclamo = models.CharField(max_length=50, db_column="numero_reclamo")

    class Meta:
        db_table = "reparaciones_mantenimientos"
        verbose_name = "Reparación y mantenimiento"
        verbose_name_plural = "Reparaciones y mantenimientos"

    def clean(self) -> None:
        """Valida reglas de reparaciones/mantenimientos.

        Raises:
            ValidationError: Si el CUIT no cumple el formato.
        """

        super().clean()
        validate_regex_digits(self.proveedor_id, "CUIT")

    def __str__(self) -> str:
        """Devuelve una representación legible del registro.

        Returns:
            str: Texto descriptivo del registro.
        """

        return build_model_str(
            "ReparacionMantenimiento",
            [
                ("cuit", self.proveedor_id, True),
                ("numero_reclamo", self.numero_reclamo, True),
            ],
        )
