import json
from datetime import date
from decimal import Decimal

from django.test import TestCase

from consorcios.models import Consorcio


class TestSaldoMensualIntegration(TestCase):
    def test_01_flujo_completo_crud_saldo_mensual_por_endpoints(self):
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
        payload = {
            "numero_de_unidad_funcional": 1,
            "consorcio": consorcio.cuit,
            "mes_anio": date(2026, 1, 1).isoformat(),
            "saldo_inicial": "100.00",
            "total_gastos": "50.00",
            "total_pagos": "30.00",
        }
        create_resp = self.client.post(
            "/api/saldos-mensuales/crear/",
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(create_resp.status_code, 201)

        list_resp = self.client.get("/api/saldos-mensuales/")
        self.assertEqual(list_resp.status_code, 200)

        get_resp = self.client.get("/api/saldos-mensuales/1/")
        self.assertEqual(get_resp.status_code, 200)

        update_resp = self.client.put(
            "/api/saldos-mensuales/1/actualizar/",
            data=json.dumps({"total_gastos": "80.00"}),
            content_type="application/json",
        )
        self.assertEqual(update_resp.status_code, 200)

        delete_resp = self.client.delete("/api/saldos-mensuales/1/eliminar/")
        self.assertEqual(delete_resp.status_code, 200)
