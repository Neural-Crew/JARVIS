# Guide de Déploiement avec Docker

Ce guide explique comment déployer Jarvis en quelques minutes à l'aide de Docker et Docker Compose.

## 1. Prérequis

- **Docker** installé sur votre machine.
- **Docker Compose** (inclus dans Docker Desktop ou à installer séparément sous Linux).

## 2. Préparation

Assurez-vous d'avoir configuré votre fichier `.env` à la racine du projet avec votre clé API :

```env
MISTRAL_API_KEY=votre_clef_ici
```

!!! note "Clé API"
    Conformément aux bonnes pratiques de sécurité, la clé API n'est pas incluse dans l'image Docker. Elle est injectée au moment du lancement via le fichier `.env`.

## 3. Lancement

Lancez l'intégralité de la stack (Backend + Frontend) avec une seule commande :

```bash
docker compose up -d --build
```

### Ce qui se passe lors du lancement :
1. **Service `backend`** : L'image est construite à partir de `backend.Dockerfile`. Les dépendances Poetry sont installées et le serveur FastAPI est lancé sur le port `8000`.
2. **Service `frontend`** : L'image est construite via `frontend.Dockerfile` (multi-stage build). L'application React est compilée en fichiers statiques, puis servie par un serveur **Nginx** optimisé sur le port `8080` (mappé depuis le port 80 du conteneur).
3. **Service `docs`** : Un serveur MkDocs Material est lancé sur le port `8008`, synchronisant en temps réel vos fichiers de documentation.

## 4. Accès aux services

Une fois les conteneurs démarrés, Jarvis est accessible via :

- **Interface Utilisateur** : [http://localhost:8080](http://localhost:8080)
- **Documentation du projet** : [http://localhost:8008](http://localhost:8008)
- **Documentation API (Swagger)** : [http://localhost:8000/docs](http://localhost:8000/docs)

## 5. Gestion des services

- **Arrêter les services** : `docker compose stop`
- **Supprimer les conteneurs** : `docker compose down`
- **Voir les logs** : `docker compose logs -f`
- **Mettre à jour après modification du code** : `docker compose up -d --build`

!!! tip "Optimisation Nginx"
    La configuration Docker utilise un proxy Nginx pour le point d'entrée `/chat`. Cela évite les problèmes de CORS en production en permettant au frontend de communiquer avec le backend sur le même domaine/hôte.
