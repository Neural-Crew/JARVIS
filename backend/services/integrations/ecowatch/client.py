"""
ECOWATCH API Client
Client Python pour interagir avec l'API B2B ECOWATCH.
"""

import os
from datetime import datetime
from typing import Any, Dict, List, Optional

import requests
from dotenv import load_dotenv

load_dotenv()


class EcoWatchAPIError(Exception):
    """Exception levée pour les erreurs de l'API ECOWATCH."""
    pass


class EcoWatchClient:
    """
    Client pour l'API ECOWATCH.
    
    Permet de récupérer les données des capteurs agricoles (aquacheck)
    et de qualité de l'air (climatrack).
    """
    
    BASE_URL = "https://ecowatch.fr/api"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialise le client ECOWATCH.
        
        Args:
            api_key: Clé API ECOWATCH. Si non fournie, utilise ECOWATCH_API_KEY depuis .env
        
        Raises:
            ValueError: Si aucune clé API n'est fournie
        """
        self.api_key = api_key or os.getenv("ECOWATCH_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Clé API ECOWATCH requise. "
                "Fournir via paramètre ou variable d'environnement ECOWATCH_API_KEY"
            )
        
        self.headers = {
            "X-API-Key": self.api_key
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """
        Effectue une requête HTTP GET vers l'API.
        
        Args:
            endpoint: Endpoint relatif à BASE_URL
            params: Paramètres de requête optionnels
        
        Returns:
            Réponse JSON décodée
        
        Raises:
            EcoWatchAPIError: Si la requête échoue
        """
        url = f"{self.BASE_URL}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response is not None:
                try:
                    error_data = e.response.json()
                    error_msg = error_data.get("error", str(e))
                except:
                    error_msg = str(e)
            else:
                error_msg = str(e)
            raise EcoWatchAPIError(f"Erreur API ECOWATCH: {error_msg}") from e
        except requests.exceptions.RequestException as e:
            raise EcoWatchAPIError(f"Erreur de connexion: {str(e)}") from e
    
    def test_connection(self) -> Dict[str, str]:
        """
        Test la connexion à l'API.
        
        Returns:
            Dict avec status et message
        
        Example:
            >>> client.test_connection()
            {'status': 'ok', 'message': 'Connexion au backend réussie'}
        """
        return self._make_request("test-connection")
    
    def get_devices(self, table: str) -> List[str]:
        """
        Récupère la liste des IDs de devices pour une table.
        
        Args:
            table: Nom de la table ('aquacheck' ou 'climatrack')
        
        Returns:
            Liste des IDs de devices
        
        Raises:
            EcoWatchAPIError: Si la table est invalide
        
        Example:
            >>> client.get_devices("aquacheck")
            ['20250314140500', '20250513115530', ...]
        """
        return self._make_request("b2b/devices", params={"table": table})
    
    def get_device_data(self, table: str, device_id: str) -> List[Dict[str, Any]]:
        """
        Récupère toutes les données historiques d'un device.
        
        Args:
            table: Nom de la table ('aquacheck' ou 'climatrack')
            device_id: ID du device
        
        Returns:
            Liste des mesures avec tous les champs
        
        Example:
            >>> client.get_device_data("aquacheck", "20250314140500")
            [{'id': 4626, 'ID_boitier': '20250314140500', ...}, ...]
        """
        return self._make_request(f"b2b/data/{table}/{device_id}")
    
    def get_latest_data(self, table: str, device_id: str) -> Dict[str, Any]:
        """
        Récupère la dernière mesure d'un device.
        
        Args:
            table: Nom de la table ('aquacheck' ou 'climatrack')
            device_id: ID du device
        
        Returns:
            Dict avec la dernière mesure
        
        Example:
            >>> client.get_latest_data("climatrack", "20240313101500")
            {'id': 134158, 'temperature': 27.26, 'co2': 739, ...}
        """
        return self._make_request(f"b2b/data/{table}/{device_id}/latest")
    
    def get_filtered_data(
        self,
        table: str,
        device_id: str,
        start_date: str,
        end_date: str
    ) -> List[Dict[str, Any]]:
        """
        Récupère les données filtrées par période.
        
        Args:
            table: Nom de la table ('aquacheck' ou 'climatrack')
            device_id: ID du device
            start_date: Date de début au format YYYY-MM-DD
            end_date: Date de fin au format YYYY-MM-DD
        
        Returns:
            Liste des mesures dans la période
        
        Example:
            >>> client.get_filtered_data(
            ...     "aquacheck",
            ...     "20250314140500",
            ...     "2025-06-16",
            ...     "2025-06-17"
            ... )
            [{'id': 4583, 'timestamp': '2025-06-16T07:42:28.000Z', ...}, ...]
        """
        params = {
            "start": start_date,
            "end": end_date
        }
        return self._make_request(f"b2b/data/{table}/{device_id}/filter", params=params)
    
    def __repr__(self) -> str:
        return f"<EcoWatchClient api_key=***{self.api_key[-8:]}>"