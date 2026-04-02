"""Configuración de la app usuarios."""

from django.apps import AppConfig


class UsuariosConfig(AppConfig):
    """Configura la app usuarios."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "usuarios"
    verbose_name = "Usuarios"