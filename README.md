# J4RVIS 360

## Architecture du projet

```text
.
├── backend/                # Logique serveur (Python + FastAPI)
│   ├── app/
│   │   ├── agents/         # Agent(s) Langchain
│   │   ├── tools/          # Tools pour l'agent (ex : recupérer données)
│   │   ├── services/       # Services tiers ( Client Ollama, RAG si on en fait)
│   │   ├── core/           # Configuration globale et constantes
│   │   └── main.py         # fastapi
├── frontend/               # Frontend a déterminer
├── data/                   # (si jamais on a besoin de stocker des données)
└── .env                    # Variables d'environnement
```

## Gestion des dépendances
Je propose d'utiliser poetry (pour installer : https://python-poetry.org/docs/)

Pour installer les dépendances
```bash
poetry install
```
Activer l'environnement :
(si .venv existe)
```bash
# Linux / Mac
source .venv/bin/activate

# Windows (Powershell)
.venv\Scripts\activate
```
sinon
```bash
source $(poetry env info --path)/bin/activate
```
Ajouter une librairie au projet
```bash
poetry add <nom_de_la_librairie>
```