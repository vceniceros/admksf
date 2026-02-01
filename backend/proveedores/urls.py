"""URLs para la app proveedores."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.listar_proveedores, name="listar_proveedores"),
    path("crear/", views.crear_proveedor, name="crear_proveedor"),
    path("tipo/<str:tipo_proveedor>/", views.listar_proveedores_por_tipo, name="listar_proveedores_por_tipo"),
    path("<str:cuit>/", views.obtener_proveedor, name="obtener_proveedor"),
    path("<str:cuit>/actualizar/", views.actualizar_proveedor, name="actualizar_proveedor"),
    path("<str:cuit>/eliminar/", views.eliminar_proveedor, name="eliminar_proveedor"),
]
