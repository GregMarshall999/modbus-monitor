"""Pytest fixtures for modbus-monitor API tests.

We mock minimalmodbus.Instrument before importing main so that monitor.py
never opens the serial port (no USB device required). Tests then patch
main.read_input_register to inject fake register values.
"""
import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

# Prevent monitor from opening /dev/ttyUSB0 when main (and thus monitor) is loaded
with patch("minimalmodbus.Instrument", MagicMock()):
    from main import app  # noqa: E402


@pytest.fixture
def client():
    """FastAPI test client (no live Modbus)."""
    return TestClient(app)
