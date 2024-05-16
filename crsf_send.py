import struct
import serial
import crc8


sync_byte = 0xC8 # int 200
packet_type = 0x50 # int 80


def calculate_crc(data):
    crc = crc8.crc8()
    crc.update(data)
    return crc.digest()


def send_crsf_packet(payload):
    packet_len = len(payload) + 2  # PayloadLength + 2 (after len and type)
    # Build package
    packet = bytearray([sync_byte, packet_len, packet_type])
    packet.extend(payload)

    # Calc CRC8
    crc = calculate_crc(packet[1:])  # Exclude SYNC from CRC

    # Add CRC to package
    packet.append(crc[0])

    # Send data to serial port
    ser = serial.Serial('/dev/ttyUSB0', 115200)
    ser.write(packet)
    ser.close()


def int_to_bytes(n):
    return struct.pack('<h', n)


def send_delta(num1, num2):
    # Converting numbers to bytes
    num1_bytes = int_to_bytes(int(num1))
    num2_bytes = int_to_bytes(int(num2))

    # Forming a payload from two numbers
    payload = bytearray()
    payload.extend(num1_bytes)
    payload.extend(num2_bytes)

    # Sending a CRSF packet
    send_crsf_packet(payload)


# send_delta(128, -350)
