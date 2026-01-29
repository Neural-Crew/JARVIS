# API ECOWATCH - Endpoints Disponibles

## URL de Base
```
https://ecowatch.fr/api/b2b
```

## Authentification
```
Header: X-API-Key: VOTRE_CLE_API
```

---

## Endpoints

### 1. Test de Connexion

#### GET `/api/test-connection`
#### GET `/api/b2b/test-connection`

Vérifie que l'API est accessible et que la clé est valide.

**Exemple**:
```bash
curl -H "X-API-Key: VOTRE_CLE" "https://ecowatch.fr/api/test-connection"
```

**Réponse**:
```json
{
  "status": "ok",
  "message": "Connexion au backend réussie"
}
```

---

### 2. Liste des Devices

#### GET `/api/b2b/devices`

Récupère la liste des IDs de tous les devices disponibles pour une table donnée.

**Paramètres Query (obligatoires)**:
- `table` (string) : Nom de la table (`aquacheck` ou `climatrack`)

**Exemple**:
```bash
curl -H "X-API-Key: VOTRE_CLE" \
  "https://ecowatch.fr/api/b2b/devices?table=aquacheck"
```

**Réponse**:
```json
[
  "20250314140500",
  "20250513115530",
  "20250513120540",
  "20250513142900",
  "20250513144750",
  "..."
]
```

**Erreurs**:
- Sans paramètre `table`: `{"error":"Invalid table \"undefined\"."}`

---

### 3. Toutes les Données d'un Device

#### GET `/api/b2b/data/{table}/{device_id}`

Récupère toutes les mesures historiques d'un device spécifique.

**Paramètres Path**:
- `table` (string) : Nom de la table (`aquacheck` ou `climatrack`)
- `device_id` (string) : ID du device (ex: `20250314140500`)

**Exemple**:
```bash
curl -H "X-API-Key: VOTRE_CLE" \
  "https://ecowatch.fr/api/b2b/data/aquacheck/20250314140500"
```

**Réponse**:
```json
[
  {
    "id": 4626,
    "ID_boitier": "20250314140500",
    "timestamp": "2025-06-16T08:49:30.000Z",
    "humidity": 0.61,
    "temperature": 24.16,
    "ground_humidity": 100,
    "humidex": "29.03"
  },
  {
    "id": 4630,
    "ID_boitier": "20250314140500",
    "timestamp": "2025-06-16T08:54:45.000Z",
    "humidity": 0.61,
    "temperature": 24.07,
    "ground_humidity": 100,
    "humidex": "28.81"
  },
  "..."
]
```

**Champs de données**:

**Table `aquacheck` (capteurs agricoles)**:
- `id` (int) : Identifiant unique de la mesure
- `ID_boitier` (string) : ID du device
- `timestamp` (ISO 8601) : Date/heure de la mesure
- `humidity` (float|null) : Humidité de l'air (0-1)
- `temperature` (float|null) : Température en °C
- `ground_humidity` (int|null) : Humidité du sol (0-100)
- `humidex` (string|null) : Indice humidex

**Table `climatrack` (qualité de l'air)**:
- `id` (int) : Identifiant unique de la mesure
- `ID_boitier` (string) : ID du device
- `timestamp` (ISO 8601) : Date/heure de la mesure
- `humidity` (float|null) : Humidité de l'air (%)
- `temperature` (float|null) : Température en °C
- `tvoc` (int|null) : Composés organiques volatils totaux (ppb)
- `co2` (int|null) : Niveau de CO2 (ppm)
- `pm1_0` (int|null) : Particules fines 1.0µm (µg/m³)
- `pm2_5` (int|null) : Particules fines 2.5µm (µg/m³)
- `pm10` (int|null) : Particules fines 10µm (µg/m³)
- `sound_level` (float|null) : Niveau sonore (dB)

---

### 4. Dernière Mesure d'un Device

#### GET `/api/b2b/data/{table}/{device_id}/latest`

Récupère uniquement la dernière mesure disponible pour un device.

**Paramètres Path**:
- `table` (string) : Nom de la table (ex: `aquacheck`)
- `device_id` (string) : ID du device

**Exemple**:
```bash
curl -H "X-API-Key: VOTRE_CLE" \
  "https://ecowatch.fr/api/b2b/data/aquacheck/20250314140500/latest"
```

**Réponse**:
```json
{
  "id": 33496,
  "ID_boitier": "20250314140500",
  "timestamp": "2025-07-31T14:33:41.000Z",
  "humidity": null,
  "temperature": null,
  "ground_humidity": 17,
  "humidex": null
}
```

---

### 5. Données Filtrées par Date

#### GET `/api/b2b/data/{table}/{device_id}/filter`

Récupère les mesures d'un device pour une période donnée.

**Paramètres Path**:
- `table` (string) : Nom de la table
- `device_id` (string) : ID du device

**Paramètres Query (obligatoires)**:
- `start` (date) : Date de début au format `YYYY-MM-DD`
- `end` (date) : Date de fin au format `YYYY-MM-DD`

**Exemple**:
```bash
curl -H "X-API-Key: VOTRE_CLE" \
  "https://ecowatch.fr/api/b2b/data/aquacheck/20250314140500/filter?start=2025-06-16&end=2025-06-17"
```

**Réponse**: Array identique à l'endpoint "Toutes les Données", filtré sur la période.

**Erreurs**:
- Sans paramètres: `{"error":"start/end (ou startDateTime/endDateTime, startTime/endTime) requis."}`
- Aucune donnée trouvée: `[]`

---

## Codes d'Erreur

| Code HTTP | Signification |
|-----------|---------------|
| `200` | Succès |
| `401` | Clé API manquante |
| `403` | Clé API invalide |
| `405` | Méthode HTTP non autorisée (POST, PUT, DELETE...) |

---

## Notes Importantes

1. **Préfixe `/b2b/`** : Tous les endpoints de données utilisent le préfixe `/api/b2b/`
2. **Paramètre `table`** : Obligatoire pour `/devices`, valeurs disponibles: `aquacheck`, `climatrack`
3. **Format dates** : ISO 8601 pour les timestamps, `YYYY-MM-DD` pour les filtres
4. **Valeurs null** : Les capteurs peuvent retourner `null` si la mesure n'est pas disponible
5. **READ ONLY** : Seules les méthodes GET et HEAD sont autorisées
6. **Types de capteurs** :
   - `aquacheck` : Capteurs agricoles (humidité sol, température, humidex)
   - `climatrack` : Qualité de l'air (CO2, TVOC, particules, bruit)

---

## Quick Test

```bash
# Test connexion
curl -H "X-API-Key: VOTRE_CLE" "https://ecowatch.fr/api/test-connection"

# Liste devices
curl -H "X-API-Key: VOTRE_CLE" "https://ecowatch.fr/api/b2b/devices?table=aquacheck"

# Dernière mesure
curl -H "X-API-Key: VOTRE_CLE" "https://ecowatch.fr/api/b2b/data/aquacheck/DEVICE_ID/latest"
```
