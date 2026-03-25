from django.contrib import admin
from .models import UnidadFuncional

@admin.register(UnidadFuncional)
class UnidadFuncionalAdmin(admin.ModelAdmin):
    # Esto evita que el admin explote si faltan campos, 
    # ya que solo usa los que realmente existen en el modelo.
    list_display = [field.name for field in UnidadFuncional._meta.fields]
