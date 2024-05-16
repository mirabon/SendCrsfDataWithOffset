import struct
import serial

def bytes_to_int(b):
    # Convert 2 bytes to integer (int16) in little-endian order
    return struct.unpack('<h', b)[0]


def decode_payload(payload):
    # We split the payload into two numbers of two bytes each
    num1_bytes = payload[:2]
    num2_bytes = payload[2:]

    # Converting bytes to integers
    num1 = bytes_to_int(num1_bytes)
    num2 = bytes_to_int(num2_bytes)
    return num1, num2


def read_crsf_packet(packet):
    sync = packet[0]
    packet_len = packet[1]
    type = packet[2]
    payload = packet[3:-1]  # Payload excluding SYNC, LEN, TYPE and CRC8
    delta_x, delta_y = decode_payload(payload)
    crc = packet[-1]

    print("SYNC:", sync)
    print("Packet length:", packet_len)
    print("packet type:", type)
    print("All payload:", payload)
    print("Delta x:", delta_x)
    print("Delta y:", delta_y)
    print("CRC8:", crc)


def read_serial_port(port_name):
    with serial.Serial(port_name, 115200) as ser:
        input = bytearray()
        while True:
            if ser.in_waiting > 0:
                input.extend(ser.read(ser.in_waiting))
            if len(input) > 2:
                read_crsf_packet(input)


read_serial_port('/dev/ttyUSB0')
