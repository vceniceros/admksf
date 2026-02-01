from datetime import datetime
from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from caratula.models import Caratula
from consorcios.models import Consorcio


class TestCaratulaModel(TestCase):
    def test_01_se_puede_crear_caratula_valida_y_describirla(self):
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
        fecha = timezone.now()
        caratula = Caratula(
            fecha_caratula=fecha,
            consorcio=consorcio,
            texto_caratula="Texto de prueba",
        )
        caratula.full_clean()
        caratula.save()
        self.assertIn("Caratula", str(caratula))
