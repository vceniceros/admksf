"""Configuración de la app expensas.

Fecha:
    14 - 02 - 2026
"""

from django.apps import AppConfig


class ExpensasConfig(AppConfig):
    """Configuración de la app expensas."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "expensas"
