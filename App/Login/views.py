from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages 
from django.contrib.auth import  authenticate, login, logout

#Formularios 
# Creación de usuario

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password1', 'password2']

# Create your views here.

#-------------------------------------------------------------------------------------#
def registrarse(request):
    #Chequeadmos si ya esta autenticado
    if request.user.is_authenticated:
        return redirect('inicio')

    form = CreateUserForm()

    # Si el user ya completó el formulario
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid(): #Si el form es válido
            form.save() #Creame el usuario
            #Para que le indique al usuario que su cuenta fue creada
            usuario = form.cleaned_data.get('username')
            messages.success(request, 'Usuario %s fue creado' % (usuario))
            return redirect ('login')

    context = {'form': form}
    return render(request, 'registrarse.html', context)    
#-------------------------------------------------------------------------------------#

#-------------------------------------------------------------------------------------#
def loginPage(request):
    #Chequeadmos si ya esta autenticado
    if request.user.is_authenticated:
        return redirect('inicio')

    if request.method == 'POST':
        username = request.POST.get ('username')
        password = request.POST.get ('password')

        user = authenticate(request, username = username, password = password)

        if user is not None: 
            login(request, user)
            return redirect('inicio')
        else:
            messages.info(request, 'Usuario o password erróneos')
    context ={}
    return render(request, 'login.html', context)
#-------------------------------------------------------------------------------------#
def logoutUser(request):
    logout(request)
    return redirect('login')
#-------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------#
# Reseteo de password
def ps_complete(request):
    return render(request, 'pass_reset/5-complete.html')
def ps_confirm(request):
    return render(request, 'pass_reset/4-confirm.html')
def ps_done(request):
    return render(request, 'pass_reset/2-done.html')
def ps_email(request):
    return render(request, 'pass_reset/3-email.html')
def ps_form(request):
    return render(request, 'pass_reset/1-form.html')
