# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.0.1] - Multiple device support

### Added

- Multiple device support: monitor can talk to several inverters (e.g. `/dev/ttyUSB0`, `/dev/ttyUSB1`).
- FastAPI routes now use a path variable for device selection: `/device/{device_id}/...`.
- Endpoints: `/device/{device_id}/system-status`, `/device/{device_id}/pv-voltage`, `/device/{device_id}/pv1-power`, `/device/{device_id}/battery-soc`.
- Device index validation (404 for invalid device ID); responses include `device` in the JSON.
- Root `GET /` response includes `devices` count.

## [1.0.0] - Initial release

### Added

- Simple Modbus RTU reader using minimalmodbus (Growatt SPF5000ES).
- FastAPI HTTP API exposing inverter data:
  - System status (register 0).
  - PV voltage (register 1).
  - PV1 power from high/low registers (registers 3–4, 0.1 W scale).
  - Battery SOC (register 18).
