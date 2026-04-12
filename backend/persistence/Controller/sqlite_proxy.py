from backend.persistence.Model.engine import engine
from backend.utils.singleton import Singleton
from backend.persistence.Model.ecowatch_model import EcowatchModel
from backend.persistence.Controller.query_controller import QueryController, QueryIDS
from typing import Callable, Any, List

from threading import Lock

class SQLiteProxy(metaclass=Singleton):
    def __init__(self, lock = Lock()) -> None:
        self.query_controller = QueryController(lock=Lock())

    def search_query_data(self,
                      ecowatch_model : type[EcowatchModel],
                      select_function : Callable[..., Any],
                      **kwargs) -> List | dict | None:
        """
        This method will fetch some data inside one of the ecowatch
        tables. The data is supposed to be there since the query execution
        was cheked before
        This method represents the READ part of the CRUD chain.

        Parameters: 
            select_function : The select function should be an ecowatch model function to be used by an ecowatchmodel instace inside the get_data method

        """
        data = ecowatch_model().get_data(select_function, **kwargs)
        if data and len(data) > 1:
            return [ row[0].to_json() for row in data ]
        elif len(data)==1:
            return data[0][0].to_json()
        return data
    
    def add_data_to_tables(self, 
                            ecowatch_model : type[EcowatchModel], 
                            select_function : Callable[..., Any], 
                            new_response : Any,
                            **kwargs):
        
        """
        This method should be used by the user only when
        the expiricy date of the request has been confirmed to not be
        valid
        It represent the CREATE/UPDATE part of the CRUD chain
        
        Parameters:
            select_function : The select function should be an ecowatch model function to be used by an ecowatchmodel instace inside the get_data method
        """
        ecowatch_model().set_data(select_function, new_response, **kwargs)    
    
    
