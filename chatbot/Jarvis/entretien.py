import json
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from threading import Thread
from gtts import gTTS
from shared import client, conversation_history, save_conversation_to_json  # Veille à ce que shared.py existe et soit correct

app = Flask(__name__)
CORS(app)

# Variables globales
num_responses = 0
total_score = 0
current_question_index = 0

# Chargement des questions
try:
    with open("questions.json", encoding="utf-8") as f:
        question_bank = json.load(f)
except FileNotFoundError:
    print("Le fichier questions.json est introuvable.")
    question_bank = []
except json.JSONDecodeError:
    print("Erreur lors du décodage du fichier questions.json.")
    question_bank = []

# Lecture audio (TTS)
def text_to_speech(text, filename="response.mp3"):
    tts = gTTS(text=text, lang="fr")
    tts.save(filename)
    os.system(f"mpg123 {filename}")

# Question suivante
def get_next_question():
    global current_question_index
    if current_question_index < len(question_bank):
        question = question_bank[current_question_index]["question"]
        current_question_index += 1
        return question
    else:
        return None

# Évaluation de la réponse
def evaluate_response(response, expected_keywords):
    score = 0
    total = len(expected_keywords)
    response_lower = response.lower()
    for keyword in expected_keywords:
        if keyword.lower() in response_lower:
            score += 1
    return round((score / total) * 20)

# === ROUTES ===

# Route principale de dialogue
@app.route("/entretien-ask", methods=["POST"])
def entretien_ask():
    global current_question_index, num_responses, total_score
    data = request.get_json()
    if not data or 'user_input' not in data:
        return jsonify({"response": "Données invalides"}), 400

    user_input = data['user_input'].strip()
    print("Données reçues :", user_input)

    # Première interaction : poser une première question
    if len(conversation_history) == 0:
        intro = "Bonjour ! Je suis votre recruteur virtuel. Voici une question technique pour commencer :"
        question = get_next_question()
        if question:
            conversation_history.append({"role": "assistant", "content": question})
            save_conversation_to_json()
            Thread(target=text_to_speech, args=(question,)).start()
            return jsonify({"response": f"{intro} {question}"})
        else:
            Thread(target=text_to_speech, args=("Plus de questions disponibles.",)).start()
            return jsonify({"response": "Plus de questions disponibles."})

    # Évaluer la réponse de l'utilisateur
    if user_input:
        conversation_history.append({"role": "user", "content": user_input})
        last_question_data = question_bank[current_question_index - 1]
        expected_keywords = last_question_data.get("keywords", [])
        note = evaluate_response(user_input, expected_keywords)

        num_responses += 1
        total_score += note

        # Feedback
        feedback = f"Merci pour votre réponse. Note : {note}/20."
        if note < 10:
            feedback += " Il manque plusieurs éléments importants. Essayez de préciser davantage."
        elif note < 16:
            feedback += " Réponse correcte, mais peut être améliorée avec plus de détails."
        else:
            feedback += " Très bonne réponse, bravo !"

        conversation_history.append({"role": "assistant", "content": feedback})

        next_q = get_next_question()
        if next_q:
            conversation_history.append({"role": "assistant", "content": next_q})
            full_response = f"{feedback} Question suivante : {next_q}"
            Thread(target=text_to_speech, args=(next_q,)).start()
        else:
            full_response = f"{feedback} Fin de l'entretien."
            Thread(target=text_to_speech, args=("Fin de l'entretien.",)).start()

        save_conversation_to_json()
        return jsonify({"response": full_response})

# Score moyen
@app.route("/average-score", methods=["GET"])
def get_average_score():
    if num_responses > 0:
        avg_score = total_score / num_responses
        return jsonify({"average_score": round(avg_score, 2)})
    else:
        return jsonify({"average_score": 0})

# Route de test
@app.route('/ping', methods=['GET'])
def ping():
    return "pong"

# Favicon pour éviter erreur 404 dans console
@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico')

# Lancement
if __name__ == "__main__":
    app.run(debug=True)
