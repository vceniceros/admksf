"""Configuración de la app propietarios.

Fecha:
    27 - 01 - 2026
"""

from django.apps import AppConfig


class PropietariosConfig(AppConfig):
    """Configura la app propietarios."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "propietarios"
    verbose_name = "Propietarios"
