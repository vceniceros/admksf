from django.contrib import admin

from .models import Rol, Usuario


@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("nombre",)


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "correo_electronico",
        "nombre",
        "apellido",
        "esta_activo",
        "rol",
        "ultimo_ingreso",
    )
    list_filter = ("esta_activo", "rol")
    search_fields = ("correo_electronico", "nombre", "apellido")