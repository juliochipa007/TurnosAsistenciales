function confirmarEliminar(idUsuario) {
    Swal.fire({
        title: '¿Estás seguro?',
        text: "Esta acción no se puede deshacer.",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            // Si el usuario confirma, enviar la solicitud con HTMX
            fetch(`/eliminar-usuario/${idUsuario}`, {
                method: 'POST',
                headers: {
                    'HX-Request': 'true' // Para que Flask sepa que es una solicitud HTMX
                }
            }).then(response => response.text())
              .then(html => {
                  // Actualizar la tabla de usuarios
                  document.getElementById('tabla-usuarios').innerHTML = html;

                  // Mostrar mensaje de éxito
                  Swal.fire(
                      '¡Eliminado!',
                      'El usuario ha sido eliminado.',
                      'success'
                  );
              }).catch(error => {
                  // Mostrar mensaje de error
                  Swal.fire(
                      'Error',
                      'No se pudo eliminar el usuario.',
                      'error'
                  );
              });
        }
    });
}

function procesarRespuesta(event) {
    const xhr = event.detail.xhr;  // La respuesta del servidor
    const response = JSON.parse(xhr.responseText);  // Convertir a JSON

    if (response.status === "success") {
        // Mostrar alerta de éxito
        Swal.fire({
            title: 'Éxito',
            text: response.message,
            icon: 'success',
            confirmButtonText: 'Aceptar'
        });

        // Cerrar el modal
        var modal = bootstrap.Modal.getInstance(document.getElementById('crearUsuarioModal'));
        modal.hide();

        // Actualizar la tabla (puedes hacer un fetch manual o recargar la tabla con HTMX)
        fetch("/tabla-usuarios")
            .then(response => response.text())
            .then(html => {
                document.getElementById("tabla-usuarios").innerHTML = html;
            });

    } else {
        // Mostrar alerta de error
        Swal.fire({
            title: 'Error',
            text: response.message,
            icon: 'error',
            confirmButtonText: 'Aceptar'
        });
    }
}

// Registrar el evento personalizado
document.body.addEventListener('htmx:afterRequest:procesarRespuesta', procesarRespuesta);