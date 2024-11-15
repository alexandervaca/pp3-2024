from django import forms
from .models import *

# 1. Formulario para el paso de geolocalización
class GeolocalizarForm(forms.Form):
    pass  # No se necesita ningun campo, solo un boton de Siguiente

# 2. Formulario para elegir que rastrear (cargando opciones desde la BD)
class QueRastrearForm(forms.Form):
    vehiculo = forms.ModelChoiceField(
        queryset=Vehiculo.objects.all(),  # Cargar los vehiculos desde la base de datos
        widget=forms.RadioSelect,         # Usa radio buttons para las opciones
        label="¿Qué necesitas rastrear?",
        required=True
    )

# 3. Formulario para cuantos rastreadores necesita
class CuantosForm(forms.Form):
    cantidad = forms.IntegerField(
        label="¿Cuántos rastreadores necesitas?",
        min_value=1,  # Asegura que al menos pidan 1 rastreador
        widget=forms.NumberInput(attrs={
            'class': 'contact cantidad',  # Aplica las clases CSS
            'placeholder': 'Cantidad en números',  # Placeholder del campo
            'min': '1',  # Asegura que el valor sea al menos 1
            'step': '1',  # Asegura que se acepten solo numeros enteros
        })
    )

# 4. Formulario para los servicios de interes
class ServicioInteresForm(forms.Form):
    def __init__(self, *args, **kwargs):
        vehiculo_id = kwargs.pop('vehiculo_id', None)  # Obtener el vehiculo seleccionado
        super(ServicioInteresForm, self).__init__(*args, **kwargs)

        # Asegurarse de que el vehiculo esta presente antes de intentar filtrar
        if vehiculo_id:
            # Filtrar las categorias segun el vehiculo elegido y los servicios relacionados
            categorias = Categoria.objects.filter(servicio__vehiculoservicio__Vehiculo=vehiculo_id).exclude(descripcion="Software").distinct()
            print(f"Categorías filtradas por vehículo {vehiculo_id}: {categorias}")
            # Asignar queryset de categorias basado en el vehiculo
            self.fields['categoria'].queryset = categorias
            self.fields['vehiculo_id'].initial = vehiculo_id
        else:
            # Si no hay vehiculo seleccionado, se deja el queryset vacío
            self.fields['categoria'].queryset = Categoria.objects.none()

        # Inicialmente, no se muestran servicios hasta que se seleccione una categoria
        #self.fields['servicio'].queryset = Servicio.objects.none()

        # Si hay datos de POST (cuando el formulario se envia), actualizar los servicios en funcion de la categoria elegida
        
        if 'categoria' in self.data:
            try:
                #print(f"self.data: {self.data}")
                categoria_id = int(self.data.get('categoria'))
                print(f"Categoría seleccionada: {categoria_id}")
                 # Filtrar los servicios para la categoria seleccionada y el vehiculo
                servicios = Servicio.objects.filter(
                    idCategoria=categoria_id, 
                    vehiculoservicio__Vehiculo=vehiculo_id
                ).exclude(idCategoria__descripcion="Software")

                #print(f"Servicios disponibles para la categoría {categoria_id}:")
                #for servicio in servicios:
                #    print(f"- {servicio.descripcion} (ID: {servicio.id})")

                self.fields['servicio'].queryset = servicios

            except (ValueError, TypeError):
                # Si la categoria seleccionada es invalida, no mostrar servicios
                print(f"Error al seleccionar categoría: ")
                self.fields['servicio'].queryset = Servicio.objects.none()

    # Campo para seleccionar una categoria
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.none(),  # Se llenara dinamicamente
        label="Seleccione una categoría",
        widget=forms.RadioSelect,
        required=False
    )

    # Campo para seleccionar uno o mas servicios CheckboxSelectMultiple
    servicio = forms.ModelMultipleChoiceField(
        queryset=Servicio.objects.none(),  # Se llenara dinamicamente
        widget=forms.CheckboxSelectMultiple,
        label="¿Qué servicio te interesa cotizar?",
        required=False
    )

    # Campo oculto para el vehiculo
    categoria_id = forms.IntegerField(
        widget=forms.HiddenInput(attrs={'id': 'categoria_hidden', 'name': 'categoria_id'}),  # Campo oculto
        required=False  # No requerido para que no falle la validación
    )

    # Campo oculto para el vehiculo
    vehiculo_id = forms.IntegerField(
        widget=forms.HiddenInput(attrs={'id': 'vehiculo_hidden', 'name': 'vehiculo_id'}),  # Campo oculto
        required=False  # No requerido para que no falle la validación
    )

