import json
from datetime import date
from decimal import Decimal

from django.test import TestCase

from consorcios.models import Consorcio
from propietarios.models import Propietario
from proveedores.models import Proveedor, TipoProveedor
from unidades_funcionales.models import UnidadFuncional, TipoUnidad, EstadoVivienda
from gastos.models import Gasto, TipoGasto
from saldo_mensual.models import SaldoMensual

from expensas.models import ExpensaTemplate, LiquidacionExpensa


class TestLiquidacionIntegration(TestCase):
    def test_01_flujo_completo_liquidacion(self):
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
            descripcion="Mantenimiento",
            monto=Decimal("100.00"),
            tipo_gasto=TipoGasto.MANTENIMIENTO,
        )
        SaldoMensual.objects.create(
            numero_de_unidad_funcional=1,
            consorcio=consorcio,
            mes_anio=date(2026, 1, 1),
            saldo_inicial=Decimal("100.00"),
            total_gastos=Decimal("0"),
            total_pagos=Decimal("0"),
        )
        SaldoMensual.objects.create(
            numero_de_unidad_funcional=2,
            consorcio=consorcio,
            mes_anio=date(2026, 1, 1),
            saldo_inicial=Decimal("0"),
            total_gastos=Decimal("0"),
            total_pagos=Decimal("0"),
        )
        template = ExpensaTemplate.objects.create(
            consorcio=consorcio,
            nombre="Template Febrero",
            version=1,
            config={
                "rounding": {"metodo": "none"},
                "columns": [
                    {
                        "id": "saldo_anterior",
                        "label": "Saldo Anterior",
                        "calc_type": "saldo_anterior",
                        "visible": True,
                    },
                    {
                        "id": "interes_mora",
                        "label": "Interés Mora",
                        "calc_type": "interes",
                        "metodo": "simple",
                        "base": "saldo_anterior",
                        "tasa": "consorcio.interes_por_mora",
                    },
                    {
                        "id": "gastos_ordinarios_a",
                        "label": "Gastos Ordinarios A",
                        "calc_type": "prorrateo",
                        "gasto_tipo": TipoGasto.MANTENIMIENTO,
                    },
                    {
                        "id": "reparaciones",
                        "label": "Reparaciones",
                        "calc_type": "concepto_particular",
                    },
                    {
                        "id": "total",
                        "label": "Total",
                        "calc_type": "formula",
                        "expr": "saldo_anterior + interes_mora + gastos_ordinarios_a + reparaciones",
                        "apply_rounding": True,
                    },
                ],
            },
        )

        payload = {
            "template_id": template.id_expensa_template,
            "consorcio": consorcio.cuit,
            "periodo": "2026-02",
            "cerrar": True,
            "parametros": {
                "conceptos_particulares": [
                    {"unidad": 1, "column_id": "reparaciones", "monto": "200.00"}
                ]
            },
        }

        response = self.client.post(
            "/api/liquidar/",
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()["data"]
        self.assertEqual(data["template_id"], template.id_expensa_template)
        self.assertEqual(len(data["unidades"]), 2)

        self.assertEqual(LiquidacionExpensa.objects.count(), 1)
