from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from caratula.services import CaratulaService
from consorcios.models import Consorcio


class TestCaratulaService(TestCase):
    def test_01_el_servicio_realiza_crud_completo_de_caratula(self):
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
        data = {
            "fecha_caratula": fecha,
            "consorcio": consorcio,
            "texto_caratula": "Texto de prueba",
        }
        created = CaratulaService.crear_caratula(data)
        fetched = CaratulaService.obtener_caratula(created.fecha_caratula)
        self.assertEqual(fetched.texto_caratula, "Texto de prueba")

        listado = CaratulaService.listar_caratulas()
        self.assertEqual(listado.count(), 1)

        actualizado = CaratulaService.actualizar_caratula(
            created.fecha_caratula, {"texto_caratula": "Texto actualizado"}
        )
        self.assertEqual(actualizado.texto_caratula, "Texto actualizado")

        CaratulaService.eliminar_caratula(created.fecha_caratula)
        self.assertEqual(CaratulaService.listar_caratulas().count(), 0)
