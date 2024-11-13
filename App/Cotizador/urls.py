from django.urls import path
from . import views # Importa el módulo de vistas
from django.contrib.auth import views as auth_views
from .views import CotizacionWizard
from .views import get_servicios_por_categoria
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('inicio/', views.inicio, name='inicio' ),
    path('cotizacion/', views.cotizacion, name='cotizacion' ), #donde va luego de cargar le form
    #path('cotizar/', views.cotizar, name='cotizar' ),
    #path('cotizar/', CotizacionWizard.as_view(), name='cotizacion_wizard'),
    path('cotizar/', CotizacionWizard.as_view(), name='cotizar' ),
    path('cotizar/get-servicios/', get_servicios_por_categoria, name='get_servicios_por_categoria'),
    path('fin/', views.fin, name='fin' )
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
