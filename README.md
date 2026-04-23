# Jarvis 🤖

Jarvis est un assistant intelligent (agentique) conçu pour la supervision environnementale. Basé sur **FastAPI**, **LangGraph** (backend) et **React** (frontend), il permet d'interagir avec des capteurs en temps réel et de visualiser des données historiques.

## 🚀 Lancement Rapide (Méthode Recommandée)

Le déploiement via **Docker** est la méthode standard pour lancer Jarvis.

### 1. Prérequis
- [Docker](https://www.docker.com/get-started) & [Docker Compose](https://docs.docker.com/compose/install/)

### 2. Configuration
Créez un fichier `.env` à la racine du projet :
```env
MISTRAL_API_KEY=votre_clef_ici
```

### 3. Démarrage
```bash
docker compose up -d --build
```

- **Interface Jarvis** : [http://localhost:8080](http://localhost:8080)
- **Documentation API** : [http://localhost:8000/docs](http://localhost:8000/docs)
- **Documentation Projet** : [http://localhost:8008](http://localhost:8008) (si le serveur de doc est lancé localement)

---

## 🛠️ Développement Local (Méthode Manuelle)

Si vous souhaitez modifier le code et profiter du rechargement à chaud (hot-reload).

### Backend (Python)
Utilise **Poetry** pour la gestion des dépendances.
```bash
# Installation
poetry install

# Lancement
uvicorn backend.main:app --reload
```

### Frontend (React)
```bash
cd frontend
npm install
npm run dev
```

---

## 📚 Documentation Complète

Une documentation détaillée basée sur le framework **Diátaxis** est disponible dans le dossier `docs/` ou via le site MkDocs :
- [Tutoriels](docs/tutorials/getting-started.md) : Prise en main étape par étape.
- [Architecture](docs/explanation/architecture.md) : Comprendre le fonctionnement interne (LangGraph, NDJSON).
- [Déploiement Docker](docs/how-to/docker-deployment.md) : Guide détaillé pour la mise en production.

---

## 🧪 Tests et CI
La CI (GitHub Actions) valide automatiquement :
- **Backend** : Tests unitaires via `pytest` et vérification du démarrage.
- **Frontend** : Linting, tests Vitest et build de production.

*Note : Les fonctionnalités nécessitant une clé API sont ignorées lors des tests de CI.*



