"""API tests for Growatt SPF5000ES Modbus API.

All tests mock monitor.read_input_register so no USB/serial device is required.
"""
import pytest
from unittest.mock import patch


class TestRoot:
    """GET /"""

    def test_returns_service_info(self, client):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "Growatt SPF5000ES Modbus API"
        assert "docs" in data


class TestSystemStatus:
    """GET /system-status"""

    def test_success_returns_status(self, client):
        with patch("main.read_input_register", return_value=[5]):
            response = client.get("/system-status")
        assert response.status_code == 200
        assert response.json() == {"register": 0, "status": 5}

    def test_device_failure_returns_503(self, client):
        with patch("main.read_input_register", return_value=None):
            response = client.get("/system-status")
        assert response.status_code == 503
        assert "system status" in response.json()["detail"].lower()


class TestPvVoltage:
    """GET /pv-voltage"""

    def test_success_returns_voltage_scaled_by_0_1(self, client):
        with patch("main.read_input_register", return_value=[2400]):
            response = client.get("/pv-voltage")
        assert response.status_code == 200
        assert response.json() == {"register": 1, "voltage": 240.0}

    def test_device_failure_returns_503(self, client):
        with patch("main.read_input_register", return_value=None):
            response = client.get("/pv-voltage")
        assert response.status_code == 503
        assert "pv voltage" in response.json()["detail"].lower()


class TestPv1Power:
    """GET /pv1-power (high/low registers, 0.1 W scale)"""

    def test_success_combines_high_low_and_scales(self, client):
        # high=0, low=1000 -> raw 1000, power = 100.0 W
        with patch("main.read_input_register", return_value=[0, 1000]):
            response = client.get("/pv1-power")
        assert response.status_code == 200
        assert response.json()["register"] == 3
        assert response.json()["power"] == 100.0

    def test_success_32bit_high_low(self, client):
        # high=1, low=0 -> raw 65536, power = 6553.6 W
        with patch("main.read_input_register", return_value=[1, 0]):
            response = client.get("/pv1-power")
        assert response.status_code == 200
        assert response.json()["power"] == 6553.6

    def test_device_failure_returns_503(self, client):
        with patch("main.read_input_register", return_value=None):
            response = client.get("/pv1-power")
        assert response.status_code == 503
        assert "pv1 power" in response.json()["detail"].lower()

    def test_short_read_returns_503(self, client):
        with patch("main.read_input_register", return_value=[1]):
            response = client.get("/pv1-power")
        assert response.status_code == 503


class TestBatterySoc:
    """GET /battery-soc"""

    def test_success_returns_soc(self, client):
        with patch("main.read_input_register", return_value=[85]):
            response = client.get("/battery-soc")
        assert response.status_code == 200
        assert response.json() == {"register": 18, "soc": 85}

    def test_device_failure_returns_503(self, client):
        with patch("main.read_input_register", return_value=None):
            response = client.get("/battery-soc")
        assert response.status_code == 503
        assert "battery soc" in response.json()["detail"].lower()
