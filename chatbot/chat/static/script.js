document.addEventListener("DOMContentLoaded", function () {
    const sendBtn = document.getElementById("sendBtn");
  
    sendBtn.addEventListener("click", async function () {
      const userInput = document.getElementById("userInput").value;
      console.log("Message à envoyer :", userInput);
  
      const response = await fetch("/send", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: userInput }),
      });
  
      const data = await response.json();
      console.log("Réponse reçue :", data);
  
      document.getElementById("responseText").innerText = data.response;
  
      if (data.audio) {
        const audioPlayer = document.getElementById("audioPlayer");
        audioPlayer.src = data.audio;
        audioPlayer.load();
      }
    });
  });
  