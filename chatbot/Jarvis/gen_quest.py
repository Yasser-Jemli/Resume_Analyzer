import os
import json
import requests
from pathlib import Path
from typing import List, Dict, Any

from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

# ──────────────────── Flask init ──────────────────── #
app = Flask(__name__)
CORS(app)

# ─────────────────── API KEY Groq ─────────────────── #
load_dotenv()
API_KEY: str | None = os.getenv("GROQ_API_KEY")

if not API_KEY and Path("groq.txt").exists():
    API_KEY = Path("groq.txt").read_text(encoding="utf-8").strip()
    print("✅ Clé API chargée depuis groq.txt")

if not API_KEY:
    print("❌ Clé API Groq introuvable dans .env ou groq.txt")
    raise RuntimeError("Clé API Groq introuvable (.env ou groq.txt).")

print(f"[DEBUG] Clé API chargée : {API_KEY[:6]}...")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}
API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "llama3-70b-8192"

# ─────────────────── Fonctions utilitaires ─────────────────── #
def build_prompt(skills: List[str]) -> str:
    comp = ", ".join(skills)
    return (
        f"Tu es un assistant RH. Génère STRICTEMENT un objet JSON en français contenant 5 questions techniques pour chacune des compétences suivantes : {comp}. "
        "Chaque question doit avoir un champ 'question' (texte) et 'keywords' (liste de mots-clés). "
        "Ne fournis aucun texte supplémentaire, uniquement le JSON pur au format : "
        "{"
        + ", ".join(f"\"questions_{s.replace('+', 'p').replace(' ', '_')}\": [{{\"question\": \"...\", \"keywords\": [\"...\", ...]}}]" for s in skills)
        + "}."
    )

def call_groq(prompt: str) -> Dict[str, Any]:
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 2048
    }
    res = requests.post(API_URL, headers=HEADERS, json=payload, timeout=60)
    print("[DEBUG] Requête envoyée à Groq.")
    print(f"[DEBUG] Status code : {res.status_code}")
    print(f"[DEBUG] Réponse brute complète :\n{res.text}\n")

    res.raise_for_status()
    content = res.json()["choices"][0]["message"]["content"]

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        raise ValueError(f"La réponse Groq n'est pas un JSON valide.\nContenu reçu :\n{content}")

# ─────────────────── Route API ─────────────────── #
@app.route("/sendPost", methods=["POST"])
def recevoir_competences():
    data = request.get_json(silent=True) or {}
    print("============================",data)
    skills = data.get("skills")

    if not isinstance(skills, list) or not skills:
        return jsonify({"error": "Aucune compétence reçue"}), 400

    print("🧠 Compétences reçues :", skills)

    try:
        prompt = build_prompt(skills)
        questions_json = call_groq(prompt)
    except requests.HTTPError as err:
        return jsonify({"error": f"Erreur HTTP Groq {err.response.status_code}"}), 502
    except (json.JSONDecodeError, KeyError) as err:
        return jsonify({"error": f"Réponse Groq invalide : {err}"}), 502
    except ValueError as err:
        # Erreur JSON non valide avec message clair
        return jsonify({"error": str(err)}), 502
    except Exception as err:
        return jsonify({"error": f"Erreur inattendue : {err}"}), 500

    # Sauvegarde locale
    Path("questions.json").write_text(json.dumps(questions_json, indent=2, ensure_ascii=False), encoding="utf-8")
    print("📝 Questions enregistrées dans questions.json")

    return jsonify(questions_json)

# ─────────────────── Ping ─────────────────── #
@app.route("/ping")
def ping():
    return "pong"

# ─────────────────── Main ─────────────────── #
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5003)

