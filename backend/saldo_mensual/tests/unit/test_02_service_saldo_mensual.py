from datetime import date
from decimal import Decimal

from django.test import TestCase

from consorcios.models import Consorcio
from saldo_mensual.services import SaldoMensualService


class TestSaldoMensualService(TestCase):
    def test_01_el_servicio_realiza_crud_completo_de_saldo_mensual(self):
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
        data = {
            "numero_de_unidad_funcional": 1,
            "consorcio": consorcio,
            "mes_anio": date(2026, 1, 1),
            "saldo_inicial": Decimal("100.00"),
            "total_gastos": Decimal("50.00"),
            "total_pagos": Decimal("30.00"),
        }
        created = SaldoMensualService.crear_saldo_mensual(data)
        fetched = SaldoMensualService.obtener_saldo_mensual(created.id_saldo_mensual)
        self.assertEqual(fetched.numero_de_unidad_funcional, 1)

        listado = SaldoMensualService.listar_saldos_mensuales()
        self.assertEqual(listado.count(), 1)

        actualizado = SaldoMensualService.actualizar_saldo_mensual(
            created.id_saldo_mensual, {"total_gastos": Decimal("80.00")}
        )
        self.assertEqual(actualizado.total_gastos, Decimal("80.00"))

        SaldoMensualService.eliminar_saldo_mensual(created.id_saldo_mensual)
        self.assertEqual(SaldoMensualService.listar_saldos_mensuales().count(), 0)
