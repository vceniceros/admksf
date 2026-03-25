import json

from decimal import Decimal

from django.test import TestCase

from consorcios.models import Consorcio
from propietarios.models import Propietario


class TestUnidadFuncionalIntegration(TestCase):
    def test_01_flujo_completo_crud_unidad_funcional_por_endpoints(self):
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
        propietario = Propietario.objects.create(
            dni="12345678",
            nombre="Juan",
            apellido="Perez",
        )
        payload = {
            "numero_de_unidad_funcional": 1,
            "consorcio": consorcio.cuit,
            "tipo_de_unidad": "Departamento",
            "estado_de_vivienda": "Propietario",
            "superficie": "45.50",
            "propietario": propietario.dni,
        }
        create_resp = self.client.post(
            "/api/unidades-funcionales/crear/",
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(create_resp.status_code, 201)

        list_resp = self.client.get("/api/unidades-funcionales/")
        self.assertEqual(list_resp.status_code, 200)

        get_resp = self.client.get("/api/unidades-funcionales/1/")
        self.assertEqual(get_resp.status_code, 200)

        update_resp = self.client.put(
            "/api/unidades-funcionales/1/actualizar/",
            data=json.dumps({"tipo_de_unidad": "PH"}),
            content_type="application/json",
        )
        self.assertEqual(update_resp.status_code, 200)

        delete_resp = self.client.delete("/api/unidades-funcionales/1/eliminar/")
        self.assertEqual(delete_resp.status_code, 200)
