from django.contrib import admin
from .models import Consorcio


@admin.register(Consorcio)
class ConsorcioAdmin(admin.ModelAdmin):
	list_display = ("cuit", "razon_social", "ciudad", "usuario")
	search_fields = ("cuit", "razon_social", "ciudad")
