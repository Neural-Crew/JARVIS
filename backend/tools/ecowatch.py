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
        Un dictionnaire normalisé:
        - success: bool
        - source: nom de la source
        - en succès: city, temperature, humidity, air_quality_index,
          air_quality_level, recommendation, data={...mêmes champs métiers...}
        - en erreur: error, city
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

        temperature = f"{random.randint(10, 35)}°C"
        humidity = f"{random.randint(30, 80)}%"

        return {
            "success": True,
            "city": city,
            "temperature": temperature,
            "humidity": humidity,
            "air_quality_index": aqi,
            "air_quality_level": quality,
            "recommendation": advice,
            "data": {
                "city": city,
                "temperature": temperature,
                "humidity": humidity,
                "air_quality_index": aqi,
                "air_quality_level": quality,
                "recommendation": advice,
            },
            "source": "EcoWatch Live Sensor (Mock)"
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": f"Impossible de récupérer les données pour {city}: {str(e)}",
            "city": city,
            "source": "EcoWatch API"
        }