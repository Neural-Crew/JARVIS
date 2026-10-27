@.claude/CLAUDE-commun.md

# CLAUDE.md — JARVIS

Assistant agentique de supervision environnementale : il interroge les capteurs ecowatch (AquaCheck, ClimaTrack) et affiche mesures et graphiques dans un chat. Dépôt partagé avec : Eliot, Noah, Henrei, Titouan, Beusts, Alfonso, Damien.
Config du socle : `_dev/projet.json`. Règles communes : `.claude/CLAUDE-commun.md` (ne pas dupliquer ici).

## Stack

- Backend `backend/` : Python ≥ 3.11, FastAPI + LangGraph/LangChain, LLM Mistral (`MISTRAL_API_KEY`) ou Ollama local, client de l'API ecowatch (`ECOWATCH_API_KEY`). Poetry, `.venv` dans le dépôt (`poetry.toml`), `package-mode = false`.
- Frontend `frontend/` : React + Vite + TypeScript, shadcn/ui (`src/components/ui`), Vitest ; port 8080, API sur 8000.
- Docker : `docker-compose.yml` (backend 8000, frontend Nginx 8080, docs MkDocs 8008).
- Générés (ne pas éditer à la main) : `poetry.lock`, `package-lock.json`, `frontend/package-lock.json`, `frontend/bun.lockb`.

## Commandes

```bash
poetry install --no-interaction && npm --prefix frontend ci --no-audit --no-fund   # cf. commandes.installer
poetry run uvicorn backend.main:app --reload   # API (MISTRAL_API_KEY requise pour /chat)
npm --prefix frontend run dev                  # front, http://localhost:8080
ECOWATCH_API_KEY= MISTRAL_API_KEY= poetry run pytest backend/tests --ignore=backend/tests/models -q -p no:cacheprovider && npm --prefix frontend run test   # cf. commandes.tester
npm --prefix frontend run build                # cf. commandes.construire
```

## Gros risques du projet

En plus de `CLAUDE-commun.md` § 3 :
- ⛔ `backend/tests/integrations` avec une vraie `ECOWATCH_API_KEY` appelle l'API de prod `https://ecowatch.fr/api`.
- ⛔ `/chat` et les tests Mistral avec une vraie clé consomment l'API payante.
- ⛔ Pas de `docker compose up` sur un serveur sans GO : conteneurs `restart: unless-stopped` qui chargent le `.env` racine.

## Pièges

- Vide les clés devant `pytest` (`ECOWATCH_API_KEY= MISTRAL_API_KEY=`) : les tests appellent `load_dotenv()`, et un `.env` local les ferait sortir sur le réseau.
- Exclus `backend/tests/models` : ils exigent Mistral (clé) ou Ollama (`qwen3:14b` local), et ne font que se sauter sinon.
- `verifier-tout` voit un « secret en dur » dans `backend/tests/integrations/client_test.py` : c'est une clé factice de test, pas une fuite.
- Le dépôt garde sa propre CI `.github/workflows/ci.yml` (Python 3.11, Node 20, sur `main` seulement) ; le `socle.yml` du socle n'y est pas.
- Le `package-lock.json` racine est vide : les dépendances JS sont dans `frontend/`.
