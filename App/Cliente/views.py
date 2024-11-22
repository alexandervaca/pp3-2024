from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Cotizador.models import Cotizacion_cabecera, Cotizacion_linea
from django.contrib.auth.forms import UserChangeForm

# Create your views here.

@login_required(login_url='login')
def mis_cotizaciones(request):
    # Obtenemos las cotizaciones del usuario logueado
    usuario = request.user
    cotizaciones = Cotizacion_cabecera.objects.filter(idCliente=usuario)
    contexto = []

    # Recorremos cada cotización para calcular el total
    for cotizacion in cotizaciones:
        total_por_proveedor = {}

        # Recorremos cada línea de la cotización para calcular el total por proveedor
        for linea in cotizacion.cotizacion_linea_set.all():
            proveedor = linea.idProveedor
            precio_unitario = linea.precio_unitario
            cantidad = cotizacion.cantidad

            # Inicializar datos del proveedor si aún no existe en el diccionario
            if proveedor not in total_por_proveedor:
                total_por_proveedor[proveedor] = {
                    "empresa": proveedor.empresa,
                    "lineas": [],
                    "total": 0, 
                    "contacto": linea.contacto
                }
            if linea.idCategoria.descripcion == "Software":
                subtotal = linea.precio_unitario  # Multiplica por 1 si es Software
            else:
                subtotal = linea.precio_unitario * cotizacion.cantidad  # Multiplica por cantidad para otros servicios

            # Agregamos la línea al proveedor
            total_por_proveedor[proveedor]["lineas"].append({
                "categoria": linea.idCategoria.descripcion,
                "servicio": linea.idServicio.descripcion if linea.idServicio else "N/A",  # Aseguramos que se maneje la ausencia de servicio
                "precio_unitario": precio_unitario,
                "contacto": linea.contacto
            })

            # Acumular el subtotal en el total del proveedor
            total_por_proveedor[proveedor]["total"] += subtotal

        # Agregamos cada cotización y su total al contexto
        contexto.append({
        "cotizacion": cotizacion,
        "proveedores": total_por_proveedor.values()
         })

    # Pasamos el contexto al template
    return render(request, 'mis_cotizaciones.html', {'cotizaciones': contexto})

#-------------------------------------------------------------------------------------#

@login_required(login_url='login')  # Asegura que el usuario esté logueado
def ver_editar_perfil(request):
    # Obtener los datos del usuario logueado
    usuario = request.user
    
    # Si es una petición POST (cuando se envía el formulario)
    if request.method == 'POST':
        # Crear un formulario con los datos del usuario
        formulario = UserChangeForm(request.POST, instance=usuario)
        if formulario.is_valid():
            formulario.save()  # Guardar los cambios
            return redirect('perfil')  # Redirigir después de guardar
    else:
        formulario = UserChangeForm(instance=usuario)  # Mostrar el formulario con los datos actuales

    return render(request, 'mis_datos.html', {'formulario': formulario})