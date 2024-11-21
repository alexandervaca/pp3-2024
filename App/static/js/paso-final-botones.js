// Array para almacenar los proveedores seleccionados
let selectedProviders = [];

// Seleccionar proveedores al hacer clic en los botones
document.querySelectorAll('.btn-contacto').forEach(function (btn) {
    btn.addEventListener('click', function () {
        const providerId = this.getAttribute('data-id');
        if (!selectedProviders.includes(providerId)) {
            selectedProviders.push(providerId);
            this.classList.add('selected');
        } else {
            selectedProviders = selectedProviders.filter(id => id !== providerId);
            this.classList.remove('selected');
        }
        updateContactButton();
    });
});

// Actualizar el botón final dinámicamente
function updateContactButton() {
    const contactButton = document.getElementById('finalContact');
    if (selectedProviders.length > 0) {
        contactButton.textContent = 'Quiero que me contacten';
        contactButton.classList.remove('no-contact');
        contactButton.classList.add('contact');
    } else {
        contactButton.textContent = 'No Quiero que me contacten';
        contactButton.classList.remove('contact');
        contactButton.classList.add('no-contact');
    }
}

// Acción al hacer clic en el botón final
document.getElementById('finalContact').addEventListener('click', function () {
    const contactButton = document.getElementById('finalContact');
    // Confirmar la selección del usuario
    if (confirm('Confirme su elección o presione CANCELAR para regresar al menú')) {
        if (contactButton.textContent === 'No Quiero que me contacten') {
            // Si el texto es "No Quiero que me contacten", redirige al inicio
            window.location.href = 'http://localhost:8000/inicio/';
        } else {
            // Envia los proveedores seleccionados y el cliente
            // invocar AJAX para enviar datos y emails a proveedores
            enviarMailAProveedores();
            // Si el texto es "Quiero que me contacten", redirige a la página final
            window.location.href = '../fin';
        }
    } else {
        // Si elige "Cancelar", lo lleva al inicio de la cotización
        //window.location.href = '../cotizacion';
    }
});

function enviarMailAProveedores() {
    fetch('proveedores/enviar-mail?proveedores='+selectedProviders)
    .then(response => response.json())
    .then(data => {
        console.log('data: '+data);
    })
    .catch(error => console.error('Error al enviar mails a proveedores:', error));
}