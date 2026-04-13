from collections import defaultdict
from datetime import datetime, timedelta
from typing import Any

from langchain_core.tools import tool

from backend.services.integrations.ecowatch.client import EcoWatchAPIError, EcoWatchClient
from backend.services.integrations.ecowatch.ecowatch_client_interface import EcowatchClientInterface
from backend.services.integrations.ecowatch.proxy import EcowatchProxy

proxy = True


@tool(parse_docstring=True)
def test_ecowatch_connection() -> dict:
    """Teste la connexion à l'API ECOWATCH et vérifie que la clé API est valide.
    
    Utilisez ce tool quand l'utilisateur demande :
    - Si l'API ECOWATCH est accessible
    - Si la connexion fonctionne
    - Si la clé API est valide
    - De vérifier l'état du service ECOWATCH
    
    Returns:
        Un dictionnaire normalisé:
        - success: bool
        - source: "ECOWATCH API"
        - en succès: status, message, data={status, message}
        - en erreur: error
    """
    try:
        client : EcowatchClientInterface = EcowatchProxy() if proxy else EcoWatchClient()
        result = client.test_connection()
        
        return {
            "success": True,
            "status": result.get("status"),
            "message": result.get("message"),
            "data": {
                "status": result.get("status"),
                "message": result.get("message"),
            },
            "source": "ECOWATCH API"
        }
    
    except EcoWatchAPIError as e:
        return {
            "success": False,
            "error": f"Erreur ECOWATCH API: {str(e)}",
            "source": "ECOWATCH API"
        }
    except ValueError as e:
        return {
            "success": False,
            "error": f"Configuration manquante: {str(e)}. Vérifiez la variable ECOWATCH_API_KEY dans .env",
            "source": "ECOWATCH API"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Erreur inattendue: {str(e)}",
            "source": "ECOWATCH API"
        }


@tool(parse_docstring=True)
def get_latest_sensor_data(device_id: str, sensor_type: str = "climatrack") -> dict:
    """Récupère les dernières données d'un capteur ECOWATCH en temps réel.
    
    Utilisez ce tool quand l'utilisateur demande :
    - Les dernières mesures d'un capteur spécifique
    - Les données actuelles de qualité de l'air (climatrack)
    - Les données agricoles actuelles (aquacheck: humidité du sol, température)
    - L'état actuel d'un device ECOWATCH
    
    Args:
        device_id: L'ID boitier (date de naissance du boitier), identifiant unique et clé secondaire pour récupérer les données (exemple "20240313101500").
            Différent de l'ID classique (clé primaire auto-incrémentée en base).
        sensor_type: Type de capteur - "climatrack" pour qualité de l'air ou "aquacheck" pour agriculture. Par défaut "climatrack"

    Returns:
        Un dictionnaire enveloppe avec les clés:
        - success, device_id, sensor_type, source
        - data: dernière mesure brute renvoyée par l'API ECOWATCH

        Structure de `data` selon le type de capteur:
        - Pour climatrack: id, ID_boitier, timestamp, humidity, temperature,
          tvoc, co2, pm1_0, pm2_5, pm10, sound_level
        - Pour aquacheck: id, ID_boitier, timestamp, humidity, temperature,
          ground_humidity, humidex
    """
    try:
        client :EcowatchClientInterface = EcowatchProxy() if proxy else EcoWatchClient()
        data = client.get_latest_data(table=sensor_type, device_id=device_id)
        
        return {
            "success": True,
            "device_id": device_id,
            "sensor_type": sensor_type,
            "data": data,
            "source": "ECOWATCH API"
        }
    
    except EcoWatchAPIError as e:
        return {
            "success": False,
            "error": f"Erreur ECOWATCH API: {str(e)}",
            "device_id": device_id,
            "sensor_type": sensor_type,
            "source": "ECOWATCH API"
        }
    except ValueError as e:
        return {
            "success": False,
            "error": f"Configuration manquante: {str(e)}. Vérifiez la variable ECOWATCH_API_KEY dans .env",
            "device_id": device_id,
            "sensor_type": sensor_type,
            "source": "ECOWATCH API"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Erreur inattendue: {str(e)}",
            "device_id": device_id,
            "sensor_type": sensor_type,
            "source": "ECOWATCH API"
        }


