import requests
import os
import json
from dotenv import load_dotenv

# Charger la clé API depuis un fichier .env (recommandé pour la sécurité)
load_dotenv()
API_KEY = "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"  # Assure-toi que la clé est définie dans un fichier .env

# Option pour utiliser la clé directement (NON recommandé pour la production)
# API_KEY = "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"

API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Vérifier que la clé API est définie
if not API_KEY:
    raise ValueError("❌ Erreur : La clé API GROQ_API_KEY n'est pas définie. Ajoute-la dans un fichier .env.")

# En-têtes pour la requête API
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Liste des compétences pour lesquelles générer des questions
skills = ["c++", "C", "Jira"]

# Prompt en français pour générer des questions avec mots-clés
prompt = (
    f"Génère 5 questions d'entretien technique en français pour chacune des compétences suivantes : {', '.join(skills)}. "
    "Les questions doivent couvrir différents niveaux de difficulté (débutant à avancé) et se concentrer sur des concepts pratiques et pertinents pour un emploi. "
    "Pour chaque question, fournis une liste de 3 à 5 mots-clés pertinents associés à la question. "
    "Formate la sortie en JSON avec le format suivant : "
    "[{\"question\": \"texte de la question\", \"keywords\": [\"mot1\", \"mot2\", \"mot3\", ...]}, ...]. "
    "Assure-toi que toutes les questions et mots-clés sont en français."
)

# Données de la requête API
data = {
    "model": "llama-3.3-70b-versatile",
    "messages": [
        {"role": "user", "content": prompt}
    ],
    "temperature": 0.7,
    "max_tokens": 2000,
    "response_format": {"type": "json_object"}
}

try:
    # Envoyer la requête à l'API
    response = requests.post(API_URL, headers=headers, json=data)

    # Vérifier la réponse
    if response.status_code == 200:
        print("✅ Requête réussie !")
        response_content = response.json()["choices"][0]["message"]["content"]

        # Parser la réponse JSON
        try:
            questions_data = json.loads(response_content)
        except json.JSONDecodeError:
            print("❌ Erreur : La réponse de l'API n'est pas un JSON valide.")
            print(response_content)
            raise

        # Afficher les questions
        print(json.dumps(questions_data, indent=2, ensure_ascii=False))

        # Sauvegarder les questions dans un fichier JSON
        with open("questions.json", "w", encoding="utf-8") as f:
            json.dump(questions_data, f, indent=2, ensure_ascii=False)
        print("📝 Questions sauvegardées dans 'questions.json'")

    else:
        print(f"❌ Erreur : {response.status_code}")
        print(response.text)

except requests.exceptions.RequestException as e:
    print(f"❌ Erreur réseau : {e}")
except KeyError as e:
    print(f"❌ Erreur dans la réponse JSON : {e}. Vérifie la structure de la réponse API.")
except Exception as e:
    print(f"❌ Erreur inattendue : {e}")
