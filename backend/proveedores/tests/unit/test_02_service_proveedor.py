from django.test import TestCase

from proveedores.models import TipoProveedor
from proveedores.services import ProveedorService


class TestProveedorService(TestCase):
    def test_01_el_servicio_realiza_crud_completo_de_proveedor(self):
        data = {
            "cuit": "30123456789",
            "razon_social": "Proveedor Test",
            "telefono": "1133221100",
            "email": "prov@test.com",
            "calle": "Calle 1",
            "numero": 10,
            "codigo_postal": "1000",
            "ciudad": "CABA",
            "tipo_proveedor": TipoProveedor.SERVICIOS_MENSUALES,
        }
        created = ProveedorService.crear_proveedor(data)
        fetched = ProveedorService.obtener_proveedor(created.cuit)
        self.assertEqual(fetched.razon_social, "Proveedor Test")

        listado = ProveedorService.listar_proveedores()
        self.assertEqual(listado.count(), 1)

        actualizado = ProveedorService.actualizar_proveedor(
            created.cuit, {"razon_social": "Proveedor Actualizado"}
        )
        self.assertEqual(actualizado.razon_social, "Proveedor Actualizado")

        ProveedorService.eliminar_proveedor(created.cuit)
        self.assertEqual(ProveedorService.listar_proveedores().count(), 0)
