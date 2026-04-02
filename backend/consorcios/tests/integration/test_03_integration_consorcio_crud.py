import json

from django.test import TestCase

from usuarios.auth_service import AuthService
from usuarios.models import Rol, Usuario


class TestConsorcioIntegration(TestCase):
    def setUp(self):
        rol_admin = Rol.objects.get(nombre="administrador")
        self.usuario = Usuario.objects.create(
            correo_electronico="admin-consorcio@test.com",
            contrasena="clave123",
            nombre="Admin",
            apellido="Consorcio",
            rol=rol_admin,
        )
        self.auth_header = {"HTTP_AUTHORIZATION": f"Bearer {AuthService.generate_jwt(self.usuario)}"}

    def test_01_flujo_completo_crud_consorcio_por_endpoints(self):
        payload = {
            "cuit": "20304050607",
            "razon_social": "Consorcio Test",
            "calle": "Av Siempre Viva",
            "numero": 123,
            "codigo_postal": "1000",
            "ciudad": "CABA",
            "interes_por_mora": "1.50",
            "redondeo_aumento": "0.50",
        }
        create_resp = self.client.post(
            "/api/consorcios/crear/",
            data=json.dumps(payload),
            content_type="application/json",
            **self.auth_header,
        )
        self.assertEqual(create_resp.status_code, 201)

        list_resp = self.client.get("/api/consorcios/", **self.auth_header)
        self.assertEqual(list_resp.status_code, 200)

        get_resp = self.client.get("/api/consorcios/20304050607/", **self.auth_header)
        self.assertEqual(get_resp.status_code, 200)

        update_resp = self.client.put(
            "/api/consorcios/20304050607/actualizar/",
            data=json.dumps({"razon_social": "Consorcio Actualizado"}),
            content_type="application/json",
            **self.auth_header,
        )
        self.assertEqual(update_resp.status_code, 200)

        delete_resp = self.client.delete("/api/consorcios/20304050607/eliminar/", **self.auth_header)
        self.assertEqual(delete_resp.status_code, 200)

    def test_02_endpoints_requieren_autenticacion(self):
        response = self.client.get("/api/consorcios/")

        self.assertEqual(response.status_code, 401)
