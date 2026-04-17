# Bienvenue sur la documentation de Jarvis

Jarvis est un assistant intelligent (agentique) capable d'interagir avec divers outils et services, notamment pour le suivi énergétique avec Ecowatch.

!!! tip "Découvrez Jarvis"
    Vous voulez savoir comment parler à Jarvis ? Consultez notre [Guide d'Utilisation](how-to/user-guide.md) pour découvrir des exemples de conversations !

## 🚀 Démarrage Rapide (Docker)

!!! failure "Clés API Requises"
    Jarvis ne peut pas fonctionner sans clés API valides. Avant de lancer le projet, assurez-vous d'avoir :
    
    1. Une clé **Mistral AI** (`MISTRAL_API_KEY`) pour le raisonnement de l'agent.
    2. (Optionnel) Une clé **Ecowatch** (`ECOWATCH_API_KEY`) pour les outils de supervision réels.
    
    Sans `MISTRAL_API_KEY`, l'agent refusera de répondre à toute demande.

Le projet est conçu pour être déployé instantanément avec **Docker Compose**. 

```bash
# Clonez et remplissez votre .env avec MISTRAL_API_KEY
docker compose up -d
```

Pour plus de détails, consultez notre [Guide de Déploiement Docker](how-to/docker-deployment.md).

## Structure de la documentation

Cette documentation suit le framework **Diátaxis** :

!!! tip "Tutoriels"
    Apprenez à utiliser Jarvis étape par étape dans la section [Tutoriels](tutorials/getting-started.md).

!!! note "Guides"
    Des guides pratiques pour accomplir des tâches spécifiques (ex: configuration, [Docker](how-to/docker-deployment.md)) dans la section [Guides](how-to/configuration.md).

!!! info "Référence"
    Documentation technique détaillée du code (API, modules) dans la section [Référence](reference/backend/agent.md).

!!! abstract "Explications"
    Comprenez les concepts fondamentaux et l'architecture du projet dans la section [Explications](explanation/architecture.md).
