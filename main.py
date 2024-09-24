from ads1115 import i2c_setup, Sensor, port
from pid import calculate_crc, construct_request, set_temp, read_set_temp, read_temp

import serial
import struct 

import tkinter as tk
from tkinter import messagebox

GAS_LIMIT = 1000

ads_1, ads_2 = i2c_setup()

gas_sensor_1 = Sensor(ads_1, port(0), "ch1")
gas_sensor_2 = Sensor(ads_1, port(1), "ch2")
gas_sensor_3 = Sensor(ads_1, port(2), "ch3")
gas_sensor_4 = Sensor(ads_1, port(3), "ch4")
gas_sensor_5 = Sensor(ads_2, port(0), "ch5")
gas_sensor_6 = Sensor(ads_2, port(1), "ch6")
gas_sensor_7 = Sensor(ads_2, port(2), "ch7")
gas_sensor_8 = Sensor(ads_2, port(3), "ch8")
gas_sensors = [gas_sensor_1, gas_sensor_2, gas_sensor_3, gas_sensor_4, gas_sensor_5, gas_sensor_6, gas_sensor_7, gas_sensor_8]

READ_REGISTER = 0x03
WRITE_REGISTER = 0x06
SLAVE_ADDRESS = 1

SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 115200
TIMEOUT = 1
TEST_TEMP = 37


def tare_sensors():
	for sensor in gas_sensors:
		sensor.tare()

def update_sensors(sensors):
	for sensor in sensors:
		sensor.read_sensor()

def print_readings(sensors):
	for sensor in sensors:
		print(sensor.reading, "  ", end="")
	print("")

def check_gas_limit(sensors):
	for sensor in sensors:
		if sensor.reading < GAS_LIMIT:
				sensor.flag = 0
		elif sensor.reading >= GAS_LIMIT:
				sensor.flag += 1

	flagged_sensors = []

	for sensor in sensors:
		if sensor.flag > 0:
			flagged_sensors.append(sensor.name)
	
	return flagged_sensors

def run_envirbox():
	try:
		ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)
		tare_sensors()
		heater_start = False
		gas_detected = False

		# Start up by checking presence of gas before turning on the heater
		update_sensors(gas_sensors)
		if check_gas_limit(gas_sensors) is None:
			heater_start = True
			gas_detected = False
			set_temp(TEST_TEMP)
		else:
			print(check_gas_limit(gas_sensors), "are over the acceptable limit.")
			heater_start = False
			gas_detected = True

		# Monitor temperature and gas sensors and act appropriately
		while heater_start == True:
			update_sensors(gas_sensors)	
			print_readings(gas_sensors)

			if check_gas_limit(gas_sensors) is True:
				gas_detected = True
				set_temp(0)
			else:
				if gas_detected is True:
					gas_detected = False
					set_temp(TEST_TEMP)

	except KeyboardInterrupt:
		print("KeyboardInterrupt, exiting...")

	finally:	
		ser.close()
		print("Serial connection closed.")

def button_click():
	try:
		user_input = int(entry.get())
		messagebox.showinfo("Start", f"You entered:{user_input}")
	except ValueError:
		messagebox.showeror("Error", "Please enter a valid integer")

# root = tk.Tk()
# root.title("Environmental Box")

# # Create and place the input box
# entry_label = tk.Label(root, text="Set Temp:")
# entry_label.pack(pady=5)
# entry = tk.Entry(root)
# entry.pack(pady=5)

# # Create and place the button
# button = tk.Button(root, text="Submit", command=button_click)
# button.pack(pady=20)

# # Run the application
# root.mainloop()

if __name__ == "__main__":
	run_envirbox()


    

#try:
#	ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)
#	temp_ramp_test(3600)
#	ser.close()
	
#except KeyboardInterrupt:
#	ser.close()
