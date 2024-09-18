from ads1115 import i2c_setup, Sensor, tare_sensors, read_sensor, port

import serial
import struct

ads_1, ads_2 = i2c_setup()

gas_sensor_1 = Sensor(ads_1, port(0))
gas_sensor_2 = Sensor(ads_1, port(1))
gas_sensor_3 = Sensor(ads_1, port(2))
gas_sensor_4 = Sensor(ads_1, port(3))
gas_sensor_5 = Sensor(ads_2, port(0))
gas_sensor_6 = Sensor(ads_2, port(1))
gas_sensor_7 = Sensor(ads_2, port(2))
gas_sensor_8 = Sensor(ads_2, port(3))

gas_sensors = [gas_sensor_1, gas_sensor_2, gas_sensor_3, gas_sensor_4, gas_sensor_5, gas_sensor_6, gas_sensor_7, gas_sensor_8]

for sensor in gas_sensors:
    sensor.tare()
    print(sensor + " " + sensor.tare_value() + " " + sensor.read_sensor())
    

#try:
#	ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)
#	temp_ramp_test(3600)
#	ser.close()
	
#except KeyboardInterrupt:
#	ser.close()
