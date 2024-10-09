from django import forms
from .models import *


# 1. Formulario para el paso de geolocalización
class GeolocalizarForm(forms.Form):
    pass  # No se necesita ningún campo, solo un botón de Siguiente

# 2. Formulario para elegir qué rastrear (cargando opciones desde la BD)
class QueRastrearForm(forms.Form):
    vehiculo = forms.ModelChoiceField(
        queryset=Vehiculo.objects.all(),  # Cargar los vehículos desde la base de datos
        widget=forms.RadioSelect,         # Usa radio buttons para las opciones
        label="¿Qué necesitas rastrear?",
        required=True
    )

# 3. Formulario para cuántos rastreadores necesita
class CuantosForm(forms.Form):
    cantidad = forms.IntegerField(
        label="¿Cuántos rastreadores necesitas?",
        min_value=1,  # Asegura que al menos pidan 1 rastreador
        widget=forms.NumberInput(attrs={
            'class': 'contact cantidad',  # Aplica las clases CSS
            'placeholder': 'Cantidad en números',  # Placeholder del campo
            'min': '1',  # Asegura que el valor sea al menos 1
            'step': '1',  # Asegura que se acepten solo números enteros
        })
    )

# 4. Formulario para los servicios de interés
class ServicioInteresForm(forms.Form):
    def __init__(self, *args, **kwargs):
        vehiculo_id = kwargs.pop('vehiculo_id', None)  # Obtener el vehículo seleccionado
        super(ServicioInteresForm, self).__init__(*args, **kwargs)

        # Asegurarse de que el vehículo está presente antes de intentar filtrar
        if vehiculo_id:
            # Filtrar las categorías según el vehículo elegido y los servicios relacionados
            categorias = Categoria.objects.filter(servicio__vehiculoservicio__Vehiculo=vehiculo_id).exclude(descripcion="Software").distinct()
            print(f"Categorías filtradas por vehículo {vehiculo_id}: {categorias}")
            # Asignar queryset de categorías basado en el vehículo
            self.fields['categoria'].queryset = categorias
            self.fields['vehiculo_id'].initial = vehiculo_id
        else:
            # Si no hay vehículo seleccionado, se deja el queryset vacío
            self.fields['categoria'].queryset = Categoria.objects.none()

        # Inicialmente, no se muestran servicios hasta que se seleccione una categoría
        self.fields['servicio'].queryset = Servicio.objects.none()

        # Si hay datos de POST (cuando el formulario se envía), actualizar los servicios en función de la categoría elegida
        
        if 'categoria' in self.data:
            try:
                categoria_id = int(self.data.get('categoria'))
                print(f"Categoría seleccionada: {categoria_id}")
                 # Filtrar los servicios para la categoría seleccionada y el vehículo
                servicios = Servicio.objects.filter(
                    idCategoria=categoria_id, 
                    vehiculoservicio__Vehiculo=vehiculo_id
                ).exclude(idCategoria__descripcion="Software")

                print(f"Servicios disponibles para la categoría {categoria_id}:")
                for servicio in servicios:
                    print(f"- {servicio.descripcion} (ID: {servicio.id})")

                self.fields['servicio'].queryset = servicios

            except (ValueError, TypeError):
                # Si la categoría seleccionada es inválida, no mostrar servicios
                print(f"Error al seleccionar categoría: ")
                self.fields['servicio'].queryset = Servicio.objects.none()

    # Campo para seleccionar una categoría
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.none(),  # Se llenará dinámicamente
        label="Seleccione una categoría",
        widget=forms.RadioSelect,
        required=False
    )

    # Campo para seleccionar uno o más servicios
    servicio = forms.ModelMultipleChoiceField(
        queryset=Servicio.objects.none(),  # Se llenará dinámicamente
        widget=forms.CheckboxSelectMultiple,
        label="¿Qué servicio te interesa cotizar?",
        required=False
    )

    # Campo oculto para el vehículo
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
        super(SoftwareForm, self).__init__(*args, **kwargs)

        if vehiculo_id:
            # Obtener los servicios asociados al vehículo
            servicios = Servicio.objects.filter(
                vehiculo__id=vehiculo_id
            ).distinct()
            
            # Filtrar servicios que están en la categoría 'Software'
            servicios_software = servicios.filter(
                idCategoria__descripcion='Software' )

            # Crear un queryset con los servicios que pertenecen a la categoría 'Software'
            # Añadir la opción "Ninguno" al inicio de la lista de opciones
            self.fields['software'].choices = [(0, 'Ninguno')] + [(s.id, s.descripcion) for s in servicios_software]

    def clean_software(self):
        data = self.cleaned_data['software']
        
        # Si el valor "Ninguno" (0) está seleccionado, limpiar el campo
        if data == 0:
            return []  # Retornar una lista vacía para indicar que no se seleccionó ningún servicio
        
        return data

    software = forms.ChoiceField(
        #queryset=Servicio.objects.none(),  # Se actualizará dinámicamente
        choices=[],  # Se llenará dinámicamente
        widget=forms.RadioSelect,
        label="¿Necesitas algún software de gestión?"
    )

# 6. Formulario para los datos de contacto
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
    
    
    
