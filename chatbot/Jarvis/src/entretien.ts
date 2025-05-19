const chatbox = document.getElementById("chatbox") as HTMLDivElement;
const input = document.getElementById("user_input") as HTMLInputElement;

function appendMessage(content: string, sender: "user" | "bot") {
  const message = document.createElement("div");
  message.className = `message ${sender}`;
  message.innerText = content;
  chatbox.appendChild(message);
  chatbox.scrollTop = chatbox.scrollHeight;
}

export function sendMessage(): void {
  const userInput = input.value.trim();
  if (!userInput) return;

  appendMessage(userInput, "user");
  input.value = "";

  fetch("/entretien-ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_input: userInput }),
  })
    .then((res) => res.json())
    .then((data) => {
      appendMessage(data.response, "bot");
    })
    .catch((err) => {
      console.error("Erreur d'envoi :", err);
      appendMessage("❌ Erreur de communication avec le serveur.", "bot");
    });
}

document.addEventListener("DOMContentLoaded", () => {
  // Démarrage de la session d'entretien
  fetch("/entretien-ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_input: "" }),
  })
    .then((res) => res.json())
    .then((data) => appendMessage(data.response, "bot"))
    .catch((err) => {
      console.error("Erreur d'initialisation :", err);
    });
});
