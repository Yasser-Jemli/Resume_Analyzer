import os
import json
from pathlib import Path
from threading import Thread
from typing import List, Dict, Any

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from gtts import gTTS

# ─────────────────────────── Flask & CORS ─────────────────────────── #
app = Flask(__name__)
CORS(app)

# ─────────────────── Variables globales & historiques ─────────────── #
question_bank: List[Dict[str, Any]] = []
current_question_index = 0
num_responses = 0
total_score = 0
conversation_history: List[Dict[str, str]] = []

# ─────────────────────── Fonction utilitaires ─────────────────────── #
DATA_PATH = Path("questions.json")

def load_questions() -> List[Dict[str, Any]]:
    """Charge les questions depuis questions.json et fusionne toutes les clés
       commençant par 'questions_'. Renvoie une liste plate d'objets question."""
    if not DATA_PATH.exists():
        print("❌ Le fichier questions.json est introuvable.")
        return []

    try:
        full_data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        print("❌ Erreur de décodage JSON.")
        return []

    bank: List[Dict[str, Any]] = []
    for key, val in full_data.items():
        if key.startswith("questions_") and isinstance(val, list):
            bank.extend(val)
    print(f"✅ {len(bank)} questions chargées.")
    return bank

def save_conversation_to_json(path: Path = Path("conversation.json")) -> None:
    path.write_text(json.dumps(conversation_history, indent=2, ensure_ascii=False), encoding="utf-8")

def text_to_speech(text: str, filename: str = "response.mp3") -> None:
    """Génère un MP3 en français et le lit avec mpg123 (silencieusement)."""
    tts = gTTS(text=text, lang="fr")
    tts.save(filename)
    os.system(f"mpg123 -q {filename}")  # -q pour ne pas polluer la console

def get_next_question() -> Dict[str, Any] | None:
    """Renvoie l'objet question suivant ou None si terminé."""
    global current_question_index
    if current_question_index < len(question_bank):
        q = question_bank[current_question_index]
        current_question_index += 1
        return q
    return None

def evaluate_response(resp: str, expected_keywords: List[str]) -> int:
    """Retourne une note /20 en fonction des mots‑clés présents dans la réponse."""
    if not expected_keywords:
        return 0
    score = sum(1 for kw in expected_keywords if kw.lower() in resp.lower())
    return round((score / len(expected_keywords)) * 20)

# ─────────────────────── Chargement initial ───────────────────────── #
question_bank = load_questions()

# ───────────────────────────── Routes ─────────────────────────────── #
@app.route("/entretien-ask", methods=["POST"])
def entretien_ask():
    global num_responses, total_score

    data = request.get_json(silent=True) or {}
    user_input = data.get("user_input", "").strip()

    # 1) Première interaction : envoie la 1ʳᵉ question
    if not conversation_history:
        first_q = get_next_question()
        if not first_q:
            return jsonify({"response": "Plus de questions disponibles."})
        intro = "Bonjour ! Je suis votre recruteur virtuel. Voici une question technique pour commencer :"
        conversation_history.append({"role": "assistant", "content": first_q["question"]})
        save_conversation_to_json()
        Thread(target=text_to_speech, args=(first_q["question"],)).start()
        return jsonify({"response": f"{intro} {first_q['question']}"})

    # 2) Réponse vide
    if not user_input:
        return jsonify({"response": "❌ Votre réponse est vide."}), 400

    # 3) Évalue la réponse sur la dernière question posée
    conversation_history.append({"role": "user", "content": user_input})
    prev_q = question_bank[current_question_index - 1]
    note = evaluate_response(user_input, prev_q.get("keywords", []))

    num_responses += 1
    total_score += note

    # 4) Retour de feedback
    feedback = f"Merci pour votre réponse. Note : {note}/20."
    if note < 10:
        feedback += " Il manque plusieurs éléments importants."
    elif note < 16:
        feedback += " Réponse correcte, mais elle peut être améliorée."
    else:
        feedback += " Très bonne réponse, bravo !"

    conversation_history.append({"role": "assistant", "content": feedback})

    # 5) Question suivante ou fin d'entretien
    next_q = get_next_question()
    if next_q:
        conversation_history.append({"role": "assistant", "content": next_q["question"]})
        full_response = f"{feedback} Question suivante : {next_q['question']}"
        Thread(target=text_to_speech, args=(next_q["question"],)).start()
    else:
        average = total_score / num_responses if num_responses else 0
        full_response = f"{feedback} Fin de l'entretien. Score moyen : {average:.1f}/20."
        Thread(target=text_to_speech, args=("Fin de l'entretien.",)).start()

    save_conversation_to_json()
    return jsonify({"response": full_response})

@app.route("/average-score", methods=["GET"])
def get_average_score():
    average = total_score / num_responses if num_responses else 0
    return jsonify({"average_score": round(average, 2)})

@app.route("/ping", methods=["GET"])
def ping():
    return "pong"

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico')

# ──────────────────────────── Main ─────────────────────────────────── #
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

