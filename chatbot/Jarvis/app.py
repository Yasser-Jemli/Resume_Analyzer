from flask import Flask, render_template, request, jsonify
import os, re, tempfile, uuid
import pyautogui
from gtts import gTTS
from shared import client, conversation_history, save_conversation_to_json
from nouvelle_page import nouvelle_page

app = Flask(__name__, static_folder="static", template_folder="templates")

# ──────────────────── ROUTES GÉNÉRALES ──────────────────── #

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/nouvelle-page")
def nouvelle_page_route():
    return nouvelle_page()

# ──────────────────── CHAT GÉNÉRIQUE ──────────────────── #

def get_chat_response(user_input: str) -> dict:
    """Traite l’entrée utilisateur et renvoie un dict {text, audio_url}."""
    global conversation_history
    txt_lower = user_input.lower().strip()

    # 1. Commandes locales simples
    if txt_lower == "créer un fichier test":
        with open("fichier_test.txt", "w", encoding="utf-8") as f:
            f.write("Bonjour")
        return {"text": "✅ Fichier test créé, Monsieur.", "audio_url": None}

    if txt_lower == "faire une capture d'écran":
        save_path = os.path.join("Documents", "Python", "Jarvis", "capture.png")
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        pyautogui.screenshot().save(save_path)
        return {"text": f"✅ Capture d'écran enregistrée ici : '{save_path}', Monsieur.", "audio_url": None}

    # 2. Création de fichier personnalisé
    match = re.search(
        r"(créer|faire|générer)\s+.*fichier\s+(nommé|appelé)?\s*(\w+\.\w+)?\s*(dans\s+(\w+))?\s*(avec\s+le\s+contenu\s*'([^']+)')?",
        txt_lower
    )
    if match:
        filename   = match.group(3) or "fichier.txt"
        directory  = match.group(5) or ""
        content    = match.group(7) or "Bonjour"
        file_path  = os.path.join(directory, filename) if directory else filename

        os.makedirs(os.path.dirname(file_path) or ".", exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return {"text": f"✅ Fichier '{file_path}' créé avec le contenu : '{content}', Monsieur.", "audio_url": None}

    # 3. Appel au LLM
    messages = [
        {
            "role": "system",
            "content": "Tu es J.A.R.V.I.S., l'assistant de Tony Stark. Tu parles français, restes courtois et appelles ton interlocuteur « Monsieur »."
        },
        *conversation_history,                        # historique
        {"role": "user", "content": user_input}       # nouveau message
    ]

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7,
            max_tokens=1024,
            top_p=1
        )
        assistant_reply = completion.choices[0].message.content.strip()

        # Mémorisation light
        conversation_history.extend([
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": assistant_reply}
        ])
        if len(conversation_history) > 20:
            conversation_history = conversation_history[-20:]
        save_conversation_to_json()

        # Génération audio non‑bloquante
        audio_url = None
        try:
            audio_dir = os.path.join(app.static_folder, "audio")
            os.makedirs(audio_dir, exist_ok=True)
            mp3_name  = f"{uuid.uuid4()}.mp3"
            mp3_path  = os.path.join(audio_dir, mp3_name)
            gTTS(text=assistant_reply, lang="fr").save(mp3_path)
            audio_url = f"/static/audio/{mp3_name}"
        except Exception as tts_err:
            print("❗ Erreur TTS :", tts_err)

        return {"text": assistant_reply, "audio_url": audio_url}

    except Exception as e:
        import traceback; traceback.print_exc()
        return {"text": "⚠️ Erreur système : veuillez réessayer, Monsieur.", "audio_url": None}

@app.route("/ask", methods=["POST"])
def ask():
    # Support JSON et x‑www‑form‑urlencoded
    if request.is_json:
        data = request.get_json(silent=True) or {}
        user_input = data.get("user_input", "").strip()
    else:
        user_input = request.form.get("user_input", "").strip()

    if not user_input:
        return jsonify({"response": "Champ 'user_input' manquant."}), 400

    resp = get_chat_response(user_input)
    return jsonify(resp)

# ──────────────────── OUTILS CONVERSATION ENTREVUE ──────────────────── #

@app.route("/entretien")
def entretien():
    return render_template("entretien.html")

from entretien import entretien_ask
app.add_url_rule("/entretien-ask", view_func=entretien_ask, methods=["POST"])

# ──────────────────── HISTORIQUE ──────────────────── #

@app.route("/clear-history", methods=["POST"])
def clear_history():
    global conversation_history
    conversation_history = []
    save_conversation_to_json()
    return jsonify({"status": "success"})

# ──────────────────── LANCEMENT ──────────────────── #

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
