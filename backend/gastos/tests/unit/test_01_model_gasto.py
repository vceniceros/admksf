from datetime import date
from decimal import Decimal

from django.test import TestCase

from consorcios.models import Consorcio
from proveedores.models import Proveedor, TipoProveedor
from gastos.models import EstadoPago, Gasto, TipoGasto


class TestGastoModel(TestCase):
    def test_01_se_puede_crear_gasto_valido_y_describirlo(self):
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
        gasto = Gasto(
            consorcio=consorcio,
            proveedor=proveedor,
            periodo=date(2026, 1, 1),
            descripcion="Gasto de prueba",
            monto=Decimal("1500.00"),
            tipo_gasto=TipoGasto.SERVICIOS,
            estado_pago=EstadoPago.PENDIENTE,
        )
        gasto.full_clean()
        gasto.save()
        self.assertIn("Gasto", str(gasto))
