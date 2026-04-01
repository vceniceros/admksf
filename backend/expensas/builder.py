"""Builder de la liquidación de expensas.

Fecha:
    14 - 02 - 2026
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Dict, Iterable, List, Mapping

from django.core.exceptions import ValidationError

from consorcios.models import Consorcio
from gastos.models import Gasto
from saldo_mensual.models import SaldoMensual
from unidades_funcionales.models import UnidadFuncional

from .strategies import (
    CompoundInterestStrategy,
    EarlyPaymentStrategy,
    NoRoundingStrategy,
    RoundingStrategy,
    SimpleInterestStrategy,
    StepRoundingStrategy,
    CeilingRoundingStrategy,
    FloorRoundingStrategy,
)
from .utils import evaluate_expression, parse_decimal


@dataclass
class ColumnResult:
    """Representa el resultado de una columna para una UF."""

    column_id: str
    value: Decimal


class LiquidacionBuilder:
    """Construye el resultado de una liquidación con base en metadata."""

    def __init__(
        self,
        consorcio: Consorcio,
        periodo,
        template_config: Mapping[str, Any],
        parametros: Mapping[str, Any] | None = None,
    ) -> None:
        self.consorcio = consorcio
        self.periodo = periodo
        self.template_config = template_config
        self.parametros = parametros or {}
        self.columns = list(self.template_config.get("columns", []))

        self._conceptos_particulares = self._build_conceptos_particulares()
        self._custom_coeficientes = self.parametros.get("coeficientes_custom", {})
        self._rounding_strategy = self._build_rounding_strategy()

    def build(self) -> Dict[str, Any]:
        """Ejecuta el proceso de liquidación y devuelve el JSON final."""

        unidades = list(
            UnidadFuncional.objects.filter(consorcio=self.consorcio).select_related("propietario")
        )
        total_superficie = sum((uf.superficie for uf in unidades), Decimal("0"))
        gastos_por_tipo, total_gastos = self._aggregate_gastos()

        resultados_unidades = []
        totales_columnas: Dict[str, Decimal] = {col["id"]: Decimal("0") for col in self.columns}

        for uf in unidades:
            coef_superficie = (
                (uf.superficie / total_superficie) if total_superficie else Decimal("0")
            )
            context: Dict[str, Decimal] = {
                "coeficiente": coef_superficie,
                "coeficiente_superficie": coef_superficie,
                "saldo_anterior": self._get_saldo_anterior(uf),
            }
            valores: Dict[str, Decimal] = {}

            for column in self.columns:
                col_id = column.get("id")
                calc_type = column.get("calc_type") or column.get("tipo_calculo")
                if not col_id or not calc_type:
                    raise ValidationError("Columna inválida: falta id o tipo de cálculo.")
                value = self._calculate_column(
                    column,
                    calc_type,
                    context,
                    gastos_por_tipo,
                    total_gastos,
                    uf,
                )
                if column.get("apply_rounding", False):
                    value = self._rounding_strategy.apply(value)
                value = value.quantize(Decimal("0.01"))
                valores[col_id] = value
                context[col_id] = value
                totales_columnas[col_id] += value

            resultados_unidades.append(
                {
                    "numero_unidad_funcional": uf.numero_de_unidad_funcional,
                    "propietario": uf.propietario.nombre,
                    "apellido": uf.propietario.apellido,
                    "valores": {key: str(val) for key, val in valores.items()},
                }
            )

        totales_serializados = {key: str(val.quantize(Decimal("0.01"))) for key, val in totales_columnas.items()}

        return {
            "consorcio": self.consorcio.cuit,
            "periodo": self.periodo.isoformat(),
            "columns": [
                {
                    "id": col["id"],
                    "label": col.get("label", col["id"]),
                    "visible": col.get("visible", True),
                    "calc_type": col.get("calc_type") or col.get("tipo_calculo"),
                }
                for col in self.columns
            ],
            "unidades": resultados_unidades,
            "totales": totales_serializados,
        }

    def _build_conceptos_particulares(self) -> Dict[int, Dict[str, Decimal]]:
        conceptos = {}
        for item in self.parametros.get("conceptos_particulares", []):
            numero = item.get("unidad")
            column_id = item.get("column_id")
            if numero is None or not column_id:
                continue
            conceptos.setdefault(numero, {})[column_id] = parse_decimal(item.get("monto", 0))
        return conceptos

    def _aggregate_gastos(self) -> tuple[Dict[str, Decimal], Decimal]:
        gastos = Gasto.objects.filter(
            consorcio=self.consorcio,
            periodo__year=self.periodo.year,
            periodo__month=self.periodo.month,
        )
        gastos_por_tipo: Dict[str, Decimal] = {}
        total = Decimal("0")
        for gasto in gastos:
            gastos_por_tipo.setdefault(gasto.tipo_gasto, Decimal("0"))
            gastos_por_tipo[gasto.tipo_gasto] += gasto.monto
            total += gasto.monto
        return gastos_por_tipo, total

    def _get_saldo_anterior(self, uf: UnidadFuncional) -> Decimal:
        saldo = (
            SaldoMensual.objects.filter(
                consorcio=self.consorcio,
                numero_de_unidad_funcional=uf.numero_de_unidad_funcional,
                mes_anio__lt=self.periodo,
            )
            .order_by("-mes_anio")
            .first()
        )
        if saldo and saldo.saldo_final is not None:
            return saldo.saldo_final
        return Decimal("0")

    def _calculate_column(
        self,
        column: Mapping[str, Any],
        calc_type: str,
        context: Dict[str, Decimal],
        gastos_por_tipo: Mapping[str, Decimal],
        total_gastos: Decimal,
        uf: UnidadFuncional,
    ) -> Decimal:
        unidad_numero = uf.numero_de_unidad_funcional
        if calc_type == "saldo_anterior":
            return context.get("saldo_anterior", Decimal("0"))
        if calc_type == "interes":
            return self._calculate_interes(column, context)
        if calc_type == "prorrateo":
            return self._calculate_prorrateo(column, gastos_por_tipo, total_gastos, context, uf)
        if calc_type == "fijo":
            return parse_decimal(column.get("valor", 0))
        if calc_type == "concepto_particular":
            return self._conceptos_particulares.get(unidad_numero, {}).get(column.get("id"), Decimal("0"))
        if calc_type == "formula":
            expression = column.get("expr") or column.get("formula")
            if not expression:
                raise ValidationError("Falta expresión en columna de fórmula.")
            return evaluate_expression(expression, context)
        raise ValidationError(f"Tipo de cálculo no soportado: {calc_type}")

    def _calculate_prorrateo(
        self,
        column: Mapping[str, Any],
        gastos_por_tipo: Mapping[str, Decimal],
        total_gastos: Decimal,
        context: Dict[str, Decimal],
        uf: UnidadFuncional,
    ) -> Decimal:
        gasto_tipo = column.get("gasto_tipo")
        base_gasto = total_gastos if not gasto_tipo else gastos_por_tipo.get(gasto_tipo, Decimal("0"))
        coef_type = column.get("coeficiente", "superficie")
        if coef_type == "custom":
            coef_val = parse_decimal(
                self._custom_coeficientes.get(str(uf.numero_de_unidad_funcional), uf.coeficiente)
            )
        else:
            coef_val = context.get("coeficiente_superficie", Decimal("0"))
        return base_gasto * coef_val

    def _calculate_interes(self, column: Mapping[str, Any], context: Dict[str, Decimal]) -> Decimal:
        metodo = column.get("metodo", "simple")
        base_key = column.get("base", "saldo_anterior")
        rate_raw = column.get("tasa", "consorcio.interes_por_mora")
        periods = int(column.get("periodos", 1))
        base_value = context.get(base_key, Decimal("0"))

        if isinstance(rate_raw, str) and rate_raw == "consorcio.interes_por_mora":
            rate = self.consorcio.interes_por_mora
        else:
            rate = parse_decimal(rate_raw, "tasa")

        strategy = self._get_interest_strategy(metodo)
        return strategy.calculate(base_value, rate, periods)

    def _get_interest_strategy(self, metodo: str):
        if metodo == "compuesto":
            return CompoundInterestStrategy()
        if metodo == "pronto_pago":
            return EarlyPaymentStrategy()
        return SimpleInterestStrategy()

    def _build_rounding_strategy(self) -> RoundingStrategy:
        rounding = self.template_config.get("rounding", {})
        metodo = rounding.get("metodo", "none")
        if metodo == "step":
            increment = parse_decimal(rounding.get("increment", "0.01"), "increment")
            return StepRoundingStrategy(increment)
        if metodo == "ceil":
            return CeilingRoundingStrategy()
        if metodo == "floor":
            return FloorRoundingStrategy()
        return NoRoundingStrategy()
