from decimal import Decimal

from django.test import TestCase

from consorcios.models import Consorcio
from propietarios.models import Propietario
from pagos.models import Pago


class TestPagoModel(TestCase):
    def test_01_se_puede_crear_pago_valido_y_describirlo(self):
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
        propietario = Propietario.objects.create(
            dni="12345678",
            nombre="Juan",
            apellido="Perez",
        )
        pago = Pago(
            numero_de_unidad_funcional=1,
            consorcio=consorcio,
            propietario=propietario,
            monto=Decimal("2500.00"),
        )
        pago.full_clean()
        pago.save()
        self.assertIn("Pago", str(pago))
