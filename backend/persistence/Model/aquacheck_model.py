from backend.persistence.Model.ecowatch_model import EcowatchModel
from backend.persistence.Model.ecowatch_bd import Aquacheck
from backend.persistence.engine import engine
from sqlalchemy import select, update, insert
from sqlalchemy.orm import Session

from datetime import datetime

class AquacheckModel(EcowatchModel):
    def get_devices(self, **kwargs):
        stmt = select(Aquacheck.ID_boitier).distinct()
        return self._execute(stmt)
    
    def get_device_data(self, **kwargs):
        stmt = select(Aquacheck).where(Aquacheck.ID_boitier == kwargs['ID_boitier'])
        return self._execute(stmt)
    
    def get_latest_data(self, **kwargs):

        stmt = (select(Aquacheck)
                .where(Aquacheck.ID_boitier == kwargs['ID_boitier'])
                .order_by(Aquacheck.timestamp.desc()).limit(1))
        
        return  self._execute(stmt)

    def get_filtered_data(self, **kwargs):
        print("ID_Boitier",kwargs['ID_boitier'])
        start_date = datetime.fromisoformat(kwargs['start_date'])
        end_date = datetime.fromisoformat(kwargs['end_date'])

        stmt = select(Aquacheck).where(Aquacheck.timestamp.between(start_date, end_date) 
                                       ,Aquacheck.ID_boitier == kwargs['ID_boitier'])
    
        return self._execute(stmt)
    
    def get_data(self, select_function, **kwargs):
        return select_function(self, **kwargs)

    def set_data(self, select_function, data, **kwargs):
        result = select_function(self, **kwargs)
        if result:
            self._update_data(data)
        else:
            self._insert_data(data)

    def _update_data(self, data):
        if isinstance(data, dict):
            data = [data]
        
        to_insert = []
        for row in data:
            stmt = select(Aquacheck).where(Aquacheck.id == row['id'])
            row_in_table = self._execute(stmt)
            if not row_in_table:
                to_insert.append(row)
                continue

            stmt = (update(Aquacheck)
                    .where( Aquacheck.id == row['id'] )
                    .values(
                        id = row['id'], 
                        ID_boitier = row['ID_boitier'], 
                        timestamp = datetime.fromisoformat(row['timestamp']),
                        humidity = row['humidity'],
                        temperature = row['temperature'],
                        ground_humidity = row['ground_humidity'],
                        humidex = row['humidex']
                    ))
            self._execute_and_commit(stmt)

        if to_insert: self._insert_data(to_insert)

    def _insert_data(self, data):
        if isinstance(data, dict):
            data = [data]

        for row in data:
            stmt = insert(Aquacheck).values(
                                    id = row['id'], 
                                    ID_boitier = row['ID_boitier'], 
                                    timestamp = datetime.fromisoformat(row['timestamp']),
                                    humidity = row['humidity'],
                                    temperature = row['temperature'],
                                    ground_humidity = row['ground_humidity'],
                                    humidex = row['humidex']
                                            )
            self._execute_and_commit(stmt)
