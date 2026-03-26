"""Modelos de la app expensas.

Fecha:
    14 - 02 - 2026
"""

from django.db import models

from shared import build_model_str


class RuleType(models.TextChoices):
    """Tipos de reglas permitidas en un template de expensas."""

    PRORRATEO = "Prorrateo", "Prorrateo"
    INTERES = "Interes", "Interés"
    REDONDEO = "Redondeo", "Redondeo"


class ExpensaTemplate(models.Model):
    """Representa un template de liquidación de expensas basado en metadata."""

    id_expensa_template = models.BigAutoField(
        primary_key=True,
        db_column="id_expensa_template",
    )
    consorcio = models.ForeignKey(
        "consorcios.Consorcio",
        on_delete=models.CASCADE,
        db_column="cuit_consorcio",
        to_field="cuit",
        null=True,
        blank=True,
    )
    nombre = models.CharField(max_length=120, db_column="nombre")
    version = models.PositiveIntegerField(db_column="version", default=1)
    config = models.JSONField(db_column="config")
    activo = models.BooleanField(db_column="activo", default=True)
    creado_en = models.DateTimeField(db_column="creado_en", auto_now_add=True)

    class Meta:
        db_table = "expensa_templates"
        verbose_name = "Template de expensa"
        verbose_name_plural = "Templates de expensa"
        constraints = [
            models.UniqueConstraint(
                fields=["consorcio", "nombre", "version"],
                name="expensa_template_consorcio_nombre_version_unique",
            )
        ]

    def __str__(self) -> str:
        return build_model_str(
            "ExpensaTemplate",
            [
                ("id_expensa_template", self.id_expensa_template, False),
                ("cuit_consorcio", self.consorcio_id, True),
                ("nombre", self.nombre, False),
                ("version", self.version, False),
                ("activo", self.activo, False),
                ("creado_en", self.creado_en, False),
            ],
        )


class ExpensaRule(models.Model):
    """Reglas asociadas a un template de expensa."""

    id_expensa_rule = models.BigAutoField(
        primary_key=True,
        db_column="id_expensa_rule",
    )
    template = models.ForeignKey(
        ExpensaTemplate,
        on_delete=models.CASCADE,
        related_name="rules",
        db_column="id_expensa_template",
    )
    nombre = models.CharField(max_length=120, db_column="nombre")
    tipo = models.CharField(
        max_length=20,
        choices=RuleType.choices,
        db_column="tipo",
    )
    config = models.JSONField(db_column="config")
    orden = models.PositiveIntegerField(db_column="orden", default=0)

    class Meta:
        db_table = "expensa_rules"
        verbose_name = "Regla de expensa"
        verbose_name_plural = "Reglas de expensa"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(tipo__in=list(RuleType.values)),
                name="expensa_rules_tipo_valido",
            )
        ]

    def __str__(self) -> str:
        return build_model_str(
            "ExpensaRule",
            [
                ("id_expensa_rule", self.id_expensa_rule, False),
                ("id_expensa_template", self.template_id, False),
                ("nombre", self.nombre, False),
                ("tipo", self.tipo, False),
                ("orden", self.orden, False),
            ],
        )


class EstadoLiquidacion(models.TextChoices):
    """Estados permitidos de una liquidación de expensas."""

    BORRADOR = "BORRADOR", "Borrador"
    EN_EDICION = "EN_EDICION", "En edición"
    CERRADA = "CERRADA", "Cerrada"


class LiquidacionExpensa(models.Model):
    """Resultado inmutable de una liquidación de expensas."""

    id_liquidacion_expensa = models.BigAutoField(
        primary_key=True,
        db_column="id_liquidacion_expensa",
    )
    consorcio = models.ForeignKey(
        "consorcios.Consorcio",
        on_delete=models.CASCADE,
        db_column="cuit_consorcio",
        to_field="cuit",
    )
    template = models.ForeignKey(
        ExpensaTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="id_expensa_template",
    )
    periodo = models.DateField(db_column="periodo")
    resultado = models.JSONField(db_column="resultado")
    template_snapshot = models.JSONField(db_column="template_snapshot")
    creada_en = models.DateTimeField(db_column="creada_en", auto_now_add=True)
    cerrada = models.BooleanField(db_column="cerrada", default=False)
    estado = models.CharField(
        max_length=20,
        db_column="estado",
        choices=EstadoLiquidacion.choices,
        default=EstadoLiquidacion.BORRADOR,
    )

    class Meta:
        db_table = "liquidaciones_expensa"
        verbose_name = "Liquidación de expensa"
        verbose_name_plural = "Liquidaciones de expensa"

    def __str__(self) -> str:
        return build_model_str(
            "LiquidacionExpensa",
            [
                ("id_liquidacion_expensa", self.id_liquidacion_expensa, False),
                ("cuit_consorcio", self.consorcio_id, True),
                ("id_expensa_template", self.template_id, False),
                ("periodo", self.periodo, False),
                ("cerrada", self.cerrada, False),
                ("creada_en", self.creada_en, False),
            ],
        )
