import time
import busio
import board
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

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
	
channel_1 = AnalogIn(ads_1, ADS.P0)
channel_2 = AnalogIn(ads_1, ADS.P1)
channel_3 = AnalogIn(ads_1, ADS.P2)
channel_4 = AnalogIn(ads_1, ADS.P3)
channel_5 = AnalogIn(ads_2, ADS.P0)
channel_6 = AnalogIn(ads_2, ADS.P1)
channel_7 = AnalogIn(ads_2, ADS.P2)
channel_8 = AnalogIn(ads_2, ADS.P3)

channels = [channel_1, channel_2, channel_3, channel_4, channel_5, channel_6, channel_7, channel_8]

class Sensor:
	def __init__(self, ads, port):
		self.ads = ads
		self.port = port
	
	def setup(self):
		gas_sensor = AnalogIn(self.ads, self.port)
		return (gas_sensor)

def tare_sensors():
	reading = read_sensors()

	with open('tare.txt', 'w') as file:
		for value in reading:
			file.write(f"{value}]\n")

def read_tare_values():
	with open('tare.txt', 'r') as file:
		tare_values = file.readlines()
		tare_values = [int(number.strip()) for number in tare_values]
	return tare_values

def read_sensors(readings, time):
	read_running_total = [] * len(channels)
	read_counter = 0

	while read_counter < readings:
		channel_counter = 0
		for channel in channels:
			read_running_total[channel_counter] += channel.value
			channel_counter += 1	
		read_counter += 1
		time.sleep(time)

	averaged_read_values = [x / readings for x in read_running_total]
	return averaged_read_values