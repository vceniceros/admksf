"""Estrategias de cálculo para el motor de expensas.

Fecha:
    14 - 02 - 2026
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR


class InterestStrategy(ABC):
    """Interfaz base para estrategias de interés."""

    @abstractmethod
    def calculate(self, base: Decimal, rate: Decimal, periods: int = 1) -> Decimal:
        """Calcula interés sobre un capital base."""


class SimpleInterestStrategy(InterestStrategy):
    """Interés simple: base * tasa% * periodos."""

    def calculate(self, base: Decimal, rate: Decimal, periods: int = 1) -> Decimal:
        if base <= 0 or rate <= 0:
            return Decimal("0")
        return (base * rate * Decimal(periods) / Decimal("100"))


class CompoundInterestStrategy(InterestStrategy):
    """Interés compuesto: base * ((1 + tasa%)^periodos - 1)."""

    def calculate(self, base: Decimal, rate: Decimal, periods: int = 1) -> Decimal:
        if base <= 0 or rate <= 0:
            return Decimal("0")
        factor = (Decimal("1") + (rate / Decimal("100"))) ** Decimal(periods)
        return base * (factor - Decimal("1"))


class EarlyPaymentStrategy(InterestStrategy):
    """Pronto pago: se aplica como descuento (interés negativo)."""

    def calculate(self, base: Decimal, rate: Decimal, periods: int = 1) -> Decimal:
        if base <= 0 or rate <= 0:
            return Decimal("0")
        return -(base * rate * Decimal(periods) / Decimal("100"))


class RoundingStrategy(ABC):
    """Interfaz base para estrategias de redondeo."""

    @abstractmethod
    def apply(self, value: Decimal) -> Decimal:
        """Aplica redondeo al valor recibido."""


class NoRoundingStrategy(RoundingStrategy):
    """Sin redondeo."""

    def apply(self, value: Decimal) -> Decimal:
        return value


class StepRoundingStrategy(RoundingStrategy):
    """Redondea al múltiplo más cercano de un incremento."""

    def __init__(self, increment: Decimal) -> None:
        self.increment = increment

    def apply(self, value: Decimal) -> Decimal:
        if self.increment == 0:
            return value
        quotient = (value / self.increment).quantize(Decimal("1"))
        return quotient * self.increment


class CeilingRoundingStrategy(RoundingStrategy):
    """Redondea hacia arriba a 2 decimales."""

    def apply(self, value: Decimal) -> Decimal:
        return value.quantize(Decimal("0.01"), rounding=ROUND_CEILING)


class FloorRoundingStrategy(RoundingStrategy):
    """Redondea hacia abajo a 2 decimales."""

    def apply(self, value: Decimal) -> Decimal:
        return value.quantize(Decimal("0.01"), rounding=ROUND_FLOOR)
