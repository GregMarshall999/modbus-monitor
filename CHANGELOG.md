# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.0.0] - Initial release

### Added

- Simple Modbus RTU reader using minimalmodbus (Growatt SPF5000ES).
- FastAPI HTTP API exposing inverter data:
  - System status (register 0).
  - PV voltage (register 1).
  - PV1 power from high/low registers (registers 3–4, 0.1 W scale).
  - Battery SOC (register 18).
