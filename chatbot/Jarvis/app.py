from flask import Flask, render_template, request, jsonify
import os, pyautogui, re, time, tempfile, pygame
from gtts import gTTS
from shared import client, conversation_history, save_conversation_to_json
from nouvelle_page import nouvelle_page  # Correct the import to match the function name
app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/nouvelle-page')
def nouvelle_page_route():
    return nouvelle_page()
# Réponse principale
def get_chat_response(user_input):
    global conversation_history

    if user_input.lower() == "créer un fichier test":
        os.system("echo Bonjour > fichier_test.txt")
        return "✅ Fichier test créé, Monsieur."

    if user_input.lower() == "faire une capture d'écran":
        screenshot = pyautogui.screenshot()
        save_path = r"Documents\Python\Jarvis\capture.png"
        screenshot.save(save_path)
        return f"✅ Capture d'écran enregistrée ici : '{save_path}', Monsieur."

    match = re.search(r"(créer|faire|générer)\s+.*fichier\s+(nommé|appelé)?\s*(\w+\.\w+)?\s*(dans\s+(\w+))?\s*(avec\s+le\s+contenu\s*'([^']+)')?", user_input.lower())
    if match:
        filename = match.group(3) or "fichier.txt"
        directory = match.group(5) or ""
        content = match.group(7) or "Bonjour"
        file_path = os.path.join(directory, filename) if directory else filename

        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        with open(file_path, "w") as f:
            f.write(content)

        return f"✅ Fichier '{file_path}' créé avec le contenu : '{content}', Monsieur."

    messages = [
        {
            "role": "system",
            "content": "Tu es J.A.R.V.I.S., l'assistant de Tony Stark. Tu parles en français, tu es courtois, utile, concis et tu appelles ton interlocuteur 'Monsieur'."
        }
    ]

    for entry in conversation_history:
        messages.append({"role": entry["role"], "content": entry["content"]})

    messages.append({"role": "user", "content": user_input})

    try:
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
        )

        assistant_response = chat_completion.choices[0].message.content

        conversation_history.append({"role": "user", "content": user_input})
        conversation_history.append({"role": "assistant", "content": assistant_response})

        save_conversation_to_json()

        if len(conversation_history) > 20:
            conversation_history = conversation_history[-20:]

        tts = gTTS(text=assistant_response, lang='fr')
        with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as temp_audio:
            tts.save(temp_audio.name)
            pygame.mixer.init()
            pygame.mixer.music.load(temp_audio.name)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.2)

        return assistant_response

    except Exception as e:
        print(f"Erreur : {e}")
        return "⚠️ Erreur système : Dysfonctionnement temporaire. Veuillez réessayer, Monsieur."


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.form["user_input"]
    response = get_chat_response(user_input)
    return jsonify({"response": response})

@app.route("/clear-history", methods=["POST"])
def clear_history():
    global conversation_history
    conversation_history = []
    save_conversation_to_json()
    return jsonify({"status": "success"})



@app.route("/entretien")

def entretien():
    print("Requête reçue")
    data = request.get_json()
    print("Données reçues :", data)
    user_input = data.get("user_input", "") if data else ""
    print("User input:", user_input)
    return render_template("entretien.html")

# Import du module entretien (placé ici pour éviter les imports circulaires)
from entretien import entretien_ask
app.add_url_rule("/entretien-ask", view_func=entretien_ask, methods=["POST"])

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
