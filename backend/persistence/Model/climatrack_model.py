from backend.persistence.Model.ecowatch_model import EcowatchModel
from sqlalchemy import select, update, insert
from backend.persistence.Model.ecowatch_bd import Climatrack

from datetime import datetime
from typing import Callable, Any

class ClimatrackModel(EcowatchModel):
    def get_devices(self, **kwargs):
        stmt = select(Climatrack.ID_boitier).distinct()
        return self._execute(stmt)
    
    def get_device_data(self, **kwargs):
        stmt = select(Climatrack).where(Climatrack.ID_boitier == kwargs['ID_boitier'])
        return self._execute(stmt)

    def get_latest_data(self, **kwargs):
        stmt = (select(Climatrack)
                .where(Climatrack.ID_boitier == kwargs['ID_boitier'])
                .order_by(Climatrack.timestamp.desc()).limit(1))
        
        return self._execute(stmt)
    
    def get_filtered_data(self, **kwargs):
        start_date = datetime.fromisoformat(kwargs['start_date'])
        end_date = datetime.fromisoformat(kwargs['end_date'])
        stmt = select(Climatrack).where(Climatrack.timestamp.between(start_date, end_date)
                                        ,Climatrack.ID_boitier == kwargs['ID_boitier'])
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
            stmt = select(Climatrack).where(Climatrack.id == row['id'])
            row_in_table = self._execute(stmt)
            if not row_in_table:
                to_insert.append(row)
                continue

            stmt = (update(Climatrack)
                    .where( Climatrack.id == row['id'] )
                    .values(
                        id = row['id'], 
                        ID_boitier = row['ID_boitier'], 
                        timestamp = datetime.fromisoformat(row['timestamp']),
                        humidity = row['humidity'],
                        temperature = row['temperature'],
                        tvoc = row['tvoc'],
                        co2 = row['co2'],
                        pm1_0 = row['pm1_0'],
                        pm10 = row['pm10'],
                        pm2_5 = row['pm2_5'],
                        sound_level = row['sound_level']
                    ))
            self._execute_and_commit(stmt)

        if to_insert: self._insert_data(to_insert)

    def _insert_data(self, data):
        if isinstance(data, dict):
            data = [data]

        for row in data:
            stmt = insert(Climatrack).values(
                                    id = row['id'], 
                                    ID_boitier = row['ID_boitier'], 
                                    timestamp = datetime.fromisoformat(row['timestamp']),
                                    humidity = row['humidity'],
                                    temperature = row['temperature'],
                                    tvoc = row['tvoc'],
                                    co2 = row['co2'],
                                    pm1_0 = row['pm1_0'],
                                    pm10 = row['pm10'],
                                    pm2_5 = row['pm2_5'],
                                    sound_level = row['sound_level']
                                    )
            self._execute_and_commit(stmt)
