"""URLs para la app reparaciones_mantenimientos."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.listar_reparaciones_mantenimientos, name="listar_reparaciones_mantenimientos"),
    path("crear/", views.crear_reparacion_mantenimiento, name="crear_reparacion_mantenimiento"),
    path("<str:cuit_proveedor>/", views.obtener_reparacion_mantenimiento, name="obtener_reparacion_mantenimiento"),
    path("<str:cuit_proveedor>/actualizar/", views.actualizar_reparacion_mantenimiento, name="actualizar_reparacion_mantenimiento"),
    path("<str:cuit_proveedor>/eliminar/", views.eliminar_reparacion_mantenimiento, name="eliminar_reparacion_mantenimiento"),
]
