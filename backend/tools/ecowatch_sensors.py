from langchain_core.tools import tool

from backend.services.integrations.ecowatch.client import (EcoWatchAPIError,
                                                           EcoWatchClient)


@tool(parse_docstring=True)
def test_ecowatch_connection() -> dict:
    """Teste la connexion à l'API ECOWATCH et vérifie que la clé API est valide.
    
    Utilisez ce tool quand l'utilisateur demande :
    - Si l'API ECOWATCH est accessible
    - Si la connexion fonctionne
    - Si la clé API est valide
    - De vérifier l'état du service ECOWATCH
    
    Returns:
        Un dictionnaire contenant le statut de la connexion et un message
    """
    try:
        client = EcoWatchClient()
        result = client.test_connection()
        
        return {
            "success": True,
            "status": result.get("status"),
            "message": result.get("message"),
            "source": "ECOWATCH API"
        }
    
    except EcoWatchAPIError as e:
        return {
            "success": False,
            "error": f"Erreur ECOWATCH API: {str(e)}"
        }
    except ValueError as e:
        return {
            "success": False,
            "error": f"Configuration manquante: {str(e)}. Vérifiez la variable ECOWATCH_API_KEY dans .env"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Erreur inattendue: {str(e)}"
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
        Un dictionnaire contenant les dernières mesures du capteur avec des clés variées selon le type:
        - Pour climatrack: temperature, humidity, co2, pm25, pm10, voc, formaldehyde, timestamp
        - Pour aquacheck: temperature, humidity, ground_humidity, humidex, timestamp
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
            "sensor_type": sensor_type
        }
    except ValueError as e:
        return {
            "success": False,
            "error": f"Configuration manquante: {str(e)}. Vérifiez la variable ECOWATCH_API_KEY dans .env",
            "device_id": device_id,
            "sensor_type": sensor_type
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Erreur inattendue: {str(e)}",
            "device_id": device_id,
            "sensor_type": sensor_type
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
        Un dictionnaire contenant la liste des IDs boitier (date de naissance) et le nombre total
    """
    try:
        client = EcoWatchClient()
        devices = client.get_devices(table=sensor_type)
        
        return {
            "success": True,
            "sensor_type": sensor_type,
            "device_count": len(devices),
            "devices": devices,
            "source": "ECOWATCH API"
        }
    
    except EcoWatchAPIError as e:
        return {
            "success": False,
            "error": f"Erreur ECOWATCH API: {str(e)}",
            "sensor_type": sensor_type
        }
    except ValueError as e:
        return {
            "success": False,
            "error": f"Configuration manquante: {str(e)}. Vérifiez la variable ECOWATCH_API_KEY dans .env",
            "sensor_type": sensor_type
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Erreur inattendue: {str(e)}",
            "sensor_type": sensor_type
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
        Un dictionnaire contenant la liste des mesures dans la période spécifiée
    """
    try:
        client = EcoWatchClient()
        data = client.get_filtered_data(
            table=sensor_type,
            device_id=device_id,
            start_date=start_date,
            end_date=end_date
        )
        
        return {
            "success": True,
            "device_id": device_id,
            "sensor_type": sensor_type,
            "period": f"{start_date} to {end_date}",
            "record_count": len(data),
            "data": data,
            "source": "ECOWATCH API"
        }
    
    except EcoWatchAPIError as e:
        return {
            "success": False,
            "error": f"Erreur ECOWATCH API: {str(e)}",
            "device_id": device_id,
            "sensor_type": sensor_type,
            "period": f"{start_date} to {end_date}"
        }
    except ValueError as e:
        return {
            "success": False,
            "error": f"Configuration manquante: {str(e)}. Vérifiez la variable ECOWATCH_API_KEY dans .env",
            "device_id": device_id,
            "sensor_type": sensor_type,
            "period": f"{start_date} to {end_date}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Erreur inattendue: {str(e)}",
            "device_id": device_id,
            "sensor_type": sensor_type,
            "period": f"{start_date} to {end_date}"
        }


@tool(parse_docstring=True)
def get_all_sensor_data(device_id: str, sensor_type: str = "climatrack") -> dict:
    """Récupère TOUTES les données historiques complètes d'un capteur ECOWATCH.
    
    Utilisez ce tool quand l'utilisateur demande :
    - Toutes les mesures historiques d'un capteur
    - L'ensemble des données d'un device sans filtre de date
    - L'historique complet depuis le début
    - Une analyse sur toute la période de fonctionnement
    
    ATTENTION: Peut retourner un grand volume de données. Pour des périodes spécifiques, utilisez plutôt get_sensor_history.
    
    Args:
        device_id: L'ID boitier (date de naissance du boitier), identifiant unique et clé secondaire pour récupérer les données (exemple "20240313101500").
            Différent de l'ID classique (clé primaire auto-incrémentée en base).
        sensor_type: Type de capteur - "climatrack" pour qualité de l'air ou "aquacheck" pour agriculture. Par défaut "climatrack"
    
    Returns:
        Un dictionnaire contenant toutes les mesures historiques du capteur
    """
    try:
        client = EcoWatchClient()
        data = client.get_device_data(table=sensor_type, device_id=device_id)
        
        # Extraire des infos utiles sur la période couverte
        timestamps = [record.get("timestamp") for record in data if record.get("timestamp")]
        period_info = {}
        if timestamps:
            period_info = {
                "first_record": min(timestamps),
                "last_record": max(timestamps)
            }
        
        return {
            "success": True,
            "device_id": device_id,
            "sensor_type": sensor_type,
            "record_count": len(data),
            "period": period_info,
            "data": data,
            "source": "ECOWATCH API"
        }
    
    except EcoWatchAPIError as e:
        return {
            "success": False,
            "error": f"Erreur ECOWATCH API: {str(e)}",
            "device_id": device_id,
            "sensor_type": sensor_type
        }
    except ValueError as e:
        return {
            "success": False,
            "error": f"Configuration manquante: {str(e)}. Vérifiez la variable ECOWATCH_API_KEY dans .env",
            "device_id": device_id,
            "sensor_type": sensor_type
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Erreur inattendue: {str(e)}",
            "device_id": device_id,
            "sensor_type": sensor_type
        }
