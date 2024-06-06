const video = document.getElementById('video');
const input = document.getElementById('input');
const responses = document.getElementById('responses');

navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(err => {
        console.error('Error accessing media devices.', err);
    });

const ws = new WebSocket(`ws://${window.location.host}/ws`);

ws.onmessage = function(event) {
    const response = document.createElement('div');
    response.textContent = `Médico AI: ${event.data}`;
    responses.appendChild(response);
};

function sendMessage() {
    const message = input.value;
    ws.send(message);
    const userMessage = document.createElement('div');
    userMessage.textContent = `Usuario: ${message}`;
    responses.appendChild(userMessage);
    input.value = '';
}


//otra opción
/*
$.ajax({
    type: "POST",
    url: "http://localhost:11434/api/generate", // Cambia el puerto si es diferente
    data: JSON.stringify(cuerpo),
    contentType: "application/json",
    xhrFields: {
        onprogress: function (e) {
            var response = e.currentTarget.response;
            var lines = response.split('\n');
            var respuestaAcumulada = ""; // Variable para acumular la respuesta
            lines.forEach(function (line) {
                if (line.trim() !== '') {
                    try {
                        var responseObject = JSON.parse(line);
                        if (responseObject && responseObject.response) {
                            respuestaAcumulada += responseObject.response + " "; // Acumular la respuesta
                            $("#textaRespuesta").val(respuestaAcumulada); // Mostrar la respuesta acumulada en el textarea mientras se recibe
                        }
                    } catch (e) {
                        console.error("Error parsing line: ", line);
                    }
                }
            });
        }
    }
});
*/
