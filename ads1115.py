import time
import busio
import board
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

i2c = busio.I2C(board.SCL, board.SDA)

ads_1 = ADS.ADS1115(i2c, address=0x48, gain=2)
ads_2 = ADS.ADS1115(i2c, address=0x49)

channel_1 = AnalogIn(ads_1, ADS.P0)
channel_2 = AnalogIn(ads_1, ADS.P1)
channel_3 = AnalogIn(ads_1, ADS.P2)
channel_4 = AnalogIn(ads_1, ADS.P3)
channel_5 = AnalogIn(ads_2, ADS.P0)
channel_6 = AnalogIn(ads_2, ADS.P1)
channel_7 = AnalogIn(ads_2, ADS.P2)
channel_8 = AnalogIn(ads_2, ADS.P3)


while True:
	print(channel_1.value, "\t", channel_2.value, "\t", channel_5.value) 

	time.sleep(5)
