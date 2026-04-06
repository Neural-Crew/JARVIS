from backend.utils.singleton import Singleton
from backend.persistence.engine import engine
from sqlalchemy.orm import Session

class EcowatchModel(metaclass=Singleton):
    def get_devices(self):
        pass 

    def get_device_data(self, ID_boitier):
        pass

    def get_latest_data(self, ID_boitier):
        pass

    def get_filtered_data(self, ID_boitier, start_date, end_date):
        pass

    def set_data(self, select_function, data, **kwargs):
        pass

    def _execute(self, statement):
        with Session(engine) as conn:
            result = conn.execute( statement )
        return result
    
    def _execute_and_commit(self, statement):
        with Session(engine) as conn:
            result = conn.execute( statement )
            conn.commit()
        return result