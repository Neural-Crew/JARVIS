import os
import sys

import pytest
from unittest import TestCase
from dotenv import load_dotenv
from backend.services.integrations.ecowatch.proxy import EcowatchProxy
from backend.persistence.Model.ecowatch_bd import Query
from backend.persistence.Controller.query_controller import QueryController, QueryIDS
from backend.persistence.Model.aquacheck_model import AquacheckModel
from backend.persistence.Model.climatrack_model import ClimatrackModel
from backend.persistence.Model.ecowatch_model import EcowatchModel
from datetime import timedelta
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.persistence.Model.engine import engine

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))


load_dotenv()


"""
Test Unitaires des Methodes du Proxy
"""

@pytest.fixture(scope="session", autouse=True)
def initalize():
    print("\033[0;34;43m Initialize \033[0m")
    sql_controller = QueryController()
    sql_controller._reset_query_table()
    
@pytest.fixture()
def sql_controller() -> QueryController:
    "Composante du proxy a tester"
    sql_controller = QueryController()
    return sql_controller

@pytest.mark.parametrize("query, kwargs", [
    (QueryIDS.get_device_data, {'table':"aquacheck", 'ID_boitier':"20250314140500"}),
    (QueryIDS.get_devices, {'table':"aquacheck", 'ID_boitier':"20250314140500"} ),
    (QueryIDS.get_filtered_data, { 'table':'aquacheck','ID_boitier': "20250314140500", 'start_date': "2025-06-16", 'end_date':"2025-06-17" }),
    (QueryIDS.get_latest_data, {'table':'aquacheck','ID_boitier': "20250314140500"})
])

def test_InsertQuery(sql_controller : QueryController, query , kwargs):
    table = kwargs['table']
    del kwargs['table']

    response = sql_controller.add_query(query, table, **kwargs) 
    with Session(engine) as session:
        for row in session.execute( select(Query) ):
            print(row)

@pytest.mark.parametrize("fonction, table, device_id, timedelta, start_date, end_date", [
    (QueryController.get_latter_get_devices_call, "aquacheck" ,"20250314140500", timedelta(days=31), None, None),
    (QueryController.get_latter_get_device_data_call,"aquacheck" , "20250314140500", timedelta(days=31), None, None),
    (QueryController.get_latter_get_latest_data_call,"aquacheck" , "20250314140500", timedelta(hours=1), None, None),
    (QueryController.get_latter_get_filtered_data_call,"aquacheck" , "20250314140500", timedelta(hours=1), "2025-06-16", "2025-06-17"),
])

def test_SelectGetDevicesQuery(sql_controller: QueryController, fonction, table, device_id, timedelta, start_date, end_date):
    if(start_date and end_date):
        result = sql_controller.check_latter_call(fonction, timedelta, table=table, ID_boitier=device_id, start_date=start_date, end_date=end_date)
    else:
        result = sql_controller.check_latter_call(fonction, timedelta, table=table, ID_boitier=device_id)
    print(f"{'='*20}{result}{'='*20}")
    assert isinstance(result, Query)


def test_getAllInfoFromQuery():
    print(f"{'*'*20}GetAllInfoFromQuery{'*'*20}")
    stmt = select(Query)
    with Session(engine) as conn:
        rows = conn.execute(stmt).all()

        print(type(rows))
    
    print(f"check insert{'-'*50}")
    for row in rows:
        print(row, type(row))    
    print(f"{'-'*50}")

def test_cleanup(sql_controller):
    sql_controller._reset_query_table()


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
