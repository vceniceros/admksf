from decimal import Decimal

from django.test import TestCase

from consorcios.services import ConsorcioService


class TestConsorcioService(TestCase):
    def test_01_el_servicio_realiza_crud_completo_de_consorcio(self):
        data = {
            "cuit": "20304050607",
            "razon_social": "Consorcio Test",
            "calle": "Av Siempre Viva",
            "numero": 123,
            "codigo_postal": "1000",
            "ciudad": "CABA",
            "interes_por_mora": Decimal("1.50"),
            "redondeo_aumento": Decimal("0.50"),
        }
        created = ConsorcioService.crear_consorcio(data)
        fetched = ConsorcioService.obtener_consorcio(created.cuit)
        self.assertEqual(fetched.razon_social, "Consorcio Test")

        listado = ConsorcioService.listar_consorcios()
        self.assertEqual(listado.count(), 1)

        actualizado = ConsorcioService.actualizar_consorcio(
            created.cuit, {"razon_social": "Consorcio Actualizado"}
        )
        self.assertEqual(actualizado.razon_social, "Consorcio Actualizado")

        ConsorcioService.eliminar_consorcio(created.cuit)
        self.assertEqual(ConsorcioService.listar_consorcios().count(), 0)
