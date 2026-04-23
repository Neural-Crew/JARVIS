# Utilise l'image Python 3.13 slim pour plus de légèreté
FROM python:3.13-slim

# Évite la création de fichiers .pyc et assure que les logs sont envoyés à stdout
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /app

# Répertoire de travail
WORKDIR /app

# Installation des dépendances système nécessaires
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Installation de Poetry
RUN pip install poetry

# Désactive la création d'un environnement virtuel par Poetry (car on est dans Docker)
RUN poetry config virtualenvs.create false

# Copie des fichiers de dépendances
COPY pyproject.toml poetry.lock ./

# Installation des dépendances (sans les dépendances de dev)
RUN poetry install --no-interaction --no-ansi --only main

# Copie du code source
COPY backend ./backend
COPY .env* ./

# Port exposé par FastAPI/Uvicorn
EXPOSE 8000

# Commande de lancement
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
