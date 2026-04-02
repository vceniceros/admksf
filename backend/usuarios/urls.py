"""URLs para la app usuarios."""

from django.urls import path

from . import views

urlpatterns = [
    path("registrar/", views.registrar_usuario, name="registrar_usuario"),
    path("login/", views.login_usuario, name="login_usuario"),
    path("autenticado/", views.verificar_autenticacion, name="verificar_autenticacion"),
    path("recuperar-contrasena/", views.recuperar_contrasena_usuario, name="recuperar_contrasena_usuario"),
]