from backend.utils.singleton import Singleton
from typing import Any, Dict, List, Optional
from backend.services.integrations.ecowatch.ecowatch_client_interface import EcowatchClientInterface
from backend.services.integrations.ecowatch.client import EcoWatchClient
from backend.persistence.sqlite_proxy import SQLiteProxy, QueryIDS
from datetime import timedelta

class EcowatchProxy(EcowatchClientInterface):
    def __init__(self) -> None:
        super().__init__()
        self.client = EcoWatchClient()
        self.sqlproxy = SQLiteProxy()

    def test_connection(self) -> Dict[str, str]:
        "Redireccion vers l'API"
        return self.client.test_connection()

    def get_devices(self, table: str) -> List[str]:
        "Tous les mois"
        return self._proxy_execute(SQLiteProxy.get_latter_get_device_call,
                            timedelta(days=30),
                            QueryIDS.get_devices,
                            self.client.get_devices,
                            (table) )

    def get_device_data(self, table: str, device_id: str) -> List[Dict[str, Any]]:
        "Tous les mois"
        return self._proxy_execute(SQLiteProxy.get_latter_get_device_data_call, 
                            timedelta(days=30),
                            QueryIDS.get_device_data,
                            self.client.get_device_data,
                            (table, device_id) )

    def get_latest_data(self, table: str, device_id: str) -> Dict[str, Any]:
        "Tous les heures"
        return self._proxy_execute(SQLiteProxy.get_latter_get_latest_data_call, 
                            timedelta(hours=1), 
                            QueryIDS.get_latest_data, 
                            self.client.get_latest_data, 
                            (table, device_id) )
    
    def get_filtered_data(
        self,
        table: str,
        device_id: str,
        start_date: str,
        end_date: str
    ) -> List[Dict[str, Any]]:
        " Tous les heures "
        return self._proxy_execute( SQLiteProxy.get_latter_get_filtered_data_call, 
                                   timedelta(hours=1), 
                                   QueryIDS.get_filtered_data, 
                                   self.client.get_filtered_data, 
                                   (table, device_id, start_date, end_date) )
        

    def _proxy_execute(self, proxy_method ,  timedelta, query_id, client_method, *args):
        response = self.sqlproxy.check_latter_call(proxy_method,timedelta)
        if response is None:
            response = client_method(*args)
            self.sqlproxy.insert_OR_update_latest_query(query_id, response)
        assert response is not None
        return response

    def __repr__(self) -> str:
        return "Proxy redirection"
    
