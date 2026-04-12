from backend.utils.singleton import Singleton
from backend.persistence.Model.ecowatch_bd import Query
from backend.persistence.Model.engine import engine

from sqlalchemy import select, insert, update
from sqlalchemy.orm import Session

from threading import Lock
from enum import Enum
from datetime import datetime, timedelta
from typing import Callable, Any

class QueryIDS(Enum):
    get_devices = "get_devices"
    get_device_data = "get_device_data"
    get_latest_data = "get_latest_data"
    get_filtered_data = "get_filtered_data"

class QueryModel(metaclass=Singleton):
    def __init__(self, lock = Lock()) -> None:
        pass

    def get_query(self, query_id : QueryIDS, table, device_ID):
        stmt = select(Query).where(Query.query_id == query_id.value,
                                   Query.table == table,
                                   Query.device_ID == device_ID)
        return self._execute(stmt)
    
    def get_query_with_dates(self, query_id : QueryIDS, table, device_ID, start_date, end_date):
        start_date = datetime.fromisoformat(start_date)
        end_date = datetime.fromisoformat(end_date)
        assert start_date <= end_date

        stmt = select(Query).where(Query.query_id == query_id.value,
                                   Query.table == table,
                                   Query.device_ID == device_ID,
                                   start_date >= Query.start_date,
                                   end_date <= Query.end_date)
        return self._execute(stmt)
    
    def get_query_without_device(self, query_id : QueryIDS, table):
        stmt = select(Query).where(Query.query_id == query_id.value,
                                   Query.table == table )
        return self._execute(stmt)
    
    def _execute(self, stmt):
        with Session(engine) as session:
            #print(f"\033[0;37;44m {stmt} \033[0m")
            query = session.scalars(stmt).one_or_none()
            #print("Query:", query)
        return query
    
