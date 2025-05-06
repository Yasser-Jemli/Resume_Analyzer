
# Utilise une image Python officielle comme base
FROM python:3.12-slim

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Copie les fichiers du projet dans le conteneur
COPY . /app

# Installe les dépendances système nécessaires (ex: pour pyautogui)
RUN apt-get update && apt-get install -y \
    libx11-dev \
    libxtst6 \
    libpng-dev \
    libxss1 \
    libxrandr2 \
    libxi6 \
    x11-utils \
    && rm -rf /var/lib/apt/lists/*

# Installe les dépendances Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose le port sur lequel l'app Flask s'exécutera
EXPOSE 5000

# Commande pour démarrer l'application Flask
CMD ["python", "app.py"]

