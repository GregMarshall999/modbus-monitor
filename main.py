from fastapi import FastAPI, HTTPException

from monitor import read_input_register

# Register addresses (Growatt SPF5000ES - see inverter modbus.pdf)
REG_SYSTEM_STATUS = 0
REG_PV_VOLTAGE = 1
REG_PPV1_H = 3
REG_BATTERY_SOC = 18

app = FastAPI(title="Growatt SPF5000ES Modbus API")


@app.get("/")
def read_root():
    return {"service": "Growatt SPF5000ES Modbus API", "docs": "/docs"}


@app.get("/system-status")
def get_system_status():
    """Read system status from Modbus input register 0."""
    result = read_input_register(REG_SYSTEM_STATUS)
    if result is None:
        raise HTTPException(status_code=503, detail="Failed to read system status from device")
    value = result[0] if result else None
    return {"register": REG_SYSTEM_STATUS, "status": value}

@app.get("/pv-voltage")
def get_pv_voltage():
    """Read PV voltage from Modbus input register 1."""
    result = read_input_register(REG_PV_VOLTAGE)
    if result is None:
        raise HTTPException(status_code=503, detail="Failed to read PV voltage from device")
    value = result[0] if result else None
    return {"register": REG_PV_VOLTAGE, "voltage": value / 10}

@app.get("/pv1-power")
def get_pv1_power():
    """Read PV1 power from Modbus input register 3 and input register 4."""
    result = read_input_register(REG_PPV1_H, length=2)
    if result is None or len(result) < 2:
        raise HTTPException(status_code=503, detail="Failed to read PV1 power from device")

    high, low = result
    raw_value = (high << 16) | low
    power_watts = raw_value / 10.0

    return {"register": REG_PPV1_H, "power": power_watts}

@app.get("/battery-soc")
def get_battery_soc():
    """Read battery state of charge (SOC) from Modbus input register 18."""
    result = read_input_register(REG_BATTERY_SOC)
    if result is None:
        raise HTTPException(status_code=503, detail="Failed to read battery SOC from device")
    value = result[0] if result else None
    return {"register": REG_BATTERY_SOC, "soc": value}