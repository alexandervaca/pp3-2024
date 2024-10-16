from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import CotizacionWizard
from .views import get_servicios_por_categoria


urlpatterns = [
    path('inicio/', views.inicio, name='inicio' ),
    path('cotizacion/', views.cotizacion, name='cotizacion' ), #donde va luego de cargar le form
    #path('cotizar/', views.cotizar, name='cotizar' ),
    #path('cotizar/', CotizacionWizard.as_view(), name='cotizacion_wizard'),
    path('cotizar/', CotizacionWizard.as_view(), name='cotizar' ),
    path('cotizar/get-servicios/', get_servicios_por_categoria, name='get_servicios_por_categoria'),
    path('fin/', views.fin, name='fin' )
]