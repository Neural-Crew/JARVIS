FROM python:3.11-slim

WORKDIR /app

# Installation des dépendances pour MkDocs Material et mkdocstrings
RUN pip install --no-cache-dir \
    mkdocs-material \
    "mkdocstrings[python]" \
    mkdocstrings-python

# Copie de la configuration et des sources de documentation
COPY mkdocs.yml ./
COPY docs/ ./docs/
COPY backend/ ./backend/

# Port exposé par MkDocs
EXPOSE 8000

# Lancement du serveur MkDocs (écoute sur toutes les interfaces pour Docker)
CMD ["mkdocs", "serve", "--dev-addr", "0.0.0.0:8000"]
