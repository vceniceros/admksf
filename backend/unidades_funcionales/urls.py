"""URLs para la app unidades_funcionales."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.listar_unidades_funcionales, name="listar_unidades_funcionales"),
    path("crear/", views.crear_unidad_funcional, name="crear_unidad_funcional"),
    path("consorcio/<str:cuit_consorcio>/", views.listar_unidades_por_consorcio, name="listar_unidades_por_consorcio"),
    path("propietario/<str:dni_propietario>/", views.listar_unidades_por_propietario, name="listar_unidades_por_propietario"),
    path("<int:numero>/", views.obtener_unidad_funcional, name="obtener_unidad_funcional"),
    path("<int:numero>/actualizar/", views.actualizar_unidad_funcional, name="actualizar_unidad_funcional"),
    path("<int:numero>/eliminar/", views.eliminar_unidad_funcional, name="eliminar_unidad_funcional"),
]
