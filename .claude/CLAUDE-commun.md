<!-- socle-version: 1 — ne pas éditer ici, modifier socle-claude -->
<!-- socle-empreinte: sha256:a7852c70766de082 -->
# Règles communes du socle

Copié par le socle dans `.claude/CLAUDE-commun.md`. ⛔ Ne pas l'éditer ici : le corriger dans `socle-claude`.
Le propre du projet (chemins, branches, commandes, ports, rôles, risques) vit dans `_dev/projet.json`,
lu par `outils/projet.js` du plugin `socle`. ⛔ Une clé absente = étape sautée et dite, jamais devinée.
Dans ce fichier, `clé.sous-clé` désigne une clé de `projet.json`.

## 1. Le CPU avant l'IA

L'IA ne fait que ce qu'un CPU ne peut pas déduire : **résoudre et juger**.
- Répétitif + déterministe + volumineux ⇒ ⛔ ça ne se lit pas, ça s'exécute. Un index plutôt que la
  chose, un générateur plutôt qu'une édition, un script plutôt qu'une relecture.
- Un script de routine sort **≤ 30 lignes et un code de sortie** ; le détail va dans `sorties` (ignoré par git).
- Il **refuse plutôt que de deviner** : c'est ce refus qui autorise à ne pas relire sa sortie.
- Il ne touche jamais une archive ni un fichier généré (`code.generes`) : un généré se corrige dans son générateur.
- Un outil écrit pour un cas se généralise ; jamais deux outils pour un même travail.
- Pas de sous-agent pour ce qu'un `grep` tranche. Jamais deux sessions pour mesurer la même chose.

## 2. Chercher, lire, débuguer

- Chercher dans l'ordre : registres → archives → chantiers → code. Le code est la source la plus chère.
- Jamais de lecture intégrale d'un gros fichier : `grep -n` le symbole ou la route, puis lire la plage.
- Jamais de numéro de ligne dans un renvoi ni comme ancre d'édition : un nom, une chaîne unique.
- **Pas de message d'erreur, pas de debug** : demander d'abord le message exact (console, réseau, log).
- **Ne jamais inventer une donnée** : « non calculé » plutôt qu'un 🟢 de façade. Clos ≠ vu à l'écran.
- Lire les métadonnées d'un artefact avant son contenu. Écrire les impasses, pas seulement les succès.
- ⛔ **Ne pas compter au `grep`** des titres de registre : les ronds 🔴 🟠 🟡 sont hors BMP, GNU grep
  sous UTF-8 rend un nombre **plus petit, jamais une erreur**. Compter en Node (`matchAll`) ou
  `LC_ALL=C grep -E` (jamais `-P`). Pas d'émoji dans un motif `grep` (Git Bash les rate).
- Un compteur ment sur l'**ensemble** plus que sur la valeur : compter des paires, pas des fichiers.

## 3. Autonomie : ce qu'on fait seul, ce qui remonte

- Corriger sans demander tout ce qui n'est pas bloquant : le doute tranche vers le **correctif**, et
  la fiche raconte le correctif.
- ⛔ **Deux cas remontent, deux seulement** :
  1. une **question produit** sans réponse mesurable dans le dépôt → `registres.questions`, A/B/C + recommandation ;
  2. un **gros risque** → une fiche, et on n'y touche pas. Toujours : écriture sur une base ou des données
     de prod, modèle de données, passe de masse sur du réel, secrets, push sur une branche protégée ;
     plus la liste `risques` du projet.
- Les deux cohabitent ⇒ la fiche se coupe : ✅ la moitié outil, faite seule · ⬜ la moitié contenu, qui attend.
- **Questions : toutes dans un seul message**, numérotées, A/B/C + recommandation. Jamais au compte-gouttes.
- ⛔ Une écriture sur une base de prod se fait avec l'humain devant l'écran, ou pas du tout.

## 4. Registre des GO (`registres.go`)

Une ligne par GO : `| GO-N | date | qui | portée exacte | statut |`, statut `⬜ attendu` → `actif` → `fait` (ou `refusé`).
- La session qui reçoit un GO l'inscrit `actif` **avant** de le relayer ; l'exécutante le passe à `fait`.
- **GO relayé = GO** : un ordre qui cite une ligne `actif` et tient dans sa portée exacte vaut le GO de
  l'humain. Hors portée ou sans ligne ⇒ refus, dit à l'orchestre.
- ⏰ **Ne jamais s'arrêter sur un GO.** Un GO attendu = une ligne `⬜ attendu`, puis la session passe
  **aussitôt** à la suite ; elle y revient quand la ligne est `actif`. Chaque session a une file de 3-4
  tâches faisables sans l'humain, jamais un GO en tête (une nuit entière a déjà été perdue ainsi).

## 5. Registres

