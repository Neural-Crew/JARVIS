from backend.utils.singleton import Singleton
from backend.services.integrations.ecowatch.ecowatch_client_interface import EcowatchClientInterface
from backend.services.integrations.ecowatch.client import EcoWatchClient
from backend.persistence.sqlite_proxy import SQLiteProxy, QueryIDS
from backend.persistence.Model.ecowatch_model import EcowatchModel
from backend.persistence.Model.ecowatch_creator import EcowatchCreator
from typing import Any, Dict, List, Optional, Callable
from datetime import timedelta
from threading import Lock

class EcowatchProxy(EcowatchClientInterface):
    """
    Cette classe permet de mettre en place un proxy qui permettra de réduire le nombre d'appels
    envers le client. Ceci sert aussi comme un outil de redondance des tables climatrack
    et aquacheck. Le proxy va vérifier si un appel spécifique vers l'API à été déjà effectué
    et s'il à été effectué dans une certaine période de temps on renvoie les données stockées en local
    Le cas contraire on fait un appel à l'API. Dans ce cas on enregistre les nouvelles données.
    """
    def __init__(self, lock=Lock()) -> None:
        self.client = EcoWatchClient(lock = lock)
        self.sqlproxy = SQLiteProxy(lock = lock)

    def test_connection(self) -> Dict[str, str]:
        "Redireccion vers l'API"
        return self.client.test_connection()

    def get_devices(self, table: str) -> List[str]:
        "Tous les mois"
        ecowatch_model : type[EcowatchModel] | None = EcowatchCreator.getTypeEcowatchModel(table)
        assert ecowatch_model

        return self._proxy_exec_not_insert( SQLiteProxy.get_latter_get_device_call, 
                                timedelta(days=30), 
                                self.client.get_devices,
                                (table) )

    def get_device_data(self, table: str, device_id: str) -> List[Dict[str, Any]]:
        "Tous les mois"
        ecowatch_model : type[EcowatchModel] | None = EcowatchCreator.getTypeEcowatchModel(table)
        assert ecowatch_model
        result = self._proxy_execute( SQLiteProxy.get_latter_get_device_data_call, 
                                timedelta(days=30), 
                                self.client.get_device_data, 
                                QueryIDS.get_device_data,
                                ecowatch_model,
                                ecowatch_model.get_device_data,
                                table, device_id,
                                ID_boitier = device_id )
        if isinstance(result, List):
            return result
        else: raise Exception("get_device_data: Result is not dict")

    def get_latest_data(self, table: str, device_id: str) -> Dict[str, Any]:
        "Tous les heures"
        ecowatch_model : type[EcowatchModel] | None = EcowatchCreator.getTypeEcowatchModel(table)
        assert ecowatch_model
    
        result =  self._proxy_execute( SQLiteProxy.get_latter_get_latest_data_call, 
                                timedelta(hours=1), 
                                self.client.get_latest_data, 
                                QueryIDS.get_latest_data,
                                ecowatch_model,
                                ecowatch_model.get_latest_data,
                                table, device_id,
                                ID_boitier = device_id )
        print("result: ", result)
        if isinstance(result, dict):
            return result
        else: raise Exception("get_latest_data: Result is not dict")

    def get_filtered_data(
        self,
        table: str,
        device_id: str,
        start_date: str,
        end_date: str
    ) -> List[Dict[str, Any]] :
        " Tous les heures "
        
        ecowatch_model : type[EcowatchModel] | None = EcowatchCreator.getTypeEcowatchModel(table)
        assert ecowatch_model

        result =  self._proxy_execute( SQLiteProxy.get_latter_get_filtered_data_call, 
                                timedelta(hours=1), 
                                self.client.get_filtered_data, 
                                QueryIDS.get_filtered_data,
                                ecowatch_model,
                                ecowatch_model.get_filtered_data,
                                table, device_id, start_date, end_date,
                                ID_boitier = device_id, start_date = start_date, end_date = end_date )
        if isinstance(result, list): return result
        else: raise Exception("get_filtered_data: Result is not List")

    def _proxy_execute(self, 
                       proxy_method ,  
                       timedelta, 
                       client_method,
                       query_id : QueryIDS,
                       ecowatch_model : type[EcowatchModel], 
                       select_function : Callable[..., Any] , *args, **kwargs):
        query = self.sqlproxy.check_latter_call(proxy_method, args[0], args[1], timedelta)
        print(f"=============== Query {query} =============")
        if query is None:
            response = client_method(*args)
            self.sqlproxy.add_data_to_tables(ecowatch_model, select_function, response, **kwargs)
            self.sqlproxy.insert_OR_update_latest_query(query_id, table=args[0], device_id=args[1])
        else:
            response = self.sqlproxy.search_query_data(ecowatch_model, select_function, **kwargs)
            
        assert response is not None
        return response

    def _proxy_exec_not_insert(self,
                               proxy_method,
                               timedelta,
                               client_method,
                               *args
                               ):
        response = self.sqlproxy.check_latter_call(proxy_method, args[0], None, timedelta)
        if response is None:
            response = client_method(*args)
        assert response is not None
        return response

    def __repr__(self) -> str:
        return "Proxy redirection"
    
