from django.db import models
from Proveedores.models import Proveedor
import datetime

# Create your models here.
class Categoria(models.Model):
    descripcion =  models.CharField(max_length= 30,unique= True, verbose_name='Categoría', null= False)
    def __str__(self):
        return self.descripcion
    class Meta:
        db_table = 'categorias'
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['id']

class Servicio(models.Model):
    idCategoria    = models.ForeignKey(Categoria, on_delete=models.CASCADE, )
    descripcion =  models.CharField(max_length= 60, unique= False, verbose_name='Servicio', null= False)
    def __str__(self):
        return self.descripcion
        #return self.idCategoria, '-',  self.descripcion
    class Meta:
        db_table = 'servicios'
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'
        ordering = ['id']

class Vehiculo(models.Model):
    descripcion =  models.CharField(max_length= 30, unique= True, verbose_name='Vehículo', null= False)
    Servicio = models.ManyToManyField(Servicio, blank=True, through='VehiculoServicio') 
    def __str__(self):
        return self.descripcion
        #return f'{self.descripcion}-{self.idServicios}'
    class Meta:
        db_table = 'vehiculos'
        verbose_name = 'Vehículo'
        verbose_name_plural = 'Vehículos'
        ordering = ['id']

class VehiculoServicio(models.Model):
    Servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, blank=True, null=True)
    Vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return f'{self.Vehiculo} - {self.Servicio} '
    class Meta:
        db_table = 'vehiculoservicio'
        verbose_name = 'Vehículo Y Servicio'
        verbose_name_plural = 'Vehículos y Servicios'
        ordering = ['id']

class Cliente(models.Model):
    nombre   = models.CharField(max_length= 30, unique= True, verbose_name='Nombre', null= False)
    email    = models.EmailField(max_length= 40, verbose_name='E-Mail', null= False, blank= False)
    telefono = models.CharField(max_length= 25, verbose_name='Teléfono', null= True, blank= True)
    def __str__(self):
        return self.nombre
    class Meta:
        db_table = 'clientes'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['id']


class Cotizacion_cabecera(models.Model):
    idCliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, )
    fecha     = models.DateField( auto_now_add=True, null= True, verbose_name='Fecha',)
    def __str__(self):
        return self.nombre
    class Meta:
        db_table = 'cotizaciones_cab'
        verbose_name = 'Cotización cabecera'
        verbose_name_plural = 'Cotizaciones cabecera'
        ordering = ['id']


class Cotizacion_linea(models.Model):
    idCoticazion_cab    = models.ForeignKey(Cotizacion_cabecera, on_delete=models.CASCADE, verbose_name='Cotización cabecera' )
    idProveedor         = models.ForeignKey(Proveedor, on_delete=models.CASCADE,verbose_name='Proveedor', )
    idVechiculoServicio = models.ForeignKey(VehiculoServicio, on_delete=models.CASCADE, verbose_name='Vehículo-Servicio',)
    cantidad            = models.IntegerField(verbose_name='Cantidad',)
    precio_unitario     = models.DecimalField( decimal_places=2, max_digits=10, verbose_name='Precio x Unidad',)
    contacto            = models.BooleanField(default= False,verbose_name='Contacto' )
    def __str__(self):
        return self.nombre
    class Meta:
        db_table = 'cotizaciones_linea'
        verbose_name = 'Cotización linea'
        verbose_name_plural = 'Cotizaciones linea'
        ordering = ['id']

class Tarifa(models.Model):
    idVechiculoServicio = models.ForeignKey(VehiculoServicio, on_delete=models.CASCADE, verbose_name='Vehículo-Servicio',)
    idProveedor         = models.ForeignKey(Proveedor, on_delete=models.CASCADE,verbose_name='Proveedor', )
    precio_unitario     = models.DecimalField( decimal_places=2, max_digits=10, verbose_name='Precio x Unidad',)
    def __str__(self):
        return f'{self.idVechiculoServicio}-{self.idProveedor}-{self.precio_unitario}'
    class Meta:
        db_table = 'tarifa'
        verbose_name = 'Tarifa'
        verbose_name_plural = 'Tarifas'
        ordering = ['id']