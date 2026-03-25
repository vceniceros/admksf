"""Modelos de la app gastos.

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


class TipoGasto(models.TextChoices):
    """Tipos de gasto permitidos."""

    MANTENIMIENTO = "Mantenimiento", "Mantenimiento"
    SERVICIOS = "Servicios", "Servicios"
    LIMPIEZA = "Limpieza", "Limpieza"
    SEGURIDAD = "Seguridad", "Seguridad"
    ADMINISTRACION = "Administracion", "Administración"
    OTROS = "Otros", "Otros"


class EstadoPago(models.TextChoices):
    """Estados de pago permitidos."""

    PENDIENTE = "Pendiente", "Pendiente"
    PAGADO = "Pagado", "Pagado"


class Gasto(models.Model):
    """Representa un gasto registrado para un consorcio.

    Args:
        id_gasto (int): Identificador del gasto.
        consorcio (Consorcio): Consorcio asociado.
        proveedor (Proveedor): Proveedor asociado.
        periodo (date): Periodo del gasto.
        descripcion (str): Descripción del gasto.
        monto (Decimal): Monto del gasto (> 0).
        fecha_registro (datetime): Fecha de registro.
        tipo_gasto (str): Tipo del gasto.
        estado_pago (str): Estado del pago.
    """

    id_gasto = models.BigAutoField(primary_key=True, db_column="id_gasto")
    consorcio = models.ForeignKey(
        "consorcios.Consorcio",
        on_delete=models.CASCADE,
        db_column="cuit_consorcio",
        to_field="cuit",
    )
    proveedor = models.ForeignKey(
        "proveedores.Proveedor",
        on_delete=models.CASCADE,
        db_column="cuit_proveedor",
        to_field="cuit",
    )
    periodo = models.DateField(db_column="periodo")
    descripcion = models.TextField(db_column="descripcion")
    monto = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        db_column="monto",
        validators=[min_value_validator(Decimal("0.01"), "Monto")],
    )
    fecha_registro = models.DateTimeField(db_column="fecha_registro", default=timezone.now)
    tipo_gasto = models.CharField(
        max_length=20,
        db_column="tipo_gasto",
        choices=TipoGasto.choices,
        default=TipoGasto.OTROS,
    )
    estado_pago = models.CharField(
        max_length=20,
        db_column="estado_pago",
        choices=EstadoPago.choices,
        default=EstadoPago.PENDIENTE,
    )

    class Meta:
        db_table = "gastos"
        verbose_name = "Gasto"
        verbose_name_plural = "Gastos"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(monto__gt=0),
                name="gastos_monto_gt_0",
            ),
            models.CheckConstraint(
                condition=models.Q(tipo_gasto__in=list(TipoGasto.values)),
                name="gastos_tipo_gasto_valido",
            ),
            models.CheckConstraint(
                condition=models.Q(estado_pago__in=list(EstadoPago.values)),
                name="gastos_estado_pago_valido",
            ),
        ]

    def clean(self) -> None:
        """Valida reglas del gasto.

        Raises:
            ValidationError: Si el monto o estados no son válidos.
        """

        super().clean()
        validate_positive_decimal(self.monto, "Monto")

    def __str__(self) -> str:
        """Devuelve una representación legible del gasto.

        Returns:
            str: Texto descriptivo del gasto.
        """

        return build_model_str(
            "Gasto",
            [
                ("id_gasto", self.id_gasto, False),
                ("cuit_consorcio", self.consorcio_id, True),
                ("cuit_proveedor", self.proveedor_id, True),
                ("periodo", self.periodo, False),
                ("descripcion", self.descripcion, False),
                ("monto", self.monto, False),
                ("fecha_registro", self.fecha_registro, False),
                ("tipo_gasto", self.tipo_gasto, False),
                ("estado_pago", self.estado_pago, False),
            ],
        )
