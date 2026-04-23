# Guide Utilisateur : Échangez avec Jarvis 🤖

Bienvenue dans l'interface de Jarvis ! Plus qu'un simple chatbot, Jarvis est un **agent intelligent** capable d'agir sur votre environnement et d'analyser vos données en temps réel.

## 🌟 Ce que Jarvis peut faire pour vous

Jarvis est spécialisé dans la supervision environnementale via la plateforme **Ecowatch**. Voici ses super-pouvoirs :

### 📊 Visualisation de données
Jarvis ne se contente pas de parler, il agit. Demandez-lui une courbe ou un historique, et il générera instantanément un graphique interactif directement dans le chat.

### 🌡️ Monitoring en temps réel
Connecté aux capteurs Climatrack (Air) et Aquacheck (Agriculture), il vous donne l'état précis de vos installations à l'instant T.

### 🧠 Raisonnement intelligent & Chaînage d'outils
Jarvis ne se contente pas d'exécuter une commande. Il est capable de **chaîner plusieurs réflexions** pour répondre à une demande complexe.

*Exemple de ce qui se passe "sous le capot" :*
- **Vous** : "Donne-moi la température du premier boitier Climatrack de la liste."
- **Jarvis** : 
    1. 🔍 Appelle `list_ecowatch_devices` pour découvrir vos installations.
    2. 🎯 Identifie l'ID du premier boitier dans la liste reçue.
    3. 🌡️ Appelle `get_latest_sensor_data` pour ce boitier spécifique.
    4. ✍️ Vous synthétise le résultat final de manière élégante.

---

## 💬 Exemples de questions (Prompts vérifiés)

=== "🌿 Air & Environnement"
    > "Jarvis, fais la liste de mes capteurs Climatrack."
    
    > "Donne-moi la température du premier boitier de la liste." (Démonstration du chaînage d'outils).
    
    > "Fais-moi un graphique du CO2 pour le boitier 20240313101500 sur les 3 derniers jours."

=== "🚜 Agriculture (Aquacheck)"
    > "Quels sont les boitiers Aquacheck actuellement actifs ?"
    
    > "Affiche-moi l'humidité du sol actuelle pour mon installation agricole."
    
    > "Trace une courbe de la température du sol (boitier 20250314140500)."

=== "🛠️ Utilitaires"
    > "Quelle heure est-il ?" (L'agent consultera l'heure du serveur pour calculer vos périodes relatives).
    
    > "Teste la connexion avec l'API Ecowatch."
    
    > "Peux-tu simuler les données environnementales pour la ville de Montpellier ?"

---

## 🛠️ Comprendre l'interface

Pendant que Jarvis travaille, vous verrez apparaître des **indicateurs d'outils** (Tool Calls) :

- ⏳ **En cours** : Jarvis est en train d'interroger une base de données ou une API.
- ✅ **Succès** : Les données ont été récupérées. Vous pouvez cliquer sur le badge pour voir le détail technique (entrée/sortie).
- ❌ **Erreur** : Un problème est survenu (ex: boitier introuvable). Jarvis vous expliquera pourquoi.

!!! tip "Conseil d'expert"
    Jarvis est proactif ! Si votre demande est imprécise, il vous proposera des suggestions pertinentes pour vous guider. N'hésitez pas à lui demander conseil sur l'interprétation des données de vos capteurs.

---

## 💡 Conseils pour une expérience optimale

### 📅 Maîtrise du temps
Jarvis dispose d'une **intelligence temporelle**. Si vous lui demandez "le mois dernier" ou "hier", il consultera d'abord l'heure du serveur pour calculer les dates exactes avant d'interroger vos capteurs. Vous n'avez pas besoin de retenir les dates !

### ⏳ Gestion du débit (Rate Limit)
Si vous utilisez le plan gratuit de Mistral AI, vous pourriez occasionnellement voir un message d'erreur indiquant que Jarvis est "surmené" (Rate Limit). 
- **Astuce** : Attendez 2 ou 3 secondes entre chaque question complexe pour laisser l'agent reprendre son souffle.

### 🎯 Précision des demandes
Jarvis est proactif. Si vous lui dites simplement "Aide-moi à surveiller mon champ", il ne se contentera pas d'une réponse vide : il vous proposera de lister vos boitiers Aquacheck ou de vérifier l'humidité du sol pour vous guider.
