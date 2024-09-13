from ads1115 import i2c_setup, Sensor, tare_sensors, read_tare_values, read_sensors, port

import serial
import struct

ads_1, ads_2 = i2c_setup()
gas_1 = Sensor(ads_1, port(0)).setup()

print(gas_1.value)
#try:
#	ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)
#	temp_ramp_test(3600)
#	ser.close()
	
#except KeyboardInterrupt:
#	ser.close()
