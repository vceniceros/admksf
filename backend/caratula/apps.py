"""Configuración de la app caratula.

Fecha:
    27 - 01 - 2026
"""

from django.apps import AppConfig


class CaratulaConfig(AppConfig):
    """Configura la app caratula."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "caratula"
    verbose_name = "Carátula"
