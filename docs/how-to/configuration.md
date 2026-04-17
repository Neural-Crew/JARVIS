# Guide de Configuration

Comment configurer les différentes briques de Jarvis.

## Variables d'environnement

Jarvis utilise un fichier `.env` à la racine pour charger les paramètres sensibles.

| Variable | Description | Par défaut |
|----------|-------------|------------|
| `MISTRAL_API_KEY` | Clé API pour le modèle Mistral | (Requis) |
| `VITE_API_BASE` | URL du backend pour le frontend | `http://localhost:8000` |

!!! warning "Sécurité"
    Ne committez jamais votre fichier `.env`. Il est listé dans `.gitignore`.
