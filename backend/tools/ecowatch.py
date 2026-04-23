"""Outils de simulation environnementale (Mock).

Fournit des données fictives pour les tests et démonstrations lorsque
l'accès aux capteurs réels n'est pas possible.
"""

import random

from langchain_core.tools import tool


@tool(parse_docstring=True)
def get_environmental_data(city: str) -> dict:
    """Récupère les données environnementales simulées pour une ville donnée.

    Args:
        city: Nom de la ville à interroger (ex: "Paris", "Londres").

    Returns:
        Dictionnaire contenant la température, l'humidité et l'indice de qualité de l'air.
    """
    try:
        # Simulation d'appel API (Mock)
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