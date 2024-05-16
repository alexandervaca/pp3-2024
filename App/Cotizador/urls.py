from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('inicio/', views.inicio, name='inicio' ),
    path('cotizacion/', views.cotizacion, name='cotizacion' ),
    path('cotizar/', views.cotizar, name='cotizar' ),
]

