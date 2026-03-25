"""URLs para la app caratula."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.listar_caratulas, name="listar_caratulas"),
    path("crear/", views.crear_caratula, name="crear_caratula"),
    path("consorcio/<str:cuit_consorcio>/", views.listar_caratulas_por_consorcio, name="listar_caratulas_por_consorcio"),
    path("<str:fecha_caratula>/", views.obtener_caratula, name="obtener_caratula"),
    path("<str:fecha_caratula>/actualizar/", views.actualizar_caratula, name="actualizar_caratula"),
    path("<str:fecha_caratula>/eliminar/", views.eliminar_caratula, name="eliminar_caratula"),
]
