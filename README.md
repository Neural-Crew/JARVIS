# J4RVIS 360
<img width="800" height="450" alt="ezgif com-video-to-gif-converter" src="https://github.com/user-attachments/assets/0bc02459-6bd7-4ad7-97b8-7f342913d357" />
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
Lancer le backend :
```bash
uvicorn backend.main:app --reload
```

Lancer le frontend (Vite) :
```bash
cd frontend
npm install
npm run dev
```

## CI
La CI (GitHub Actions) execute les tests backend et frontend sur Ubuntu.

Ce qui est verifie :
- Backend: demarrage `uvicorn` + health check sur `/`, puis `poetry run pytest`
- Frontend: demarrage `npm run dev` + ping HTTP, puis `npm run lint`, `npm run test`, `npm run build`

Note: les tests qui necessitent `MISTRAL_API_KEY` ou `ECOWATCH_API_KEY` restent en mode skip en CI.
Le endpoint `/chat` requiert `MISTRAL_API_KEY` pour fonctionner.