@tool(parse_docstring=True)
def list_ecowatch_devices(sensor_type: str = "climatrack") -> dict:
    """Liste tous les capteurs ECOWATCH disponibles pour un type donné.
    
    Utilisez ce tool quand l'utilisateur demande :
    - La liste des capteurs disponibles
    - Quels devices sont accessibles
    - Les IDs des capteurs climatrack ou aquacheck
    - Combien de capteurs sont déployés
    
    Args:
        sensor_type: Type de capteur - "climatrack" pour qualité de l'air ou "aquacheck" pour agriculture. Par défaut "climatrack"
    
    Returns:
        Un dictionnaire normalisé:
        - success: bool
        - source: "ECOWATCH API"
        - en succès: sensor_type, device_count, devices, data={device_count, devices}
        - en erreur: error
    """
    try:
        client :EcowatchClientInterface = EcowatchProxy() if proxy else EcoWatchClient()
        devices = client.get_devices(table=sensor_type)
        
        return {
            "success": True,
            "sensor_type": sensor_type,
            "device_count": len(devices),
            "devices": devices,
            "data": {
                "device_count": len(devices),
                "devices": devices,
            },
            "source": "ECOWATCH API"
        }
    
    except EcoWatchAPIError as e:
        return {
            "success": False,
            "error": f"Erreur ECOWATCH API: {str(e)}",
            "sensor_type": sensor_type,
            "source": "ECOWATCH API"
        }
    except ValueError as e:
        return {
            "success": False,
            "error": f"Configuration manquante: {str(e)}. Vérifiez la variable ECOWATCH_API_KEY dans .env",
            "sensor_type": sensor_type,
            "source": "ECOWATCH API"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Erreur inattendue: {str(e)}",
            "sensor_type": sensor_type,
            "source": "ECOWATCH API"
        }


@tool(parse_docstring=True)
def get_sensor_history(device_id: str, start_date: str, end_date: str, sensor_type: str = "climatrack") -> dict:
    """Récupère l'historique des mesures d'un capteur sur une période donnée.
    
    Utilisez ce tool quand l'utilisateur demande :
    - L'évolution des mesures sur une période
    - Les données historiques d'un capteur
    - Les tendances de température, CO2, pollution sur plusieurs jours
    - Une comparaison entre différentes dates
    
    Args:
        device_id: L'ID boitier (date de naissance du boitier), identifiant unique et clé secondaire pour récupérer les données (exemple "20240313101500").
            Différent de l'ID classique (clé primaire auto-incrémentée en base).
        start_date: Date de début au format YYYY-MM-DD (exemple "2025-06-16")
        end_date: Date de fin au format YYYY-MM-DD (exemple "2025-06-17")
        sensor_type: Type de capteur - "climatrack" pour qualité de l'air ou "aquacheck" pour agriculture. Par défaut "climatrack"
    
    Returns:
        Un dictionnaire normalisé:
        - success: bool
        - source: "ECOWATCH API"
        - en succès: device_id, sensor_type, period, record_count,
          truncated, max_records, data (liste des mesures)
        - en erreur: error
    """
    max_records = 300

    try:
        client :EcowatchClientInterface = EcowatchProxy() if proxy else EcoWatchClient()
        data = client.get_filtered_data(
            table=sensor_type,
            device_id=device_id,
            start_date=start_date,
            end_date=end_date
        )

        original_count = len(data)
        if original_count > max_records:
            data = data[-max_records:]
        
        return {
            "success": True,
            "device_id": device_id,
            "sensor_type": sensor_type,
            "period": f"{start_date} to {end_date}",
            "record_count": len(data),
            "truncated": original_count > max_records,
            "max_records": max_records,
            "data": data,
            "source": "ECOWATCH API"
        }
    
    except EcoWatchAPIError as e:
        return {
            "success": False,
            "error": f"Erreur ECOWATCH API: {str(e)}",
            "device_id": device_id,
            "sensor_type": sensor_type,
            "period": f"{start_date} to {end_date}",
            "source": "ECOWATCH API"
        }
    except ValueError as e:
        return {
            "success": False,
            "error": f"Configuration manquante: {str(e)}. Vérifiez la variable ECOWATCH_API_KEY dans .env",
            "device_id": device_id,
            "sensor_type": sensor_type,
            "period": f"{start_date} to {end_date}",
            "source": "ECOWATCH API"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Erreur inattendue: {str(e)}",
            "device_id": device_id,
            "sensor_type": sensor_type,
            "period": f"{start_date} to {end_date}",
            "source": "ECOWATCH API"
        }


