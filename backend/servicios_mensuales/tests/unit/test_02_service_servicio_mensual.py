from django.test import TestCase

from proveedores.models import Proveedor, TipoProveedor
from servicios_mensuales.services import ServicioMensualService


class TestServicioMensualService(TestCase):
    def test_01_el_servicio_realiza_crud_completo_de_servicio_mensual(self):
        proveedor = Proveedor.objects.create(
            cuit="30123456789",
            razon_social="Proveedor Test",
            calle="Calle 1",
            numero=10,
            codigo_postal="1000",
            ciudad="CABA",
            tipo_proveedor=TipoProveedor.SERVICIOS_MENSUALES,
        )
        data = {
            "proveedor": proveedor,
            "numero_cuenta": "NC-123",
            "numero_reclamo": "NR-456",
        }
        created = ServicioMensualService.crear_servicio_mensual(data)
        fetched = ServicioMensualService.obtener_servicio_mensual(proveedor.cuit)
        self.assertEqual(fetched.numero_cuenta, "NC-123")

        listado = ServicioMensualService.listar_servicios_mensuales()
        self.assertEqual(listado.count(), 1)

        actualizado = ServicioMensualService.actualizar_servicio_mensual(
            proveedor.cuit, {"numero_reclamo": "NR-999"}
        )
        self.assertEqual(actualizado.numero_reclamo, "NR-999")

        ServicioMensualService.eliminar_servicio_mensual(proveedor.cuit)
        self.assertEqual(ServicioMensualService.listar_servicios_mensuales().count(), 0)
