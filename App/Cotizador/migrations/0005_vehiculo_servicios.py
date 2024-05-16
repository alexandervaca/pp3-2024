# Generated by Django 5.0.4 on 2024-05-02 23:46
import pandas as pd
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cotizador', '0004_alter_servicio_descripcion'),
    ]
    def insert_init_data(apps, schema_editor):
        df = pd.read_csv('Cotizador/migrations/Vehículos, Servicios y categorías.csv', usecols= range(2, 10 ))
        cabecera = df.columns
        Vehiculo = apps.get_model('Cotizador', 'Vehiculo')

        # Crea los vehículos en la tabla
        for i in cabecera:
            Vehiculo.objects.create(descripcion = i)
        
        df = pd.read_csv('Cotizador/migrations/Vehículos, Servicios y categorías.csv')
        Categoria = apps.get_model('Cotizador', 'Categoria')
        Servicio = apps.get_model('Cotizador', 'Servicio')

        #Crea la relación entre Vehículos y servicios en la tabla
        for i, row in df.iterrows():
            categoriabd = Categoria.objects.get(descripcion = row['CATEGORIA'])
            serviciobd = Servicio.objects.get(idCategoria = categoriabd, descripcion = row['SERVICIO'])

            for item in cabecera:
                if row[item] == 'a':
                    vehiculobd = Vehiculo.objects.get(descripcion = item )
                    vehiculobd.servicios.add(serviciobd)


    def undo_insert_data(apps, schema_editor):
        Vehiculos = apps.get_model('Cotizador', 'Vehiculo')
        Vehiculos.objects.all().delete()

    operations = [
        migrations.AddField(
            model_name='vehiculo',
            name='servicios',
            field=models.ManyToManyField(to='Cotizador.servicio'),
        ),

    migrations.RunPython(insert_init_data, reverse_code =  undo_insert_data)
    ]