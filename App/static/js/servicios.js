document.addEventListener('DOMContentLoaded', function() {
    console.log("JavaScript cargado y ejecutándose");
    // Escuchar los cambios en la selección de categoría
    const categoriaRadios = document.querySelectorAll('input[name="{{ form.categoria.name }}"]');
    
    categoriaRadios.forEach(function(radio) {
        radio.addEventListener('change', function() {
            const categoriaId = this.value;

            // Enviar una solicitud AJAX para obtener los servicios de la categoría seleccionada
            fetch(`{% url 'get_servicios_por_categoria' %}?categoria_id=${categoriaId}&vehiculo_id=${vehiculoId}`)
                .then(response => response.json())
                .then(data => {
                    const serviciosDiv = document.getElementById('servicios');
                    serviciosDiv.innerHTML = '';  // Limpiar la lista actual

                    // Crear la lista de servicios con checkboxes
                    data.servicios.forEach(function(servicio) {
                        const checkbox = document.createElement('input');
                        checkbox.type = 'checkbox';
                        checkbox.id = 'servicio_' + servicio.id;
                        checkbox.name = 'servicio';
                        checkbox.value = servicio.id;
                        checkbox.className = 'form-check-input';

                        const label = document.createElement('label');
                        label.htmlFor = 'servicio_' + servicio.id;
                        label.className = 'form-check-label';
                        label.innerText = servicio.descripcion;

                        const div = document.createElement('div');
                        div.className = 'form-check';
                        div.appendChild(checkbox);
                        div.appendChild(label);

                        serviciosDiv.appendChild(div);
                    });
                })
                .catch(error => console.error('Error al cargar los servicios:', error));
        });
    });
});