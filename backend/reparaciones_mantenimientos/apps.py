"""Configuración de la app reparaciones_mantenimientos.

Fecha:
    27 - 01 - 2026
"""

from django.apps import AppConfig


class ReparacionesMantenimientosConfig(AppConfig):
    """Configura la app reparaciones_mantenimientos."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "reparaciones_mantenimientos"
    verbose_name = "Reparaciones y mantenimientos"
