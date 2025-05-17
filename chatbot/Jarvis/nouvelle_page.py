from flask import render_template, request, jsonify
import os

# Fonction pour afficher la page de l'entretien RH
def nouvelle_page():
    return render_template("nouvelle_page.html")

# Fonction pour gérer la soumission de l'entretien
def submit_interview():
    # Récupérer les réponses des QCM
    answers = request.form.getlist('answers')  # Liste des réponses aux QCM
    text_responses = request.form.get("text_responses")  # Réponse textuelle

    # Vous pouvez ici sauvegarder ou traiter les réponses selon vos besoins
    # Par exemple, les afficher dans le terminal (ou les enregistrer dans un fichier ou base de données)
    print("Réponses QCM :", answers)
    print("Réponse textuelle :", text_responses)

    # Retourner un message de succès (ou une réponse JSON si besoin)
    return jsonify({"status": "success", "message": "Entretien soumis avec succès"})
