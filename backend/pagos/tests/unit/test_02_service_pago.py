from decimal import Decimal

from django.test import TestCase

from consorcios.models import Consorcio
from propietarios.models import Propietario
from pagos.services import PagoService


class TestPagoService(TestCase):
    def test_01_el_servicio_realiza_crud_completo_de_pago(self):
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
        data = {
            "numero_de_unidad_funcional": 1,
            "consorcio": consorcio,
            "propietario": propietario,
            "monto": Decimal("2500.00"),
        }
        created = PagoService.crear_pago(data)
        fetched = PagoService.obtener_pago(created.id_pago)
        self.assertEqual(fetched.monto, Decimal("2500.00"))

        listado = PagoService.listar_pagos()
        self.assertEqual(listado.count(), 1)

        actualizado = PagoService.actualizar_pago(
            created.id_pago, {"monto": Decimal("3000.00")}
        )
        self.assertEqual(actualizado.monto, Decimal("3000.00"))

        PagoService.eliminar_pago(created.id_pago)
        self.assertEqual(PagoService.listar_pagos().count(), 0)
