from django.db import models

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
    servicios = models.ManyToManyField(Servicio) 
    def __str__(self):
        return self.descripcion
    class Meta:
        db_table = 'vehiculos'
        verbose_name = 'Vehículo'
        verbose_name_plural = 'Vehículos'
        ordering = ['id']

#Video con queries    https://www.youtube.com/watch?v=QBzsoQPgJQ8&t=338s&ab_channel=codigofacilito
#Video que me falta ver   https://www.youtube.com/watch?v=hX8Mcj3-8hk&t=201s&ab_channel=Neunapp   
#Ver este https://www.youtube.com/watch?v=DpHqdb2uaDs&t=2s&ab_channel=OpenBootcamp !!!!!!!!!!!!!!!!!!!!!!