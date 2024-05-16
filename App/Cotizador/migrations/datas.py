import pandas as pd
from django.db import migrations, models
#from Cotizador.models import Vehiculo

#Borramos los vehículos
#vehiculos = Vehiculo.get_model('Cotizador', 'Vehiculo')
#vehiculos.objects.all().delete()
print ('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')    
#df = pd.read_csv('Vehículos, Servicios y categorías.csv', usecols= range(2, 10 ))
#print(df['CATEGORIA'])
#print(df['SERVICIO'])



#df = pd.read_csv('Vehículos, Servicios y categorías.csv')
#print (df)

df = pd.read_csv('Vehículos, Servicios y categorías.csv', usecols= range(2, 10 ))
cabecera = df.columns


df = pd.read_csv('Vehículos, Servicios y categorías.csv')



for i, row in df.iterrows():
    print ('************************************************************')
    print (row)
    for item in cabecera:
        print (row[item] )
        if row[item] == 'a':
            print ('es igual a "a"')

   
    print ('------------------------------------------')
    print(row['CATEGORIA'])

    print(row['SERVICIO'])
    print (i)
    #print(row[vehiculos[0]])
   

#print (df.objects.first_valid_index)


#Categoria = models.get_model('Cotizador', 'Categoria')


#df['CATEGORIA'].unique()

#categorias = []
#for i in df['CATEGORIA'].unique():
#    categorias.append(i)

#print(categorias)


'''

#Código borrado
def insert_init_data(apps, schema_editor):
        df = pd.read_csv('Cotizador/migrations/Servicios y categorías.csv')
        
        #list_categorias = df['CATEGORIA'].unique()
        
        Categoria = apps.get_model('Cotizador', 'Categoria')
        Servicio = apps.get_model('Cotizador', 'Servicio')
        
        for categoria in Categoria.objects.values_list("id", "descripcion"):
            
            df.loc[df['CATEGORIA']==categoria[1],'idCategoria'] = categoria[0]

        list_servicios_register_objs = []
        print('0-------------------------------------------------------------------------------------------------------------------')
        for i, row in df.iterrows():
            print('categoria:')
            print(row['idCategoria'])
            print('descripción:')
            print(row['SERVICIO'])
            Servicio.objects.create(idCategoria  = row['idCategoria'], descripcion = row['SERVICIO'])
            
            print('1-------------------------------------------------------------------------------------------------------------------')
            pd.read_csv('Cotizador/migrrvicios y categorías.csv')
            #No funciona
            
            list_servicios_register_objs.append(
                Servicio(
                    idCategoria = row['idCategoria'],
                    descripcion = row['SERVICIO']
                )
            )
           
        #print(list_servicios_register_objs)
        Servicio.objects.bulk_create (list_servicios_register_objs)
#python datas.py
'''




'''
    def insert_init_data(apps, schema_editor):
        df = pd.read_csv('Cotizador/migrations/Servicios y categorías.csv')
        
        #list_categorias = df['CATEGORIA'].unique()
        
        Categoria = apps.get_model('Cotizador', 'Categoria')
        Servicio = apps.get_model('Cotizador', 'Servicio')
#-----------------------------------------------------------------------------------------------------------------------------------------------        
        list_servicios_register_objs = []
        for i, row in df.iterrows():

            categoriabd = Categoria.objects.get(descripcion = row['CATEGORIA'])
            print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            Servicio.objects.create(idCategoria = categoriabd, descripcion = row['SERVICIO'] )
            print('-----------------------------------------------------------------------------------------------------------------------------')
'''


'''
def insert_init_data(apps, schema_editor):
        df = pd.read_csv('Cotizador/migrations/Servicios y categorías.csv')
        
        #list_categorias = df['CATEGORIA'].unique()
        
        Categoria = apps.get_model('Cotizador', 'Categoria')
        Servicio = apps.get_model('Cotizador', 'Servicio')
        

        list_servicios_register_objs = []
        print('0-------------------------------------------------------------------------------------------------------------------')
        for i, row in df.iterrows():

            categoriabd = Categoria.objects.get(descripcion = row['CATEGORIA'])

            #No funciona
            
            list_servicios_register_objs.append(
                Servicio(
                    idCategoria = categoriabd,
                    descripcion = row['SERVICIO']
                )
            )
        print('1-------------------------------------------------------------------------------------------------------------------')      
        print(list_servicios_register_objs)
        print('2-------------------------------------------------------------------------------------------------------------------')  
        Servicio.objects.bulk_create (list_servicios_register_objs)
        print('3-------------------------------------------------------------------------------------------------------------------')  
def undo_insert_data(apps, schema_editor):
    Servicio = apps.get_model('Cotizador', 'Servicio')
    Servicio.objects.all().delete()

'''