# Growatt SPF5000ES Modbus Monitor

Read data from a **Growatt SPF5000ES** inverter via Modbus RTU using a Raspberry Pi.

## Status

**SNAPSHOT** — The project successfully reads data from the requested Modbus registers. It is not yet a full monitoring solution.

## Goal

- Connect a Raspberry Pi to the Growatt SPF5000ES via Modbus (RS485).
- Read input registers (e.g. system status, battery SOC) and use them for monitoring or automation.

## Requirements

- **Raspberry Pi** with Python 3.8+
- **USB–RS485 adapter** (or built-in serial) to talk Modbus RTU to the inverter
- Physical wiring: inverter RS485 A/B to adapter, and power as per inverter manual

## Protocol Reference

Modbus register mapping and protocol details for the SPF5000 are in:

- **`inverter modbus.pdf`** — official Modbus protocol documentation for the SPF5000.

Refer to it for register addresses, data types, and scaling.

## Installation

1. **Hardware**
   - Connect the inverter’s RS485 port to the Raspberry Pi (e.g. via USB–RS485 dongle).
   - See the photos in **`installation/`** for wiring and setup:
     - `rbp.jpg` — Raspberry Pi setup
     - `mbp.jpg` — Modbus / Responses
     - `gwi.jpg` — Growatt wiring
     - `ba.jpg` — Battery / adapter

2. **Software on the Raspberry Pi**
   ```bash
   # Clone or copy the project, then:
   pip install -r requirements.txt
   ```

3. **Serial port**
   - The script uses `/dev/ttyUSB0` by default (typical for USB–RS485).
   - If your adapter appears as another device (e.g. `/dev/ttyAMA0`), set `DEVICE` in `monitor.py` accordingly.
   - Ensure the Pi user has access to the serial port (e.g. add user to `dialout` group).

## Usage

```bash
python monitor.py
```

This reads a few example registers (e.g. system status, battery SOC) and prints them. Adjust `read_input_register()` calls and register addresses in `monitor.py` as needed; use **`inverter modbus.pdf`** for the correct addresses and formats.

## Project Layout

```
modbus-monitor/
├── README.md           # This file
├── requirements.txt    # Python dependencies
├── monitor.py          # Modbus read script
├── inverter modbus.pdf # SPF5000 Modbus protocol
└── installation/       # Setup and wiring photos
    ├── rbp.jpg
    ├── mbp.jpg
    ├── gwi.jpg
    └── ba.jpg
```

## Configuration (in `monitor.py`)

| Setting    | Default      | Description              |
|-----------|--------------|--------------------------|
| `DEVICE`  | `/dev/ttyUSB0` | Serial port device     |
| `BAUDRATE`| 9600         | Modbus baud rate         |
| `SLAVE_ID`| 1            | Inverter Modbus slave ID |

Change these if your inverter or adapter use different values (see inverter manual / Modbus PDF).

## License

Use and modify as needed for your home monitoring setup.
