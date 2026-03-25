import json

from django.test import TestCase

from proveedores.models import Proveedor, TipoProveedor


class TestReparacionMantenimientoIntegration(TestCase):
    def test_01_flujo_completo_crud_reparacion_mantenimiento_por_endpoints(self):
        Proveedor.objects.create(
            cuit="30987654321",
            razon_social="Proveedor RM",
            calle="Calle 2",
            numero=20,
            codigo_postal="2000",
            ciudad="Rosario",
            tipo_proveedor=TipoProveedor.REPARACIONES_MANTENIMIENTOS,
        )
        payload = {
            "proveedor": "30987654321",
            "numero_reclamo": "RM-001",
        }
        create_resp = self.client.post(
            "/api/reparaciones-mantenimientos/crear/",
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(create_resp.status_code, 201)

        list_resp = self.client.get("/api/reparaciones-mantenimientos/")
        self.assertEqual(list_resp.status_code, 200)

        get_resp = self.client.get("/api/reparaciones-mantenimientos/30987654321/")
        self.assertEqual(get_resp.status_code, 200)

        update_resp = self.client.put(
            "/api/reparaciones-mantenimientos/30987654321/actualizar/",
            data=json.dumps({"numero_reclamo": "RM-999"}),
            content_type="application/json",
        )
        self.assertEqual(update_resp.status_code, 200)

        delete_resp = self.client.delete(
            "/api/reparaciones-mantenimientos/30987654321/eliminar/"
        )
        self.assertEqual(delete_resp.status_code, 200)
