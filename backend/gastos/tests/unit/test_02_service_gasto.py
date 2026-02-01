from datetime import date
from decimal import Decimal

from django.test import TestCase

from consorcios.models import Consorcio
from proveedores.models import Proveedor, TipoProveedor
from gastos.models import TipoGasto
from gastos.services import GastoService


class TestGastoService(TestCase):
    def test_01_el_servicio_realiza_crud_completo_de_gasto(self):
        consorcio = Consorcio.objects.create(
            cuit="20304050607",
            razon_social="Consorcio Test",
            calle="Av Siempre Viva",
            numero=123,
            codigo_postal="1000",
            ciudad="CABA",
            interes_por_mora=Decimal("1.50"),
            redondeo_aumento=Decimal("0.50"),
        )
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
            "consorcio": consorcio,
            "proveedor": proveedor,
            "periodo": date(2026, 1, 1),
            "descripcion": "Gasto de prueba",
            "monto": Decimal("1500.00"),
            "tipo_gasto": TipoGasto.SERVICIOS,
        }
        created = GastoService.crear_gasto(data)
        fetched = GastoService.obtener_gasto(created.id_gasto)
        self.assertEqual(fetched.descripcion, "Gasto de prueba")

        listado = GastoService.listar_gastos()
        self.assertEqual(listado.count(), 1)

        actualizado = GastoService.actualizar_gasto(
            created.id_gasto, {"descripcion": "Gasto actualizado"}
        )
        self.assertEqual(actualizado.descripcion, "Gasto actualizado")

        GastoService.eliminar_gasto(created.id_gasto)
        self.assertEqual(GastoService.listar_gastos().count(), 0)
