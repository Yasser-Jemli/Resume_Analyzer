import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# ───────── 1. Config générale ───────── #

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

@app.route("/ask-assis", methods=["POST"])
def ask():
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

@app.route("/", methods=["GET"])
def root():
    return send_from_directory(app.static_folder, "index.html")

# ───────── 6. Main ───────── #

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