def _to_datetime(value: str):
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None


def _aggregate_records(records: list[dict[Any, Any]], value_key: str, aggregation: str) -> list[dict]:
    if aggregation == "raw":
        points = []
        for record in records:
            ts = record.get("timestamp")
            value = record.get(value_key)
            if ts is None or value is None:
                continue
            try:
                numeric_value = float(value)
            except (TypeError, ValueError):
                continue
            points.append({"timestamp": ts, value_key: round(numeric_value, 3)})
        return points

    buckets: dict[str, list[float]] = defaultdict(list)
    for record in records:
        tstamp : str | None = record.get("timestamp")
        assert tstamp is not None
        dt = _to_datetime(tstamp)
        value = record.get(value_key)
        if dt is None or value is None:
            continue
        try:
            numeric_value = float(value)
        except (TypeError, ValueError):
            continue

        if aggregation == "day":
            bucket_key = dt.strftime("%Y-%m-%d")
        else:
            bucket_key = dt.strftime("%Y-%m-%dT%H:00:00Z")
        buckets[bucket_key].append(numeric_value)

    points = []
    for bucket_key in sorted(buckets.keys()):
        values = buckets[bucket_key]
        if not values:
            continue
        avg_value = sum(values) / len(values)
        points.append({"timestamp": bucket_key, value_key: round(avg_value, 3)})
    return points


