"""Modelos de la app pagos.

Fecha:
    27 - 01 - 2026
"""

from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from shared import (
    build_model_str,
    min_value_validator,
    validate_positive_decimal,
)


class EstadoPago(models.TextChoices):
    """Estados permitidos de un pago."""

    APROBADO = "Aprobado", "Aprobado"
    PENDIENTE = "Pendiente", "Pendiente"
    PARCIAL = "Parcial", "Parcial"


class Pago(models.Model):
    """Representa un pago realizado por un propietario.

    Args:
        id_pago (int): Identificador del pago.
        numero_de_unidad_funcional (int): Número de unidad funcional.
        consorcio (Consorcio): Consorcio asociado.
        propietario (Propietario): Propietario asociado.
        monto (Decimal): Monto del pago (> 0).
        fecha_pago (datetime): Fecha del pago.
    """

    id_pago = models.BigAutoField(primary_key=True, db_column="id_pago")
    numero_de_unidad_funcional = models.IntegerField(db_column="numero_de_unidad_funcional")
    consorcio = models.ForeignKey(
        "consorcios.Consorcio",
        on_delete=models.CASCADE,
        db_column="cuit_consorcio",
        to_field="cuit",
    )
    propietario = models.ForeignKey(
        "propietarios.Propietario",
        on_delete=models.CASCADE,
        db_column="dni_propietario",
        to_field="dni",
    )
    monto = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        db_column="monto",
        validators=[min_value_validator(Decimal("0.01"), "Monto")],
    )
    estado_pago = models.CharField(
        max_length=20,
        db_column="estado_pago",
        choices=EstadoPago.choices,
        default=EstadoPago.PENDIENTE,
    )
    fecha_pago = models.DateTimeField(db_column="fecha_pago", default=timezone.now)

    class Meta:
        db_table = "pagos"
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(monto__gt=0),
                name="pagos_monto_gt_0",
            ),
            models.CheckConstraint(
                condition=models.Q(estado_pago__in=list(EstadoPago.values)),
                name="pagos_estado_pago_valido",
            ),
            models.UniqueConstraint(
                fields=["id_pago", "numero_de_unidad_funcional", "consorcio"],
                name="pagos_id_unidad_consorcio_unique",
            ),
        ]

    def clean(self) -> None:
        """Valida reglas del pago.

        Raises:
            ValidationError: Si el monto no es válido.
        """

        super().clean()
        validate_positive_decimal(self.monto, "Monto")

    def __str__(self) -> str:
        """Devuelve una representación legible del pago.

        Returns:
            str: Texto descriptivo del pago.
        """

        return build_model_str(
            "Pago",
            [
                ("id_pago", self.id_pago, False),
                ("numero_de_unidad_funcional", self.numero_de_unidad_funcional, False),
                ("cuit_consorcio", self.consorcio_id, True),
                ("dni_propietario", self.propietario_id, True),
                ("monto", self.monto, False),
                ("estado_pago", self.estado_pago, False),
                ("fecha_pago", self.fecha_pago, False),
            ],
        )
