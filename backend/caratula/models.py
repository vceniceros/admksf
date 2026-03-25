"""Modelos de la app caratula.

Fecha:
    27 - 01 - 2026
"""

from django.core.exceptions import ValidationError
from django.db import models

from shared import build_model_str


class Caratula(models.Model):
    """Representa una carátula para un consorcio.

    Args:
        fecha_caratula (datetime): Fecha de la carátula.
        consorcio (Consorcio): Consorcio asociado.
        texto_caratula (str): Texto de la carátula.
    """

    fecha_caratula = models.DateTimeField(primary_key=True, db_column="fecha_caratula")
    consorcio = models.ForeignKey(
        "consorcios.Consorcio",
        on_delete=models.CASCADE,
        db_column="cuit_consorcio",
        to_field="cuit",
    )
    texto_caratula = models.TextField(db_column="texto_caratula")

    class Meta:
        db_table = "caratula"
        verbose_name = "Carátula"
        verbose_name_plural = "Carátulas"

    def clean(self) -> None:
        """Valida reglas de carátula."""

        super().clean()

    def __str__(self) -> str:
        """Devuelve una representación legible de la carátula.

        Returns:
            str: Texto descriptivo de la carátula.
        """

        return build_model_str(
            "Caratula",
            [
                ("fecha_caratula", self.fecha_caratula, False),
                ("cuit_consorcio", self.consorcio_id, True),
                ("texto_caratula", self.texto_caratula, False),
            ],
        )
