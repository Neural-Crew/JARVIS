from backend.utils.singleton import Singleton
from typing import Any, Dict, List, Optional

class EcowatchClientInterface(metaclass=Singleton):
    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        pass

    def test_connection(self) -> Dict[str, str] | None:
        pass

    def get_devices(self, table: str) -> List[str] | None :
        pass

    def get_device_data(self, table: str, device_id: str) -> List[Dict[str, Any]] | None :
        pass

    def get_latest_data(self, table: str, device_id: str) -> Dict[str, Any] | None:
        pass

    def get_filtered_data(
        self,
        table: str,
        device_id: str,
        start_date: str,
        end_date: str
    ) -> List[Dict[str, Any]] | None:
        pass

    def __repr__(self) -> str | None:
        pass