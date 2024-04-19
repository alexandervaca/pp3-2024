from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('inicio/', views.inicio, name='inicio' ),
    path('bienvenida/', views.bienvenida, name='bienvenida' ),
    path('que/', views.que, name='que' ),
    path('resumen/', views.resumen, name='resumen' ),
]
