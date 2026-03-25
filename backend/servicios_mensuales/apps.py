"""Configuración de la app servicios_mensuales.

Fecha:
    27 - 01 - 2026
"""

from django.apps import AppConfig


class ServiciosMensualesConfig(AppConfig):
    """Configura la app servicios_mensuales."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "servicios_mensuales"
    verbose_name = "Servicios Mensuales"
