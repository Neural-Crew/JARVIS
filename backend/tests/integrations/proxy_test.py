"""
Tests Unitaires pour le proxy du client Ecowatch
"""

import os
import sys

import pytest
from unittest import TestCase
from dotenv import load_dotenv
from backend.services.integrations.ecowatch.proxy import EcowatchProxy
from backend.persistence.sqlite_proxy import SQLiteProxy, Query
from datetime import timedelta
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))


load_dotenv()

"""
Test Unitaires des Methodes du Proxy
"""
@pytest.fixture()
def proxy():
    " Proxy a tester "
    return EcowatchProxy()


class ProxyTest(TestCase):
    def testTestConnexionProxyCall(self, proxy):
        result = proxy.test_connection()
        print("Proxy Test",result)
        

    def test_GetDevicesProxyCall(self, proxy):
        devices =  proxy.get_devices("aquacheck")
        print("Proxy Test",devices)
        assert devices

    def test_GetDeviceDataProxyCall(self,proxy):
        devices = proxy.get_devices("aquacheck")
        if devices:
            device_id = devices[0]
            data = proxy.get_device_data("aquacheck", device_id)
        print("Proxy Test",data)
        assert data

    def test_GetLatestDataProxyCall(self,proxy):
        devices = proxy.get_devices("aquacheck")
        if devices:
            device_id = devices[0]
            data = proxy.get_latest_data("aquacheck", device_id)
        print("Proxy Test",data)
        assert data

    def test_GetFilteredDataProxyCall(self,proxy):
        devices = proxy.get_devices("aquacheck")
        for device_id in devices:
            # Période connue avec des données
            data = proxy.get_filtered_data(
                "aquacheck",
                device_id,
                "2025-06-16",
                "2025-06-17"
            )
            print("Proxy Test",data)
        assert data

if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
