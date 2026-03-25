import json
from datetime import date
from decimal import Decimal

from django.test import TestCase

from consorcios.models import Consorcio
from proveedores.models import Proveedor, TipoProveedor


class TestGastoIntegration(TestCase):
    def test_01_flujo_completo_crud_gasto_por_endpoints(self):
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
        proveedor = Proveedor.objects.create(
            cuit="30123456789",
            razon_social="Proveedor Test",
            calle="Calle 1",
            numero=10,
            codigo_postal="1000",
            ciudad="CABA",
            tipo_proveedor=TipoProveedor.SERVICIOS_MENSUALES,
        )
        payload = {
            "consorcio": consorcio.cuit,
            "proveedor": proveedor.cuit,
            "periodo": date(2026, 1, 1).isoformat(),
            "descripcion": "Gasto de prueba",
            "monto": "1500.00",
            "tipo_gasto": "Servicios",
            "estado_pago": "Pendiente",
        }
        create_resp = self.client.post(
            "/api/gastos/crear/",
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(create_resp.status_code, 201)

        list_resp = self.client.get("/api/gastos/")
        self.assertEqual(list_resp.status_code, 200)

        get_resp = self.client.get("/api/gastos/1/")
        self.assertEqual(get_resp.status_code, 200)

        update_resp = self.client.put(
            "/api/gastos/1/actualizar/",
            data=json.dumps({"descripcion": "Gasto actualizado"}),
            content_type="application/json",
        )
        self.assertEqual(update_resp.status_code, 200)

        delete_resp = self.client.delete("/api/gastos/1/eliminar/")
        self.assertEqual(delete_resp.status_code, 200)
