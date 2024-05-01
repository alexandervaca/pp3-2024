from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages 
from django.contrib.auth import  authenticate, login, logout


from django.http import HttpResponse
# Create your views here.
def inicio(request):
    #return render(request, 'hola')
    context ={}
    return render(request, '0-inicio.html', context)  
    

def bienvenida(request):
    context = {}
    return render(request, '1-bienvenida.html', context)

def que(request):
    # Esta lista habría que obtenerla de la BD
    rastrear = ["AUTO/SUV", "MOTO", "UTILITARIO", "CAMION", "CONTAINER", "TRAILER", "PRECINTO ELECTRÓNICO", "MERCADERIA"]
    context ={"rastrear": rastrear}
    return render(request, '2-que.html', context)     

def resumen(request):
    context = {}
    return render(request, '6-resumen.html', context)