from decimal import Decimal

from django.test import TestCase

from consorcios.models import Consorcio
from propietarios.models import Propietario
from unidades_funcionales.models import EstadoVivienda
from unidades_funcionales.services import UnidadFuncionalService


class TestUnidadFuncionalService(TestCase):
    def test_01_el_servicio_realiza_crud_completo_de_unidad_funcional(self):
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
            "tipo_de_unidad": "Departamento",
            "estado_de_vivienda": EstadoVivienda.PROPIETARIO,
            "superficie": Decimal("45.50"),
            "propietario": propietario,
        }
        created = UnidadFuncionalService.crear_unidad_funcional(data)
        fetched = UnidadFuncionalService.obtener_unidad_funcional(
            created.numero_de_unidad_funcional
        )
        self.assertEqual(fetched.tipo_de_unidad, "Departamento")

        listado = UnidadFuncionalService.listar_unidades_funcionales()
        self.assertEqual(listado.count(), 1)

        actualizado = UnidadFuncionalService.actualizar_unidad_funcional(
            created.numero_de_unidad_funcional, {"tipo_de_unidad": "PH"}
        )
        self.assertEqual(actualizado.tipo_de_unidad, "PH")

        UnidadFuncionalService.eliminar_unidad_funcional(
            created.numero_de_unidad_funcional
        )
        self.assertEqual(UnidadFuncionalService.listar_unidades_funcionales().count(), 0)
