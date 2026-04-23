# Référence : Composants Chat

Cette section décrit les composants React essentiels au fonctionnement du chat.

## `ChatMessage`
Composant responsable du rendu d'un message.
- **Markdown** : Utilise `react-markdown` avec support GFM (GitHub Flavored Markdown).
- **Tool Rendu** : Affiche des indicateurs visuels (badges) pour chaque appel d'outil.
- **Visualisation** : Intègre le sous-composant `ToolChart` pour rendre les graphiques Recharts.

## `ChatInput`
Champ de saisie intelligent.
- **Auto-resize** : S'agrandit automatiquement en fonction de la longueur du texte.
- **Raccourcis** : Support de `Entrée` pour l'envoi et `Shift + Entrée` pour le saut de ligne.

## `ChatSidebar`
Gestion de la liste des conversations. Permet le switch rapide entre sessions et la suppression de discussions obsolètes.

## `EmptyState` & `TypingIndicator`
Composants d'état gérant l'expérience utilisateur lorsque la discussion est vide ou que l'assistant est en train de réfléchir.
