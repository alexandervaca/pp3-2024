document.addEventListener('DOMContentLoaded', function() {
    console.log("carga JS para categoriaRadios");
    // Escuchar los cambios en la selección de categoría - {{ form.categoria.name }}
    const categoriaRadios = document.querySelectorAll('input[name="categoria"]');
    //console.log('categoriaRadios: ' + categoriaRadios.values.length);

    categoriaRadios.forEach(function(radio) {
        console.log('radio: ' + radio.name + ' value: ' + radio.value);

        //radio.addEventListener('change', function() {
        radio.onclick = function() {
            const categoriaId = this.value;
            const vehiculoId = document.getElementById('vehiculo_hidden').value;
            console.log('radio event change categoriaId: ' + categoriaId + ' vehiculoId: ' + vehiculoId);
            // Enviar una solicitud AJAX para obtener los servicios de la categoría seleccionada ${vehiculoId}
            //fetch(`{% url 'get_servicios_por_categoria' %}?categoria_id=${categoriaId}&vehiculo_id=1`)
            if (categoriaId && vehiculoId) {
                document.getElementById('categoria_hidden').value = categoriaId;

                fetch('get-servicios/?categoria_id='+categoriaId+'&vehiculo_id='+vehiculoId)
                    .then(response => response.json())
                    .then(data => {
                        const serviciosDiv = document.getElementById('id_3-servicio');
                        serviciosDiv.innerHTML = '';  // Limpiar la lista actual
                        serviciosDiv.classList.add('active');
                        //console.log('serviciosDiv: ' + serviciosDiv.value);
                        
                        var idx = 0;
                        // Crear la lista de servicios con checkboxes
                        data.servicios.forEach(function(servicio) {
                            const checkbox = document.createElement('input');
                            checkbox.type = 'checkbox';
                            checkbox.id = 'id_3-servicio_' + idx;
                            checkbox.name = '3-servicio';
                            checkbox.value = servicio.id;
                            checkbox.className = 'form-check-input';
    
                            const label = document.createElement('label');
                            label.htmlFor = 'id_3-servicio_' + idx;
                            label.className = 'form-check-label';
                            label.innerText = servicio.descripcion;
                            
                            const div = document.createElement('div');
                            div.className = 'form-check';
                            div.appendChild(checkbox);
                            div.appendChild(label);
    
                            serviciosDiv.appendChild(div);

                            idx++;
                        });
                    })
                    .catch(error => console.error('Error al cargar los servicios:', error));
            }

        };
    });
});