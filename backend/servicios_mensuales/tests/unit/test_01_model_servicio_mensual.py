from django.test import TestCase

from proveedores.models import Proveedor, TipoProveedor
from servicios_mensuales.models import ServicioMensual


class TestServicioMensualModel(TestCase):
    def test_01_se_puede_crear_servicio_mensual_valido_y_describirlo(self):
        proveedor = Proveedor.objects.create(
            cuit="30123456789",
            razon_social="Proveedor Test",
            calle="Calle 1",
            numero=10,
            codigo_postal="1000",
            ciudad="CABA",
            tipo_proveedor=TipoProveedor.SERVICIOS_MENSUALES,
        )
        servicio = ServicioMensual(
            proveedor=proveedor,
            numero_cuenta="NC-123",
            numero_reclamo="NR-456",
        )
        servicio.full_clean()
        servicio.save()
        self.assertIn("ServicioMensual", str(servicio))
