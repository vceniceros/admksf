from decimal import Decimal

from django.test import TestCase

from expensas.strategies import (
    CompoundInterestStrategy,
    EarlyPaymentStrategy,
    SimpleInterestStrategy,
)


class TestInterestStrategies(TestCase):
    def test_01_interes_simple(self):
        estrategia = SimpleInterestStrategy()
        resultado = estrategia.calculate(Decimal("1000"), Decimal("2"), periods=1)
        self.assertEqual(resultado, Decimal("20"))

    def test_02_interes_compuesto(self):
        estrategia = CompoundInterestStrategy()
        resultado = estrategia.calculate(Decimal("1000"), Decimal("2"), periods=2)
        self.assertEqual(resultado.quantize(Decimal("0.01")), Decimal("40.40"))

    def test_03_pronto_pago(self):
        estrategia = EarlyPaymentStrategy()
        resultado = estrategia.calculate(Decimal("1000"), Decimal("5"), periods=1)
        self.assertEqual(resultado, Decimal("-50"))
