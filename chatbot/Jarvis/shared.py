from groq import Groq
import json

# Initialisation du client Groq
client = Groq(api_key='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')

# Historique de conversation
conversation_history = []

# Fonction de sauvegarde JSON
def save_conversation_to_json():
    with open("conversation.json", "w", encoding="utf-8") as f:
        json.dump(conversation_history, f, indent=4, ensure_ascii=False)