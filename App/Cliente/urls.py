from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('mis_cotizaciones/', views.mis_cotizaciones, name='mis_cotizaciones'),
    path('mis_datos/', views.ver_editar_perfil, name='perfil'),
    
]

