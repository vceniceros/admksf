from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from consorcios.models import Consorcio


class TestConsorcioModel(TestCase):
    def test_01_se_puede_crear_consorcio_valido_y_describirlo(self):
        consorcio = Consorcio(
            cuit="20304050607",
            razon_social="Consorcio Test",
            calle="Av Siempre Viva",
            numero=123,
            codigo_postal="1000",
            ciudad="CABA",
            interes_por_mora=Decimal("1.50"),
            redondeo_aumento=Decimal("0.50"),
        )
        consorcio.full_clean()
        consorcio.save()
        self.assertIn("Consorcio", str(consorcio))

    def test_02_no_se_puede_crear_consorcio_con_cuit_invalido(self):
        consorcio = Consorcio(
            cuit="20A040",
            razon_social="Consorcio Test",
            calle="Av Siempre Viva",
            numero=123,
            codigo_postal="1000",
            ciudad="CABA",
            interes_por_mora=Decimal("1.50"),
            redondeo_aumento=Decimal("0.50"),
        )
        with self.assertRaises(ValidationError):
            consorcio.full_clean()
