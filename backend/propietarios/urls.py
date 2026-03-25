"""URLs para la app propietarios."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.listar_propietarios, name="listar_propietarios"),
    path("crear/", views.crear_propietario, name="crear_propietario"),
    path("<str:dni>/", views.obtener_propietario, name="obtener_propietario"),
    path("<str:dni>/actualizar/", views.actualizar_propietario, name="actualizar_propietario"),
    path("<str:dni>/eliminar/", views.eliminar_propietario, name="eliminar_propietario"),
]
