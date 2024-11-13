from django.shortcuts import render

# Create your views here.

def login(request):
    context = {}
    return render(request, 'login.html', context)

def registrarse(request):
    context = {}
    return render(request, 'registrarse.html', context)