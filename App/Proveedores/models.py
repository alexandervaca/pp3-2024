from django.db import models

# Create your models here.
class Pais(models.Model):
    nombre =  models.CharField(max_length= 30,unique= True, verbose_name='Pais', null= False)
    def __str__(self):
        return self.nombre
    class Meta:
        db_table = 'paises'
        verbose_name = 'País'
        verbose_name_plural = 'Paises'
        ordering = ['id']

class Provincia(models.Model):
    idPais   = models.ForeignKey(Pais, on_delete=models.CASCADE, verbose_name='País' )
    nombre  =  models.CharField(max_length= 30, unique= False, verbose_name='Provincia', null= False)
    def __str__(self):
        return self.nombre
        #return self.idCategoria, '-',  self.descripcion
    class Meta:
        db_table = 'provincia'
        verbose_name = 'Provincia'
        verbose_name_plural = 'Provincias'
        ordering = ['id']

class Ciudad(models.Model):
    idProvincia   = models.ForeignKey(Provincia, on_delete=models.CASCADE,verbose_name='Provincia' )
    nombre  =  models.CharField(max_length= 30, unique= False, verbose_name='Ciudad', null= False)
    def __str__(self):
        return self.nombre
        #return self.idCategoria, '-',  self.descripcion
    class Meta:
        db_table = 'ciudad'
        verbose_name = 'Ciudad'
        verbose_name_plural = 'Ciudades'
        ordering = ['id']

class Proveedor(models.Model):
    empresa     = models.CharField(max_length= 30, unique= True, verbose_name='Empresa', null= False)
    idPais      = models.ForeignKey(Pais, on_delete=models.SET_NULL,verbose_name='Pais', null= True,blank= True )  
    idProvincia = models.ForeignKey(Provincia, on_delete=models.SET_NULL,verbose_name='Provincia', null= True,blank= True ) 
    idCiudad    = models.ForeignKey(Ciudad, on_delete=models.SET_NULL,verbose_name='Ciudad', null= True,blank= True ) 
    calle       = models.CharField(max_length= 30, verbose_name='Calle', null= True, blank= True)
    altura      = models.CharField(max_length= 10, verbose_name='Altura', null= True, blank= True)
    telefono    = models.CharField(max_length= 25, verbose_name='Teléfono', null= True, blank= True)
    email       = models.EmailField(max_length= 40, verbose_name='E-Mail', null= False, blank= False)
    web         = models.CharField(max_length= 40, verbose_name='Web', null= True, blank= True)
    logo        = models.ImageField( upload_to= "proveedores" , default= 'proveedores/default.png', null=False)
    def __str__(self):
        return self.empresa

    class Meta:
        db_table = 'proveedor'
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['id']