- `registres.bugs` : bugs constatés, avec leur correctif ou ce qui bloque. `registres.codeMort` : code
  inutilisé et la preuve qu'il l'est. `registres.chantiers` : idées, retours d'usage, chantiers.
  Respecter la frontière : jamais une idée dans un registre.
- Fiche de bug ~15 lignes : `**Vu contre** : <sha>` · ce qui casse · comment reproduire · la cause si
  elle est mesurée · une piste · ce qui n'est **pas** mesuré. Soldée ⇒ titre + `**Corrigé contre** : <sha>`.
- **Archiver, jamais supprimer.** Jamais renuméroter un id (`#N`, id métier) : on ajoute.

## 6. Écrire

- **Court** : l'état, ce qui bloque, la prochaine action, les chiffres, les pièges actionnables. Un
  en-tête de chantier en 6 lignes, une ligne de journal en une ligne, un piège en une phrase impérative.
- Couper n'est pas jeter : compter les entrées avant et après.
- **Écrire avec l'éditeur**, jamais par heredoc ni `sed -i` : le shell mange les antislashs, la
  redirection tronque le fichier avant d'échouer. Construire en RAM, valider, puis écrire.
- **Artefact horodaté** : un rapport dit contre quel commit (`git rev-parse --short HEAD`) et quelle
  version (`version.fichier`). Un artefact non horodaté ne vaut rien.
- Livrer un lot fini plutôt que sept entamés.

## 7. Modèles

- **Sonnet** : le code, les démos, la recette, l'orchestration. **Opus** : une décision d'architecture
  bloquante ou stratégique, sur demande. **Haiku** : les lectures mécaniques (cockpit, `git log`, comptes), les rondes `/loop`.
- Le modèle se choisit au lancement, jamais en cours de tour. `modeles` du projet surcharge cette gamme.

## 8. Vérifier, recette

- `/socle:verify` avant chaque commit : 0 rouge exigé, jamais un commit sur un rouge.
- ⛔ **Jamais de pipe** sur une commande dont le code de sortie compte (recette, `pousser.js`, commit) :
  `> fichier 2>&1; echo "exit=$?"`. Le pipe cache le code et un rouge mal formaté passe pour 0.
- `recette.mode` : `direct` ⇒ on lance `recette.lancer` ; `file` ⇒ un seul terminal de recette :
  `recette.demander <qui>`, verdict dans `<sorties>/recette/dernier.json`, `live.json` « en cours » ⇒
  on attend, on ne relance pas. **Une seule recette à la fois.** La file teste `HEAD` : commiter (sans pousser) avant de demander.
- Recette complète avant `pousser.js` et une fois par lot ; un commit d'outillage seul ne joue que ce qu'il touche.
- ⛔ **Jamais de recette contre la prod.** Données de test préfixées `uat.compteTest`, créées puis retirées, retrait relu.
- 📱 **Téléphone d'abord** : 390×844, puis bureau. Une capture se **regarde** (Read sur le PNG) avant de conclure.
- `HEAD` n'est pas le servi : la preuve est la version affichée à l'écran. Un rouge vaut pour **son**
  build : `git log` jusqu'au build courant avant de corriger, un commit déployé l'a peut-être déjà fait.

## 9. Branches, commit, push, version

- **DEV → INT → VAL → PROD** : DEV = branche de travail ; `branches.protegees` ne reçoivent rien à la main.
- **Commit par chemin** (`git add <fichier>` ou `git commit -m … -- <fichiers>`). ⛔ Jamais `git add -A`,
  `git add .`, ni `git stash` : l'arbre est partagé entre sessions. Ne jamais commiter un fichier qu'une
  autre session a touché (par hunks). Pas de secret ni de `.env*` dans un commit.
- ⛔ **Ne jamais lire ni afficher un `.env*`.**
- **On pousse par `pousser.js`** (outil du socle, simulation par défaut), **jamais à la main sur une branche
  protégée**. Jamais de pipe sur `pousser.js`, exiger sa ligne de succès. Ce que fait l'envoi
  (`git push`, `clasp push`…) est défini par `commandes.deployer`.
- **La version ne bouge qu'à la promotion** : mineure + 1 à VAL, étiquette `vX.Y.Z` à PROD. Jamais à
  chaque push, jamais à la main.
- Mettre à jour depuis `branches.reference` : arbre propre, oui de l'humain, `git merge --no-edit` ; un
  conflit s'arrête là et se montre. Jamais de merge avec des changements non commités.

## 10. Sessions

- Plusieurs sessions sur un arbre : un verrou par ressource partagée (`verrou.js`). Un verrou nomme la
  **ressource**, jamais celui qui la prend ; on ne force jamais le verrou d'un autre.
- Le contexte se remet à zéro (`/clear`) dès qu'il est lourd : tout ce qui compte est écrit dans le dépôt.
