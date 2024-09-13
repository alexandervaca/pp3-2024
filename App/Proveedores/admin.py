from django.contrib import admin
from django import forms
from django.contrib import admin
from django.utils.html import format_html
from .models import Pais, Provincia, Ciudad, Proveedor


@admin.register(Pais)
class PaisAdmin(admin.ModelAdmin):
    list_display=('id','nombre',)
    list_display_links=('nombre',)

@admin.register(Provincia)
class ProvinciaAdmin(admin.ModelAdmin):
    list_display=('id','idPais','nombre',)
    list_display_links=('nombre',)

@admin.register(Ciudad)
class CiudadAdmin(admin.ModelAdmin):
    list_display=('id','idProvincia','nombre',)
    list_display_links=('nombre',)
    search_fields=('nombre',)
    list_filter=('idProvincia',)

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display=('id','empresa', 'idPais', 'idProvincia', 'idCiudad', 'calle', 'altura', 'telefono', 'email', 'web', 'imagen')
    list_display_links=('empresa',)
    list_filter=('empresa',)
    def imagen(self, obj):
        return format_html('<img src= {} width="100" heigth="70" />', obj.logo.url )