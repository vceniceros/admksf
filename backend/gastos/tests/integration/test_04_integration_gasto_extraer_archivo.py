from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase


class TestGastoExtraerArchivoIntegration(TestCase):
    @patch("gastos.views.process_file")
    def test_01_extraer_gasto_desde_archivo_ok(self, mock_process_file):
        mock_process_file.return_value = {
            "raw_text": "Factura ejemplo",
            "fecha": "01/01/2026",
            "numero_factura": "A-0001-00000001",
            "importe_total": "1500,00",
            "cuit_proveedor": "30-12345678-9",
            "periodo_facturado": "01/2026",
            "descripcion": "Servicio mensual",
            "fecha_vencimiento": "10/01/2026",
        }

        archivo = SimpleUploadedFile(
            "factura.png",
            b"fake-image-content",
            content_type="image/png",
        )

        response = self.client.post(
            "/api/gastos/extraer-desde-archivo/",
            data={"archivo": archivo},
        )

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["status"], "success")
        self.assertEqual(body["data"]["cuit_proveedor"], "30-12345678-9")
        self.assertEqual(body["data"]["periodo"], "01/2026")
        self.assertEqual(body["data"]["monto"], "1500,00")
