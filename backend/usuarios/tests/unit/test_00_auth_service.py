import os
from unittest.mock import patch

from django.test import TestCase

from usuarios.auth_service import AuthService
from usuarios.models import Rol, Usuario


class TestAuthService(TestCase):
    def test_01_generate_jwt_genera_token_valido(self):
        rol = Rol.objects.get(nombre="administrador")
        usuario = Usuario.objects.create(
            correo_electronico="jwt@test.com",
            contrasena="clave123",
            nombre="Ada",
            apellido="Lovelace",
            rol=rol,
        )

        token = AuthService.generate_jwt(usuario)
        payload = AuthService.decode_jwt(token)

        self.assertEqual(payload["sub"], str(usuario.id))
        self.assertEqual(payload["correo_electronico"], usuario.correo_electronico)
        self.assertEqual(payload["rol"], "administrador")

    def test_01b_generate_temporary_password_devuelve_longitud_esperada(self):
        temp_password = AuthService.generate_temporary_password()

        self.assertEqual(len(temp_password), AuthService.TEMP_PASSWORD_LENGTH)

    @patch.dict(os.environ, {"JWT_EXPIRATION_SECONDS": "5", "JWT_REFRESH_WINDOW_SECONDS": "60"}, clear=False)
    def test_02_should_refresh_token_detecta_ventana_de_refresh(self):
        rol = Rol.objects.get(nombre="administrador")
        usuario = Usuario.objects.create(
            correo_electronico="refresh@test.com",
            contrasena="clave123",
            nombre="Grace",
            apellido="Hopper",
            rol=rol,
        )

        payload = AuthService.decode_jwt(AuthService.generate_jwt(usuario))

        self.assertTrue(AuthService.should_refresh_token(payload))