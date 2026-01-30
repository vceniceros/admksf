"""Configuración de la app gastos.

Fecha:
    27 - 01 - 2026
"""

from django.apps import AppConfig


class GastosConfig(AppConfig):
    """Configura la app gastos."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "gastos"
    verbose_name = "Gastos"
