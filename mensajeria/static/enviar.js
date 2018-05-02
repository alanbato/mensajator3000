$(document).ready(function () {
    $("#botonEnviar").click(function () {

        var enviador = $("#deNombre").val();
        var recibidor = $("#paraNombre").val();
        var contenido = $("#contenidoMensaje").val();

        var jsonToSend = {
            uEnviador: enviador,
            uRecibidor: recibidor,
            uContenido: contenido
        }

        $.ajax({
            url: "../enviar",
            type: "POST",
            data: JSON.stringify(jsonToSend),
            contentType: 'application/json; charset=utf-8',
            jsonToSend,
            success: function (jsonResponse) {
                if (jsonResponse.status == 'success') {
                    alert("El mensaje ha sido enviado");
                } else if (jsonResponse.status == 'error') {
                    alert("El mensaje no se ha enviado.");
                }
            }
        });
    });
});

