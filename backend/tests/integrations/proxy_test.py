"""
Tests Unitaires pour le proxy du client Ecowatch
"""

import os
import sys

import pytest
from dotenv import load_dotenv
from backend.services.integrations.ecowatch.proxy import EcowatchProxy

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))


load_dotenv()

"""
Test Unitaires des Methodes du Proxy
"""
class ProxyTests():
    proxy = EcowatchProxy()

    def testMakeRequestProxyCall(self):
        pass

    def testTestConnexionProxyCall(self):
        pass

    def testGetDevicesProxyCall(self):
        pass

    def testGetDeviceDataProxyCall(self):
        pass

    def testGetLatestDataProxyCall(self):
        pass

    def testGetFilteredDataProxyCall(self):
        pass

    def testReprProxyCall(self):
        pass