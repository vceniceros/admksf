"""Modelos de la app unidades_funcionales.

Fecha:
    27 - 01 - 2026
"""

from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models

from shared import (
    build_model_str,
    min_value_validator,
    validate_positive_decimal,
)


class EstadoVivienda(models.TextChoices):
    """Estados permitidos de una unidad funcional."""

    PROPIETARIO = "Propietario", "Propietario"
    INQUILINO = "Inquilino", "Inquilino"
    VACIO = "Vacio", "Vacío"


class UnidadFuncional(models.Model):
    """Representa una unidad funcional de un consorcio.

    Args:
        numero_de_unidad_funcional (int): Número de la unidad funcional.
        consorcio (Consorcio): Consorcio al que pertenece.
        tipo_de_unidad (str): Tipo de unidad.
        estado_de_vivienda (str): Estado de vivienda.
        superficie (Decimal): Superficie en m² (> 0).
        propietario (Propietario): Propietario asociado.
    """

    numero_de_unidad_funcional = models.IntegerField(
        primary_key=True,
        db_column="numero_de_unidad_funcional",
    )
    consorcio = models.ForeignKey(
        "consorcios.Consorcio",
        on_delete=models.CASCADE,
        db_column="cuit_consorcio",
        to_field="cuit",
    )
    tipo_de_unidad = models.CharField(max_length=50, db_column="tipo_de_unidad")
    estado_de_vivienda = models.CharField(
        max_length=50,
        db_column="estado_de_vivienda",
        choices=EstadoVivienda.choices,
    )
    superficie = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        db_column="superficie",
        validators=[min_value_validator(Decimal("0.01"), "Superficie")],
    )
    propietario = models.ForeignKey(
        "propietarios.Propietario",
        on_delete=models.CASCADE,
        db_column="dni_propietario",
        to_field="dni",
    )

    class Meta:
        db_table = "unidades_funcionales"
        verbose_name = "Unidad funcional"
        verbose_name_plural = "Unidades funcionales"
        constraints = [
            models.CheckConstraint(
                check=models.Q(estado_de_vivienda__in=list(EstadoVivienda.values)),
                name="unidades_funcionales_estado_valido",
            ),
            models.CheckConstraint(
                check=models.Q(superficie__gt=0),
                name="unidades_funcionales_superficie_gt_0",
            ),
            models.UniqueConstraint(
                fields=["numero_de_unidad_funcional", "consorcio"],
                name="unidades_funcionales_numero_consorcio_unique",
            ),
        ]

    def clean(self) -> None:
        """Valida reglas de unidad funcional.

        Raises:
            ValidationError: Si la superficie no es válida.
        """

        super().clean()
        validate_positive_decimal(self.superficie, "Superficie")

    def __str__(self) -> str:
        """Devuelve una representación legible de la unidad funcional.

        Returns:
            str: Texto descriptivo de la unidad funcional.
        """

        return build_model_str(
            "UnidadFuncional",
            [
                ("numero_de_unidad_funcional", self.numero_de_unidad_funcional, False),
                ("cuit_consorcio", self.consorcio_id, True),
                ("tipo_de_unidad", self.tipo_de_unidad, False),
                ("estado_de_vivienda", self.estado_de_vivienda, False),
                ("superficie", self.superficie, False),
                ("dni_propietario", self.propietario_id, True),
            ],
        )
