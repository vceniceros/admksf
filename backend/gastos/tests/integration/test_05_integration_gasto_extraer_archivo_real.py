import os

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase


class TestGastoExtraerArchivoRealIntegration(TestCase):
    def test_01_extraer_gasto_desde_archivo_real(self):
        factura_path = os.path.join(
            settings.BASE_DIR,
            "gastos",
            "tests",
            "integration",
            "facturas test",
            "20260205_E_83668593-9127001587556.pdf",
        )
        self.assertTrue(os.path.exists(factura_path))

        with open(factura_path, "rb") as factura_file:
            archivo = SimpleUploadedFile(
                "20260205_E_83668593-9127001587556.pdf",
                factura_file.read(),
                content_type="application/pdf",
            )

        response = self.client.post(
            "/api/gastos/extraer-desde-archivo/",
            data={"archivo": archivo},
        )

        if response.status_code != 200:
            try:
                payload = response.json()
            except ValueError:
                payload = response.content.decode("utf-8", errors="replace")
            self.fail(f"Respuesta {response.status_code}: {payload}")

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body.get("status"), "success")
        data = body.get("data") or {}
        self.assertIn("cuit_proveedor", data)
        self.assertIn("periodo", data)
        self.assertIn("descripcion", data)
        self.assertIn("monto", data)
        self.assertIn("raw_text", data)
