from flask import Flask, render_template, request, jsonify
from groq import Groq
from gtts import gTTS
import os
import tempfile
from dotenv import load_dotenv

print("DEBUG: Chargement des variables d'environnement...")
load_dotenv()  # Charge les variables d'environnement à partir de .env

api_key = os.getenv("GROQ_API_KEY")
print("DEBUG: GROQ_API_KEY =", api_key)

if not api_key:
    raise ValueError("ERREUR: GROQ_API_KEY non défini. Vérifie ton fichier .env ou les variables d'environnement.")

app = Flask(__name__)
print("DEBUG: Flask initialisé.")

client = Groq(api_key=api_key)
print("DEBUG: Client Groq initialisé.")

history = []

AUDIO_FOLDER = "static/audio"
os.makedirs(AUDIO_FOLDER, exist_ok=True)
print(f"DEBUG: Dossier audio '{AUDIO_FOLDER}' prêt.")

@app.route("/")
def index():
    print("DEBUG: Route '/' appelée.")
    return render_template("index.html")

@app.route("/send", methods=["POST"])
def send():
    user_msg = request.json.get("message")
    print("DEBUG: Message reçu du client :", user_msg)

    history.append({"role": "user", "content": user_msg})
    print("DEBUG: Historique après ajout du message utilisateur :", history)

    try:
        full_context = [{"role": "system", "content": "Tu es un assistant technique francophone, concis et pertinent."}] + history
        print("DEBUG: Contexte complet envoyé au modèle :", full_context)

        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=full_context
        ).choices[0].message.content

        print("DEBUG: Réponse du modèle :", response)

        history.append({"role": "assistant", "content": response})
        print("DEBUG: Historique après ajout de la réponse :", history)

        tts = gTTS(response, lang="fr")
        audio_name = next(tempfile._get_candidate_names()) + ".mp3"
        audio_path = os.path.join(AUDIO_FOLDER, audio_name)
        print("DEBUG: Chemin du fichier audio généré :", audio_path)

        tts.save(audio_path)
        print("DEBUG: Fichier audio enregistré.")

        return jsonify({
            "response": response,
            "audio": f"/static/audio/{audio_name}"
        })
    except Exception as e:
        print("ERREUR dans /send :", str(e))
        return jsonify({"response": f"Erreur : {str(e)}", "audio": ""})

if __name__ == "__main__":
    print("DEBUG: Démarrage de l'application Flask...")
    app.run(debug=True)

