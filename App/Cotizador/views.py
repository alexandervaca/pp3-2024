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
from .utils import *
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
        if step == '3' or step == '4': #'ServicioInteresForm'
            #print ("paso 3")
            #print (kwargs)
                        
            vehiculo_form_data = self.get_cleaned_data_for_step('1')
            print("hola")
            
            if vehiculo_form_data:
                vehiculo_id = vehiculo_form_data.get('vehiculo')  # Aquí debes ajustar 'vehiculo' según el nombre del campo en 'CuantosForm'
                if vehiculo_id:
                    kwargs['vehiculo_id'] = vehiculo_id.id
        
        elif step == '4':
            servicio_interes_data = self.get_cleaned_data_for_step('3')  
            print (servicio_interes_data)

            #Vehículo
            #vehiculo = servicio_interes_data.get('vehiculo_id')
            #Categoría 
            #categoria = servicio_interes_data.get('categoria')
            #Servicios
            #servicios = servicio_interes_data.get('servicio')
            #print(f"Vehículo: {vehiculo}")
            #print(f"Categoría: {categoria}")
            #print(f"Servicios: {servicios}")
        
            
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
        vehiculo_form_data = self.get_cleaned_data_for_step('4')
        if vehiculo_form_data:
            context['vehiculo_id'] = vehiculo_form_data.get('vehiculo')

        return context    

    def done(self, form_list, **kwargs):
        # Recorre cada paso y extrae los datos de cada formulario
        for step, form in enumerate(form_list):
            print(f"Datos del paso {step}: {form.cleaned_data}")

        #Creación/obtención del cliente
        datos_contacto_data = self.get_cleaned_data_for_step('5')  # Paso 6: DatosContactoForm
        # Llamar a la función que crea o actualiza el cliente
        cliente = obtener_o_crear_cliente(datos_contacto_data)

        #Obtención de datos necesarios para la cotización
        vehiculo_data         = self.get_cleaned_data_for_step('1')
        cuantos_data          = self.get_cleaned_data_for_step('2')  # Paso 3: CuantosForm
        servicio_interes_data = self.get_cleaned_data_for_step('3')  # Paso 4: ServicioInteresForm
        software_data         = self.get_cleaned_data_for_step('4')  # Paso 5: SoftwareForm
        #Cantidad
        cantidad = cuantos_data.get('cantidad')
        #Vehículo
        vehiculo = vehiculo_data.get('vehiculo')
        #Categoría 
        categoria = servicio_interes_data.get('categoria')
        #Servicios
        servicios = servicio_interes_data.get('servicio')
        #Software
        software_ids = software_data.get('software')
        software = Servicio.objects.filter(id__in=software_ids)


        print(f"Cantidad: {cantidad}")
        print(f"Vehículo: {vehiculo}")
        print(f"Categoría: {categoria}")
        print(f"Servicios: {servicios}")
        print(f"Software: {software}")
        print (f"Paso 3: {servicio_interes_data}")



        #Clase Cotizacion - crea instancia
        cotizacion = Cotizacion(cantidad, vehiculo, categoria, servicios, software, cliente)
        # Calcular total por proveedor
        total_por_proveedor = cotizacion.calcular_total_por_proveedor()
        #print("Total por proveedor:", total_por_proveedor)  # Para verificar en la consola
        # Guardar la cotización
        cotizacion_cabecera = cotizacion.guardar_cotizacion()        

        contexto = {
            'cliente': cliente,
            'vehiculo': vehiculo,
            'cantidad': cantidad,
            'categoria':categoria,
            'servicios':servicios,
            'software':software,
            'total_por_proveedor':total_por_proveedor,
            'cotizacion_cabecera':cotizacion_cabecera,
        }

        # Llamar a la función para enviar el correo
        enviar_cotizacion_cliente(contexto)

        return render(self.request, 'cotizacion.html', contexto)

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