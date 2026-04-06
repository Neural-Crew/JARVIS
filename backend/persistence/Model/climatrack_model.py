from backend.persistence.Model.ecowatch_model import EcowatchModel
from sqlalchemy import select, update, insert
from backend.persistence.Model.ecowatch_bd import Climatrack

from datetime import datetime
from typing import Callable, Any

class ClimatrackModel(EcowatchModel):
    def get_devices(self, **kwargs):
        stmt = select(Climatrack.ID_boitier).group_by(Climatrack.ID_boitier)
        return self._execute(stmt).all()
    
    def get_device_data(self, **kwargs):
        stmt = select(Climatrack).where(Climatrack.ID_boitier == kwargs['ID_boitier'])
        return self._execute(stmt).all()

    def get_latest_data(self, **kwargs):
        stmt = (select(Climatrack)
                .where(Climatrack.ID_boitier == kwargs['ID_boitier'])
                .order_by(Climatrack.timestamp.desc()).limit(1))
        
        return self._execute(stmt).one_or_none()
    
    def get_filtered_data(self,**kwargs):
        start_date = datetime.fromisoformat(kwargs['start_date'])
        end_date = datetime.fromisoformat(kwargs['end_date'])
        stmt = select(Climatrack).where(Climatrack.timestamp.between(start_date, end_date)
                                        , Climatrack.ID_boitier == kwargs['ID_boitier'])
        print(stmt)
        return self._execute(stmt).all()
    
    def set_data(self, select_function, data, **kwargs):
        result = select_function(self, **kwargs)
        if result:
            print("update")
        else: 
            print("insert")
        
        print(f"Climatrack: {'*'*10}{data}{'*'*10}")