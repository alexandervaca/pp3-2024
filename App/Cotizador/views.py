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
        print(f"get_form_kwargs: step: { step }")
        # Obtener el vehículo seleccionado en un paso anterior (por ejemplo, en el paso 'CuantosForm')
        #print (step)
        if step == '3': #'ServicioInteresForm'
            #print ("paso 3")
            #print (kwargs)
                        
            vehiculo_form_data = self.get_cleaned_data_for_step('1')
            print("hola")
            
            if vehiculo_form_data:
                vehiculo_id = vehiculo_form_data.get('vehiculo')  # Aquí debes ajustar 'vehiculo' según el nombre del campo en 'CuantosForm'
                if vehiculo_id:
                    kwargs['vehiculo_id'] = vehiculo_id.id
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
        servicio_form_data = self.get_cleaned_data_for_step('3')
        print(f"servicio_form_data {servicio_form_data}")


        # para guardar el cliente en la BD
        print(form_list)
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

        return print("done return") 


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
