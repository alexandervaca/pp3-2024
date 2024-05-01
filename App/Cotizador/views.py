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

def cotizar(request):
    #return render(request, 'hola')
    context ={}
    return render(request, 'cotizador.html', context)

def fin(request):
    context = {}
    return render(request, '6-resumen.html', context)