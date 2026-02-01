"""URLs para la app saldo_mensual."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.listar_saldos_mensuales, name="listar_saldos_mensuales"),
    path("crear/", views.crear_saldo_mensual, name="crear_saldo_mensual"),
    path("consorcio/<str:cuit_consorcio>/", views.listar_saldos_por_consorcio, name="listar_saldos_por_consorcio"),
    path("unidad/<int:numero_unidad>/", views.listar_saldos_por_unidad_funcional, name="listar_saldos_por_unidad_funcional"),
    path("<int:id_saldo>/", views.obtener_saldo_mensual, name="obtener_saldo_mensual"),
    path("<int:id_saldo>/actualizar/", views.actualizar_saldo_mensual, name="actualizar_saldo_mensual"),
    path("<int:id_saldo>/eliminar/", views.eliminar_saldo_mensual, name="eliminar_saldo_mensual"),
]
