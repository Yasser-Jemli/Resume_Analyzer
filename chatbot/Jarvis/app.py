from flask import Flask, render_template, request, jsonify
import os, re, tempfile, uuid
import pyautogui
from gtts import gTTS
from shared import client, conversation_history, save_conversation_to_json
from nouvelle_page import nouvelle_page
import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder="static", template_folder="templates")

# ──────────────────── ROUTES GÉNÉRALES ──────────────────── #

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/nouvelle-page")
def nouvelle_page_route():
    return nouvelle_page()

load_dotenv()
try:
    with open("groq.txt", "r", encoding="utf-8") as f:
        API_KEY = f.read().strip()
except FileNotFoundError:
    raise FileNotFoundError("❌ Erreur : Le fichier groq.txt est introuvable.")
if not API_KEY:
    raise RuntimeError("❌ Clé API GROQ_API_KEY manquante.")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(exist_ok=True)
HISTORY_FILE = DATA_DIR / "actia_answers.json"

# ───────── 2. Flask + CORS ───────── #

app = Flask(__name__, static_folder="static")


# ───────── 3. Connaissances ───────── #

KNOWLEDGE_BASE = """
Actia Engineering Services est une division du groupe ACTIA spécialisée dans la conception...
(texte raccourci)
"""

PROMPT_TEMPLATE = (
    "Tu es un expert d’Actia Engineering Services. "
    "Réponds uniquement aux questions concernant cette entité, en français, en t’appuyant sur : {knowledge}. "
    "Si la question n’est pas pertinente, réponds : "
    "'Désolé, je ne peux répondre qu’aux questions sur Actia Engineering Services.'. "
    'Formate ta réponse en JSON strict, sous la forme : {{"answer": "…"}}. '
    "Question : {question}"
)

# ───────── 4. Fonction appel API Groq ───────── #

def _ask_groq(question: str) -> str:
    prompt = PROMPT_TEMPLATE.format(knowledge=KNOWLEDGE_BASE, question=question)
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 400,
        "response_format": {"type": "json_object"},
    }
    resp = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=HEADERS,
        json=payload,
        timeout=30,
    )
    resp.raise_for_status()

    raw = resp.json()["choices"][0]["message"]["content"]
    data = json.loads(raw)
    if "answer" not in data:
        raise KeyError("Champ 'answer' manquant dans la réponse Groq.")
    return data["answer"]

# ───────── 5. Routes ───────── #

@app.route("/test", methods=["GET"])
def test():
    return "Test OK", 200



@app.route("/", methods=["GET"])
def root():
    return send_from_directory(app.static_folder, "index.html")

# ───────── 6. Main ───────── #
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

@app.route("/ask-assis", methods=["POST"])
def askin():
    print("Route /ask-assis appelée")
    question = (
        request.form.get("question")
        or (request.get_json(silent=True) or {}).get("question")
        or ""
    ).strip()
    if not question:
        return jsonify(error="La question ne peut pas être vide."), 400

    try:
        answer = _ask_groq(question)
    except (requests.RequestException, json.JSONDecodeError, KeyError) as e:
        return jsonify(error=f"Erreur appel API : {e}"), 502

    # Historique
    history = []
    if HISTORY_FILE.exists():
        try:
            history = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
            if not isinstance(history, list):
                history = [history]
        except json.JSONDecodeError:
            history = []

    history.append({"question": question, "answer": answer})
    HISTORY_FILE.write_text(json.dumps(history, indent=2, ensure_ascii=False), encoding="utf-8")

    return jsonify(answer=answer), 200 


# ──────────────────── LANCEMENT ──────────────────── #

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
