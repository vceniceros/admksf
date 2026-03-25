"""URLs para la app servicios_mensuales."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.listar_servicios_mensuales, name="listar_servicios_mensuales"),
    path("crear/", views.crear_servicio_mensual, name="crear_servicio_mensual"),
    path("<str:cuit_proveedor>/", views.obtener_servicio_mensual, name="obtener_servicio_mensual"),
    path("<str:cuit_proveedor>/actualizar/", views.actualizar_servicio_mensual, name="actualizar_servicio_mensual"),
    path("<str:cuit_proveedor>/eliminar/", views.eliminar_servicio_mensual, name="eliminar_servicio_mensual"),
]