@tool(parse_docstring=True)
def generate_sensor_chart(
    device_id: str,
    value_key: str,
    start_date: str,
    end_date: str,
    sensor_type: str = "climatrack",
    aggregation: str = "hour",
) -> dict:
    """Génère une spécification de graphique compacte (chart_spec) pour affichage en dessous de votre réponse.

    Utilisez ce tool en PRIORITE quand l'utilisateur demande :
    - Un graphique ou une courbe d'évolution d'un capteur
    - Une visualisation temporelle (jour/heure) d'une mesure
    - Un graphique pour température, humidité, co2, pm2_5, etc.
    - Des formulations comme: "tracer", "plot", "courbe", "visualiser", "dashboard"

        Règles d'or d'utilisation :
        - Si la demande contient un besoin de graphique ET un device_id ET une période,
            appelez obligatoirement ce tool avant toute réponse analytique.
        - Ne répondez pas avec une "simulation", un "exemple de rendu" ou un graphique ASCII
            si les paramètres nécessaires sont présents: utilisez ce tool.
        - Après appel de ce tool, la réponse finale ne doit pas contenir de graphe textuel,
            de bloc ASCII, d'image markdown, ni de lien quickchart.
        - Faire un seul appel par demande utilisateur, sauf si l'utilisateur demande explicitement
            plusieurs graphiques/mesures.
        - Si la demande est générique (ex: "visualiser les mesures"), générer UN seul graphique
            principal (temperature par défaut pour climatrack, ground_humidity pour aquacheck),
            puis proposer d'afficher les autres mesures dans un second temps.
        - Si des paramètres essentiels manquent (device_id, période), demander une clarification
            au lieu d'appeler ce tool avec des hypothèses.
        - Le rendu frontend est actuellement en `line`.

    Args:
        device_id: L'ID boitier (date de naissance du boitier), identifiant unique de collecte (exemple "20240313101500").
        value_key: Champ mesuré à tracer. Pour climatrack: "temperature", "humidity", "co2", "pm1_0", "pm2_5", "pm10", "tvoc", "sound_level". Pour aquacheck: "temperature", "humidity", "ground_humidity", "humidex".
        start_date: Date de début au format YYYY-MM-DD.
        end_date: Date de fin au format YYYY-MM-DD.
        sensor_type: Type de capteur - "climatrack" ou "aquacheck". Par défaut "climatrack".
        aggregation: Agrégation temporelle - "raw", "hour", "day". Par défaut "hour".

    Returns:
        Un dictionnaire normalisé:
        - success: bool
        - source: "ECOWATCH API"
        - en succès: summary, payload={type:"chart", chart:chart_spec},
          data={type:"chart", chart:chart_spec}
        - en erreur: error
    """
    allowed_agg = {"raw", "hour", "day"}
    allowed_sensor_value_keys = {
        "climatrack": {
            "temperature",
            "humidity",
            "co2",
            "pm2_5",
            "pm10",
            "pm1_0",
            "tvoc",
            "sound_level",
        },
        "aquacheck": {
            "temperature",
            "humidity",
            "ground_humidity",
            "humidex",
        },
    }
    max_points = 240
    max_days = 31
    chart_type = "line"

    normalized_sensor_type = sensor_type.strip().lower()
    raw_value_key = value_key.strip().lower()
    normalized_value_key = raw_value_key

    if normalized_sensor_type not in allowed_sensor_value_keys:
        return {
            "success": False,
            "error": f"sensor_type invalide: {sensor_type}. Valeurs autorisées: climatrack, aquacheck",
            "device_id": device_id,
            "sensor_type": sensor_type,
            "source": "ECOWATCH API",
        }

    if normalized_value_key not in allowed_sensor_value_keys[normalized_sensor_type]:
        allowed_keys = ", ".join(sorted(allowed_sensor_value_keys[normalized_sensor_type]))
        return {
            "success": False,
            "error": (
                f"value_key invalide pour {normalized_sensor_type}: {value_key}. "
                f"Valeurs autorisées: {allowed_keys}"
            ),
            "device_id": device_id,
            "sensor_type": normalized_sensor_type,
            "value_key": value_key,
            "source": "ECOWATCH API",
        }

    if aggregation not in allowed_agg:
        return {
            "success": False,
            "error": f"aggregation invalide: {aggregation}. Valeurs autorisées: raw, hour, day",
            "device_id": device_id,
            "sensor_type": normalized_sensor_type,
            "source": "ECOWATCH API",
        }

    try:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError as e:
        return {
            "success": False,
            "error": f"Format de date invalide. Utilisez YYYY-MM-DD: {str(e)}",
            "device_id": device_id,
            "sensor_type": normalized_sensor_type,
            "source": "ECOWATCH API",
        }

    if end_dt < start_dt:
        return {
            "success": False,
            "error": "La date de fin doit être supérieure ou égale à la date de début",
            "device_id": device_id,
            "sensor_type": normalized_sensor_type,
            "source": "ECOWATCH API",
        }

    if (end_dt - start_dt) > timedelta(days=max_days):
        return {
            "success": False,
            "error": f"Période trop longue. Maximum autorisé: {max_days} jours",
            "device_id": device_id,
            "sensor_type": normalized_sensor_type,
            "source": "ECOWATCH API",
        }

    try:
        client :EcowatchClientInterface = EcowatchProxy() if proxy else EcoWatchClient()
        records = client.get_filtered_data(
            table=normalized_sensor_type,
            device_id=device_id,
            start_date=start_date,
            end_date=end_date,
        )

        points = _aggregate_records(records, value_key=normalized_value_key, aggregation=aggregation)
        points = points[-max_points:]

        chart_spec = {
            "kind": "chart_spec",
            "chart_type": chart_type,
            "title": f"{normalized_value_key} - {device_id}",
            "x_key": "timestamp",
            "y_keys": [normalized_value_key],
            "points": points,
            "metadata": {
                "sensor_type": normalized_sensor_type,
                "device_id": device_id,
                "aggregation": aggregation,
                "record_count": len(points),
                "source": "ECOWATCH API",
            },
        }

        message = (
            f"Graphique généré pour {normalized_value_key} du {start_date} au {end_date} "
            f"({len(points)} points, agrégation={aggregation})."
        )

        return {
            "success": True,
            "payload": {
                "type": "chart",
                "chart": chart_spec,
            },
            "data": {
                "type": "chart",
                "chart": chart_spec,
            },
            "summary": message,
            "source": "ECOWATCH API",
        }

    except EcoWatchAPIError as e:
        return {
            "success": False,
            "error": f"Erreur ECOWATCH API: {str(e)}",
            "device_id": device_id,
            "sensor_type": normalized_sensor_type,
            "source": "ECOWATCH API",
        }
    except ValueError as e:
        return {
            "success": False,
            "error": f"Configuration manquante: {str(e)}. Vérifiez la variable ECOWATCH_API_KEY dans .env",
            "device_id": device_id,
            "sensor_type": normalized_sensor_type,
            "source": "ECOWATCH API",
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Erreur inattendue: {str(e)}",
            "device_id": device_id,
            "sensor_type": normalized_sensor_type,
            "source": "ECOWATCH API",
        }
