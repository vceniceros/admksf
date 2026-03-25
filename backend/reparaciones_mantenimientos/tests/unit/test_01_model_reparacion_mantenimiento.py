from django.test import TestCase

from proveedores.models import Proveedor, TipoProveedor
from reparaciones_mantenimientos.models import ReparacionMantenimiento


class TestReparacionMantenimientoModel(TestCase):
    def test_01_se_puede_crear_reparacion_mantenimiento_valido_y_describirlo(self):
        proveedor = Proveedor.objects.create(
            cuit="30987654321",
            razon_social="Proveedor RM",
            calle="Calle 2",
            numero=20,
            codigo_postal="2000",
            ciudad="Rosario",
            tipo_proveedor=TipoProveedor.REPARACIONES_MANTENIMIENTOS,
        )
        rm = ReparacionMantenimiento(
            proveedor=proveedor,
            numero_reclamo="RM-001",
        )
        rm.full_clean()
        rm.save()
        self.assertIn("ReparacionMantenimiento", str(rm))
