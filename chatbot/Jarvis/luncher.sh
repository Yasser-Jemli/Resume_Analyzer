#!/bin/bash

# Activer l'environnement virtuel
source ./venv/bin/activate

# Lancer ton script (par exemple app.py ou main.py)
python app.py

python3 -m venv venv 
source venv/bin/activate 
pip install flask groq pyautogui

