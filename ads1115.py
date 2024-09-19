import time
import busio
import board
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

class Sensor:
	def __init__(self, ads, port, name):
		self.sensor = AnalogIn(ads, port)
		self.tareval = None
		self.reading = None
		self.name = name
		self.flag = 0
	
	def tare(self):
		read_running_total = 0
		read_counter = 0

		while read_counter < 10:
			read_running_total += self.sensor.value	
			read_counter += 1
			time.sleep(0.1)

		self.tareval = read_running_total / 10

	def tare_value(self):
		return self.tareval
	
	def read_sensor(self):
		readings = 5
		read_delay = 0.05
		read_counter = 0
		read_running_total = 0

		while read_counter < readings:
			read_running_total += self.sensor.value
			read_counter += 1
			time.sleep(read_delay)

		averaged_read_values = (read_running_total / readings) - self.tareval
		self.reading = averaged_read_values

def i2c_setup():
	i2c = busio.I2C(board.SCL, board.SDA)
	ads_1 = ADS.ADS1115(i2c, address=0x48, gain=2)
	ads_2 = ADS.ADS1115(i2c, address=0x49)
	return ads_1, ads_2

def port(number):
	if number == 0:
		return ADS.P0
	elif number == 1:
		return ADS.P1
	elif number == 2:
		return ADS.P2
	elif number == 3:
		return ADS.P3


