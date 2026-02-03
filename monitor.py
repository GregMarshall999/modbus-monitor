import minimalmodbus
import serial

# Serial port configuration:
DEVICE1 = '/dev/ttyUSB0'
DEVICE2 = '/dev/ttyUSB1'
BAUDRATE = 9600
SLAVE_ID = 1

instrument1 = minimalmodbus.Instrument(DEVICE1, SLAVE_ID, debug=True)
instrument2 = minimalmodbus.Instrument(DEVICE2, SLAVE_ID, debug=True)
instruments = [instrument1, instrument2]
devices = [DEVICE1, DEVICE2]

for instrument in instruments:
    instrument.serial.port = devices[instruments.index(instrument)]
    instrument.serial.baudrate = BAUDRATE
    instrument.serial.bytesize = 8
    instrument.serial.parity = serial.PARITY_NONE
    instrument.serial.stopbits = 1
    instrument.serial.timeout = 1.0
    instrument.mode = minimalmodbus.MODE_RTU

def read_input_register(reg, instrument_index=0, fun_code=4, length=1):
    try:
        return instruments[instrument_index].read_registers(reg, length, functioncode=fun_code)
    except Exception as e:
        print(f"Error reading register {reg}: {e}")
        return None