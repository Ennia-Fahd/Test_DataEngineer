# Étape 1 : Image de base
FROM python:3.11-slim

# Étape 2 : Répertoire de travail
WORKDIR /app

# Étape 3 : Copier les fichiers dans le conteneur
COPY . .

# Étape 4 : Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Étape 5 : Point d’entrée
CMD ["python", "weather_pipeline.py"]
