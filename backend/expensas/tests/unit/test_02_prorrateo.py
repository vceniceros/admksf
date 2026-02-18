from decimal import Decimal
from datetime import date

from django.test import TestCase

from consorcios.models import Consorcio
from propietarios.models import Propietario
from unidades_funcionales.models import UnidadFuncional, TipoUnidad, EstadoVivienda
from gastos.models import Gasto, TipoGasto
from proveedores.models import Proveedor, TipoProveedor

from expensas.builder import LiquidacionBuilder


class TestProrrateo(TestCase):
    def test_01_prorrateo_por_superficie(self):
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
        UnidadFuncional.objects.create(
            numero_de_unidad_funcional=1,
            consorcio=consorcio,
            tipo_de_unidad=TipoUnidad.DEPARTAMENTO,
            estado_de_vivienda=EstadoVivienda.PROPIETARIO,
            superficie=Decimal("60"),
            propietario=propietario,
        )
        UnidadFuncional.objects.create(
            numero_de_unidad_funcional=2,
            consorcio=consorcio,
            tipo_de_unidad=TipoUnidad.DEPARTAMENTO,
            estado_de_vivienda=EstadoVivienda.PROPIETARIO,
            superficie=Decimal("40"),
            propietario=propietario,
        )
        proveedor = Proveedor.objects.create(
            cuit="20304050608",
            razon_social="Proveedor Test",
            telefono="123456",
            email="proveedor@test.com",
            calle="Av Test",
            numero=10,
            codigo_postal="1000",
            ciudad="CABA",
            tipo_proveedor=TipoProveedor.SERVICIOS_MENSUALES,
        )
        Gasto.objects.create(
            consorcio=consorcio,
            proveedor=proveedor,
            periodo=date(2026, 2, 1),
            descripcion="Limpieza",
            monto=Decimal("100.00"),
            tipo_gasto=TipoGasto.LIMPIEZA,
        )
        template_config = {
            "columns": [
                {
                    "id": "gastos_ordinarios",
                    "label": "Gastos Ordinarios",
                    "calc_type": "prorrateo",
                    "visible": True,
                    "gasto_tipo": TipoGasto.LIMPIEZA,
                }
            ]
        }
        builder = LiquidacionBuilder(consorcio, date(2026, 2, 1), template_config, {})
        resultado = builder.build()

        unidades = resultado["unidades"]
        valor_uf1 = Decimal(unidades[0]["valores"]["gastos_ordinarios"])
        valor_uf2 = Decimal(unidades[1]["valores"]["gastos_ordinarios"])
        self.assertEqual(valor_uf1, Decimal("60.00"))
        self.assertEqual(valor_uf2, Decimal("40.00"))
