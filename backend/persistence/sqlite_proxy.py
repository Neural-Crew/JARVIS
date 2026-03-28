from backend.persistence.engine import engine
from backend.utils.singleton import Singleton
from backend.persistence.Model.ecowatch_bd import Query

from typing import Callable, Any, List
from datetime import datetime, timedelta
from enum import Enum

from sqlalchemy.orm import Session
from sqlalchemy import select, update, insert, delete


class QueryIDS(Enum):
    get_devices = "get_devices"
    get_device_data = "get_device_data"
    get_latest_data = "get_latest_data"
    get_filtered_data = "get_filtered_data"

class SQLiteProxy(metaclass=Singleton):

    def check_latter_call(self, select_function : Callable[..., Any], expiry : timedelta ):
        """
        This method should be used by the user to check whether a certain
        query call is expired and should be renewed.
        If it is expired this method return None
        Otherwise it return the non expired query.
        """
        latest_query : Query | None = select_function(self)
        if not latest_query or latest_query is None:
            print("\033[92m check_latter_call not query found\033[0m")
            return None
        if((latest_query.latest_query_call - expiry).second <= 0):
            return None
        return latest_query
    
    def get_latter_get_device_call(self) -> Query:
        return self._get_query(QueryIDS.get_devices)

    def get_latter_get_device_data_call(self) -> Query:
        return self._get_query(QueryIDS.get_device_data)

    def get_latter_get_latest_data_call(self) -> Query:
        return self._get_query(QueryIDS.get_filtered_data)

    def get_latter_get_filtered_data_call(self) -> Query:
        return self._get_query(QueryIDS.get_filtered_data)

    def _get_query(self, query_id : QueryIDS):
        stmt = select(Query).where(Query.query_id == query_id.value)
        with engine.begin() as conn:
            query = conn.scalars(stmt).first() 
        if query is not None and query: return Query(query)
        return None
    
    def _check_exists(self, query_id : QueryIDS):
        stmt = select(Query).where(Query.query_id == query_id.value)
        query = None
        with Session(engine) as conn:
            query = conn.execute( stmt )
        return query.first() != None

    def insert_OR_update_latest_query(self, query_id : QueryIDS, new_response : Any):
        "This method should be used by the user only when"
        "the expiricy date of the request has been confirmed to not be"
        "valid"
        if not self._check_exists(query_id):
            stmt = insert(Query).values(query_id=query_id.value, response = new_response )
        else:
            stmt = (
            update(Query)
            .where(Query.query_id == query_id.value)
            .values(response = new_response))
        print(f"{'_'*20} statement: {stmt} {'_'*20}")
        with Session(engine) as conn:
            rows = conn.execute(stmt)
            conn.commit()
        
        

    def _reset_query_table(self):
        """
        !!Caution!! 
        This method should be executed only for testing
        It erases the whole Query table
        """
        stmt = delete(Query)
        with Session(engine) as conn:
            conn.execute(stmt)
            conn.commit()
