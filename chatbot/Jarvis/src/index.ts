const inputField = document.getElementById("user_input") as HTMLInputElement;
const responseBox = document.getElementById("response_box") as HTMLElement | null;

function appendResponse(content: string) {
  if (responseBox) responseBox.innerText = content;
}

export function sendToJarvis(): void {
  const userInput = inputField.value.trim();
  if (!userInput) return;

  fetch("/ask", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: `user_input=${encodeURIComponent(userInput)}`
  })
    .then((res) => res.json())
    .then((data) => appendResponse(data.response))
    .catch((err) => appendResponse("Erreur : " + err));
}
