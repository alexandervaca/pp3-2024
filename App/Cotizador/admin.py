from django.contrib import admin
from django import forms
from django.contrib import admin
from django.utils.html import format_html
from .models import  Categoria, Vehiculo, Servicio, VehiculoServicio, Cliente, Cotizacion_cabecera, Cotizacion_linea, Tarifa
#,Cliente, Cotizacion_cabecera, Cotizacion_linea


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display=('id','descripcion',)
    list_display_links=('descripcion',)
    
@admin.register(VehiculoServicio)
class VehiculoServicioAdmin(admin.ModelAdmin):
    #list_display=('Servicio','Vehiculo','Servicio_id','Vehiculo_id',)
    list_display=('Vehiculo', 'Servicio',)
    #search_fields=('Servicio ','Vehiculo',)
    #list_display_links=('id',)
    list_filter=('Vehiculo','Servicio',)

class VehiculoServicioInline(admin.TabularInline):
    model = VehiculoServicio
    extra = 1
    

class ServicioForm(forms.ModelForm): 
    def __init__(self, *args, **kwargs):
        super(ServicioForm, self).__init__(*args, **kwargs)
        wtf = Servicio.objects.filter(pk=self.instance.id);
        w = self.fields['servicio'].widget
        choices = []
        for choice in wtf:
            choices.append((choice.id, choice.descripcion))
        w.choices = choices

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    inlines = [VehiculoServicioInline,]
    list_display=('id','descripcion',)
    list_display_links=('descripcion',)
    #filter_horizontal= ('Servicio',)
    #form = ServicioForm
    

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    #inlines = [VehiculoServicioInline,]
    list_display=('id','idCategoria','descripcion',)
    search_fields=('descripcion',)
    list_display_links=('descripcion',)
    list_filter=('idCategoria',)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display=('id','nombre','email','telefono',)
    search_fields=('nombre','email',)
    list_display_links=('nombre',)

@admin.register(Cotizacion_cabecera)
class Cotizaciones_CabeceraAdmin(admin.ModelAdmin):
    list_display=('id','idCliente','fecha',)
    search_fields=('idCliente',)
    list_display_links=('id',)    
    list_filter=('fecha',)

@admin.register(Cotizacion_linea)
class Cotizaciones_LineaAdmin(admin.ModelAdmin):
    list_display=('id', 'idCoticazion_cab', 'idProveedor', 'idVechiculoServicio', 'cantidad', 'precio_unitario', 'contacto')
    search_fields=('idVechiculoServicio', 'idProveedor',)
    list_display_links=('id',)    
    list_filter=('contacto', 'idProveedor',)

@admin.register(Tarifa)
class TarifaAdmin(admin.ModelAdmin):
    list_display=('id','idVechiculoServicio', 'idProveedor', 'precio_unitario')
    search_fields=('idVechiculoServicio', 'idProveedor',)
    list_display_links=('id',)    
    list_filter=('idVechiculoServicio', 'idProveedor',)