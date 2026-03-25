from django.test import TestCase

from proveedores.models import Proveedor, TipoProveedor
from reparaciones_mantenimientos.services import ReparacionMantenimientoService


class TestReparacionMantenimientoService(TestCase):
    def test_01_el_servicio_realiza_crud_completo_de_reparacion_mantenimiento(self):
        proveedor = Proveedor.objects.create(
            cuit="30987654321",
            razon_social="Proveedor RM",
            calle="Calle 2",
            numero=20,
            codigo_postal="2000",
            ciudad="Rosario",
            tipo_proveedor=TipoProveedor.REPARACIONES_MANTENIMIENTOS,
        )
        data = {
            "proveedor": proveedor,
            "numero_reclamo": "RM-001",
        }
        created = ReparacionMantenimientoService.crear_reparacion_mantenimiento(data)
        fetched = ReparacionMantenimientoService.obtener_reparacion_mantenimiento(
            proveedor.cuit
        )
        self.assertEqual(fetched.numero_reclamo, "RM-001")

        listado = ReparacionMantenimientoService.listar_reparaciones_mantenimientos()
        self.assertEqual(listado.count(), 1)

        actualizado = ReparacionMantenimientoService.actualizar_reparacion_mantenimiento(
            proveedor.cuit, {"numero_reclamo": "RM-999"}
        )
        self.assertEqual(actualizado.numero_reclamo, "RM-999")

        ReparacionMantenimientoService.eliminar_reparacion_mantenimiento(proveedor.cuit)
        self.assertEqual(
            ReparacionMantenimientoService.listar_reparaciones_mantenimientos().count(), 0
        )
