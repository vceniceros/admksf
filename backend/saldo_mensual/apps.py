"""Configuración de la app saldo_mensual.

Fecha:
    27 - 01 - 2026
"""

from django.apps import AppConfig


class SaldoMensualConfig(AppConfig):
    """Configura la app saldo_mensual."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "saldo_mensual"
    verbose_name = "Saldo mensual"
