from backend.persistence.Model.query_model import QueryModel, Query, QueryIDS
from backend.persistence.Model.engine import engine
from backend.utils.singleton import Singleton

from sqlalchemy.orm import Session
from sqlalchemy import select, update, insert, delete
from threading import Lock
from datetime import timedelta, datetime, timezone
from dateutil.parser import parse
from typing import Callable, Any


class QueryController(metaclass=Singleton):
    def __init__(self, lock = Lock()) -> None:
        lock = Lock()
        self.query_model = QueryModel(lock=lock)

    def check_latter_call(self, 
                          select_function : Callable[..., Any], 
                          expiry : timedelta,
                        **kwargs ):
        """
        This method should be used by the user to check whether a certain
        query call is expired and should be renewed.
        If it is expired this method return None
        Otherwise it return the non expired query.

        Prameters:
         select_function: The select function has to be an sqliteproxy method specifying the query to search for ex [ get_latter_get_device_call ]

        """
        latest_query : Query | None = select_function(self, **kwargs)
        if latest_query is None:
            print("\033[92m check_latter_call not query found\033[0m")
            return None
        time_threshold = datetime.now(tz=timezone.utc) - expiry
        query_call_utc_0 = latest_query.latest_query_call.replace(tzinfo = timezone.utc)
        if(query_call_utc_0.timestamp() < time_threshold.timestamp()):
            return None
        return latest_query

    def get_latter_get_devices_call(self, **kwargs) -> Query|None:
        return self.query_model.get_query_without_device(QueryIDS.get_devices, kwargs['table'])

    def get_latter_get_device_data_call(self, **kwargs) -> Query|None:
        return self.query_model.get_query(QueryIDS.get_device_data, kwargs['table'], kwargs['ID_boitier'])

    def get_latter_get_latest_data_call(self, **kwargs) -> Query|None:
        return self.query_model.get_query(QueryIDS.get_filtered_data, kwargs['table'], kwargs['ID_boitier'])

    def get_latter_get_filtered_data_call(self, **kwargs) -> Query|None:
        return self.query_model.get_query_with_dates(QueryIDS.get_filtered_data, 
                                          kwargs['table'], 
                                          kwargs['ID_boitier'], 
                                          kwargs['start_date'], 
                                          kwargs['end_date'])
    
    
    def add_query(self, query_id:QueryIDS, table, **kwargs):
        if 'start_date' in kwargs and 'end_date' in kwargs:
            self._insert_OR_update_latest_query_with_date( query_id, table, kwargs['ID_boitier'], kwargs['start_date'], kwargs['end_date'])
        else:
            self._insert_OR_update_latest_query(query_id, table, kwargs['ID_boitier'])


    def _insert_OR_update_latest_query(self, query_id : QueryIDS, table : str, device_id:str):
        query = self.query_model.get_query(query_id, table, device_id)
        if query is None:
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
    
    def _insert_OR_update_latest_query_with_date(self, query_id : QueryIDS, table:str, device_id:str, start_date:str, end_date:str):
        start_date_i = datetime.fromisoformat(start_date)
        end_date_i = datetime.fromisoformat(end_date)
        
        query = self.query_model.get_query(query_id, table, device_id)
        if query is None:
            stmt = insert(Query).values(
                query_id=query_id.value, 
                table=table, 
                device_ID=device_id,
                start_date=start_date_i,
                end_date=end_date_i)
        else:
            start_date_u = max( start_date_i, query.start_date )
            end_date_u = max( end_date_i, query.end_date )
            stmt = (
            update(Query)
            .where(Query.query_id == query_id.value,
                   Query.table == table,
                   Query.device_ID == device_id)
            .values(start_date = start_date_u, end_date = end_date_u))
        #print(f"{'_'*20} statement: {stmt} {'_'*20}")
        with Session(engine) as conn:
            rows = conn.execute(stmt)
            conn.commit()

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