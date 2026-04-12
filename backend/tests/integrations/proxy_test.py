"""
Tests Unitaires pour le proxy du client Ecowatch
"""

import os
import sys

import pytest
from dotenv import load_dotenv
from backend.services.integrations.ecowatch.proxy import EcowatchProxy

from backend.persistence.Controller.sqlite_proxy import SQLiteProxy
from backend.persistence.Model.ecowatch_bd import Query
from datetime import timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))


load_dotenv()

"""
Test Unitaires des Methodes du Proxy
"""

@pytest.fixture
def proxy():
    " Proxy a tester "
    return EcowatchProxy()

def testTestConnexionProxyCall(proxy):
    print("testing connection...")
    result  = proxy.test_connection()
    assert isinstance(result, dict) and result['status'] == "ok"
    
def test_GetDevicesProxyCall(proxy):
    devices =  proxy.get_devices("aquacheck")
    print("Proxy Test",devices)
    assert isinstance(devices, list)
    assert all(isinstance(d, str) for d in devices)

def test_GetDeviceDataProxyCall(proxy):
    devices = proxy.get_devices("aquacheck")
    if devices:
        device_id = devices[0]
        data = proxy.get_device_data("aquacheck", device_id)

        assert isinstance(data, list)
        assert len(data) > 0
        assert all("timestamp" in item for item in data)

    for i in range(len(data)):    
        assert isinstance(data[i], dict)
    assert isinstance(data, list) and isinstance(data[0], dict)

def test_GetLatestDataProxyCall(proxy):
    devices = proxy.get_devices("aquacheck")
    if devices:
        device_id = devices[0]
        data = proxy.get_latest_data("aquacheck", device_id)
        
        assert isinstance(data, dict)
        assert "id" in data
        assert "ID_boitier" in data
        assert data["ID_boitier"] == device_id
        assert "timestamp" in data
        assert "temperature" in data or data.get("temperature") is None
        assert "ground_humidity" in data or data.get("ground_humidity") is None
    

def test_GetFilteredDataProxyCall(proxy):
    devices = proxy.get_devices("aquacheck")
    print("devices",devices)
    for device_id in devices:
        # Période connue avec des données
        
        data = proxy.get_filtered_data(
            "aquacheck",
            device_id,
            "2025-06-16",
            "2025-06-17"
        )
        assert isinstance(data, list)
        if(len(data) > 0):
            for i in range(4):
                assert isinstance(data[i], dict)

if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
