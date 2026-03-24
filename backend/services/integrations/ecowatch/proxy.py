from backend.utils.singleton import Singleton
from typing import Any, Dict, List, Optional
from backend.services.integrations.ecowatch.ecowatch_client_interface import EcowatchClientInterface

class EcowatchProxy(EcowatchClientInterface):
    
    def test_connection(self) -> Dict[str, str] | None:
        "Redireccion vers l'API"
        pass

    def get_devices(self, table: str) -> List[str] | None:
        "Tous les mois"
        pass

    def get_device_data(self, table: str, device_id: str) -> List[Dict[str, Any]] | None:
        "Tous les mois"
        pass

    def get_latest_data(self, table: str, device_id: str) -> Dict[str, Any] | None:
        "Tous les heures"
        pass

    def get_filtered_data(
        self,
        table: str,
        device_id: str,
        start_date: str,
        end_date: str
    ) -> List[Dict[str, Any]] | None:
        " Tous les heures "
        pass

    def __repr__(self) -> str:
        return "Proxy redirection"
    
