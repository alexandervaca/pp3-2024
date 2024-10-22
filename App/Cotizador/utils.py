from .models import Cliente
from .models import *
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
import base64
import os
import copy
from django.conf import settings
from pathlib import Path

def obtener_o_crear_cliente(datos_contacto_data):
    """
    Extrae los datos del contacto, intenta obtener un cliente por email. Si no existe, lo crea. 
    Si ya existe, actualiza los datos si son diferentes y devuelve el cliente.
    """
    # Extraer los datos del formulario
    tipo = datos_contacto_data.get('tipo')
    nombre = datos_contacto_data.get('nombre')
    email = datos_contacto_data.get('email')
    telefono = datos_contacto_data.get('telefono')

    # Intentar obtener un cliente con el mismo email
    cliente, created = Cliente.objects.get_or_create(
        email=email,  # Búsqueda por email
        defaults={  # Estos valores se usarán si no existe un cliente con ese email
            'nombre': nombre,
            'telefono': telefono,
            'tipo': tipo,
        }
    )

    if not created:
        # Si el cliente ya existe, verifica si alguno de los campos ha cambiado
        if cliente.nombre != nombre:
            cliente.nombre = nombre
        if cliente.telefono != telefono:
            cliente.telefono = telefono
        if cliente.tipo != tipo:
            cliente.tipo = tipo

        # Guardar los cambios si hubo alguna actualización
        cliente.save()

    return cliente

class Cotizacion:
    def __init__(self, cantidad, vehiculo, categoria, servicios, software, cliente):
        self.cantidad = cantidad
        self.vehiculo = vehiculo
        self.categoria = categoria
        self.servicios = servicios
        self.software = software
        self.cliente = cliente

        # Obtener tarifas al inicializar el objeto
        self.tarifas = self.obtener_tarifas()

    def __str__(self):
        return (f"Cotización:\n"
                f"Cantidad: {self.cantidad}\n"
                f"Vehículo: {self.vehiculo}\n"
                f"Categoría: {self.categoria}\n"
                f"Servicios: {self.servicios}\n"
                f"Software: {self.software}\n"
                f"Cliente: {self.cliente}")
    
    def obtener_tarifas(self):
        """
        Obtiene las tarifas correspondientes al vehículo y servicios asociados a esta cotización.
        """
        tarifas = []
        for servicio in self.servicios:
            tarifas_query = Tarifa.objects.filter(
                idVechiculoServicio__Vehiculo=self.vehiculo,
                idProveedor=servicio.idProveedor  # Asumiendo que `servicio` tiene un atributo `idProveedor`
            )
            tarifas.extend(tarifas_query)
        
        # Obtener tarifas para cada software seleccionado
        if self.software:
            for soft in self.software:
                tarifas_software = Tarifa.objects.filter(idVechiculoServicio__Servicio__id=soft.id)
                tarifas.extend(tarifas_software)

        return tarifas
    
    def calcular_total_por_proveedor(self):
        total_por_proveedor = []

        # Diccionario temporal para acumular los totales por proveedor
        totales = {}

        for tarifa in self.tarifas:
            proveedor = tarifa.idProveedor  
            monto = tarifa.precio_unitario

            # Si la tarifa pertenece a software, no multiplicar por cantidad
            if tarifa.idVechiculoServicio.Servicio.idCategoria == self.software:
                cantidad_a_sumar = 1  # No multiplicar
            else:
                cantidad_a_sumar = self.cantidad  # Multiplicar por la cantidad

           # Acumular el total por proveedor
            if proveedor.id in totales:
                totales[proveedor.id]['total'] += monto * cantidad_a_sumar
            else:
                #print(f'proveedor.logo.url: {proveedor.logo.url }')
                #print(f'proveedor.logo: {proveedor.logo}')
                totales[proveedor.id] = {
                    'id': proveedor.id,
                    'empresa': proveedor.empresa,
                    'email': proveedor.email,
                    'logo': proveedor.logo.url,
                    'web': proveedor.web,
                    'total': monto * cantidad_a_sumar
                }

        # Convertir el diccionario en un array de diccionarios
        for proveedor_id, data in totales.items():
            total_por_proveedor.append(data)

        return total_por_proveedor
    
    def guardar_cotizacion(self):
    # Crear la cabecera de la cotización
        cotizacion_cabecera = Cotizacion_cabecera.objects.create(
            idCliente=self.cliente
        )
        
        # Guardar líneas de cotización
        for tarifa in self.tarifas:
            Cotizacion_linea.objects.create(
                idCoticazion_cab=cotizacion_cabecera,
                idProveedor=tarifa.idProveedor ,  
                idVechiculoServicio=tarifa.idVechiculoServicio,
                cantidad=self.cantidad,
                precio_unitario=tarifa.precio_unitario,
                contacto=False  # Dejar contacto vacío
            )

        return cotizacion_cabecera  # Devolver la cabecera para referencia futura
    
def enviar_cotizacion_cliente(contexto):
    # Hacer una copia profunda del contexto para no modificar el original
    contexto2 = copy.deepcopy(contexto)
   
    # Configura los parámetros del correo
    asunto = "La cotización del GURU"
    destinatario = contexto['cliente'].email  # Dirección de correo del cliente
    remitente = settings.DEFAULT_FROM_EMAIL

     # Renderiza el cuerpo del correo con la plantilla
    mensaje_html = render_to_string('mail_cliente.html', contexto2)
    mensaje_texto = strip_tags(mensaje_html)  # Alternativa en texto plano

    # Envía el correo
    send_mail(
        asunto,
        mensaje_texto,  # Contenido en texto plano
        remitente,
        [destinatario],
        html_message=mensaje_html  # Contenido en HTML
    )


    