from backend.persistence.engine import engine
from backend.utils.singleton import Singleton
from backend.persistence.Model.ecowatch_bd import Query
from backend.persistence.Model.aquacheck_model import AquacheckModel
from backend.persistence.Model.climatrack_model import ClimatrackModel
from backend.persistence.Model.ecowatch_model import EcowatchModel
from typing import Callable, Any, List
from datetime import datetime, timedelta
from enum import Enum

from sqlalchemy.orm import Session
from sqlalchemy import select, update, insert, delete
from threading import Lock


class QueryIDS(Enum):
    get_devices = "get_devices"
    get_device_data = "get_device_data"
    get_latest_data = "get_latest_data"
    get_filtered_data = "get_filtered_data"

class SQLiteProxy(metaclass=Singleton):
    def __init__(self, lock = Lock()) -> None:
        pass

    def check_latter_call(self, select_function : Callable[..., Any], 
                          table  : str, 
                          device_ID : str|None, 
                          expiry : timedelta ):
        """
        This method should be used by the user to check whether a certain
        query call is expired and should be renewed.
        If it is expired this method return None
        Otherwise it return the non expired query.
        """
        latest_query : Query | None = select_function(self, table, device_ID)
        if not latest_query:
            #print("\033[92m check_latter_call not query found\033[0m")
            return None
        if((latest_query.latest_query_call - expiry).second <= 0):
            return None
        return latest_query
    
    def get_latter_get_device_call(self, table, device_ID) -> Query:
        return self._get_query(QueryIDS.get_devices, table, device_ID)

    def get_latter_get_device_data_call(self, table, device_ID) -> Query:
        return self._get_query(QueryIDS.get_device_data, table, device_ID)

    def get_latter_get_latest_data_call(self, table, device_ID) -> Query:
        return self._get_query(QueryIDS.get_filtered_data, table, device_ID)

    def get_latter_get_filtered_data_call(self, table, device_ID) -> Query:
        return self._get_query(QueryIDS.get_filtered_data, table, device_ID)

    def _get_query(self, query_id : QueryIDS, table, device_ID):
        stmt = select(Query).where(Query.query_id == query_id.value,
                                   Query.table == table,
                                   Query.device_ID == device_ID)
        with Session(engine) as session:
            query = session.scalars(stmt).one_or_none()
        return query
    
    def _check_exists(self, query_id : QueryIDS, table, device_id):
        stmt = select(Query).where(Query.query_id == query_id.value,
                                   Query.table == table,
                                   Query.device_ID == device_id)
        query = None
        with Session(engine) as conn:
            query = conn.execute( stmt ).first()
        return query != None

    def insert_OR_update_latest_query(self, query_id:QueryIDS, table, device_id):
        if not self._check_exists(query_id, table, device_id):
            stmt = insert(Query).values(query_id=query_id.value, table=table, device_ID=device_id )
        else:
            stmt = (
            update(Query)
            .where(Query.query_id == query_id.value,
                   Query.table == table,
                   Query.device_ID == device_id)
            .values(table = table))
        #print(f"{'_'*20} statement: {stmt} {'_'*20}")
        with Session(engine) as conn:
            rows = conn.execute(stmt)
            conn.commit()
    

    def search_query_data(self, 
                      ecowatch_model : type[EcowatchModel], 
                      select_function : Callable[..., Any], 
                      **kwargs) -> List | dict | None:
        """
        This method will fetch some data inside one of the ecowatch
        tables. The data is supposed to be there since the query execution
        was cheked before
        This method represents the READ part of the CRUD chain.
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
        """
        ecowatch_model().set_data(select_function, new_response, **kwargs)    
    
    def _reset_query_table(self):
        """
        !!Caution!! 
        This method should be executed only for testing
        It erases the whole Query table
        It represents the DELETE part of the CRUD chain
        """
        stmt = delete(Query)
        with Session(engine) as conn:
            conn.execute(stmt)
            conn.commit()
