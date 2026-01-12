import random

from langchain_core.tools import tool


@tool(parse_docstring=True)
def get_environmental_data(city: str) -> dict:
    """Récupère les données environnementales en temps réel pour une ville.
    
    Utilisez ce tool quand l'utilisateur demande des informations sur :
    - La qualité de l'air d'une ville
    - Les conditions météorologiques actuelles
    - L'indice de pollution ou l'IQA (Indice Qualité de l'Air)
    - Des recommandations basées sur la qualité de l'air
    
    Args:
        city: Le nom de la ville pour laquelle récupérer les données environnementales. Exemples: "Paris", "Lyon", "Marseille", "New York"
    
    Returns:
        Un dictionnaire contenant les données environnementales avec les clés :
        - city: nom de la ville
        - temperature: température actuelle
        - humidity: taux d'humidité
        - air_quality_index: indice de qualité de l'air (0-500)
        - air_quality_level: niveau qualitatif (Excellente/Moyenne/Mauvaise)
        - recommendation: conseil basé sur la qualité de l'air
        - source: source des données
    """
    try:
        # Simulation d'appel API (Mock)
        # Dans la version finale, remplacez ceci par requests.get("https://api.ecowatch.com/...")
        
        # Génération de données aléatoires cohérentes pour la démo
        aqi = random.randint(20, 180)
    
        if aqi <= 50:
            quality = "Excellente"
            advice = "Profitez de l'air frais !"
        elif aqi <= 100:
            quality = "Moyenne"
            advice = "L'air est correct pour la plupart des gens."
        else:
            quality = "Mauvaise"
            advice = "Évitez les activités sportives en extérieur."

        return {
            "city": city,
            "temperature": f"{random.randint(10, 35)}°C",
            "humidity": f"{random.randint(30, 80)}%",
            "air_quality_index": aqi,
            "air_quality_level": quality,
            "recommendation": advice,
            "source": "EcoWatch Live Sensor (Mock)"
        }
    
    except Exception as e:
        return {
            "error": f"Impossible de récupérer les données pour {city}: {str(e)}",
            "city": city,
            "source": "EcoWatch API"
        }