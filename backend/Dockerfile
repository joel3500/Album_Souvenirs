# Utilise une image Python officielle
FROM python:3.11-slim


# Définir le répertoire de travail (dans l'image Docker)
WORKDIR /app


# Copier les fichiers requis / COPY <source> <destination> / 
# Copie tout le contenu du dossier courant (de mon système hôte) vers le dossier courant (dans l'image Docker / dans le conteneur). 
COPY . .


# Mise à jour de pip et Installer les dépendances
RUN pip install --upgrade pip
# RUN pip install flask
RUN pip install -r requirements.txt


# Exposer le port 5000 pour Flask
EXPOSE 5000


# Commande pour lancer Flask / Commande à exécuter au lancement du conteneur
# CMD ["python", "app.py"]
CMD gunicorn -w 2 -b 0.0.0.0:$PORT app:app
