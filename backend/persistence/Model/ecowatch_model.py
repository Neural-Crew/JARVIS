from backend.utils.singleton import Singleton
from backend.persistence.Model.engine import engine
from sqlalchemy.orm import Session
from sqlalchemy import Result, Row

from typing import List

class EcowatchModel(metaclass=Singleton):

    def get_devices(self):
        pass 

    def get_device_data(self, ID_boitier):
        pass

    def get_latest_data(self, ID_boitier):
        pass

    def get_filtered_data(self, ID_boitier, start_date, end_date):
        pass

    def get_data(self, select_function, **kwargs) -> List:
        pass

    def set_data(self, select_function, data, **kwargs):
        pass
    
    def to_json(self)-> dict:
        pass

    def _execute(self, statement):
        with Session(engine) as conn:
            result = conn.execute( statement )
            content = result.all()
        return content
    
    def _execute_and_commit(self, statement):
        with Session(engine) as conn:
            result = conn.execute( statement )
            conn.commit()
        return result