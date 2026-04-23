# Référence : Frontend Core (Types & Utils)

## Types de Données (`types/chat.ts`)

Le frontend utilise des types TypeScript rigoureux pour modéliser les échanges avec l'agent.

### `Message`
Représente un message individuel.
- `role`: "user" | "assistant"
- `content`: string (Markdown supporté)
- `toolCalls`: Liste optionnelle d'appels d'outils.

### `ToolCall`
Décrit l'exécution d'un outil par l'agent.
- `status`: "running" | "success" | "error"
- `input` / `output` : Données brutes de l'outil.
- `payload` : Données structurées (ex: graphiques).

### `Conversation`
Regroupe un historique de messages et des métadonnées (titre, dates).

## Utilitaires (`lib/utils.ts`)

### `cn(...inputs)`
Utilitaire de fusion de classes CSS (Tailwind Merge + CLSX). Permet de combiner des classes conditionnelles de manière propre et sans conflits.
