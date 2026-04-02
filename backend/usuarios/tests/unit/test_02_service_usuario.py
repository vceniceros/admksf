import os
from unittest.mock import patch

from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError
from django.test import TestCase

from usuarios.auth_service import AuthService
from usuarios.models import Rol, Usuario
from usuarios.services import UsuarioService


class TestUsuarioService(TestCase):
    def test_00_generate_hashed_password_genera_hash_con_salt_de_16_bytes(self):
        hashed_password = AuthService.generate_hashed_password("clave123")

        self.assertNotEqual(hashed_password, "clave123")
        self.assertTrue(hashed_password.startswith("pbkdf2_"))
        self.assertEqual(len(hashed_password.split("$")[2]), AuthService.SALT_BYTES * 2)

    def test_01_registra_usuario_con_rol_por_nombre(self):
        usuario = UsuarioService.registrar_usuario(
            {
                "correo_electronico": "ADMIN@TEST.COM ",
                "contrasena": "clave123",
                "nombre": "Ada ",
                "apellido": " Lovelace",
                "rol": "administrador",
            }
        )

        self.assertEqual(usuario.correo_electronico, "admin@test.com")
        self.assertEqual(usuario.nombre, "Ada")
        self.assertEqual(usuario.apellido, "Lovelace")
        self.assertEqual(usuario.rol.nombre, "administrador")
        self.assertNotEqual(usuario.contrasena, "clave123")
        self.assertTrue(usuario.check_password("clave123"))
        self.assertEqual(len(usuario.contrasena.split("$")[2]), AuthService.SALT_BYTES * 2)

    def test_02_falla_si_el_rol_no_existe(self):
        with self.assertRaises(ValidationError):
            UsuarioService.registrar_usuario(
                {
                    "correo_electronico": "admin@test.com",
                    "contrasena": "clave123",
                    "nombre": "Ada",
                    "apellido": "Lovelace",
                    "rol": "inexistente",
                }
            )

        self.assertEqual(Usuario.objects.count(), 0)

    def test_03_autentica_usuario_valido(self):
        usuario = UsuarioService.registrar_usuario(
            {
                "correo_electronico": "login@test.com",
                "contrasena": "clave123",
                "nombre": "Ada",
                "apellido": "Lovelace",
                "rol": "administrador",
            }
        )

        autenticado = UsuarioService.autenticar_usuario("login@test.com", "clave123")

        self.assertEqual(autenticado.id, usuario.id)
        self.assertIsNotNone(autenticado.ultimo_ingreso)

    @patch.dict(os.environ, {"JWT_EXPIRATION_SECONDS": "5", "JWT_REFRESH_WINDOW_SECONDS": "60"}, clear=False)
    def test_04_validar_sesion_refresca_token_si_corresponde(self):
        usuario = UsuarioService.registrar_usuario(
            {
                "correo_electronico": "refresh-service@test.com",
                "contrasena": "clave123",
                "nombre": "Grace",
                "apellido": "Hopper",
                "rol": "administrador",
            }
        )

        token = AuthService.generate_jwt(usuario)
        usuario_validado, refreshed_token = UsuarioService.validar_sesion(token)

        self.assertEqual(usuario_validado.id, usuario.id)
        self.assertIsNotNone(refreshed_token)
        self.assertNotEqual(refreshed_token, token)

    def test_05_verificar_superusuario_falla_para_administrador(self):
        usuario = UsuarioService.registrar_usuario(
            {
                "correo_electronico": "admin-role@test.com",
                "contrasena": "clave123",
                "nombre": "Ada",
                "apellido": "Lovelace",
                "rol": "administrador",
            }
        )

        with self.assertRaises(PermissionDenied):
            UsuarioService.verificar_superusuario(usuario)

    def test_06_recuperar_contrasena_con_password_explicita(self):
        usuario = UsuarioService.registrar_usuario(
            {
                "correo_electronico": "recovery@test.com",
                "contrasena": "vieja123",
                "nombre": "Grace",
                "apellido": "Hopper",
                "rol": "administrador",
            }
        )

        usuario_recuperado, nueva_password = UsuarioService.recuperar_contrasena(
            "recovery@test.com",
            "NuevaClave456",
        )

        self.assertEqual(usuario_recuperado.id, usuario.id)
        self.assertEqual(nueva_password, "NuevaClave456")
        usuario.refresh_from_db()
        self.assertTrue(usuario.check_password("NuevaClave456"))

    def test_07_recuperar_contrasena_generada_automaticamente(self):
        UsuarioService.registrar_usuario(
            {
                "correo_electronico": "auto-recovery@test.com",
                "contrasena": "vieja123",
                "nombre": "Linus",
                "apellido": "Torvalds",
                "rol": "administrador",
            }
        )

        usuario, nueva_password = UsuarioService.recuperar_contrasena("auto-recovery@test.com")

        self.assertEqual(len(nueva_password), AuthService.TEMP_PASSWORD_LENGTH)
        self.assertTrue(usuario.check_password(nueva_password))