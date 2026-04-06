import os
import sys

import pytest
from unittest import TestCase
from dotenv import load_dotenv
from backend.services.integrations.ecowatch.proxy import EcowatchProxy
from backend.persistence.sqlite_proxy import SQLiteProxy, Query, QueryIDS
from backend.persistence.Model.aquacheck_model import AquacheckModel
from backend.persistence.Model.climatrack_model import ClimatrackModel
from backend.persistence.Model.ecowatch_model import EcowatchModel
from datetime import timedelta
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.persistence.engine import engine

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))


load_dotenv()


"""
Test Unitaires des Methodes du Proxy
"""

@pytest.fixture(scope="session", autouse=True)
def initalize():
    sqlproxy = SQLiteProxy()
    sqlproxy._reset_query_table()
    
@pytest.fixture()
def sqlproxy() -> SQLiteProxy:
    "Composante du proxy a tester"
    sqlproxy = SQLiteProxy()
    return sqlproxy

@pytest.mark.parametrize("fonction, timedelta", [
    (SQLiteProxy.get_latter_get_device_call, timedelta(days=31)),
    (SQLiteProxy.get_latter_get_device_data_call, timedelta(days=31)),
    (SQLiteProxy.get_latter_get_latest_data_call, timedelta(hours=1)),
    (SQLiteProxy.get_latter_get_filtered_data_call, timedelta(hours=1)),
])    
def test_SelectGetDevicesQuery(sqlproxy, fonction, timedelta):
    result = sqlproxy.check_latter_call(fonction, timedelta)
    print(f"{'='*20}{result}{'='*20}")
    assert isinstance(result, Query) or result is None

@pytest.mark.parametrize("query, kwargs", [
    (AquacheckModel.get_device_data, {'ID_boitier':"20250314140500"}),
    (AquacheckModel.get_devices, {} ),
    (AquacheckModel.get_filtered_data, { 'ID_boitier': "20250314140500", 'start_date': "2025-06-16", 'end_date':"2025-06-17" }),
    (AquacheckModel.get_latest_data, {'ID_boitier': "20250314140500"})
])
def test_InsertInformation(sqlproxy : SQLiteProxy, query , kwargs):
    response = sqlproxy.insert_OR_update_latest_query(AquacheckModel, query, "test", **kwargs)
    with Session(engine) as session:
        for row in session.execute( select(Query) ):
            print(row)

def test_getAllInfoFromQuery():
    print(f"{'*'*20}GetAllInfoFromQuery{'*'*20}")
    stmt = select(Query)
    with Session(engine) as conn:
        rows = conn.execute(stmt).all()

        print(type(rows))
    
    print(f"ckeck insert{'-'*50}")
    for row in rows:
        print(row, type(row))    
    print(f"{'-'*50}")

if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
