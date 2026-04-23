# Référence : Hooks Frontend

Documentation des hooks personnalisés gérant la logique métier du frontend.

## Hook `useChat`

Le hook `useChat` est le pivot central de la communication avec l'agent. Il gère l'état local des discussions et la consommation du flux NDJSON.

### Fonctions principales

- **`addMessage(content: string)`** : Envoie un message utilisateur au backend et gère la lecture du stream asynchrone pour mettre à jour la réponse de l'assistant en temps réel.
- **`newConversation()`** : Réinitialise l'état pour commencer une nouvelle session.
- **`deleteConversation(id: string)`** : Supprime une discussion de l'historique local.

### État retourné

| Propriété | Type | Description |
|-----------|------|-------------|
| `conversations` | `Conversation[]` | Liste de toutes les discussions stockées. |
| `activeConversation` | `Conversation` | La discussion actuellement affichée. |
| `isLoading` | `boolean` | Indique si une requête vers l'IA est en cours. |

!!! info "Stream NDJSON"
    Le hook utilise `ReadableStreamDefaultReader` pour lire la réponse HTTP ligne par ligne, permettant une mise à jour instantanée de l'interface (tokens et appels d'outils).
