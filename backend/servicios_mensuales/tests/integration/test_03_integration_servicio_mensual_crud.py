import json

from django.test import TestCase

from proveedores.models import Proveedor, TipoProveedor


class TestServicioMensualIntegration(TestCase):
    def test_01_flujo_completo_crud_servicio_mensual_por_endpoints(self):
        Proveedor.objects.create(
            cuit="30123456789",
            razon_social="Proveedor Test",
            calle="Calle 1",
            numero=10,
            codigo_postal="1000",
            ciudad="CABA",
            tipo_proveedor=TipoProveedor.SERVICIOS_MENSUALES,
        )
        payload = {
            "proveedor": "30123456789",
            "numero_cuenta": "NC-123",
            "numero_reclamo": "NR-456",
        }
        create_resp = self.client.post(
            "/api/servicios-mensuales/crear/",
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(create_resp.status_code, 201)

        list_resp = self.client.get("/api/servicios-mensuales/")
        self.assertEqual(list_resp.status_code, 200)

        get_resp = self.client.get("/api/servicios-mensuales/30123456789/")
        self.assertEqual(get_resp.status_code, 200)

        update_resp = self.client.put(
            "/api/servicios-mensuales/30123456789/actualizar/",
            data=json.dumps({"numero_reclamo": "NR-999"}),
            content_type="application/json",
        )
        self.assertEqual(update_resp.status_code, 200)

        delete_resp = self.client.delete(
            "/api/servicios-mensuales/30123456789/eliminar/"
        )
        self.assertEqual(delete_resp.status_code, 200)
