document.addEventListener("DOMContentLoaded", function () {

    console.log("JavaScript cargado correctamente");


    // ==========================================
    // CONFIRMAR ELIMINACIÓN
    // ==========================================

    const deleteForms = document.querySelectorAll(
        ".delete-form"
    );

    deleteForms.forEach(function (form) {

        form.addEventListener("submit", function (event) {

            const confirmar = confirm(
                "¿Estás seguro de que deseas eliminar este usuario?"
            );

            if (!confirmar) {
                event.preventDefault();
            }

        });

    });


    // ==========================================
    // OCULTAR MENSAJES AUTOMÁTICAMENTE
    // ==========================================

    const messages = document.querySelectorAll(
        ".flash"
    );

    messages.forEach(function (message) {

        setTimeout(function () {

            message.style.opacity = "0";

            message.style.transition =
                "opacity 0.5s ease";

            setTimeout(function () {

                message.remove();

            }, 500);

        }, 4000);

    });


    // ==========================================
    // CONFIRMAR CIERRE DE SESIÓN
    // ==========================================

    const logoutLinks = document.querySelectorAll(
        ".logout-link"
    );

    logoutLinks.forEach(function (link) {

        link.addEventListener("click", function (event) {

            const confirmar = confirm(
                "¿Deseas cerrar tu sesión?"
            );

            if (!confirmar) {
                event.preventDefault();
            }

        });

    });

});