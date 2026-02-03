"""API tests for Growatt SPF5000ES Modbus API (multi-device).

All tests mock monitor.read_input_register so no USB/serial device is required.
"""
from unittest.mock import patch


class TestRoot:
    """GET /"""

    def test_returns_service_info_and_device_count(self, client):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "Growatt SPF5000ES Modbus API"
        assert "docs" in data
        assert "devices" in data
        assert data["devices"] == 2  # monitor has 2 instruments


class TestDeviceValidation:
    """Invalid device_id returns 404."""

    def test_invalid_device_id_returns_404(self, client):
        response = client.get("/device/99/system-status")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
        assert "0 to 1" in response.json()["detail"]

    def test_negative_device_id_returns_422(self, client):
        response = client.get("/device/-1/system-status")
        assert response.status_code == 422


class TestSystemStatus:
    """GET /device/{device_id}/system-status"""

    def test_success_returns_status(self, client):
        with patch("main.read_input_register", return_value=[5]):
            response = client.get("/device/0/system-status")
        assert response.status_code == 200
        assert response.json() == {"device": 0, "register": 0, "status": 5}

    def test_success_device_1(self, client):
        with patch("main.read_input_register", return_value=[3]):
            response = client.get("/device/1/system-status")
        assert response.status_code == 200
        assert response.json()["device"] == 1
        assert response.json()["status"] == 3

    def test_device_failure_returns_503(self, client):
        with patch("main.read_input_register", return_value=None):
            response = client.get("/device/0/system-status")
        assert response.status_code == 503
        assert "system status" in response.json()["detail"].lower()


class TestPvVoltage:
    """GET /device/{device_id}/pv-voltage"""

    def test_success_returns_voltage_scaled_by_0_1(self, client):
        with patch("main.read_input_register", return_value=[2400]):
            response = client.get("/device/0/pv-voltage")
        assert response.status_code == 200
        assert response.json() == {"device": 0, "register": 1, "voltage": 240.0}

    def test_device_failure_returns_503(self, client):
        with patch("main.read_input_register", return_value=None):
            response = client.get("/device/0/pv-voltage")
        assert response.status_code == 503
        assert "pv voltage" in response.json()["detail"].lower()


class TestPv1Power:
    """GET /device/{device_id}/pv1-power (high/low registers, 0.1 W scale)"""

    def test_success_combines_high_low_and_scales(self, client):
        # high=0, low=1000 -> raw 1000, power = 100.0 W
        with patch("main.read_input_register", return_value=[0, 1000]):
            response = client.get("/device/0/pv1-power")
        assert response.status_code == 200
        assert response.json()["device"] == 0
        assert response.json()["register"] == 3
        assert response.json()["power"] == 100.0

    def test_success_32bit_high_low(self, client):
        # high=1, low=0 -> raw 65536, power = 6553.6 W
        with patch("main.read_input_register", return_value=[1, 0]):
            response = client.get("/device/0/pv1-power")
        assert response.status_code == 200
        assert response.json()["power"] == 6553.6

    def test_device_failure_returns_503(self, client):
        with patch("main.read_input_register", return_value=None):
            response = client.get("/device/0/pv1-power")
        assert response.status_code == 503
        assert "pv1 power" in response.json()["detail"].lower()

    def test_short_read_returns_503(self, client):
        with patch("main.read_input_register", return_value=[1]):
            response = client.get("/device/0/pv1-power")
        assert response.status_code == 503


class TestBatterySoc:
    """GET /device/{device_id}/battery-soc"""

    def test_success_returns_soc(self, client):
        with patch("main.read_input_register", return_value=[85]):
            response = client.get("/device/0/battery-soc")
        assert response.status_code == 200
        assert response.json() == {"device": 0, "register": 18, "soc": 85}

    def test_device_failure_returns_503(self, client):
        with patch("main.read_input_register", return_value=None):
            response = client.get("/device/0/battery-soc")
        assert response.status_code == 503
        assert "battery soc" in response.json()["detail"].lower()
