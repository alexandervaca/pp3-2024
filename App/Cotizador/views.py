from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages 
from django.contrib.auth import  authenticate, login, logout
from formtools.wizard.views import SessionWizardView
from .models import *
from .utils import *
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import (
    GeolocalizarForm,
    QueRastrearForm,
    CuantosForm,
    ServicioInteresForm,
    SoftwareForm,
)

class CotizacionWizard(LoginRequiredMixin, SessionWizardView):
    login_url = 'login'  # URL a la que redirige si no está autenticado
    redirect_field_name = 'redirect_to'  # Campo de redirección para después de iniciar sesión
    template_name = "cotizar.html"
    form_list = [
        GeolocalizarForm,
        QueRastrearForm,
        CuantosForm,
        ServicioInteresForm,
        SoftwareForm
    ]

    def get_form_kwargs(self, step=None):
        """
        Modificar los kwargs que se pasan a los formularios del wizard.
        """
        # Llamar al metodo original para obtener los kwargs estandar
        kwargs = super(CotizacionWizard, self).get_form_kwargs(step)
        #print(f"get_form_kwargs: step: { step }")
        # Obtener el vehiculo seleccionado en un paso anterior (por ejemplo, en el paso 'CuantosForm')
        #print (step)
        if step == '3' or step == '4': #'ServicioInteresForm'
            #print ("paso 3")
            #print (kwargs)
                        
            vehiculo_form_data = self.get_cleaned_data_for_step('1')
            #print("hola")
            
            if vehiculo_form_data:
                print(f"vehiculo_form_data: {vehiculo_form_data}")
                vehiculo = vehiculo_form_data.get('vehiculo')  # Aqui debes ajustar 'vehiculo' segun el nombre del campo en 'CuantosForm'
                if vehiculo:
                    kwargs['vehiculo_id'] = vehiculo.id

            if step == '4':
                categoria_form_data = self.get_cleaned_data_for_step('3')
                print(f"categoria_form_data: {categoria_form_data}")
                if categoria_form_data:
                    categoria_id = categoria_form_data.get('categoria_id')
                    print(f"categoria_id: {categoria_id}")
                    if categoria_id:
                        kwargs['categoria_id'] = categoria_id

                #vehiculo_id = vehiculo_form_data.get('vehiculo')  # Aqui debes ajustar 'vehiculo' segun el nombre del campo en 'CuantosForm'
                #if vehiculo_id:
                #    kwargs['vehiculo_id'] = vehiculo_id.id


            #Vehiculo
            #vehiculo = servicio_interes_data.get('vehiculo_id')
            #Categoria 
            #categoria = servicio_interes_data.get('categoria')
            #Servicios
            #servicios = servicio_interes_data.get('servicio')
            #print(f"Vehiculo: {vehiculo}")
            #print(f"Categoria: {categoria}")
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
        
        # Asegurarse de pasar el vehiculo seleccionado al contexto
        vehiculo_form_data = self.get_cleaned_data_for_step('1')
        print(f"vehiculo_form_data 1: {vehiculo_form_data}")
        if vehiculo_form_data:
            context['vehiculo_id'] = vehiculo_form_data.get('vehiculo').id
        return context    

    def done(self, form_list, **kwargs):
        # Recorre cada paso y extrae los datos de cada formulario
        for step, form in enumerate(form_list):
            print(f"Datos del paso {step}: {form.cleaned_data}")

        #Creacion/obtencion del cliente
        datos_contacto_data = self.get_cleaned_data_for_step('5')  # Paso 6: DatosContactoForm
        
        # Llamar a la funcion que crea o actualiza el cliente
        cliente = self.request.user

        #Obtencion de datos necesarios para la cotizacion
        vehiculo_data         = self.get_cleaned_data_for_step('1')
        cuantos_data          = self.get_cleaned_data_for_step('2')  # Paso 3: CuantosForm
        servicio_interes_data = self.get_cleaned_data_for_step('3')  # Paso 4: ServicioInteresForm
        software_data         = self.get_cleaned_data_for_step('4')  # Paso 5: SoftwareForm
        #Cantidad
        cantidad = cuantos_data.get('cantidad')
        #Vehiculo
        vehiculo = vehiculo_data.get('vehiculo')
        #Categoria 
        categoria = servicio_interes_data.get('categoria_id')
        #Servicios
        servicios = servicio_interes_data.get('servicio')
        #Software
        software_ids = software_data.get('software')
        software = Servicio.objects.filter(id__in=software_ids)

        #Clase Cotizacion - crea instancia
        cotizacion = Cotizacion(cantidad, vehiculo, categoria, servicios, software, cliente)
        # Calcular total por proveedor
        total_por_proveedor = cotizacion.calcular_total_por_proveedor()
        #print("Total por proveedor:", total_por_proveedor)  # Para verificar en la consola
        # Guardar la cotizacion
        cotizacion_cabecera = cotizacion.guardar_cotizacion()        
        categoriabd = Categoria.objects.get(id=categoria)

        contexto = {
            'cliente': cliente,
            'vehiculo': vehiculo,
            'cantidad': cantidad,
            'categoria':categoriabd,
            'servicios':servicios,
            'software':software,
            'total_por_proveedor':total_por_proveedor,
            'cotizacion_cabecera':cotizacion_cabecera,
        }

        # Llamar a la funcion para enviar el correo
        enviar_cotizacion_cliente(contexto)

        return render(self.request, 'cotizacion.html', contexto)

