from django.contrib import admin
from django import forms
from django.contrib import admin
from django.utils.html import format_html
from .models import Vehiculo, Categoria, Servicio


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display=('id','descripcion',)
    list_display_links=('descripcion',)

class ServicioForm(forms.ModelForm): 
    def __init__(self, *args, **kwargs):
        super(ServicioForm, self).__init__(*args, **kwargs)
        wtf = Servicio.objects.filter(pk=self.instance.id);
        w = self.fields['servicios'].widget
        choices = []
        for choice in wtf:
            choices.append((choice.id, choice.descripcion))
        w.choices = choices

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display=('id','descripcion',)
    list_display_links=('descripcion',)
    filter_horizontal= ('servicios',)
    #form = ServicioForm
    

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    pass
    list_display=('id','idCategoria','descripcion',)
    search_fields=('descripcion',)
    list_display_links=('descripcion',)
    list_filter=('idCategoria',)