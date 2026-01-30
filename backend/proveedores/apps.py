"""Configuración de la app proveedores.

Fecha:
    27 - 01 - 2026
"""

from django.apps import AppConfig


class ProveedoresConfig(AppConfig):
    """Configura la app proveedores."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "proveedores"
    verbose_name = "Proveedores"
