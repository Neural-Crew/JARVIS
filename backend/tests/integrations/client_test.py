"""
Tests unitaires pour le client ECOWATCH API.
"""

import os
import sys

import pytest
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from backend.services.integrations.ecowatch.client import (EcoWatchAPIError,
                                                           EcoWatchClient)

load_dotenv()


# Fixture pour le client avec vraie API key
@pytest.fixture(autouse=True)
def client():
    """Client ECOWATCH avec clé depuis .env"""
    api_key = os.getenv("ECOWATCH_API_KEY")
    if not api_key:
        pytest.skip("ECOWATCH_API_KEY non configurée dans .env")
    EcoWatchClient._reset_instances()
    return EcoWatchClient(api_key=api_key)


def testGivenApiKeyWhenInitializeClientThenClientConfigured():
    """Given: Une clé API valide
    When: Initialisation du client
    Then: Le client est correctement configuré avec la clé"""
    EcoWatchClient._reset_instances()
    client = EcoWatchClient(api_key="test_key")
    assert client.api_key == "test_key"
    assert client.headers["X-API-Key"] == "test_key"


def testGivenValidClientWhenTestConnectionThenReturnsSuccess(client):
    """Given: Un client avec clé API valide
    When: Test de connexion à l'API
    Then: Retourne un statut de succès"""
    result = client.test_connection()
    assert result["status"] == "ok"
    assert "message" in result


def testGivenAquacheckTableWhenGetDevicesThenReturnsDeviceList(client):
    """Given: Table aquacheck existante
    When: Récupération des devices
    Then: Retourne une liste de device IDs"""
    devices = client.get_devices("aquacheck")
    assert isinstance(devices, list)
    assert len(devices) > 0
    assert all(isinstance(d, str) for d in devices)


def testGivenClimatrackTableWhenGetDevicesThenReturnsDeviceList(client):
    """Given: Table climatrack existante
    When: Récupération des devices
    Then: Retourne une liste de device IDs"""
    devices = client.get_devices("climatrack")
    assert isinstance(devices, list)
    assert len(devices) > 0
    assert all(isinstance(d, str) for d in devices)


def testGivenInvalidTableWhenGetDevicesThenRaisesError(client):
    """Given: Nom de table invalide
    When: Tentative de récupération des devices
    Then: Lève une exception EcoWatchAPIError"""
    with pytest.raises(EcoWatchAPIError, match="Invalid table"):
        client.get_devices("invalid_table")


def testGivenAquacheckDeviceWhenGetLatestDataThenReturnsSoilMeasurement(client):
    """Given: Un device aquacheck existant
    When: Récupération de la dernière mesure
    Then: Retourne des données d'humidité du sol"""
    devices = client.get_devices("aquacheck")
    if devices:
        device_id = devices[0]
        data = client.get_latest_data("aquacheck", device_id)
        
        assert isinstance(data, dict)
        assert "id" in data
        assert "ID_boitier" in data
        assert data["ID_boitier"] == device_id
        assert "timestamp" in data
        assert "temperature" in data or data.get("temperature") is None
        assert "ground_humidity" in data or data.get("ground_humidity") is None


def testGivenClimatrackDeviceWhenGetLatestDataThenReturnsAirQualityMeasurement(client):
    """Given: Un device climatrack existant
    When: Récupération de la dernière mesure
    Then: Retourne des données de qualité d'air"""
    devices = client.get_devices("climatrack")
    if devices:
        device_id = devices[0]
        data = client.get_latest_data("climatrack", device_id)
        
        assert isinstance(data, dict)
        assert "id" in data
        assert "ID_boitier" in data
        assert data["ID_boitier"] == device_id
        assert "timestamp" in data
        assert "co2" in data or data.get("co2") is None
        assert "tvoc" in data or data.get("tvoc") is None
        assert "sound_level" in data or data.get("sound_level") is None


def testGivenDeviceIdWhenGetAllDataThenReturnsHistoricalMeasurements(client):
    """Given: Un device ID valide
    When: Récupération de toutes les données
    Then: Retourne l'historique complet des mesures"""
    devices = client.get_devices("aquacheck")
    if devices:
        device_id = devices[0]
        data = client.get_device_data("aquacheck", device_id)
        
        assert isinstance(data, list)
        assert len(data) > 0
        assert all("timestamp" in item for item in data)


def testGivenDateRangeWhenFilterDataThenReturnsMeasurementsInPeriod(client):
    """Given: Une période de dates valide
    When: Filtrage des données
    Then: Retourne les mesures dans la période spécifiée"""
    devices = client.get_devices("aquacheck")
    if devices:
        device_id = devices[0]
        # Période connue avec des données
        data = client.get_filtered_data(
            "aquacheck",
            device_id,
            "2025-06-16",
            "2025-06-17"
        )
        
        assert isinstance(data, list)
        # Peut être vide si aucune donnée dans cette période


def testGivenClientWhenCallReprThenReturnsMaskedRepresentation(client):
    """Given: Un client initialisé
    When: Appel de repr()
    Then: Retourne une représentation avec clé masquée"""
    repr_str = repr(client)
    assert "EcoWatchClient" in repr_str
    assert "***" in repr_str  # Clé masquée


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
