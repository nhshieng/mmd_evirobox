import serial
import struct

READ_REGISTER = 0x03
WRITE_REGISTER = 0x06
SLAVE_ADDRESS = 1

SERIAL_PORT = '/dev/ttyACM0'
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


def set_temp(temp):
	temp_sent = temp * 10
	request = construct_request('write', 0, temp_sent)
	ser.write(request)


def read_temp():
	request = construct_request('read', 1, 1)
	ser.write(request)
	response = ser.read(7)

	if len(response) == 7:
		data_bytes = response[3:5]
		value = struct.unpack('>h', data_bytes)[0]
		temp = value / 10.0
		return temp
	else:
		print ("invalid length")


def read_set_temp():
	request = construct_request('read', 0, 1)
	ser.write(request)
	response = ser.read(7)

	if len(response) == 7:
		data_bytes = response[3:5]
		value = struct.unpack('>h', data_bytes)[0]
		temp = value / 10.0
		return temp
	else:
		print ("invalid length")
	


try:
	ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)

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

	print (read_set_temp())
	ser.close()
	
except KeyboardInterrupt:
	ser.close()
