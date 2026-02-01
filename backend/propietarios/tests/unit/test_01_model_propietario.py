from django.core.exceptions import ValidationError
from django.test import TestCase

from propietarios.models import Propietario


class TestPropietarioModel(TestCase):
    def test_01_se_puede_crear_propietario_valido_y_describirlo(self):
        propietario = Propietario(
            dni="12345678",
            nombre="Juan",
            apellido="Perez",
            telefono="1122334455",
            email="juan@test.com",
        )
        propietario.full_clean()
        propietario.save()
        self.assertIn("Propietario", str(propietario))

    def test_02_no_se_puede_crear_propietario_con_dni_invalido(self):
        propietario = Propietario(
            dni="12A34",
            nombre="Juan",
            apellido="Perez",
        )
        with self.assertRaises(ValidationError):
            propietario.full_clean()
