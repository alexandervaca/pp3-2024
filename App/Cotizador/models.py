from django.db import models

# Create your models here.
class Vehiculo(models.Model):
    descripcion =  models.CharField(max_length= 30)

class Categoria(models.Model):
    descripcion =  models.CharField(max_length= 30)