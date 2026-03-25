from decimal import Decimal

from django.test import TestCase

from consorcios.models import Consorcio
from propietarios.models import Propietario
from unidades_funcionales.models import EstadoVivienda, UnidadFuncional


class TestUnidadFuncionalModel(TestCase):
    def test_01_se_puede_crear_unidad_funcional_valida_y_describirla(self):
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
        unidad = UnidadFuncional(
            numero_de_unidad_funcional=1,
            consorcio=consorcio,
            tipo_de_unidad="Departamento",
            estado_de_vivienda=EstadoVivienda.PROPIETARIO,
            superficie=Decimal("45.50"),
            propietario=propietario,
        )
        unidad.full_clean()
        unidad.save()
        self.assertIn("UnidadFuncional", str(unidad))
