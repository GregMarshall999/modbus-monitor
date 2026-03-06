from fastapi import FastAPI, HTTPException, Path

from monitor import read_input_register, instruments

# Register addresses (Growatt SPF5000ES - see inverter modbus.pdf)
REG_SYSTEM_STATUS = 0
REG_PV_VOLTAGE = 1
REG_PPV1_H = 3
REG_OUTPUT_POWER = 9
REG_BATTERY_SOC = 18

NUM_DEVICES = len(instruments)

app = FastAPI(title="Growatt SPF5000ES Modbus API")


def validate_device(device_id: int = Path(..., ge=0, description="Device index (0-based)")) -> int:
    if device_id >= NUM_DEVICES:
        raise HTTPException(
            status_code=404,
            detail=f"Device {device_id} not found. Valid devices: 0 to {NUM_DEVICES - 1}",
        )
    return device_id


@app.get("/")
def read_root():
    return {"service": "Growatt SPF5000ES Modbus API", "docs": "/docs", "devices": NUM_DEVICES}

@app.get("/device/{device_id}/system-status")
def get_system_status(device_id: int = Path(..., ge=0)):
    """Read system status from Modbus input register 0."""
    validate_device(device_id)
    result = read_input_register(REG_SYSTEM_STATUS, instrument_index=device_id)
    if result is None:
        raise HTTPException(status_code=503, detail="Failed to read system status from device")
    value = result[0] if result else None
    return {"device": device_id, "register": REG_SYSTEM_STATUS, "status": value}

@app.get("/device/{device_id}/pv-voltage")
def get_pv_voltage(device_id: int = Path(..., ge=0)):
    """Read PV voltage from Modbus input register 1."""
    validate_device(device_id)
    result = read_input_register(REG_PV_VOLTAGE, instrument_index=device_id)
    if result is None:
        raise HTTPException(status_code=503, detail="Failed to read PV voltage from device")
    value = result[0] if result else None
    return {"device": device_id, "register": REG_PV_VOLTAGE, "voltage": value / 10}

@app.get("/device/{device_id}/pv1-power")
def get_pv1_power(device_id: int = Path(..., ge=0)):
    """Read PV1 power from Modbus input register 3 and input register 4."""
    validate_device(device_id)
    result = read_input_register(REG_PPV1_H, instrument_index=device_id, length=2)
    if result is None or len(result) < 2:
        raise HTTPException(status_code=503, detail="Failed to read PV1 power from device")

    high, low = result
    raw_value = (high << 16) | low
    power_watts = raw_value / 10.0

    return {"device": device_id, "register": REG_PPV1_H, "power": power_watts}

@app.get("/device/{device_id}/output-power")
def get_output_power(device_id: int = Path(..., ge=0)):
    """Read output power from Modbus input register 9."""
    validate_device(device_id)
    result = read_input_register(REG_OUTPUT_POWER, instrument_index=device_id, length=2)
    if result is None or len(result) < 2:
        raise HTTPException(status_code=503, detail="Failed to read output power from device")

    high, low = result
    raw_value = (high << 16) | low
    power_watts = raw_value / 10.0

    return {"device": device_id, "register": REG_OUTPUT_POWER, "power": power_watts}

@app.get("/device/{device_id}/battery-soc")
def get_battery_soc(device_id: int = Path(..., ge=0)):
    """Read battery state of charge (SOC) from Modbus input register 18."""
    validate_device(device_id)
    result = read_input_register(REG_BATTERY_SOC, instrument_index=device_id)
    if result is None:
        raise HTTPException(status_code=503, detail="Failed to read battery SOC from device")
    value = result[0] if result else None
    return {"device": device_id, "register": REG_BATTERY_SOC, "soc": value}

@app.get("/device/{device_id}/growatt-data")
def get_growatt_data(device_id: int = Path(..., ge=0)):
    """Read all Growatt data from the device."""
    validate_device(device_id)
    system_status = read_input_register(REG_SYSTEM_STATUS, instrument_index=device_id)
    pv_voltage = read_input_register(REG_PV_VOLTAGE, instrument_index=device_id)
    pv1_power = read_input_register(REG_PPV1_H, instrument_index=device_id, length=2)
    output_power = read_input_register(REG_OUTPUT_POWER, instrument_index=device_id, length=2)
    battery_soc = read_input_register(REG_BATTERY_SOC, instrument_index=device_id)

    if system_status is None or pv_voltage is None or pv1_power is None or output_power is None or battery_soc is None:
        raise HTTPException(status_code=503, detail="Failed to read Growatt data from device")
    
    ssv = system_status[0] if system_status else None
    pvv = pv_voltage[0] / 10 if pv_voltage else None

    high, low = pv1_power
    raw_value = (high << 16) | low
    ppw = raw_value / 10.0

    high, low = output_power
    raw_value = (high << 16) | low
    opw = raw_value / 10.0

    bss = battery_soc[0] if battery_soc else None

    return {
        "device": device_id,
        "system_status": ssv,
        "pv_voltage": pvv,
        "pv1_power": ppw,
        "output_power": opw,
        "battery_soc": bss
    }