# views.py
from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse
from .forms import ContactForm

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Extraer los datos
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            message = form.cleaned_data['message']

            # Enviar el correo
            send_mail(
                f'Mensaje de {name}',  # Asunto
                f'Mensaje: {message}\n\nEmail: {email}\nTeléfono: {phone}',  # Cuerpo
                email,  # De
                ['cotizadortum@gmail.com'],  # A
                fail_silently=False,
            )
            return HttpResponse('Gracias por tu mensaje. ¡Nos pondremos en contacto pronto!')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})
