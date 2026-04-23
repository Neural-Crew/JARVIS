# Tutoriel : Prise en main de Jarvis

Ce tutoriel détaille les étapes pour installer, configurer et utiliser Jarvis dans un environnement de développement local.

## 1. Prérequis

Avant de commencer, assurez-vous d'avoir installé :
- **Python 3.11+**
- **Node.js 18+** et **npm** (ou bun)
- **Poetry** (gestionnaire de dépendances Python)

## 2. Installation

### Backend (Python)
Clonez le dépôt et installez les dépendances avec Poetry :
```bash
# À la racine du projet
poetry install
```
Ceci créera un environnement virtuel et installera FastAPI, LangChain, LangGraph et les clients API nécessaires.

### Frontend (React)
Accédez au dossier frontend et installez les paquets :
```bash
cd frontend
npm install
```

## 3. Configuration de l'environnement

Jarvis nécessite des clés API pour fonctionner. Créez un fichier `.env` à la racine du projet :

```env
# API Key pour le modèle Mistral (Requis)
MISTRAL_API_KEY=votre_clef_mistral_ici

# API Key pour Ecowatch (Optionnel pour le mode démo)
ECOWATCH_API_KEY=votre_clef_ecowatch_ici
```

!!! warning "Sécurité"
    Ne partagez jamais votre fichier `.env`. Il est automatiquement ignoré par Git via le fichier `.gitignore`.

## 4. Lancement de l'application

Vous devez lancer le backend et le frontend simultanément.

### Démarrer le Backend
```bash
# Depuis la racine
uvicorn backend.main:app --reload
```
Le serveur sera disponible sur `http://localhost:8000`. Vous pouvez consulter la documentation OpenAPI (Swagger) sur `http://localhost:8000/docs`.

### Démarrer le Frontend
```bash
# Depuis le dossier frontend
npm run dev
```
L'interface sera accessible sur `http://localhost:5173`.

## 5. Première utilisation

1. Ouvrez votre navigateur sur `http://localhost:5173`.
2. Saisissez un message, par exemple : *"Bonjour Jarvis, peux-tu me donner la température actuelle ?"*.
3. Observez les indicateurs d'outils (Tool Calls) qui s'affichent pendant que Jarvis consulte les capteurs.

!!! tip "Astuce"
    Si vous avez configuré Ecowatch, essayez de demander : *"Affiche-moi l'historique de température du boitier 20240313101500 pour les 3 derniers jours."* Jarvis générera automatiquement un graphique interactif.
