import pytest
from django.urls import reverse
from django.core import mail

@pytest.mark.django_db
def test_contact_form(client):
    """
    Test to validate that the contact form sends an email correctly.
    """

    # Datos del formulario
    data = {
        'name': 'Juan Pérez',
        'email': 'fermartimarche@gmail.com',
        'phone': '1234567890',
        'message': 'Hola, este es un mensaje de prueba.'
    }

    # Enviar el formulario
    response = client.post(reverse('contact'), data)

    # Validar que la respuesta sea exitosa
    assert response.status_code == 200

    # Validar que se ha enviado un email
    assert len(mail.outbox) == 1

    # Validar el contenido del correo
    sent_mail = mail.outbox[0]
    assert sent_mail.subject == 'Nuevo mensaje de contacto'
    assert 'Juan Pérez' in sent_mail.body
    assert 'Hola, este es un mensaje de prueba.' in sent_mail.body
    assert sent_mail.to == ['fermartimarche@gmail.com'] 
    assert sent_mail.from_email == 'cotizadortum@gmail.com'

    # Validar que la página muestra un mensaje de éxito
    assert 'Tu mensaje ha sido enviado con éxito' in response.content
