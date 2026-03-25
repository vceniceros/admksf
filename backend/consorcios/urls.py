"""URLs para la app consorcios."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.listar_consorcios, name="listar_consorcios"),
    path("crear/", views.crear_consorcio, name="crear_consorcio"),
    path("<str:cuit>/imagen/", views.subir_imagen_consorcio, name="subir_imagen_consorcio"),
    path("<str:cuit>/", views.obtener_consorcio, name="obtener_consorcio"),
    path("<str:cuit>/actualizar/", views.actualizar_consorcio, name="actualizar_consorcio"),
    path("<str:cuit>/eliminar/", views.eliminar_consorcio, name="eliminar_consorcio"),
]
