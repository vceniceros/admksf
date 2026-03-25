import json
from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from consorcios.models import Consorcio


class TestCaratulaIntegration(TestCase):
    def test_01_flujo_completo_crud_caratula_por_endpoints(self):
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
        fecha = timezone.now()
        payload = {
            "fecha_caratula": fecha.isoformat(),
            "consorcio": consorcio.cuit,
            "texto_caratula": "Texto de prueba",
        }
        create_resp = self.client.post(
            "/api/caratulas/crear/",
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(create_resp.status_code, 201)

        list_resp = self.client.get("/api/caratulas/")
        self.assertEqual(list_resp.status_code, 200)

        get_resp = self.client.get(f"/api/caratulas/{fecha.isoformat()}/")
        self.assertEqual(get_resp.status_code, 200)

        update_resp = self.client.put(
            f"/api/caratulas/{fecha.isoformat()}/actualizar/",
            data=json.dumps({"texto_caratula": "Texto actualizado"}),
            content_type="application/json",
        )
        self.assertEqual(update_resp.status_code, 200)

        delete_resp = self.client.delete(
            f"/api/caratulas/{fecha.isoformat()}/eliminar/"
        )
        self.assertEqual(delete_resp.status_code, 200)
