import minimalmodbus
import serial

# Serial port configuration:
DEVICE = '/dev/ttyUSB0'
BAUDRATE = 9600
SLAVE_ID = 1

instrument = minimalmodbus.Instrument(DEVICE, SLAVE_ID, debug=True)

# Serial port settings:
instrument.serial.port = DEVICE
instrument.serial.baudrate = BAUDRATE
instrument.serial.bytesize = 8
instrument.serial.parity = serial.PARITY_NONE
instrument.serial.stopbits = 1
instrument.serial.timeout = 1.0

# Modbus protocal:
instrument.mode = minimalmodbus.MODE_RTU

def read_input_register(reg, fun_code=4, length=1):
    try:
        return instrument.read_registers(reg, length, functioncode=fun_code)
    except Exception as e:
        print(f"Error reading register {reg}: {e}")
        return None

#if __name__ == "__main__":
#    print("=== Growatt SPF5000ES Modbus Test ===")
#
#    # System Status (Input Reg 0)
#    status = read_input_register(0)
#    print("Status:", status)
#
#    # Battery SOC (Input Reg 18)
#    battery_soc = read_input_register(18)
#    print("Battery SOC:", battery_soc)