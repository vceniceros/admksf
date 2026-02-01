from django.core.exceptions import ValidationError
from django.test import TestCase

from proveedores.models import Proveedor, TipoProveedor


class TestProveedorModel(TestCase):
    def test_01_se_puede_crear_proveedor_valido_y_describirlo(self):
        proveedor = Proveedor(
            cuit="30123456789",
            razon_social="Proveedor Test",
            telefono="1133221100",
            email="prov@test.com",
            calle="Calle 1",
            numero=10,
            codigo_postal="1000",
            ciudad="CABA",
            tipo_proveedor=TipoProveedor.SERVICIOS_MENSUALES,
        )
        proveedor.full_clean()
        proveedor.save()
        self.assertIn("Proveedor", str(proveedor))

    def test_02_no_se_puede_crear_proveedor_con_cuit_invalido(self):
        proveedor = Proveedor(
            cuit="30A234",
            razon_social="Proveedor Test",
            calle="Calle 1",
            numero=10,
            codigo_postal="1000",
            ciudad="CABA",
            tipo_proveedor=TipoProveedor.SERVICIOS_MENSUALES,
        )
        with self.assertRaises(ValidationError):
            proveedor.full_clean()
