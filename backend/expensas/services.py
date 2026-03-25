"""Servicios para el motor de expensas.

Fecha:
    14 - 02 - 2026
"""

from __future__ import annotations

from django.core.exceptions import ValidationError

from consorcios.models import Consorcio

from .builder import LiquidacionBuilder
from .models import ExpensaTemplate, LiquidacionExpensa
from .utils import parse_period


class LiquidacionService:
    """Servicio principal para liquidar expensas."""

    @staticmethod
    def liquidar(payload: dict) -> dict:
        """Ejecuta la liquidación con base en un template y parámetros."""

        try:
            template_id = payload.get("template_id")
            consorcio_cuit = payload.get("consorcio")
            periodo_raw = payload.get("periodo")
            cerrar = payload.get("cerrar", False)
            parametros = payload.get("parametros", {})

            if not template_id or not consorcio_cuit or not periodo_raw:
                raise ValidationError("template_id, consorcio y periodo son obligatorios.")

            template = ExpensaTemplate.objects.get(pk=template_id)
            consorcio = Consorcio.objects.get(pk=consorcio_cuit)
            periodo = parse_period(periodo_raw)

            builder = LiquidacionBuilder(consorcio, periodo, template.config, parametros)
            resultado = builder.build()
            resultado["template_id"] = template_id

            if cerrar:
                LiquidacionExpensa.objects.create(
                    consorcio=consorcio,
                    template=template,
                    periodo=periodo,
                    resultado=resultado,
                    template_snapshot=template.config,
                    cerrada=True,
                )
            return resultado
        except ExpensaTemplate.DoesNotExist as exc:
            raise ValidationError("Template no encontrado.") from exc
        except Consorcio.DoesNotExist as exc:
            raise ValidationError("Consorcio no encontrado.") from exc
