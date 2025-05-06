from flask import Flask, render_template, request, jsonify
from groq import Groq
import os
import pyautogui
import re
import time
from gtts import gTTS
import pygame
import tempfile
import json  # <-- Ajouté pour sauvegarde JSON

app = Flask(__name__, static_folder='static', template_folder='templates')

client = Groq(api_key='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')

conversation_history = []

# 📦 Sauvegarde dans un fichier JSON
def save_conversation_to_json():
    with open("conversation.json", "w", encoding="utf-8") as f:
        json.dump(conversation_history, f, indent=4, ensure_ascii=False)

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

        # 🧠 Mise à jour de l'historique
        conversation_history.append({"role": "user", "content": user_input})
        conversation_history.append({"role": "assistant", "content": assistant_response})

        # 💾 Sauvegarde dans conversation.json
        save_conversation_to_json()

        if len(conversation_history) > 20:
            conversation_history = conversation_history[-20:]

        # 🔊 Synthèse vocale
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
    #conversation_history = []
    #save_conversation_to_json()
    return jsonify({"status": "success"})
@app.route("/nouvelle-page")
def nouvelle_page():
    return render_template("nouvelle_page.html")

@app.route("/entretien")
def entretien():
    return render_template("entretien.html")




# Sauvegarder l'historique dans un fichier JSON
def save_conversation_to_json():
    with open("conversation.json", "w", encoding="utf-8") as f:
        json.dump(conversation_history, f, indent=4, ensure_ascii=False)

@app.route("/entretien-ask", methods=["POST"])
def entretien_ask():
    data = request.get_json()
    user_input = data["user_input"]

    # Initialiser les messages si c'est la première question de l'entretien
    if len(conversation_history) == 0:
        greeting_message = "Bonjour ! Je suis ravi de discuter avec vous. Comme nous avions commencé, je vais vous poser une question technique pour évaluer vos compétences en Python."
        first_question = "Pouvez-vous expliquer ce qu'est le polymorphisme en Python et donner un exemple de son utilisation ?"
        # Ajouter un message d'accueil et la première question
        conversation_history.append({"role": "assistant", "content": greeting_message})
        conversation_history.append({"role": "assistant", "content": first_question})
        save_conversation_to_json()
        return jsonify({"response": greeting_message + " " + first_question})

    # Si l'entretien est déjà en cours, évaluer la réponse
    if user_input:
        # Ajouter la réponse de l'utilisateur à l'historique
        conversation_history.append({"role": "user", "content": user_input})

        # Générer une réponse et une note via l'API
        messages = [
            {"role": "system", "content": "Tu es un recruteur technique d'une entreprise. Pose des questions techniques en français sur Python, Git, Docker, etc. Après chaque réponse, donne une note sur 20 et un feedback."},
        ]

        # Ajouter l'historique de la conversation
        for entry in conversation_history:
            messages.append({"role": entry["role"], "content": entry["content"]})

        try:
            # Demander au modèle de générer une réponse avec une note
            response = client.chat.completions.create(
                messages=messages,
                model="llama-3.3-70b-versatile",
                temperature=0.6,
                max_tokens=512
            )

            assistant_response = response.choices[0].message.content
            note = "Note : 15/20"  # Ici, la note est à ajuster dynamiquement
            feedback = assistant_response + " " + note

            # Ajouter la réponse avec la note dans l'historique de la conversation
            conversation_history.append({"role": "assistant", "content": feedback})

            # Sauvegarder l'historique dans un fichier JSON
            save_conversation_to_json()

            return jsonify({"response": feedback})

        except Exception as e:
            return jsonify({"response": f"Erreur serveur : {str(e)}"})

            
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
