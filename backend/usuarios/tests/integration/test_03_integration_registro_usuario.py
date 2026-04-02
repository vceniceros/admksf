import json
import os
from unittest.mock import patch

from django.test import TestCase

from usuarios.auth_service import AuthService
from usuarios.models import Rol, Usuario


class TestUsuarioIntegration(TestCase):
    def setUp(self):
        rol_super = Rol.objects.get(nombre="superusuario")
        self.superusuario = Usuario.objects.create(
            correo_electronico="root@test.com",
            contrasena="clave123",
            nombre="Root",
            apellido="Admin",
            rol=rol_super,
        )
        self.superusuario_token = AuthService.generate_jwt(self.superusuario)

    def test_01_registra_usuario_por_endpoint(self):
        payload = {
            "correo_electronico": "admin@test.com",
            "contrasena": "clave123",
            "nombre": "Ada",
            "apellido": "Lovelace",
            "rol": "administrador",
            "esta_activo": True,
        }

        response = self.client.post(
            "/api/usuarios/registrar/",
            data=json.dumps(payload),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.superusuario_token}",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["data"]["correo_electronico"], "admin@test.com")
        self.assertEqual(response.json()["data"]["rol"], "administrador")

        usuario = Usuario.objects.get(correo_electronico="admin@test.com")
        self.assertNotEqual(usuario.contrasena, "clave123")
        self.assertTrue(usuario.check_password("clave123"))
        self.assertEqual(len(usuario.contrasena.split("$")[2]), AuthService.SALT_BYTES * 2)

    def test_02_devuelve_400_si_el_json_es_invalido(self):
        response = self.client.post(
            "/api/usuarios/registrar/",
            data="{json_invalido",
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.superusuario_token}",
        )

        self.assertEqual(response.status_code, 400)

    def test_03_devuelve_400_si_el_rol_no_existe(self):
        payload = {
            "correo_electronico": "admin@test.com",
            "contrasena": "clave123",
            "nombre": "Ada",
            "apellido": "Lovelace",
            "rol": "owner",
        }

        response = self.client.post(
            "/api/usuarios/registrar/",
            data=json.dumps(payload),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.superusuario_token}",
        )

        self.assertEqual(response.status_code, 400)

    def test_03b_registro_requiere_autenticacion(self):
        response = self.client.post(
            "/api/usuarios/registrar/",
            data=json.dumps(
                {
                    "correo_electronico": "sin-auth@test.com",
                    "contrasena": "clave123",
                    "nombre": "No",
                    "apellido": "Auth",
                    "rol": "administrador",
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 401)

    def test_04_login_usuario_por_endpoint(self):
        rol = Rol.objects.get(nombre="administrador")
        Usuario.objects.create(
            correo_electronico="login@test.com",
            contrasena="clave123",
            nombre="Ada",
            apellido="Lovelace",
            rol=rol,
        )

        response = self.client.post(
            "/api/usuarios/login/",
            data=json.dumps({"usuario": "login@test.com", "contrasena": "clave123"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json()["data"])
        self.assertEqual(response.json()["data"]["usuario"]["correo_electronico"], "login@test.com")

    @patch.dict(os.environ, {"JWT_EXPIRATION_SECONDS": "5", "JWT_REFRESH_WINDOW_SECONDS": "60"}, clear=False)
    def test_05_verificar_autenticacion_refresca_token(self):
        rol = Rol.objects.get(nombre="administrador")
        usuario = Usuario.objects.create(
            correo_electronico="verify@test.com",
            contrasena="clave123",
            nombre="Grace",
            apellido="Hopper",
            rol=rol,
        )
        token = AuthService.generate_jwt(usuario)

        response = self.client.get(
            "/api/usuarios/autenticado/",
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["data"]["refreshed"])
        self.assertNotEqual(response.json()["data"]["token"], token)

    def test_06_login_devuelve_400_si_password_es_invalida(self):
        rol = Rol.objects.get(nombre="administrador")
        Usuario.objects.create(
            correo_electronico="invalid@test.com",
            contrasena="clave123",
            nombre="Ada",
            apellido="Lovelace",
            rol=rol,
        )

        response = self.client.post(
            "/api/usuarios/login/",
            data=json.dumps({"usuario": "invalid@test.com", "contrasena": "incorrecta"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)

    def test_07_recuperar_contrasena_requiere_superusuario(self):
        rol_admin = Rol.objects.get(nombre="administrador")
        Usuario.objects.create(
            correo_electronico="target@test.com",
            contrasena="vieja123",
            nombre="Target",
            apellido="User",
            rol=rol_admin,
        )
        admin = Usuario.objects.create(
            correo_electronico="admin-recovery@test.com",
            contrasena="clave123",
            nombre="Admin",
            apellido="NoSuper",
            rol=rol_admin,
        )

        response = self.client.post(
            "/api/usuarios/recuperar-contrasena/",
            data=json.dumps({"correo_electronico": "target@test.com"}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {AuthService.generate_jwt(admin)}",
        )

        self.assertEqual(response.status_code, 403)

    def test_08_superusuario_puede_recuperar_contrasena_generada(self):
        rol_admin = Rol.objects.get(nombre="administrador")
        rol_super = Rol.objects.get(nombre="superusuario")
        target = Usuario.objects.create(
            correo_electronico="target-generated@test.com",
            contrasena="vieja123",
            nombre="Target",
            apellido="Generated",
            rol=rol_admin,
        )
        superusuario = Usuario.objects.create(
            correo_electronico="super@test.com",
            contrasena="clave123",
            nombre="Super",
            apellido="Usuario",
            rol=rol_super,
        )

        response = self.client.post(
            "/api/usuarios/recuperar-contrasena/",
            data=json.dumps({"correo_electronico": "target-generated@test.com"}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {AuthService.generate_jwt(superusuario)}",
        )

        self.assertEqual(response.status_code, 200)
        nueva_password = response.json()["data"]["contrasena_temporal"]
        self.assertTrue(response.json()["data"]["generada_automaticamente"])
        target.refresh_from_db()
        self.assertTrue(target.check_password(nueva_password))

    def test_09_superusuario_puede_recuperar_contrasena_explicita(self):
        rol_admin = Rol.objects.get(nombre="administrador")
        rol_super = Rol.objects.get(nombre="superusuario")
        target = Usuario.objects.create(
            correo_electronico="target-explicit@test.com",
            contrasena="vieja123",
            nombre="Target",
            apellido="Explicit",
            rol=rol_admin,
        )
        superusuario = Usuario.objects.create(
            correo_electronico="super-explicit@test.com",
            contrasena="clave123",
            nombre="Super",
            apellido="Explicit",
            rol=rol_super,
        )

        response = self.client.post(
            "/api/usuarios/recuperar-contrasena/",
            data=json.dumps(
                {
                    "correo_electronico": "target-explicit@test.com",
                    "nueva_contrasena": "Temporal123ABC",
                }
            ),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {AuthService.generate_jwt(superusuario)}",
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["data"]["generada_automaticamente"])
        target.refresh_from_db()
        self.assertTrue(target.check_password("Temporal123ABC"))