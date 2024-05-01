from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('inicio/', views.inicio, name='inicio' ),
    path('fin/', views.fin, name='fin' ),
    path('cotizar/', views.cotizar, name='cotizar' ),
]

