import serial
import struct
import time

READ_REGISTER = 0x03
WRITE_REGISTER = 0x06
SLAVE_ADDRESS = 1

SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 115200
TIMEOUT = 1


def calculate_crc(data):
	crc = 0xFFFF
	for byte in data:
		crc ^= byte
		for _ in range(8):
			if crc & 0x0001:
				crc >>= 1
				crc ^= 0xA001
			else:
				crc >>= 1

	return struct.pack('<H', crc)


def construct_request(read_write, register_address, value):
	if read_write == 'read':
		read_write = READ_REGISTER
	elif read_write == 'write':
		read_write = WRITE_REGISTER
	return bytes([SLAVE_ADDRESS, read_write]) + \
		struct.pack('>HH', register_address, value) + \
		calculate_crc(bytes([SLAVE_ADDRESS, read_write, register_address >> 8, register_address & 0xFF, value >> 8, value & 0xFF]))


def set_temp(ser, temp):
	temp_sent = temp * 10
	request = construct_request('write', 0, temp_sent)
	ser.write(request)


def read_temp(ser):
	request = construct_request('read', 1, 1)
	ser.write(request)
	response = ser.read(7)
	print("pid response", response)
	if len(response) == 7:
		data_bytes = response[3:5]
		value = struct.unpack('>h', data_bytes)[0]
		temp = value / 10.0
		return temp
	else:
		print ("invalid length")


def read_set_temp(ser):
	request = construct_request('read', 0, 1)
	ser.write(request)
	print(request)
	response = ser.read(7)

	if len(response) == 7:
		data_bytes = response[3:5]
		value = struct.unpack('>h', data_bytes)[0]
		temp = value / 10.0
		return temp
	else:
		print ("invalid length")
	

def temp_ramp_test(ser, dwell_time):
	print ('Beginning Temperature Ramp Testing')

	testing_temps = [27, 30, 35, 37, 40]
	for t in testing_temps:
		print ('Setting Temp To:', t)
		set_temp(t)
		time.sleep(1)
		ser.flushInput()

		while abs(read_set_temp() - read_temp()) > 0.5:
			print (read_set_temp() - read_temp())
			time.sleep(5)
		
		print ('Set Temp Reached, Holding for ', dwell_time, ' seconds')
		time.sleep(dwell_time)
		
	set_temp(10)

#try:
#	ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)

	#request = construct_request(0, 1)
	#register_address = 0
	#value_to_write = 2 * 10

	#request = construct_request('read', register_address, 1)
	#ser.write(request)
	
	#response = ser.read(7)
	#data_bytes = response[3:5]
	#value = struct.unpack('>h', data_bytes)[0]
	#setpoint = value / 10.0
	#print (setpoint)
	
	#set_temp(30)
	#time.sleep(1)
	#ser.flushInput()
	#while True:
	#	print ('current temp is:', read_temp())
	#	time.sleep(1)
#	temp_ramp_test(3600)
#	ser.close()
	
#except KeyboardInterrupt:
#	ser.close()
