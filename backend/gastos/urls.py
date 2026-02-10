"""URLs para la app gastos."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.listar_gastos, name="listar_gastos"),
    path("crear/", views.crear_gasto, name="crear_gasto"),
    path("cargar-desde-archivo/", views.cargar_gasto_desde_archivo, name="cargar_gasto_desde_archivo"),
    path("extraer-desde-archivo/", views.extraer_gasto_desde_archivo, name="extraer_gasto_desde_archivo"),
    path("consorcio/<str:cuit_consorcio>/", views.listar_gastos_por_consorcio, name="listar_gastos_por_consorcio"),
    path("proveedor/<str:cuit_proveedor>/", views.listar_gastos_por_proveedor, name="listar_gastos_por_proveedor"),
    path("tipo/<str:tipo_gasto>/", views.listar_gastos_por_tipo, name="listar_gastos_por_tipo"),
    path("estado/<str:estado_pago>/", views.listar_gastos_por_estado, name="listar_gastos_por_estado"),
    path("<int:id_gasto>/", views.obtener_gasto, name="obtener_gasto"),
    path("<int:id_gasto>/actualizar/", views.actualizar_gasto, name="actualizar_gasto"),
    path("<int:id_gasto>/eliminar/", views.eliminar_gasto, name="eliminar_gasto"),
]
