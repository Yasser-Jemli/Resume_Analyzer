from flask import Flask, render_template, request, jsonify
from groq import Groq
from gtts import gTTS
import os
import tempfile

app = Flask(__name__)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))  # Défini cette variable d'env
history = []

AUDIO_FOLDER = "static/audio"
os.makedirs(AUDIO_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/send", methods=["POST"])
def send():
    user_msg = request.json.get("message")
    history.append({"role": "user", "content": user_msg})
    try:
        full_context = [{"role": "system", "content": "Tu es un assistant technique francophone, concis et pertinent."}] + history
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=full_context
        ).choices[0].message.content

        history.append({"role": "assistant", "content": response})

        tts = gTTS(response, lang="fr")
        audio_name = next(tempfile._get_candidate_names()) + ".mp3"
        audio_path = os.path.join(AUDIO_FOLDER, audio_name)
        tts.save(audio_path)

        return jsonify({
            "response": response,
            "audio": f"/static/audio/{audio_name}"
        })
    except Exception as e:
        return jsonify({"response": f"Erreur : {str(e)}", "audio": ""})

if __name__ == "__main__":
    app.run(debug=True)
