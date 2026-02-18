"""Rutas para la app expensas.

Fecha:
    14 - 02 - 2026
"""

from django.urls import path

from . import views

urlpatterns = [
    path("liquidar/", views.liquidar_expensa, name="liquidar-expensa"),
    path("templates/", views.listar_templates, name="listar-templates"),
    path(
        "templates/consorcio/<str:cuit_consorcio>/",
        views.listar_templates_por_consorcio,
        name="listar-templates-por-consorcio",
    ),
    path("templates/crear/", views.crear_template, name="crear-template"),
    path("templates/<int:template_id>/", views.obtener_template, name="obtener-template"),
    path(
        "templates/<int:template_id>/actualizar/",
        views.actualizar_template,
        name="actualizar-template",
    ),
    path(
        "templates/<int:template_id>/eliminar/",
        views.eliminar_template,
        name="eliminar-template",
    ),
]
