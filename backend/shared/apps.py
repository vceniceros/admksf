"""Configuración de la app shared.

Fecha:
    27 - 01 - 2026
"""

from django.apps import AppConfig


class SharedConfig(AppConfig):
    """Configura la app shared para utilidades comunes."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "shared"
    verbose_name = "Shared"
