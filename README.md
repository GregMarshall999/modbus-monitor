# Growatt SPF5000ES Modbus Monitor

Read data from a **Growatt SPF5000ES** inverter via Modbus RTU using a Raspberry Pi.

## Changelog

[CHANGELOG.md](CHANGELOG.md)

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

### Modbus CLI test

```bash
python monitor.py
```

This reads a few example registers (e.g. system status, battery SOC) and prints them. Adjust `read_input_register()` calls and register addresses in `monitor.py` as needed; use **`inverter modbus.pdf`** for the correct addresses and formats.

### Running the API (FastAPI)

```bash
uvicorn main:app --reload
```

- **Local only** (default): open http://127.0.0.1:8000 and http://127.0.0.1:8000/docs on the same machine.

### Accessing the API over LAN

To reach the API from other devices on your network (phone, tablet, another PC):

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

**Raspberry Pi’s LAN IP**:

- Base URL: `http://<PI_IP>:8000`
- Examples:
  - `GET http://192.168.1.42:8000/system-status`
  - `GET http://192.168.1.42:8000/battery-soc`
  - API docs: `http://192.168.1.42:8000/docs`

**Find the Pi’s IP**:

```bash
hostname -I
# or
ip addr
```

### Testing (no hardware required)

Tests mock the Modbus layer so they run without a USB/serial device (e.g. in CI):

```bash
pip install -r requirements-dev.txt
pytest
```

With coverage:

```bash
pytest --cov=main --cov-report=term-missing
```

## Running with Docker

### Build the image

From the project root:

```bash
docker build -t modbus-monitor .
```

### Run the container (with Modbus USB device)

On a Linux host / Raspberry Pi where the inverter is on `/dev/ttyUSB0`:

```bash
docker run --rm \
  --name modbus-monitor \
  --device=/dev/ttyUSB0:/dev/ttyUSB0 \
  -p 8000:8000 \
  modbus-monitor
```

- The container uses an internal virtual environment at `/app/.venv` to install Python dependencies.
- API will be available at `http://<HOST_IP>:8000` (e.g. `http://192.168.1.42:8000/docs`).

If your adapter uses another serial device (e.g. `/dev/ttyAMA0`), either:

- Change `DEVICE` in `monitor.py`, or
- Map it accordingly: `--device=/dev/ttyAMA0:/dev/ttyUSB0` and keep the default `DEVICE`.

## Project Layout

```
modbus-monitor/
├── README.md             # This file
├── CHANGELOG.md          # Version history
├── VENV.md               # Virtual environment setup
├── requirements.txt      # Python dependencies
├── requirements-dev.txt # Test dependencies (pytest, pytest-cov)
├── pytest.ini            # Pytest config
├── main.py               # FastAPI app (HTTP API)
├── monitor.py            # Modbus read script
├── inverter modbus.pdf   # SPF5000 Modbus protocol
├── tests/                # API tests (mocked Modbus, no USB)
│   ├── conftest.py       # Pytest fixtures (TestClient)
│   └── test_api.py       # Endpoint tests
└── installation/         # Setup and wiring photos
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
