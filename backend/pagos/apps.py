"""Configuración de la app pagos.

Fecha:
    27 - 01 - 2026
"""

from django.apps import AppConfig


class PagosConfig(AppConfig):
    """Configura la app pagos."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "pagos"
    verbose_name = "Pagos"
