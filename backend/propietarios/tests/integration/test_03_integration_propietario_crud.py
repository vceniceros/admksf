import json

from django.test import TestCase


class TestPropietarioIntegration(TestCase):
    def test_01_flujo_completo_crud_propietario_por_endpoints(self):
        payload = {
            "dni": "12345678",
            "nombre": "Juan",
            "apellido": "Perez",
            "telefono": "1122334455",
            "email": "juan@test.com",
        }
        create_resp = self.client.post(
            "/api/propietarios/crear/",
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(create_resp.status_code, 201)

        list_resp = self.client.get("/api/propietarios/")
        self.assertEqual(list_resp.status_code, 200)

        get_resp = self.client.get("/api/propietarios/12345678/")
        self.assertEqual(get_resp.status_code, 200)

        update_resp = self.client.put(
            "/api/propietarios/12345678/actualizar/",
            data=json.dumps({"nombre": "Juan Actualizado"}),
            content_type="application/json",
        )
        self.assertEqual(update_resp.status_code, 200)

        delete_resp = self.client.delete("/api/propietarios/12345678/eliminar/")
        self.assertEqual(delete_resp.status_code, 200)
