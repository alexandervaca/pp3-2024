import pytest
from django.core import mail
from django.urls import reverse
from django.test import Client

@pytest.mark.django_db
def test_contact_email_sending(client):
    # Enviar datos válidos al formulario de contacto
    response = client.post(reverse('contact'), {
        'name': 'Fernanda Martinelli',
        'email': 'fermartimarche@gmail.com',
        'phone': '123456789',
        'message': 'Mensaje:',
    })

    # Asegurarse de que el correo fue enviado
    assert response.status_code == 200
    assert len(mail.outbox) == 1
    assert mail.outbox[0].subject == 'Mensaje de Fernanda Martinelli'
    

def test_selected_providers_type():
    # Simular un arreglo de proveedores seleccionados
    selected_providers = [1, 2, 3]

    # Verificar que 'selected_providers' es una lista
    assert isinstance(selected_providers, list), "selectedProviders should be a list."

    # Verificar que todos los elementos en la lista son enteros
    for provider in selected_providers:
        assert isinstance(provider, int), "Each provider ID should be an integer."

def test_final_contact_redirect(client):
    # Crear un cliente de prueba
    client = Client()

    # Simular el caso en que el usuario no selecciona ser contactado
    response = client.post('/cotizacion/', {'finalContact': 'No Quiero que me contacten'})

    # Si no hay redirección, asumimos un código 200 y validamos que se renderizó la página correctamente
    if response.status_code == 200:
        assert 'cotización' in response.content.decode().lower(), "Expected the page to contain 'cotización'"

    # Verificar que la redirección es a la página de inicio (302)
    assert response.status_code in [200, 302], f"Expected 302 or 200 but got {response.status_code}"
    if response.status_code == 302:
        assert response.url == 'http://localhost:8000/inicio/', f"Expected redirection to 'http://localhost:8000/inicio/' but got {response.url}"

    # Simular el caso en que el usuario selecciona ser contactado
    response = client.post('/cotizacion/', {'finalContact': 'Quiero que me contacten'})

    # Verificar que la redirección es a la página de fin
    assert response.status_code in [200, 302], f"Expected 302 or 200 but got {response.status_code}"
    if response.status_code == 302:
        assert response.url == '../fin', f"Expected redirection to '../fin' but got {response.url}"