def get_servicios_por_categoria(request):
    categoria_id = request.GET.get('categoria_id', None)
    vehiculo_id = request.GET.get('vehiculo_id', None)  # Asegurate de tener el vehiculo si es necesario

    if categoria_id:
        servicios = Servicio.objects.filter(idCategoria=categoria_id)

        # Si necesitas filtrar tambien por vehiculo:
        if vehiculo_id:
            servicios = servicios.filter(vehiculoservicio__Vehiculo=vehiculo_id)

        # Serializar los servicios
        servicios_data = [{'id': servicio.id, 'descripcion': servicio.descripcion} for servicio in servicios]

        return JsonResponse({'servicios': servicios_data})

    return JsonResponse({'servicios': []})

def enviar_mail_proveedores(request):
    # Obtener el parámetro 'proveedores' desde la URL (GET)
    proveedoresReq = request.GET.get('proveedores', None)
    print(f'enviar_mail_proveedores: {proveedoresReq}')
    
    # Dividir los proveedores en una lista y convertirlos a enteros
    proveedoresReq = proveedoresReq.split(',')
    proveedores = list(map(int, proveedoresReq))

    # Obtener el id de la cotización cabecera
    cotizacion_cabecera_id = request.GET.get('cotizacion_cabecera_id')

    # Buscar la cotización cabecera correspondiente al id
    cotizacionCabList = Cotizacion_cabecera.objects.filter(id=cotizacion_cabecera_id)

    # Si encuentra la cotización en la BD
    if cotizacionCabList:

         # Si se encuentra la cotización cabecera, obtener el primer objeto
        cotizacionCab = cotizacionCabList.__getitem__(0)

        # Obtener el cliente y otros datos de la cotización cabecera
        cliente = cotizacionCab.idCliente

        vehiculo = cotizacionCab.idVehiculo

        cantidad = cotizacionCab.cantidad
        
        # Obtener la categoría 'Software'
        catSoftware =Categoria.objects.get(descripcion = 'Software')       

        # Iterar sobre los proveedores seleccionados
        for proveedorId in proveedores:
            # Se obtienen los datos del proveedor de la BD
            proveedor = Proveedor.objects.get(id=proveedorId)
            # Inicializar listas para software y servicios
            software = []
            servicios = []

            # Se obtienen las líneas de las cotizaciones para ese proveedor
            cotizacionLinList = Cotizacion_linea.objects.filter(idCotizazion_cab=cotizacionCab.id,idProveedor=proveedorId)
            if cotizacionLinList:
                for item in cotizacionLinList:
                    print (item)
                    if item.idCategoria == catSoftware:
                        software.append(item.idServicio)
                    else:
                        #Agregamos el serivicio a la lista
                        servicios.append(item.idServicio)
                        # Asignamos la categoría elegida
                        categoria= item.idCategoria

                    # Actualizar el campo 'contacto' en la BD a True**
                    item.contacto = True  
                    item.save() 
            # Por cada proveedor mandamos guardamos el contexto y mandamos un mail.
            contexto = {
                'cliente': cliente,
                'proveedor': proveedor,
                'vehiculo': vehiculo,
                'cantidad': cantidad,
                'categoria':categoria,
                'servicios':servicios,
                'software':software
                }
            

            enviar_cotizacion_proveedor(contexto)


    return JsonResponse({'status': 'ok'})


def inicio(request):
    # context ={}
    return render(request, '0-inicio.html')  

@login_required(login_url='login')
def cotizar(request):
    context ={}
    print("cotizar")
    return render(request, 'cotizador.html', context)  


@login_required(login_url='login')
def cotizacion(request):
    context = {}
    return render(request, 'cotizacion.html', context)

@login_required(login_url='login')
def fin(request):
    context = {}
    return render(request, 'fin.html', context)
