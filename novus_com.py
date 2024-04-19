import serial
import struct

READ_HOLDING_REGISTERS = 0x03
WRITE_SINGLE_REGISTER = 0x06
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


def construct_request(function_code, starting_address, quantity):
	return bytes([SLAVE_ADDRESS, function_code]) + \
		struct.pack('>HH', starting_address, quantity) + \
		calculate_crc(bytes([SLAVE_ADDRESS, function_code, starting_address >> 8, starting_address & 0xFF, quantity >> 8, quantity & 0xFF]))


def construct_write_request(register_address, value):
	return bytes([SLAVE_ADDRESS, WRITE_SINGLE_REGISTER]) + \
		struct.pack('>HH', register_address, value) + \
		calculate_crc(bytes([SLAVE_ADDRESS, WRITE_SINGLE_REGISTER, register_address >> 8, register_address & 0xFF, value >> 8, value & 0xFF]))


try:
	ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)

	#request = construct_request(READ_HOLDING_REGISTERS, 0, 1)
	#ser.write(request)
	#response = ser.read(7)

	#if len(response) == 7:
	#	data_bytes = response[3:5]
	#	value = struct.unpack('>h', data_bytes)[0]
	#	setpoint = value / 10.0
	#	print("Response: ", setpoint)

	#else:
	#	print("invalid length")

	
	register_address = 0
	value_to_write = 8 * 10

	request = construct_write_request(register_address, value_to_write)
	ser.write(request)

	ser.close()
	
except KeyboardInterrupt:
	ser.close()
