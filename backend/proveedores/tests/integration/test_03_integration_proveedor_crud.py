import json

from django.test import TestCase


class TestProveedorIntegration(TestCase):
    def test_01_flujo_completo_crud_proveedor_por_endpoints(self):
        payload = {
            "cuit": "30123456789",
            "razon_social": "Proveedor Test",
            "telefono": "1133221100",
            "email": "prov@test.com",
            "calle": "Calle 1",
            "numero": 10,
            "codigo_postal": "1000",
            "ciudad": "CABA",
            "tipo_proveedor": "servicios_mensuales",
        }
        create_resp = self.client.post(
            "/api/proveedores/crear/",
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(create_resp.status_code, 201)

        list_resp = self.client.get("/api/proveedores/")
        self.assertEqual(list_resp.status_code, 200)

        get_resp = self.client.get("/api/proveedores/30123456789/")
        self.assertEqual(get_resp.status_code, 200)

        update_resp = self.client.put(
            "/api/proveedores/30123456789/actualizar/",
            data=json.dumps({"razon_social": "Proveedor Actualizado"}),
            content_type="application/json",
        )
        self.assertEqual(update_resp.status_code, 200)

        delete_resp = self.client.delete("/api/proveedores/30123456789/eliminar/")
        self.assertEqual(delete_resp.status_code, 200)
