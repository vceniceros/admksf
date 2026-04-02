from decimal import Decimal

from django.test import TestCase

from consorcios.models import Consorcio
from usuarios.auth_service import AuthService
from usuarios.models import Rol, Usuario


class TestUsuarioModel(TestCase):
    def test_00_fecha_creacion_se_asigna_automaticamente(self):
        rol = Rol.objects.get(nombre="administrador")

        usuario = Usuario.objects.create(
            correo_electronico="creacion@test.com",
            contrasena="secreto123",
            nombre="Linus",
            apellido="Torvalds",
            rol=rol,
        )

        self.assertIsNotNone(usuario.fecha_creacion)

    def test_01_guarda_contrasena_hasheada(self):
        rol = Rol.objects.get(nombre="administrador")

        usuario = Usuario.objects.create(
            correo_electronico="admin@test.com",
            contrasena="secreto123",
            nombre="Ada",
            apellido="Lovelace",
            rol=rol,
        )

        self.assertNotEqual(usuario.contrasena, "secreto123")
        self.assertTrue(usuario.check_password("secreto123"))
        self.assertEqual(len(usuario.contrasena.split("$")[2]), AuthService.SALT_BYTES * 2)

    def test_02_un_usuario_puede_tener_multiples_consorcios(self):
        rol = Rol.objects.get(nombre="superusuario")
        usuario = Usuario.objects.create(
            correo_electronico="super@test.com",
            contrasena="clave123",
            nombre="Grace",
            apellido="Hopper",
            rol=rol,
        )

        Consorcio.objects.create(
            cuit="20304050607",
            razon_social="Consorcio Uno",
            calle="Av Siempre Viva",
            numero=100,
            codigo_postal="1000",
            ciudad="CABA",
            interes_por_mora=Decimal("1.00"),
            redondeo_aumento=Decimal("0.50"),
            usuario=usuario,
        )
        Consorcio.objects.create(
            cuit="27304050607",
            razon_social="Consorcio Dos",
            calle="Av Siempre Viva",
            numero=200,
            codigo_postal="1400",
            ciudad="CABA",
            interes_por_mora=Decimal("2.00"),
            redondeo_aumento=Decimal("1.50"),
            usuario=usuario,
        )

        self.assertEqual(usuario.consorcios.count(), 2)