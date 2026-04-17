from collections import defaultdict
from datetime import datetime, timedelta

from langchain_core.tools import tool

from backend.services.integrations.ecowatch.client import (EcoWatchAPIError,
                                                           EcoWatchClient)


@tool(parse_docstring=True)
def test_ecowatch_connection() -> dict:
    """Teste la connexion à l'API ECOWATCH et vérifie la validité de la clé API.

    Returns:
        Dictionnaire contenant le statut de la connexion, un message et la source.
    """
    try:
        client = EcoWatchClient()
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

    Args:
        device_id: L'identifiant unique du boitier (ex: "20240313101500").
        sensor_type: Type de capteur ("climatrack" ou "aquacheck").

    Returns:
        Dictionnaire contenant les dernières mesures brutes renvoyées par l'API.
    """
    try:
        client = EcoWatchClient()
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

    Args:
        sensor_type: Type de capteur ("climatrack" ou "aquacheck").

    Returns:
        Dictionnaire contenant la liste des identifiants de boitiers disponibles.
    """
    try:
        client = EcoWatchClient()
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

    Args:
        device_id: L'identifiant unique du boitier (ex: "20240313101500").
        start_date: Date de début (format YYYY-MM-DD).
        end_date: Date de fin (format YYYY-MM-DD).
        sensor_type: Type de capteur ("climatrack" ou "aquacheck").

    Returns:
        Dictionnaire contenant la liste des mesures historiques.
    """
    max_records = 300

    try:
        client = EcoWatchClient()
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
    """Convertit une chaîne ISO en objet datetime.

    Args:
        value: La chaîne à convertir.

    Returns:
        Un objet datetime ou None en cas d'erreur.
    """
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None


def _aggregate_records(records: list[dict], value_key: str, aggregation: str) -> list[dict]:
    """Agrège les mesures d'un capteur par heure ou par jour.

    Args:
        records: Liste des mesures brutes.
        value_key: Le champ à agréger.
        aggregation: Type d'agrégation ("raw", "hour", "day").

    Returns:
        Liste des points agrégés.
    """
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
        dt = _to_datetime(record.get("timestamp"))
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
    """Génère une spécification de graphique pour visualisation temporelle.

    Args:
        device_id: L'identifiant unique du boitier (ex: "20240313101500").
        value_key: Champ mesuré à tracer (ex: "temperature", "humidity", "co2").
        start_date: Date de début (format YYYY-MM-DD).
        end_date: Date de fin (format YYYY-MM-DD).
        sensor_type: Type de capteur ("climatrack" ou "aquacheck").
        aggregation: Agrégation temporelle ("raw", "hour", "day").

    Returns:
        Dictionnaire contenant la spécification du graphique (chart_spec).
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
        client = EcoWatchClient()
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
