from datetime import date
from decimal import Decimal

from django.test import TestCase

from consorcios.models import Consorcio
from saldo_mensual.models import SaldoMensual


class TestSaldoMensualModel(TestCase):
    def test_01_se_puede_crear_saldo_mensual_valido_y_calcular_saldo_final(self):
        consorcio = Consorcio.objects.create(
            cuit="20304050607",
            razon_social="Consorcio Test",
            calle="Av Siempre Viva",
            numero=123,
            codigo_postal="1000",
            ciudad="CABA",
            interes_por_mora=Decimal("1.50"),
            redondeo_aumento=Decimal("0.50"),
        )
        saldo = SaldoMensual(
            numero_de_unidad_funcional=1,
            consorcio=consorcio,
            mes_anio=date(2026, 1, 1),
            saldo_inicial=Decimal("100.00"),
            total_gastos=Decimal("50.00"),
            total_pagos=Decimal("30.00"),
        )
        saldo.full_clean()
        saldo.save()
        saldo.refresh_from_db()
        self.assertEqual(saldo.saldo_final, Decimal("120.00"))
        self.assertIn("SaldoMensual", str(saldo))
