from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages 
from django.contrib.auth import  authenticate, login, logout
from django.http import HttpResponse
from formtools.wizard.views import SessionWizardView
from .models import *
from django.http import JsonResponse
from .forms import (
    GeolocalizarForm,
    QueRastrearForm,
    CuantosForm,
    ServicioInteresForm,
    SoftwareForm,
    DatosContactoForm
)

class CotizacionWizard(SessionWizardView):
    template_name = "cotizar.html"
    form_list = [
        GeolocalizarForm,
        QueRastrearForm,
        CuantosForm,
        ServicioInteresForm,
        SoftwareForm,
        DatosContactoForm
    ]

    def get_form_kwargs(self, step=None):
        """
        Modificar los kwargs que se pasan a los formularios del wizard.
        """
        # Llamar al método original para obtener los kwargs estándar
        kwargs = super(CotizacionWizard, self).get_form_kwargs(step)
        #print(f"get_form_kwargs: step: { step }")
        # Obtener el vehículo seleccionado en un paso anterior (por ejemplo, en el paso 'CuantosForm')
        #print (step)
        if step == '3' or step == '4': #'ServicioInteresForm'
            #print ("paso 3")
            #print (kwargs)
                        
            vehiculo_form_data = self.get_cleaned_data_for_step('1')
            #print("hola")
            
            if vehiculo_form_data:
                vehiculo = vehiculo_form_data.get('vehiculo')  # Aquí debes ajustar 'vehiculo' según el nombre del campo en 'CuantosForm'
                if vehiculo:
                    kwargs['vehiculo_id'] = vehiculo.id

            if step == '4':
                categoria_form_data = self.get_cleaned_data_for_step('3')
                print(f"categoria_form_data: {categoria_form_data}")
                if categoria_form_data:
                    categoria = categoria_form_data.get('categoria')
                    if categoria:
                        kwargs['categoria_id'] = categoria.id

        '''
        elif step == '4': #SoftwareForm
            vehiculo_form_data = self.get_cleaned_data_for_step('1')
            if vehiculo_form_data:
                vehiculo_id = vehiculo_form_data.get('vehiculo')  # Aquí debes ajustar 'vehiculo' según el nombre del campo en 'CuantosForm'
                if vehiculo_id:
                    kwargs['vehiculo_id'] = vehiculo_id.id
        '''
        return kwargs
    
    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        
        # Asegurarse de pasar el vehículo seleccionado al contexto
        vehiculo_form_data = self.get_cleaned_data_for_step('1')
        if vehiculo_form_data:
            context['vehiculo_id'] = vehiculo_form_data.get('vehiculo').id
        return context    

    def done(self, form_list, **kwargs):
        print("done")
        
        vehiculo_data = self.get_cleaned_data_for_step('1')
        vehiculo = vehiculo_data.get('vehiculo')
        print(f"vehiculo.id: {vehiculo.id}")

        cantidad_data = self.get_cleaned_data_for_step('2')
        cantidad = cantidad_data.get('cantidad')
        print(f"cantidad: {cantidad}")

        servicio_data = self.get_cleaned_data_for_step('3')
        servicio = servicio_data.get('servicio')
        categoria = servicio_data.get('categoria')
        print(f"servicio: {servicio}")
        print(f"categoria: {categoria}")
        print(f"servicio_data: {servicio_data}")

        software_data = self.get_cleaned_data_for_step('4')
        software = software_data.get('software')
        print(f"software: {software}")

        
        # para guardar el cliente en la BD
        datos_contacto_form = form_list[5]
        
        # Crear una nueva instancia del Cliente y guardarla en la base de datos
        cliente = Cliente(
            tipo=datos_contacto_form.cleaned_data['tipo'],
            nombre=datos_contacto_form.cleaned_data['nombre'],
            email=datos_contacto_form.cleaned_data['email'],
            telefono=datos_contacto_form.cleaned_data['telefono']
        )
        cliente.save()
        # para guardar el cliente en la BD 

        return render(self.request, 'cotizacion.html', {})

def get_servicios_por_categoria(request):
    categoria_id = request.GET.get('categoria_id', None)
    vehiculo_id = request.GET.get('vehiculo_id', None)  # Asegúrate de tener el vehículo si es necesario

    if categoria_id:
        servicios = Servicio.objects.filter(idCategoria=categoria_id)

        # Si necesitas filtrar también por vehículo:
        if vehiculo_id:
            servicios = servicios.filter(vehiculoservicio__Vehiculo=vehiculo_id)

        # Serializar los servicios
        servicios_data = [{'id': servicio.id, 'descripcion': servicio.descripcion} for servicio in servicios]

        return JsonResponse({'servicios': servicios_data})

    return JsonResponse({'servicios': []})



# Create your views here.
def cotizar(request):
    #return render(request, 'hola')
    context ={}
    print("cotizar")
    return render(request, 'cotizador.html', context)  


# Create your views here.
def inicio(request):
    #return render(request, 'hola')
    context ={}
    return render(request, '0-inicio.html', context)  


def cotizacion(request):
    context = {}
    return render(request, 'cotizacion.html', context)

def fin(request):
    context = {}
    return render(request, 'fin.html', context)

# En views.py
from django.shortcuts import render

def mail_proveedor(request):
    # Datos de ejemplo
    context = {
        'proveedor': {'nombre': 'Proveedor Ejemplo'},
        'cliente': {'nombre': 'Cliente Ejemplo'},
        'vehiculo': {'descripcion': 'Auto'},
        'cantidad': 1,
        'categoria': {'descripcion': 'Rastreo Vehicular'},
        'servicios': [{'descripcion': 'GPS'}, {'descripcion': 'Monitoreo en tiempo real'}],
        'software': [{'descripcion': 'Gestión de Flotas'}]
    }
    return render(request, 'mail_proveedor.html', context)
