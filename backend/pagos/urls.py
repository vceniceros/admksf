"""URLs para la app pagos."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.listar_pagos, name="listar_pagos"),
    path("crear/", views.crear_pago, name="crear_pago"),
    path("consorcio/<str:cuit_consorcio>/", views.listar_pagos_por_consorcio, name="listar_pagos_por_consorcio"),
    path("propietario/<str:dni_propietario>/", views.listar_pagos_por_propietario, name="listar_pagos_por_propietario"),
    path("unidad/<int:numero_unidad>/", views.listar_pagos_por_unidad_funcional, name="listar_pagos_por_unidad_funcional"),
    path("<int:id_pago>/", views.obtener_pago, name="obtener_pago"),
    path("<int:id_pago>/actualizar/", views.actualizar_pago, name="actualizar_pago"),
    path("<int:id_pago>/eliminar/", views.eliminar_pago, name="eliminar_pago"),
]