#vehiculo_seleccionado = Vehiculo.objects.get(id=<id_del_vehiculo>)
    #servicios = Servicio.objects.filter(vehiculoservicio__Vehiculo=vehiculo_seleccionado, idCategoria__descripcion="Software")
    #categorias = Categoria.objects.filter(servicio__in=servicios, descripcion="Software").distinct()

#5. Formulario para el software que necesitan
class SoftwareForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        vehiculo_id = kwargs.pop('vehiculo_id', None)
        categoria_id = kwargs.pop('categoria_id', None)
        servicio = kwargs.pop('servicio', None)

        super(SoftwareForm, self).__init__(*args, **kwargs)

        print(f'PASO SOFTWARE {vehiculo_id}')
        print(f'PASO SOFTWARE {categoria_id}')
        print(f'PASO SOFTWARE {servicio}')

        if vehiculo_id:
            # Obtener los servicios asociados al vehiculo
            servicios = Servicio.objects.filter(
                vehiculo__id=vehiculo_id
            ).distinct()
            
            # Filtrar servicios que están en la categoria 'Software'
            servicios_software = servicios.filter(idCategoria__descripcion='Software' )

            # Crear un queryset con los servicios que pertenecen a la categoria 'Software'
            # Añadir la opcion "Ninguno" al inicio de la lista de opciones
            self.fields['software'].choices = [(0, 'Ninguno')] + [(s.id, s.descripcion) for s in servicios_software]

        else:
            servicios_software = Servicio.objects.filter(idCategoria__descripcion='Software')

        #print(f"servicios_software: { servicios_software }")
        self.fields['software'].choices = [(0, 'Ninguno')] + [(s.id, s.descripcion) for s in servicios_software]


    def clean_software(self):
        data = self.cleaned_data.get('software', [])
    
        # Si "Ninguno" está seleccionado, limpiar el campo
        if 0 in data:
            return []  # Retornar una lista vacia para indicar que no se selecciono ningún software

        # Verificar si al menos un software ha sido seleccionado
        if not data:
            raise forms.ValidationError("Debes seleccionar al menos un software de gestión.")  # Mensaje de error si no se selecciona nada
    
        return data

    software = forms.MultipleChoiceField(
        #queryset=Servicio.objects.none(),  # Se actualizara dinamicamente
        choices=[],  # Se llenara dinámicamente
        widget=forms.CheckboxSelectMultiple,
        label="¿Necesitas algún software de gestión?"
    )

# 6. Formulario para los datos de contacto
'''
class DatosContactoForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['tipo','nombre', 'email', 'telefono' ]
        widgets = {
            'tipo': forms.Select(attrs={
                'class': 'contact tipo',  # Clase CSS para el campo 'tipo'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        cliente_id = kwargs.pop('cliente_id', None)
        super(DatosContactoForm, self).__init__(*args, **kwargs)

        # Asignar clases y placeholders a los otros campos del formulario
        self.fields['nombre'].widget.attrs.update({
            'class': 'contact',
            'placeholder': 'Nombre',
        })
        self.fields['email'].widget.attrs.update({
            'class': 'contact',
            'placeholder': 'E-mail',
        })
        self.fields['telefono'].widget.attrs.update({
            'class': 'contact',
            'placeholder': 'Celular',
        })

        if cliente_id:
            try:
                cliente = Cliente.objects.get(pk=cliente_id)
                self.initial = {
                    'tipo': cliente.tipo,
                    'nombre': cliente.nombre,
                    'email': cliente.email,
                    'telefono': cliente.telefono
                }
            except Cliente.DoesNotExist:
                pass  # Si el cliente no existe, no inicializa nada.   
'''    
    
    
