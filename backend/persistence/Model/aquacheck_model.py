from backend.persistence.Model.ecowatch_model import EcowatchModel
from backend.persistence.Model.ecowatch_bd import Aquacheck
from backend.persistence.engine import engine
from sqlalchemy import select, update, insert
from sqlalchemy.orm import Session

from datetime import datetime

class AquacheckModel(EcowatchModel):
    def get_devices(self, **kwargs):
        stmt = select(Aquacheck.ID_boitier).group_by(Aquacheck.ID_boitier)
        return self._execute(stmt).all()
    
    def get_device_data(self, **kwargs):
        stmt = select(Aquacheck).where(Aquacheck.ID_boitier == kwargs['ID_boitier'])
        return self._execute(stmt).all()
    
    def get_latest_data(self, **kwargs):

        stmt = (select(Aquacheck)
                .where(Aquacheck.ID_boitier == kwargs['ID_boitier'])
                .order_by(Aquacheck.timestamp.desc()).limit(1))
        
        return  self._execute(stmt).scalar_one_or_none()

    def get_filtered_data(self, **kwargs):
        start_date = datetime.fromisoformat(kwargs['start_date'])
        end_date = datetime.fromisoformat(kwargs['end_date'])

        stmt = select(Aquacheck).where(Aquacheck.timestamp.between(start_date, end_date) 
                                       , Aquacheck.ID_boitier == kwargs['ID_boitier'])
    
        return self._execute(stmt).all()
    
    def set_data(self, select_function, data, **kwargs):
        result = select_function(self, **kwargs)
        if result:
            print("update")
            print(result)
        else: 
            print("insert")

        print(f"Aquacheck: {'*'*10}{data}{'*'*10}")

   