from backend.utils.singleton import Singleton
from typing import Any, Dict, List, Optional

class EcowatchClientInterface(metaclass=Singleton):
    
    def test_connection(self) -> Dict[str, str]:
        pass

    def get_devices(self, table: str) -> List[str]:
        pass

    def get_device_data(self, table: str, device_id: str) -> List[Dict[str, Any]]:
        pass

    def get_latest_data(self, table: str, device_id: str) -> Dict[str, Any]:
        pass

    def get_filtered_data(
        self,
        table: str,
        device_id: str,
        start_date: str,
        end_date: str
    ) -> List[Dict[str, Any]]:
        pass

    def __repr__(self) -> str:
        pass