let recognizing = false;
let recognition;

function startListening() {
    if (!('webkitSpeechRecognition' in window)) {
        alert("Votre navigateur ne supporte pas la reconnaissance vocale.");
        return;
    }

    if (!recognition) {
        recognition = new webkitSpeechRecognition();
        recognition.lang = "fr-FR";
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            input.value = transcript;
            sendMessage();
        };

        recognition.onerror = function(event) {
            console.error("Erreur de reconnaissance vocale : ", event.error);
        };

        recognition.onend = function() {
            recognizing = false;
            document.getElementById("micButton").innerText = "🎙️ Parler";
        };
    }

    if (!recognizing) {
        recognition.start();
        recognizing = true;
        document.getElementById("micButton").innerText = "⏹️ Écoute...";
    } else {
        recognition.stop();
        recognizing = false;
        document.getElementById("micButton").innerText = "🎙️ Parler";
    }
}
